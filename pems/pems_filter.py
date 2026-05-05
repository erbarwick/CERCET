import sys
import re
import os
import pandas as pd

# ---------------------------------------------------------------------------
# PeMS Station Filter
# Supports two PeMS CSV formats:
#   Format A: Fwy as "I5-N" string (index col), "Abs PM" (space), no lat/lon
#   Format B: Fwy as integer column, separate Dir col, "Abs_PM" (underscore),
#             Latitude/Longitude columns present, leading numeric index col
# ---------------------------------------------------------------------------

def prompt_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("  Please enter a valid number.")


def load_csv(file_name: str) -> pd.DataFrame:
    """Load CSV handling both format A (Fwy as index) and B (numeric index)."""
    # Peek at header to decide
    with open(file_name) as f:
        header = f.readline().strip().split(",")
    # Format B starts with an unnamed numeric index; first real col is 'ID'
    # Format A starts with 'Fwy'
    if header[0] == "" or header[0].lstrip("\ufeff") == "":
        df = pd.read_csv(file_name, index_col=0)
        df = df.reset_index(drop=True)
    else:
        df = pd.read_csv(file_name)
    return df


def detect_format(df: pd.DataFrame) -> str:
    return "B" if ("Latitude" in df.columns and "Longitude" in df.columns) else "A"


def extract_route_number(fwy) -> str:
    m = re.search(r'(\d+)', str(fwy))
    return m.group(1) if m else ""


def normalize_route(r: str) -> str:
    return re.sub(r'^0+', '', str(r).strip()) or "0"


def match_routes(df: pd.DataFrame, user_input: str, fmt: str) -> pd.Series:
    target = normalize_route(user_input)
    if fmt == "B":
        return df["Fwy"].apply(lambda f: normalize_route(str(f))) == target
    else:
        return df["Fwy"].apply(lambda f: normalize_route(extract_route_number(f))) == target


def get_abs_pm_col(df: pd.DataFrame) -> str:
    return "Abs_PM" if "Abs_PM" in df.columns else "Abs PM"


def get_district_tag(df: pd.DataFrame, filename: str) -> str:
    """Derive district tag from District column, falling back to filename prefix."""
    col_districts = []
    if "District" in df.columns:
        try:
            col_districts = sorted(df["District"].dropna().unique().astype(int).tolist())
        except (ValueError, TypeError):
            pass

    if col_districts:
        if len(col_districts) == 1:
            return f"d{col_districts[0]:02d}"
        elif len(col_districts) <= 3:
            return "_".join(f"d{d:02d}" for d in col_districts)
        else:
            return "mult_districts"

    fname_match = re.match(r'(d\d+)', os.path.basename(filename), re.IGNORECASE)
    return fname_match.group(1).lower() if fname_match else ""


def build_output_filename(input_path: str, fwys: list, district_tag: str) -> str:
    base = re.sub(r'\.csv$', '', os.path.basename(input_path), flags=re.IGNORECASE)
    # Strip leading district prefix to avoid duplication (e.g. "d07_")
    base = re.sub(r'^d\d+_?', '', base, flags=re.IGNORECASE)

    route_nums = sorted(fwys, key=lambda x: int(x) if x.isdigit() else 0)
    route_tag = ("route" + "_".join(route_nums)) if len(route_nums) <= 3 else "mult_routes"

    parts = [p for p in [base, district_tag, route_tag, "filtered"] if p]
    out_name = "_".join(parts) + ".csv"
    return os.path.join(os.path.dirname(os.path.abspath(input_path)), out_name)


def main():
    if len(sys.argv) < 2:
        print("Usage: python pems_filter.py <input_csv>")
        sys.exit(1)

    file_name = sys.argv[1]
    df = load_csv(file_name)

    fmt = detect_format(df)
    abs_pm_col = get_abs_pm_col(df)
    df[abs_pm_col] = pd.to_numeric(df[abs_pm_col], errors="coerce")
    has_latlon = fmt == "B"

    # Build route display list
    if fmt == "B":
        route_display = sorted([str(r) for r in df["Fwy"].dropna().unique().astype(int)],
                                key=lambda x: int(x))
    else:
        unique_fwys = sorted(df["Fwy"].unique())
        route_display = sorted(set(extract_route_number(f) for f in unique_fwys),
                               key=lambda x: int(x) if x.isdigit() else 0)

    fmt_label = "B: meta/stations (with lat/lon)" if fmt == "B" else "A: loop data"
    print(f"\nLoaded : {file_name}  ({len(df)} rows, format {fmt_label})")
    print(f"Routes : {', '.join(route_display)}")
    if fmt == "A":
        sample_fwys = sorted(df["Fwy"].unique())[:20]
        print(f"Fwy col: {', '.join(sample_fwys)}" + (" ..." if len(df["Fwy"].unique()) > 20 else ""))
    print(f"Lat/Lon: {'Yes' if has_latlon else 'No'}")

    # ------------------------------------------------------------------
    # Step 1: Ask which routes to keep
    # ------------------------------------------------------------------
    print("""
Enter route numbers one at a time (e.g. "5", "101", "405").
All directions for that route will be included.
Leave blank and press ENTER when done.""")

    fwys = []
    while True:
        inp = input("Enter a freeway to keep: ").strip()
        if inp == "":
            if not fwys:
                print("  No routes entered — exiting.")
                sys.exit(0)
            break
        mask = match_routes(df, inp, fmt)
        if not mask.any():
            print(f"  Warning: no stations found for '{inp}'. "
                  f"Available: {', '.join(route_display)}")
        else:
            if fmt == "B" and "Dir" in df.columns:
                dirs = sorted(df.loc[mask, "Dir"].dropna().unique())
                print(f"  Matched route {inp} — directions: {', '.join(dirs)}")
            else:
                matched = sorted(df.loc[mask, "Fwy"].unique())
                print(f"  Matched: {', '.join(matched)}")
            fwys.append(normalize_route(inp))

    route_mask = pd.Series(False, index=df.index)
    for r in fwys:
        route_mask |= match_routes(df, r, fmt)
    df = df[route_mask].copy()
    print(f"\nAfter route filter: {len(df)} rows")

    # ------------------------------------------------------------------
    # Step 2: Per-route location range filter
    # ------------------------------------------------------------------
    frames = []

    for route in fwys:
        sub = df[match_routes(df, route, fmt)].copy()
        pm_lo_val = sub[abs_pm_col].min()
        pm_hi_val = sub[abs_pm_col].max()

        print(f"\n--- Route {route} ---")
        print(f"  {len(sub)} stations")
        print(f"  Abs PM range : {pm_lo_val:.3f} – {pm_hi_val:.3f}")
        if has_latlon:
            print(f"  Latitude     : {sub['Latitude'].min():.5f} – {sub['Latitude'].max():.5f}")
            print(f"  Longitude    : {sub['Longitude'].min():.5f} – {sub['Longitude'].max():.5f}")

        print(f"\n  Filter Route {route} by:")
        print(f"    [1] Abs PM range")
        if has_latlon:
            print(f"    [2] Lat/Lon bounding box")
        keep_opt = "3" if has_latlon else "2"
        print(f"    [{keep_opt}] Keep all stations on this route")
        valid = ["1", "2", "3"] if has_latlon else ["1", "2"]

        while True:
            choice = input("  Enter choice: ").strip()
            if choice in valid:
                break
            print(f"  Please enter one of: {', '.join(valid)}")

        if choice == "1":
            lo = prompt_float("  Minimum Abs PM: ")
            hi = prompt_float("  Maximum Abs PM: ")
            filtered = sub[(sub[abs_pm_col] >= lo) & (sub[abs_pm_col] <= hi)]
            print(f"  Kept {len(filtered)} of {len(sub)} stations (Abs PM {lo}–{hi})")

        elif choice == "2" and has_latlon:
            lat_lo = prompt_float("  Minimum Latitude:  ")
            lat_hi = prompt_float("  Maximum Latitude:  ")
            lon_lo = prompt_float("  Minimum Longitude: ")
            lon_hi = prompt_float("  Maximum Longitude: ")
            filtered = sub[
                (sub["Latitude"]  >= lat_lo) & (sub["Latitude"]  <= lat_hi) &
                (sub["Longitude"] >= lon_lo) & (sub["Longitude"] <= lon_hi)
            ]
            print(f"  Kept {len(filtered)} of {len(sub)} stations "
                  f"(Lat {lat_lo}–{lat_hi}, Lon {lon_lo}–{lon_hi})")

        else:  # keep all
            filtered = sub
            print(f"  Kept all {len(filtered)} stations")

        frames.append(filtered)

    # ------------------------------------------------------------------
    # Step 3: Write output with descriptive filename
    # ------------------------------------------------------------------
    result = pd.concat(frames).sort_index()
    district_tag = get_district_tag(result, file_name)
    out_file = build_output_filename(file_name, fwys, district_tag)

    result.to_csv(out_file, index=False)
    print(f"\nDone. {len(result)} stations written to: {out_file}")


if __name__ == "__main__":
    main()

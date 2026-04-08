# Caltrans PeMS station map with interactive filtering by postmile range,
# station type, and lat/lon search. Run with `python station_map.py` then
# open http://127.0.0.1:8050 in your browser.

import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

# ── Load data ─────────────────────────────────────────────────────────────────
df = pd.read_csv('all_stations_merged.csv')
df = df.dropna(subset=['Latitude', 'Longitude'])
df['District'] = pd.to_numeric(df['District'], errors='coerce').astype('Int64')
df['CA PM']    = pd.to_numeric(df['CA PM'],    errors='coerce')
df['Abs PM']   = pd.to_numeric(df['Abs PM'],   errors='coerce')

DISTRICT_COLORS = {
    1:'#e6194b', 2:'#3cb44b', 3:'#4363d8', 4:'#f58231',
    5:'#911eb4', 6:'#42d4f4', 7:'#f032e6', 8:'#bfef45',
    9:'#fabed4', 10:'#469990', 11:'#dcbeff', 12:'#9A6324',
}
df['color'] = df['District'].map(DISTRICT_COLORS).fillna('#808080')

station_types = sorted(df['Type'].dropna().unique().tolist())

ca_pm_min  = float(df['CA PM'].min())
ca_pm_max  = float(df['CA PM'].max())
abs_pm_min = float(df['Abs PM'].min())
abs_pm_max = float(df['Abs PM'].max())

# ── App layout ────────────────────────────────────────────────────────────────
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

PANEL = {'background': '#f8f9fa', 'padding': '16px',
         'borderRadius': '8px', 'marginBottom': '16px'}
LABEL = {'fontWeight': '600', 'fontSize': '13px', 'marginBottom': '4px'}

app.layout = dbc.Container(fluid=True, children=[

    dbc.Row(dbc.Col(html.H4('Caltrans PeMS Station Map',
                            style={'margin': '16px 0 8px'}), width=12)),

    dbc.Row([

        # ── Sidebar ───────────────────────────────────────────────────────────
        dbc.Col(width=3, children=[

            html.Div(style=PANEL, children=[
                html.P('Station Type', style=LABEL),
                dcc.Dropdown(
                    id='type-filter',
                    options=[{'label': t, 'value': t} for t in station_types],
                    multi=True,
                    placeholder='All types…',
                    clearable=True,
                ),
            ]),

            html.Div(style=PANEL, children=[
                html.P('Local Postmile (CA PM) range', style=LABEL),
                dcc.RangeSlider(
                    id='ca-pm-slider',
                    min=ca_pm_min, max=ca_pm_max,
                    value=[ca_pm_min, ca_pm_max],
                    tooltip={'placement': 'bottom', 'always_visible': True},
                    marks=None,
                ),
            ]),

            html.Div(style=PANEL, children=[
                html.P('Absolute Postmile (State PM) range', style=LABEL),
                dcc.RangeSlider(
                    id='abs-pm-slider',
                    min=abs_pm_min, max=abs_pm_max,
                    value=[abs_pm_min, abs_pm_max],
                    tooltip={'placement': 'bottom', 'always_visible': True},
                    marks=None,
                ),
            ]),

            html.Div(style=PANEL, children=[
                html.P('Jump to Lat / Lon', style=LABEL),
                dbc.Input(id='lat-input', placeholder='Latitude  e.g. 37.77',
                          type='number', debounce=True,
                          style={'marginBottom': '8px'}),
                dbc.Input(id='lon-input', placeholder='Longitude  e.g. -122.41',
                          type='number', debounce=True,
                          style={'marginBottom': '8px'}),
                dbc.Input(id='radius-input', placeholder='Radius (miles, optional)',
                          type='number', debounce=True,
                          style={'marginBottom': '8px'}),
                dbc.Button('Search', id='search-btn', color='primary',
                           size='sm', className='w-100'),
                html.Div(id='search-status',
                         style={'fontSize': '12px', 'marginTop': '6px',
                                'color': '#555'}),
            ]),

            html.Div(style=PANEL, children=[
                html.P(id='station-count',
                       style={'margin': 0, 'fontSize': '13px', 'color': '#555'}),
            ]),
        ]),

        # ── Map ───────────────────────────────────────────────────────────────
        dbc.Col(width=9, children=[
            dcc.Graph(id='map', style={'height': '88vh'},
                      config={'scrollZoom': True}),
        ]),
    ]),
])

# ── Callback ──────────────────────────────────────────────────────────────────
@app.callback(
    Output('map', 'figure'),
    Output('station-count', 'children'),
    Output('search-status', 'children'),

    Input('type-filter',   'value'),
    Input('ca-pm-slider',  'value'),
    Input('abs-pm-slider', 'value'),
    Input('search-btn',    'n_clicks'),

    State('lat-input',    'value'),
    State('lon-input',    'value'),
    State('radius-input', 'value'),
)
def update_map(selected_types, ca_pm_range, abs_pm_range,
               _n_clicks, lat, lon, radius_miles):

    filtered = df.copy()

    # Station type filter
    if selected_types:
        filtered = filtered[filtered['Type'].isin(selected_types)]

    # CA PM range
    filtered = filtered[
        (filtered['CA PM'].isna()) |
        (filtered['CA PM'].between(ca_pm_range[0], ca_pm_range[1]))
    ]

    # Abs PM range
    filtered = filtered[
        (filtered['Abs PM'].isna()) |
        (filtered['Abs PM'].between(abs_pm_range[0], abs_pm_range[1]))
    ]

    # Lat/lon search — jump map center, optionally filter by radius
    center_lat = 36.5
    center_lon = -119.5
    zoom       = 5.5
    search_msg = ''

    if lat is not None and lon is not None:
        center_lat, center_lon = lat, lon
        zoom = 10

        if radius_miles:
            # Rough degree-based distance filter (fine for UI purposes)
            deg = radius_miles / 69.0
            filtered = filtered[
                ((filtered['Latitude']  - lat) ** 2 +
                 (filtered['Longitude'] - lon) ** 2) ** 0.5 <= deg
            ]
            search_msg = (f'{len(filtered):,} stations within '
                          f'{radius_miles} mi of ({lat}, {lon})')
        else:
            search_msg = f'Centered on ({lat}, {lon})'

    # Build figure
    fig = px.scatter_mapbox(
        filtered,
        lat='Latitude', lon='Longitude',
        color='District',
        color_discrete_map={str(k): v for k, v in DISTRICT_COLORS.items()},
        hover_name='Name',
        hover_data={
            'ID': True, 'Fwy': True, 'Type': True,
            'County': True, 'City': True,
            'CA PM': True, 'Abs PM': True,
            'Latitude': False, 'Longitude': False,
        },
        mapbox_style='carto-positron',
        zoom=zoom,
        center={'lat': center_lat, 'lon': center_lon},
        height=700,
    )
    fig.update_traces(marker={'size': 6, 'opacity': 0.75})
    fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0},
                      legend_title_text='District',
                      uirevision='constant')  # keeps zoom on filter change

    count_msg = f'{len(filtered):,} of {len(df):,} stations shown'
    return fig, count_msg, search_msg


if __name__ == '__main__':
    app.run(debug=True)

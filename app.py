from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)


df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/earthquakes-23k.csv')
df['Date'] = pd.to_datetime(df['Date'], utc=True)
df['year'] = df['Date'].dt.year
df['str_year'] = df['year'].astype(str)

fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", hover_name="Date", hover_data=["Magnitude"],
                        color_discrete_sequence=["fuchsia"], zoom=3, height=600)
fig.update_layout(
    mapbox_style="white-bg",
    mapbox_layers=[
        {
            "below": 'traces',
            "sourcetype": "raster",
            "sourceattribution": "United States Geological Survey",
            "source": [
                "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
            ]
        }
      ])
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

app.layout = html.Div(children=[
    html.H1(id="header", children='Significant Earthquakes, 1965-2016'),

    html.Div(id="description", children='''
        Data from https://github.com/plotly/datasets/.
    '''),

    dcc.Graph(
        id='map',
        figure=fig
    ),
    dcc.Slider(
        df['year'].min(),
        df['year'].max(),
        step=5,
        value=df['year'].max(),
        marks={str(year): str(year) for year in df['year'].unique() if year % 5 == 0},
        id='year-slider'
    )
])

@app.callback(
    Output('map', 'figure'),
    Input('year-slider', 'value'))
def update_figure(selected_year):
    filtered_df = df[df.year <= selected_year]

    fig = px.scatter_mapbox(filtered_df, lat="Latitude", lon="Longitude", hover_name="Date", hover_data=["Magnitude"],
                            color_discrete_sequence=["fuchsia"], zoom=3, height=800)
    fig.update_layout(
        mapbox_style="white-bg",
        mapbox_layers=[
            {
                "below": 'traces',
                "sourcetype": "raster",
                "sourceattribution": "United States Geological Survey",
                "source": [
                    "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
                ]
            }
        ])
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
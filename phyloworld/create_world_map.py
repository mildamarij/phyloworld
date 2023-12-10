import pandas as pd
import plotly.plotly as py
import plotly.graph_objects as go
import plotly.express as px

def generate_country_color_map(metadata):
    unique_countries = metadata["Country"].unique()
    color_map = {}
    available_colors = [
    "rgb(31, 119, 180)", "rgb(255, 127, 14)", "rgb(44, 160, 44)",
    "rgb(214, 39, 40)", "rgb(148, 103, 189)", "rgb(140, 86, 75)",
    "rgb(227, 119, 194)", "rgb(127, 127, 127)", "rgb(188, 189, 34)",
    "rgb(23, 190, 207)", "rgb(240, 228, 66)", "rgb(65, 244, 47)",
    "rgb(502, 102, 152)", "rgb(204, 204, 204)", "rgb(200, 36, 17)",
    "rgb(114, 147, 203)", "rgb(83, 81, 84)", "rgb(147, 160, 61)",
    "rgb(169, 170, 68)", "rgb(193, 190, 70)", "rgb(93, 162, 233)"
    ]

    for i, country in enumerate(unique_countries):
        color_map[country] = available_colors[i % len(available_colors)]

    return color_map

def create_world_map(metadata, title="", map_type="choropleth"):
    color_map = generate_country_color_map(metadata)

    fig = go.Figure()

    for country, color in color_map.items():
        country_data = metadata[metadata["Country"] == country]
        ids = "<br>".join(country_data["ID"].astype(str).tolist())
        hover_text = f"Country: {country}<br>ID(s): {ids}"

        if map_type == "choropleth":
            fig.add_trace(
                go.Choropleth(
                    locations=[country],
                    locationmode="country names",
                    z=[1],
                    colorscale=[[0, color], [1, color]],
                    hoverinfo="text",
                    text=hover_text,
                    colorbar=dict(title="", tickvals=[], ticktext=[]),
                    showscale=False,
                )
            )
        elif map_type == "scatter":
            fig.add_trace(
                go.Scattergeo(
                    lat=country_data["Latitude"],
                    lon=country_data["Longitude"],
                    mode="markers",
                    hoverinfo="text",
                    text=hover_text,
                    showlegend=False,
                    marker=dict(color=color, size=5, opacity=0.8),
                )
            )

    fig.update_geos(
        resolution=110,
        showcoastlines=True,
        coastlinecolor="rgb(255, 255, 255)",
        showland=True,
        landcolor="rgb(217, 217, 217)",
        showocean=True,
        oceancolor="rgb(199, 215, 255)",
        showcountries=True,
        countrycolor="rgb(0, 0, 0)",
        countrywidth=0.5,
        subunitcolor="rgb(255, 255, 255)",
        lonaxis=dict(range=[-180, 180]),
        lataxis=dict(range=[-90, 90]),
    )

    fig.update_layout(title_text=title)

    return fig
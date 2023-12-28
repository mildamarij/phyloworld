import pandas as pd
from chart_studio import plotly
import plotly.graph_objects as go
from .create_tree import generate_country_color_map


def create_world_map(metadata, title="", map_type="choropleth", colors=None):
    """
    Create a world map visualization based on country metadata.

    Parameters:
    - metadata (pd.DataFrame): A DataFrame containing metadata with a "Country" column.
    For scatter plot Latitude and Longitude columns are also needed.
    - title (str): Title for the map.
    - map_type (str): Type of map ("choropleth" or "scatter"), by default choropleth.
    - colors (dict, optional): A mapping of countries to colors, by default random colours are generated.

    Returns:
    - fig (go.Figure): A Plotly figure object representing the world map.
    """
    color_map = generate_country_color_map(metadata, colors)

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
        showcountries=True,
        countrycolor="rgb(0, 0, 0)",
        countrywidth=0.5,
        lonaxis=dict(range=[-180, 180]),
        lataxis=dict(range=[-90, 90]),
    )

    fig.update_layout(
        title_text=title,
        height=600,
        width=1000
    )

    return fig
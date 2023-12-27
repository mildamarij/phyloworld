import pandas as pd
from chart_studio import plotly
from plotly.subplots import make_subplots


def combine_tree_and_world_map(tree_plot, world_map_fig, title=""):
    """
    Combine a phylogenetic tree plot and a world map plot into a single figure.

    Parameters:
    - tree_plot (go.Figure): Plotly figure object representing the phylogenetic tree.
    - world_map_fig (go.Figure): Plotly figure object representing the world map.
    - title (str): Title for the combined figure.

    Returns:
    - combine_fig (go.Figure): A Plotly figure object representing the world map and phylogenetic tree together.
    """
    tree_traces, tree_layout = tree_plot["data"], tree_plot["layout"]
    world_map_traces, world_map_layout = world_map_fig["data"], world_map_fig["layout"]

    combined_fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=[
            tree_layout["title"]["text"],
            world_map_layout["title"]["text"],
        ],
        shared_yaxes=True,
        specs=[[{"type": "scatter"}, {"type": "choropleth"}]],
    )

    combined_fig.add_traces(
        world_map_traces,
        rows=[1] * len(world_map_traces),
        cols=[2] * len(world_map_traces),
    )
    combined_fig.update_layout(world_map_layout)
    combined_fig.add_traces(
        tree_traces, rows=[1] * len(tree_traces), cols=[1] * len(tree_traces)
    )
    combined_fig.update_layout(tree_layout)
    combined_fig.update_layout(
        title_text=title, showlegend=False, paper_bgcolor="white"
    )
    return combined_fig

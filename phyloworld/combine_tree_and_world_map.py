import pandas as pd
import matplotlib.pyplot as plt
from chart_studio import plotly
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

def combine_tree_and_world_map(tree_plot, world_map_fig, title = ""):
    tree_traces = tree_plot['data']
    tree_layout = tree_plot['layout']
    world_map_traces = world_map_fig['data']
    world_map_layout = world_map_fig['layout']
    combined_fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=[tree_layout['title']['text'], world_map_layout['title']['text']],
        shared_yaxes=True,
        specs=[[{"type": "scatter"}, {"type": "choropleth"}]]
    )

    for trace in world_map_traces:
        combined_fig.add_trace(trace, row=1, col=2)
    combined_fig.update_layout(world_map_layout)
    
    for trace in tree_traces:
        combined_fig.add_trace(trace, row=1, col=1)

    combined_fig.update_layout(tree_layout)

    combined_fig.update_layout(
        title_text=title,
        showlegend=False,
        paper_bgcolor='white', 
    )

    combined_fig.show()
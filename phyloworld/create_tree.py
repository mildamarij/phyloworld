import pandas as pd
from Bio import Phylo
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def get_x_coordinates(tree):
    xcoords = tree.depths()
    if not max(xcoords.values()):
        xcoords = tree.depths(unit_branch_lengths=True)
    return xcoords

def get_y_coordinates(tree, dist=1.3):
    maxheight = tree.count_terminals() 
    ycoords = dict((leaf, maxheight - i * dist) for i, leaf in enumerate(reversed(tree.get_terminals())))
    def calc_row(clade):
        for subclade in clade:
            if subclade not in ycoords:
                calc_row(subclade)
        ycoords[clade] = (ycoords[clade.clades[0]] +
                          ycoords[clade.clades[-1]]) / 2

    if tree.root.clades:
        calc_row(tree.root)
    return ycoords

            
def get_clade_lines(orientation='horizontal', y_curr=0, x_start=0, x_curr=0, y_bot=0, y_top=0,
                    line_color='rgb(25,25,25)', line_width=0.5):
    branch_line = dict(type='line',
                       layer='below',
                       line=dict(color=line_color,
                                 width=line_width)
                       )
    if orientation == 'horizontal':
        branch_line.update(x0=x_start,
                           y0=y_curr,
                           x1=x_curr,
                           y1=y_curr)
    elif orientation == 'vertical':
        branch_line.update(x0=x_curr,
                           y0=y_bot,
                           x1=x_curr,
                           y1=y_top)
    else:
        raise ValueError("Line type can be 'horizontal' or 'vertical'")
    return branch_line


def draw_clade(clade, x_start, line_shapes, line_color='rgb(15,15,15)', line_width=1, x_coords=0, y_coords=0):

    x_curr = x_coords[clade]
    y_curr = y_coords[clade]

    branch_line = get_clade_lines(orientation='horizontal', y_curr=y_curr, x_start=x_start, x_curr=x_curr,
                                  line_color=line_color, line_width=line_width)

    line_shapes.append(branch_line)

    if clade.clades:
        y_top = y_coords[clade.clades[0]]
        y_bot = y_coords[clade.clades[-1]]

        line_shapes.append(get_clade_lines(orientation='vertical', x_curr=x_curr, y_bot=y_bot, y_top=y_top,
                                           line_color=line_color, line_width=line_width))

        for child in clade:
            draw_clade(child, x_curr, line_shapes, x_coords=x_coords, y_coords=y_coords)
            
def create_plot(tree, x_coords, y_coords, metadata, title):
    line_shapes = []
    draw_clade(tree.root, 0, line_shapes, line_color='rgb(25,25,25)', line_width=1, x_coords=x_coords, y_coords=y_coords)
    
    X, Y, text, color = [], [], [], []
    color_map = generate_country_color_map(metadata)
    label_legend = set(metadata["Country"].unique())
    color_scale = {country: color_map.get(country, 'rgb(100,100,100)') for country in label_legend}

    for cl in x_coords.keys():
        if cl.is_terminal():
            X.append(x_coords[cl])
            Y.append(y_coords[cl])
            node_id = cl.name
            country = metadata.loc[metadata["ID"] == node_id, "Country"].values[0]
            text.append(f'Country: {country}<br>ID: {node_id}')
            color.append(color_scale[country])

    trace = go.Scatter(
        x=X,
        y=Y,
        mode='markers',
        marker=dict(color=color, size=5),
        text=text,
        hoverinfo='text',
        name='Countries'
    )

    layout = go.Layout(
        title= title,
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(title='Branch Length'),
        yaxis=dict(
            showline=False,
            zeroline=False,
            showgrid=False,
            showticklabels=False,
            title=''
        ),
        hovermode='closest',
        shapes=line_shapes,
        plot_bgcolor='rgb(250,250,250)',
        legend={'x': 0, 'y': 1}
    )


    fig = go.Figure(data=[trace], layout=layout)
    return fig
    
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

def create_phylotree(tree, metadata, title = ""):
    x_coords = get_x_coordinates(tree)
    y_coords = get_y_coordinates(tree)
    fig = create_plot(tree, x_coords, y_coords, metadata, title)
    return fig
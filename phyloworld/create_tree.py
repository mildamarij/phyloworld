import pandas as pd
from chart_studio import plotly
import plotly.graph_objects as go
import random


def get_x_coordinates(tree):
    """
    Get the x-coordinates of tree branches.

    Parameters:
    - tree: Phylogenetic tree object.

    Returns:
    - xcoords: Dictionary of x-coordinates for each node in the tree.
    """
    xcoords = tree.depths()
    if not max(xcoords.values()):
        xcoords = tree.depths(unit_branch_lengths=True)

    return xcoords


def get_y_coordinates(tree):
    """
    Get the y-coordinates of tree branches.

    Parameters:
    - tree: Phylogenetic tree object.

    Returns:
    - ycoords: Dictionary of y-coordinates for each terminal node in the tree.
    """
    maxheight = tree.count_terminals()
    ycoords = dict(
        (leaf, maxheight - i * 1.3)
        for i, leaf in enumerate(reversed(tree.get_terminals()))
    )

    def calc_row(clade):
        for subclade in clade:
            if subclade not in ycoords:
                calc_row(subclade)
        ycoords[clade] = (ycoords[clade.clades[0]] + ycoords[clade.clades[-1]]) / 2

    if tree.root.clades:
        calc_row(tree.root)

    return ycoords


def get_clade_lines(
    orientation="horizontal",
    y_curr=0,
    x_start=0,
    x_curr=0,
    y_bot=0,
    y_top=0,
    line_color="rgb(25,25,25)",
    line_width=0.5,
):
    """
    Get the shape of a branch line for a clade.

    Parameters:
    - orientation: Orientation of the line ('horizontal' or 'vertical').
    - y_curr: Current y-coordinate.
    - x_start: Starting x-coordinate.
    - x_curr: Ending x-coordinate.
    - y_bot: Bottom y-coordinate for vertical lines.
    - y_top: Top y-coordinate for vertical lines.
    - line_color: Color of the line.
    - line_width: Width of the line.

    Returns:
    - branch_line: Dictionary representing the branch line shape.
    """
    branch_line = dict(
        type="line", layer="below", line=dict(color=line_color, width=line_width)
    )
    if orientation == "horizontal":
        branch_line.update(x0=x_start, y0=y_curr, x1=x_curr, y1=y_curr)
    elif orientation == "vertical":
        branch_line.update(x0=x_curr, y0=y_bot, x1=x_curr, y1=y_top)
    else:
        raise ValueError("Line type can be 'horizontal' or 'vertical'")
    return branch_line


def draw_clade(
    clade,
    x_start,
    line_shapes,
    annotations,
    line_color="rgb(15,15,15)",
    line_width=1,
    x_coords=0,
    y_coords=0,
    include_confidence=True,
):
    """
    Recursively draw a clade and its descendants on the plot.

    Parameters:
    - clade: Phylogenetic tree clade.
    - x_start: Starting x-coordinate for the clade.
    - line_shapes: List to store shapes of branch lines.
    - annotations: List to store annotations for confidence values.
    - line_color: Color of the branch lines.
    - line_width: Width of the branch lines.
    - x_coords: Dictionary of x-coordinates for each node in the tree.
    - y_coords: Dictionary of y-coordinates for each terminal node in the tree.
    - include_confidence: Flag to include confidence values in annotations, default is TRUE.
    """
    x_curr = x_coords[clade]
    y_curr = y_coords[clade]
    branch_line = get_clade_lines(
        orientation="horizontal",
        y_curr=y_curr,
        x_start=x_start,
        x_curr=x_curr,
        line_color=line_color,
        line_width=line_width,
    )

    line_shapes.append(branch_line)

    confidence = getattr(clade, "confidence", None)
    if confidence is not None and include_confidence:
        box_annotation = dict(
            xref="x",
            yref="y",
            x=x_curr,
            y=y_curr,
            showarrow=False,
            bgcolor="rgba(255, 255, 255, 0.7)",
            bordercolor="rgb(25,25,25)",
            borderwidth=1,
            font=dict(size=6),
            align="right",
            xanchor="right",
            yanchor="bottom",
            text=f"{confidence:.2f}",
        )

        annotations.append(box_annotation)

    if clade.clades:
        y_top = y_coords[clade.clades[0]]
        y_bot = y_coords[clade.clades[-1]]

        line_shapes.append(
            get_clade_lines(
                orientation="vertical",
                x_curr=x_curr,
                y_bot=y_bot,
                y_top=y_top,
                line_color=line_color,
                line_width=line_width,
            )
        )

        for child in clade:
            draw_clade(
                child,
                x_curr,
                line_shapes,
                annotations,
                x_coords=x_coords,
                y_coords=y_coords,
                include_confidence=include_confidence,
            )


def create_plot(
    tree, x_coords, y_coords, metadata, title, colors, include_confidence=True
):
    """
    Create a phylogenetic tree plot.

    Parameters:
    - tree: Phylogenetic tree object.
    - x_coords: Dictionary of x-coordinates for each node in the tree.
    - y_coords: Dictionary of y-coordinates for each terminal node in the tree.
    - metadata: DataFrame containing metadata with a "Country" column.
    - title: Title of the plot.
    - colors: List of possible color codes (hexadecimal or other), by default random colours are generated.
    - include_confidence: Flag to include confidence values in annotations, default is TRUE.

    Returns:
    - fig: Plotly figure object.
    """
    line_shapes = []
    annotations = []

    draw_clade(
        tree.root,
        0,
        line_shapes,
        annotations,
        line_color="rgb(25,25,25)",
        line_width=1,
        x_coords=x_coords,
        y_coords=y_coords,
        include_confidence=include_confidence,
    )

    X, Y, text, color = [], [], [], []

    color_map = generate_country_color_map(metadata, colors)
    label_legend = set(metadata["Country"].unique())
    color_scale = {
        country: color_map.get(country, "rgb(100,100,100)") for country in label_legend
    }

    for cl in x_coords.keys():
        if cl.is_terminal():
            X.append(x_coords[cl])
            Y.append(y_coords[cl])
            node_id = cl.name
            country = metadata.loc[metadata["ID"] == node_id, "Country"].values[0]
            text.append(f"Country: {country}<br>ID: {node_id}")
            color.append(color_scale[country])

    trace = go.Scatter(
        x=X,
        y=Y,
        mode="markers",
        marker=dict(color=color, size=5),
        text=text,
        hoverinfo="text",
        name="Countries",
    )

    layout = go.Layout(
        title=title,
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(title="Branch Length"),
        yaxis=dict(
            showline=False,
            zeroline=False,
            showgrid=False,
            showticklabels=False,
            title="",
        ),
        hovermode="closest",
        shapes=line_shapes,
        plot_bgcolor="rgb(250,250,250)",
        legend=dict(x=0, y=1),
        annotations=annotations,
        height=600,
        width=1000
    )

    fig = go.Figure(data=[trace], layout=layout)
    return fig


def generate_country_color_map(metadata, colors=None):
    """
    Generate a mapping of unique countries to random or custom provided colors.

    Parameters:
    - metadata (pd.DataFrame): A DataFrame containing metadata with a "Country" column.
    - colors (list, optional): A list of possible color codes (hexadecimal or other).

    Returns:
    - color_map (dict): A mapping of countries to colors.
    """
    random.seed(927)
    unique_countries = metadata["Country"].unique()
    num_countries = len(unique_countries)

    if colors:
        if len(colors) < num_countries:
            raise ValueError(
                "Not enough possible colors provided for unique countries."
            )
        color_map = dict(zip(unique_countries, colors[:num_countries]))
    else:
        random_colors = [
            (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            for _ in range(num_countries)
        ]
        random_colors_hex = ["#%02x%02x%02x" % rgb for rgb in random_colors]
        color_map = dict(zip(unique_countries, random_colors_hex))

    return color_map


def create_phylotree(tree, metadata, title="", colors=None, include_confidence=True):
    """
    Create a phylogenetic tree plot with annotations and customizable styling.

    Parameters:
    - tree: Phylogenetic tree object.
    - metadata: DataFrame containing metadata with a "Country" column.
    - title: Title of the plot.
    - colors: List of possible color codes (hexadecimal or other). by default random colours are generated.
    - include_confidence: Flag to include confidence values in annotations, default is TRUE.

    Returns:
    - fig: Plotly figure object.
    """
    x_coords = get_x_coordinates(tree)
    y_coords = get_y_coordinates(tree)
    fig = create_plot(
        tree, x_coords, y_coords, metadata, title, colors, include_confidence
    )
    return fig

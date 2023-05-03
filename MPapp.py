from dash import Dash, html, dcc
import dash
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, ClientsideFunction, State
import dash_bootstrap_components as dbc
import FileReader
import DataVisualization


#######################################

filereader = FileReader.FileReader()
filereader.setRawData()

filereader.setDataFrame()


eeg_inst = DataVisualization.DataVisualization(
    filereader.raw_data, filereader.raw_df, filereader.marker_stream, filereader.markers_codes, filereader.info)

# TODO FIX THE 2d Heatmap
# container_2dHeatmap = eeg_inst.get_2dHeatmap_child(app)

singlestreamsplot = eeg_inst.graphSingleStreams(
    'Title of My Single Streams\n Plotly Graph Object', eeg_inst.raw_df.columns[0:5])
othersinglestreamsplot = eeg_inst.graphSingleStreams(
    'Another Single Streams Plot', eeg_inst.raw_df.columns[:])
# theplotiactuallycareabout = eeg_inst.graphStream('All Streams', eeg_inst.raw_df[streams])

#######################################


app = Dash(__name__, use_pages=True, external_stylesheets=[
           dbc.themes.SLATE, dbc.icons.FONT_AWESOME],)


# Sidebar navigation - REFERENCE: https://community.plotly.com/t/sidebar-with-icons-expands-on-hover-and-other-cool-sidebars/67318
sidebar = html.Div(
    [
        html.Div(
            [
                html.Img(
                    src='/assets/logo2.png',
                    className='sidebar-logo'
                ),
            ],
            className="sidebar-header",
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink(
                    [html.I(className="fas fa-home me-2"), html.Span("Home")],
                    href="/",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-calendar-alt me-2"),
                        html.Span("Streams"),
                    ],
                    href="/streams",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa-solid fa-pen-nib"),
                        html.Span("Edit"),
                    ],
                    href="/edit",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa-solid fa-sliders"),
                        html.Span("Preprocessing"),
                    ],
                    href="/preprocessing",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fa-solid fa-chess-board"),
                        html.Span("Detecting Patterns"),
                    ],
                    href="/detect-patterns",
                    active="exact",
                ),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar",
)

app.layout = html.Div([

    sidebar,
    html.Div(
        [
            dash.page_container
        ],
        className="content",
    ),
])


@app.callback(
    Output("hidden-search-value", "children"),
    Input('select_stream_dropdown', 'value'),
)
# save previous search value in hidden variable
def update_hidden_value(value):
    return value


# @app.callback(
#     Output('dd-output-container', 'children'),
#     Input('create_card_button', "n_clicks"),
#     [
#         State(component_id="dd-output-container",
#               component_property="children"),
#         State(component_id="hidden-search-value",
#               component_property="children")
#     ]
# )
# def add_card_selection(n_clicks, children, streams_list):
#     # initialize cards list if it doesn't exist
#     if not children:
#         children = []

#     # submit button pressed
#     if n_clicks and n_clicks > 0:
#         new_card = eeg_inst.create_new_card(
#             streams_list, "New Card Based On Selection")
#         children.append(new_card)

#     return children

@app.callback(
    Output('dd-output-container', 'children'),
    Input('create_card_button', 'n_clicks'),
    State('dd-output-container', 'children'),
    State('hidden-search-value', 'children'),
    State('input_card_title', 'value')
)
def add_card_selection(n_clicks, children, streams_list, card_title):
    # initialize cards list if it doesn't exist
    if not children:
        children = []

    # submit button pressed and a card title is provided
    if n_clicks and n_clicks > 0 and card_title:
        new_card = eeg_inst.create_new_card(streams_list, card_title)
        children.append(new_card)

    return children


if __name__ == '__main__':
    app.run_server(debug=True)

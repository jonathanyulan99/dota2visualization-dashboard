import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
# pip install dash (version 2.0.0 or higher)
from dash import Dash, dcc, html, Input, Output, html
import numpy as np
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# Import your data
df_hero_statistics = pd.read_csv('../data/overall_hero_cluster.csv')
# Making the Master DataFrames to be parsed and Utilized

# df_daily = pd.read_csv()
# master_df = pd.read_csv()

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Hero Analyzer", href="")),
        dbc.NavItem(dbc.NavLink("Meta Analyzer", href="")),
    ],
    brand="Dota 2 Dashboard",
    brand_href="#",
    color="primary",
    dark=True,
)

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([
    navbar,

    html.H1("Specific Hero Statistics",
            style={'text-align': 'center'}),

    html.Br(),

    # --------------------------------------------------------------------------------
    # First Map Chart
    # First we include a dropdown slector
    dcc.Dropdown(id="selected_hero",
                 options=[{"label": x, "value": x}
                           for x in df_hero_statistics.hero.unique()],
                 value="options",
                 style={'width': "40%"}
                 ),

    #  Now we include the map graph.
    html.Div(children=['''Bar Graph Displaying Important Hero Metrics.''',

    dcc.Graph(
        id="all-hero-series-chart",
        style={'display': 'inline-block'}),

    dcc.Graph(
        id="all-columns-series-chart",
        style={'display': 'inline-block'})
    ]),
    html.Div(id='output_container', children=[])
])
# --------------------------------------------------------------------------------
# Second and Thrid Charts

# Time series dropdown
#     dcc.Dropdown(
#         id="state_selected",
#         options=[{"label": x, "value": x}
#                  for x in df_daily.state.unique()],
#         value='New York',
#         style={'width': "40%"},
#         clearable=False,
#     ),

#     # Div where the time series graphs will go.
#     html.Div(
#         children=[
#             # The state time series chart will go in here
#             dcc.Graph(
#                 id="state-time-series-chart",
#                 style={'display': 'inline-block'}),

#             # The second time series chart will go in here
#             dcc.Graph(
#                 id="usa-time-series-chart",
#                 style={'display': 'inline-block'})
#             ]
#     ),

#     # Div where the output of the the selected state will go
#     html.Div(id='output_container', children=[]),


#     # --------------------------------------------------------------------------------
#     # Fourth Chart

#     # A graph component that we will fill with the scatter-plot
#     dcc.Graph(id='scatter-plot'),
#     html.Div(id='scatter_plot_value')
# ])
# @end of app.layout
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# First map chart and connecting the Plotly graphs with Dash Components
@ app.callback(
    [Output(component_id="all-hero-series-chart", component_property="figure"),
     Output(component_id="all-columns-series-chart",
            component_property="figure"),
     Output(component_id='output_container', component_property='children')],
    [Input(component_id="selected_hero", component_property="options")])

def hero_statistics(selected_hero):
    print(selected_hero)

    # copy from main DF **DO NOT MESS WITH ORIGINAL DATAFRAMES**
    tmp_df = df_hero_statistics.copy()
    display_text = "The hero chosen by user was: %s" % selected_hero
    # Just removing the rows where the values are the total USA.
    # logic to be placed here
    # tmp_df = tmp_df[tmp_df.state != 'USA']
    print(display_text)
    # Selecting just the rows that the data is the input from the user.

    # hero from cluster data frame where the 'hero' column in dataframe is equiavalent to the value 'selcted_hero' when selected
    tmp_df = tmp_df[tmp_df['hero'] == selected_hero]
    # Plotly Graph Objects (GO)
    # fig = go.Figure(
    #     data=[go.Choropleth(
    #         locationmode='USA-states',
    #         locations=tmp_df[''],
    #         z=tmp_df["gold_per_min"].astype(float)
    #     )]
    # )

    # Bar Graph for the Ouput of Hero Individual Statistics
    fig = px.bar(tmp_df, y='gold_per_min', x='hero',
                 title="%s Individual Statistics" % selected_hero)
    return fig
# ----------------------------------------------------------------
# # Time series charts
# @app.callback(
#     [Output(component_id="state-time-series-chart", component_property="figure"),
#     Output(component_id="usa-time-series-chart", component_property="figure"),
#     Output(component_id='output_container', component_property='children')],
#     [Input("state_selected", "value")])

# def display_time_series(state_selected):

#     # Use the input from the user to render some text and return it
#     display_text = "The state chosen by user was: %s" % state_selected

#     # Get just the data of the US, not the states.
#     usa_df = df_daily[df_daily['state'] == 'USA']

#     # Make a bar chart of the US daily cases
#     usa_figure = px.bar(
#         usa_df,
#         x='date',
#         y='daily_cases',
#         title="Daily Cases in all USA")

#     # Little sanity check you can see in your terminal.
#     print(state_selected)

#     # Use the users input to select just the selected state.
#     tmp_df = df_daily[df_daily['state'] == state_selected]

#     # Make a bar chart of just the selected state.
#     state_figure = px.bar(
#         tmp_df,
#         x='date',
#         y='daily_cases',
#         title=("Daily Cases in %s" % state_selected))

#     return state_figure, usa_figure, display_text


# # ----------------------------------------------------------------
# # Scatter Plot Chart
# @app.callback(
#     Output("scatter-plot", "figure"),
#     [Input('scatter_plot_value', 'children')])

# def display_scatter(scatter_plot_value):

#     # Making a temporary copy of the data frame
#     tmp_df = master_df.copy()

#     # Removing the values for the total USA.
#     tmp_df = tmp_df[tmp_df['state'] != 'USA']

#     # Making a scatter plot
#     fig = px.scatter(
#         tmp_df,
#         x="case_rate",
#         y="death_rate",
#         text='state',
#         size="popestimate2019",
#         color='region',
#         hover_name="state",
#         log_x=False,
#         size_max=25)

#     return fig

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True, port=6969)

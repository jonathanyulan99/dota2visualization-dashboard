from dash.html.Hr import Hr
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
# pip install dash (version 2.0.0 or higher)
from dash import Dash, dcc, html, Input, Output, html
import numpy as np
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.MORPH]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Import your data
df_hero_statistics = pd.read_csv('overall_hero_cluster.csv')
df_hero_statistics_updated = pd.read_csv('total_heroes_metrics.csv')
# Making the Master DataFrames to be parsed and Utilized
columns = list(df_hero_statistics.columns)
# df_daily = pd.read_csv()
# master_df = pd.read_csv()

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(html.Img(
            src='https://logos-world.net/wp-content/uploads/2020/12/Dota-2-Logo.png', height="40px")),
        dbc.NavItem(dbc.NavLink("Hero Analyzer", href='/apps/visualizations')),
        dbc.NavItem(dbc.NavLink("Meta Analyzer", href='/apps/rankings')),
    ],

    brand="Dota 2 Dashboard",
    brand_href="#",
    color="primary",
    dark=True,
)

# ------------------------------------------------------------------------------
# App layout
# app.layout = html.Div(["Single dynamic Dropdown",dcc.Dropdown(id="my-dynamic-dropdown",options=[{"label": x, "value": x} for x in df_hero_statistics.hero.unique()])]),
#                 html.Div([
#                     "Multi dynamic Dropdown",
#                     dcc.Dropdown(id="my-multi-dynamic-dropdown",
#                     options=[{"label": y, "value": y} for y in df_hero_statistics.columns])],),

#                 html.Div([dcc.Graph{id="the_graph",),]),]))

# NEW START
# create the layout with the DASH name or app in our case
app.layout = html.Div([
    navbar,
    # TITLE
    # after every html.component(parameters will be in putted here, seperated by the style CSS element style={})
    # .h1 TITLE
    # python wrapper for REACT
    html.H1("lAsthIts: DOTA2 mmr analytical Tool",
            style={'textAlign': 'center'}),
    # Horizonantal Line
    html.Hr(),
    # .p Paragraph
    html.P("Choose The Hero You'd Like to Inspect"),
    # html.DIV controls the layouts of the page
    # dcc. is a core component different than HTML; DASH CORE COMPONENTS
    # NOW LETS NEST THE html.DIV; this here will place the dcc.dropdown across a specific amount of columns; default is 12
    html.Div(html.Div([
        # dcc.Dropdown to use to populate our options
        # id= 'how to reference this component input on the @app callback
        # placing all the hero names in the dropdown
        # clearable will always have a value
        # initial value = value
        # options for loop comprehension to getthe values the column name we are trying to refernce
        dcc.Dropdown(id='hero_type', clearable=False, value="HEROES", options=[
                     {'label': i, 'value': i} for i in df_hero_statistics['hero'].unique()]),
    ], className="four columns"), className="row"),

    # NOTE that here is where the id gets connected in the backend, and the property being the children
    html.Div(id="output_div", children=[]),
    html.Div(html.Div([
        # dcc.Dropdown to use to populate our options
        # id= 'how to reference this component input on the @app callback
        # placing all the hero names in the dropdown
        # clearable will always have a value
        # initial value = value
        # options for loop comprehension to getthe values the column name we are trying to refernce
        dcc.Dropdown(id='hero_type_2', clearable=False, value="HEROES", options=[
                     {'label': i, 'value': i} for i in df_hero_statistics_updated['hero'].unique()]),
    ], className="four columns"), className="row"),

    # NOTE that here is where the id gets connected in the backend, and the property being the children
    html.Div(id="output_div_2", children=[]),
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
# First map chart and connecting the Plotly graphs with Dash Components
# The .callback is what actually updates the graphs and outputs it with the OUTPUT
# The input is the value that is passed from the list of values that are connected to our dcc.Dropdown component
@app.callback(
    # Output(component_id="variable id linked above", component_property="refer to the component in the layout")
    Output(component_id="output_div", component_property="children"),
    # NOTE tha value
    Input(component_id="hero_type", component_property="value"),
)
# def update_multi_options(search_value, search_values, values):
#     if not search_value:
#         raise PreventUpdate
#     # Make sure that the set values are in the option list, else they will disappear
#     # from the shown select list, but still part of the `value`.
#     return [df_hero_statistics for df_hero_statistics in search_values if search_value in df_hero_statistics["label"] or df_hero_statistics["values"] in (values or [])]
def hero_statistics(hero_choosen):
    if hero_choosen == None:
        raise PreventUpdate

    # copy from main DF **DO NOT MESS WITH ORIGINAL DATAFRAMES**
    tmp_df = df_hero_statistics.copy()

    # Just removing the rows where the values are the total USA.
    # logic to be placed here
    # tmp_df = tmp_df[tmp_df.state != 'USA']
    # Selecting just the rows that the data is the input from the user.

    # hero from cluster data frame where the 'hero' column in dataframe is equiavalent to the value 'selcted_hero' when selected
    tmp_df_histogram = tmp_df[tmp_df["hero"] == hero_choosen]
    fig_histogram = px.bar(tmp_df_histogram, x="hero", y='gold_per_min')
    fig_histogram.update_xaxes(title=f'Gold Per Minute {hero_choosen}',categoryorder="total descending")

    tmp_df_histogram2 = tmp_df[tmp_df["hero"] == hero_choosen]
    tmp_df_histogram2['average_gold_per_min'] = tmp_df["gold_per_min"].mean()
    fig_histogram2 = px.bar(tmp_df_histogram2,x="average_gold_per_min", y="average_gold_per_min")
    fig_histogram2.update_xaxes(title=f'Average Gold Per Minute for All Heroes',categoryorder="total descending")

    tmp_df_histogram3 = tmp_df.groupby('hero_role')['gold_per_min'].mean()
    tmp_df_histogram3 = pd.DataFrame(tmp_df_histogram3)
    tmp_df_histogram3 = tmp_df_histogram3.reset_index('hero_role')
    fig_histogram3 = px.bar(tmp_df_histogram3, x="hero_role",y='gold_per_min')
    fig_histogram3.update_xaxes(title=f'Gold Per Minute per Role',categoryorder="total descending")

    # xp_per_min
    tmp_df_histogram = tmp_df[tmp_df["hero"] == hero_choosen]
    fig_histogram4 = px.bar(tmp_df_histogram, x="hero", y='xp_per_min')
    fig_histogram.update_xaxes(title=f'Xp Per Minute {hero_choosen}',categoryorder="total descending")

    tmp_df_histogram2 = tmp_df[tmp_df["hero"] == hero_choosen]
    tmp_df_histogram2['average_xp_per_min'] = tmp_df["xp_per_min"].mean()
    fig_histogram5 = px.bar(tmp_df_histogram2, x="average_xp_per_min",y="average_xp_per_min")
    fig_histogram5.update_xaxes(title=f'Xp Per Minute for All Heroes',categoryorder="total descending")

    tmp_df_histogram3 = tmp_df.groupby('hero_role')['xp_per_min'].mean()
    tmp_df_histogram3 = pd.DataFrame(tmp_df_histogram3)
    tmp_df_histogram3 = tmp_df_histogram3.reset_index('hero_role')
    fig_histogram6 = px.bar(tmp_df_histogram3, x="hero_role", y='xp_per_min')
    fig_histogram6.update_xaxes(title=f'Xp Per Minute per Role',categoryorder="total descending")

    # last_hits
    tmp_df_histogram = tmp_df[tmp_df["hero"] == hero_choosen]
    fig_histogram7 = px.bar(tmp_df_histogram, x="hero", y='last_hits')
    fig_histogram7.update_xaxes(title=f'Average Last Hits per Minute for {hero_choosen}',categoryorder="total descending")

    tmp_df_histogram2 = tmp_df[tmp_df["hero"] == hero_choosen]
    tmp_df_histogram2['average_last_hits'] = tmp_df["last_hits"].mean()
    fig_histogram8 = px.bar(tmp_df_histogram2, x="average_last_hits", y="average_last_hits")
    fig_histogram8.update_xaxes(title=f'Average Last Hits for all Heroes', categoryorder="total descending")

    tmp_df_histogram3 = tmp_df.groupby('hero_role')['last_hits'].mean()
    tmp_df_histogram3 = pd.DataFrame(tmp_df_histogram3)
    tmp_df_histogram3 = tmp_df_histogram3.reset_index('hero_role')
    fig_histogram9 = px.bar(tmp_df_histogram3, x="hero_role", y='last_hits')
    fig_histogram9.update_xaxes(title=f'Last Hits per Minute per Role',categoryorder="total descending")
    
    # STRIP CHART
    # NOTE Y- According to the role
    # NOTE SINGLE METRIC TO SEE AGAINST
    fig_strip1 = px.strip(tmp_df_histogram, x='xp_per_min', y='hero_role')
    fig_strip2 = px.strip(tmp_df_histogram, x='kills', y='hero_role')

    # SUNBURST
    # NOTE ensure safety, null values screw up with SUNBURST
    # NOTE we are gonna use the hero cluster as the main metric
    df_sburst = df_hero_statistics.dropna(subset=['hero'])
    # filtered to ensure only these specific metrics
    # df_sburst = df_sburst[df_sburst['metric_types']==df_sburst["xp_per_min", "gold_per_min", "last_hits"]]
    # root our clusters
    # branches are the heroes
    # metric types are all the specific metrics we are trying to display
    fig_sburst = px.sunburst(
        df_sburst, path=["hero_role", "hero", "last_hits"])

    # EMPIRICAL CUM DISTRIBUTION
    df_ecdf = df_hero_statistics[df_hero_statistics["hero_role"]
                                 .isin(["Hard-Carry", "Soft-carry", "Support", "Offlaner/All-rounder"])]
    fig_ecdf = px.ecdf(df_ecdf, x='xp_per_min', color="hero_role")

    # LINECHART

    # Bar Graph for the Ouput of Hero Individual Statistics
    # fig = px.pie(tmp_df,names='col',title="%s Individual Statistics on %s" % search_value)

    for data in fig_histogram.data:
        data["width"] = 0.25

    for data in fig_histogram2.data:
        data["width"] = 0.25

    for data in fig_histogram4.data:
        data["width"] = 0.25

    for data in fig_histogram5.data:
        data["width"] = 0.25

    for data in fig_histogram7.data:
        data["width"] = 0.25

    for data in fig_histogram8.data:
        data["width"] = 0.25

    # return all the figures
    return [
        html.Div([
            html.H2("GRAPHS", style={"textAlign": "center"}),
            html.Hr(),
            html.Div([
                html.Div([dcc.Graph(figure=fig_histogram)],
                         className="four columns"),
                html.Div([dcc.Graph(figure=fig_histogram2)],
                         className="four columns"),
                html.Div([dcc.Graph(figure=fig_histogram3)],
                         className="four columns"),
            ], className="row"),
            html.Hr(),
            html.Div([
                html.Div([dcc.Graph(figure=fig_histogram4)],
                         className="four columns"),
                html.Div([dcc.Graph(figure=fig_histogram5)],
                         className="four columns"),
                html.Div([dcc.Graph(figure=fig_histogram6)],
                         className="four columns"),
            ], className="row"),
            html.Hr(),
            html.Div([
                html.Div([dcc.Graph(figure=fig_histogram7)],
                         className="four columns"),
                html.Div([dcc.Graph(figure=fig_histogram8)],
                         className="four columns"),
                html.Div([dcc.Graph(figure=fig_histogram9)],
                         className="four columns"),
            ], className="row"),
            html.Hr(),
            html.Div([
                html.Div([dcc.Graph(figure=fig_ecdf)],
                         className="six columns"),
                html.Div([dcc.Graph(figure=fig_strip1)],
                         className="six columns"),
            ], className="row"),
            html.Hr(),
            html.Div([
                html.Div([dcc.Graph(figure=fig_sburst)], className="twelve columns"), ], className="row"),
        ]),
            html.Hr(),
    ]
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
@app.callback(
    # Output(component_id="variable id linked above", component_property="refer to the component in the layout")
    Output(component_id="output_div_2", component_property="children"),
    # NOTE tha value
    Input(component_id="hero_type_2", component_property="value"),
)
# def update_multi_options(search_value, search_values, values):
#     if not search_value:
#         raise PreventUpdate
#     # Make sure that the set values are in the option list, else they will disappear
#     # from the shown select list, but still part of the `value`.
#     return [df_hero_statistics for df_hero_statistics in search_values if search_value in df_hero_statistics["label"] or df_hero_statistics["values"] in (values or [])]
def hero_statistics(hero_choosen):
    if hero_choosen == None:
        raise PreventUpdate

    # copy from main DF **DO NOT MESS WITH ORIGINAL DATAFRAMES**
    tmp_df = df_hero_statistics_updated.copy()

    # Just removing the rows where the values are the total USA.
    # logic to be placed here
    # tmp_df = tmp_df[tmp_df.state != 'USA']
    # Selecting just the rows that the data is the input from the user.

    # hero from cluster data frame where the 'hero' column in dataframe is equiavalent to the value 'selcted_hero' when selected
    # DAMAGE NUMBERS
    tmp_df_histogram = tmp_df[tmp_df["hero"] == hero_choosen]
    fig_histogram = px.bar(tmp_df_histogram, x="hero",y="result_hero_damage_per_min_2_value")
    fig_histogram.update_xaxes(title="Top 20 Percentile Damage Per Min Metric", categoryorder="total descending")

    tmp_df_histogram2 = tmp_df[tmp_df["hero"] == hero_choosen]
    tmp_df_histogram2['average_result_hero_damage_per_min_2_value'] = tmp_df["result_hero_damage_per_min_2_value"].mean()
    fig_histogram2 = px.bar(tmp_df_histogram2, x="average_result_hero_damage_per_min_2_value",y="average_result_hero_damage_per_min_2_value")
    fig_histogram2.update_xaxes(title="Average Top 20 Percentile Damage Per Min Metric", categoryorder="total descending")

    for data in fig_histogram.data:
        data["width"] = 0.25

    for data in fig_histogram2.data:
        data["width"] = 0.25

    tmp_df_histogram3 = tmp_df[tmp_df["hero"] == hero_choosen]
    fig_histogram3 = px.bar(tmp_df_histogram3, x="hero",y="result_hero_damage_per_min_4_value")
    fig_histogram3.update_xaxes(title="Top 40 Percentile Damage Per Min Metric", categoryorder="total descending")

    tmp_df_histogram4 = tmp_df[tmp_df["hero"] == hero_choosen]
    tmp_df_histogram4['average_result_hero_damage_per_min_4_value'] = tmp_df["result_hero_damage_per_min_4_value"].mean()
    fig_histogram4 = px.bar(tmp_df_histogram4, x="average_result_hero_damage_per_min_4_value",
                            y="average_result_hero_damage_per_min_4_value")
    fig_histogram4.update_xaxes(title="Average Top 40 Percentile Damage Per Min Metric", categoryorder="total descending")

    for data in fig_histogram3.data:
        data["width"] = 0.25

    for data in fig_histogram4.data:
        data["width"] = 0.25

    tmp_df_histogram5 = tmp_df[tmp_df["hero"] == hero_choosen]
    fig_histogram5 = px.bar(tmp_df_histogram5, x="hero",y="result_hero_damage_per_min_6_value")
    fig_histogram5.update_xaxes(title="Top 60 Percentile Damage Per Min Metric", categoryorder="total descending")

    tmp_df_histogram6 = tmp_df[tmp_df["hero"] == hero_choosen]
    tmp_df_histogram6['average_result_hero_damage_per_min_6_value'] = tmp_df["result_hero_damage_per_min_6_value"].mean()
    fig_histogram6 = px.bar(tmp_df_histogram6, x="average_result_hero_damage_per_min_6_value",
                            y="average_result_hero_damage_per_min_6_value")
    fig_histogram6.update_xaxes(title="Average Top 60 Percentile Damage Per Min Metric", categoryorder="total descending")

    for data in fig_histogram5.data:
        data["width"] = 0.25

    for data in fig_histogram6.data:
        data["width"] = 0.25

    tmp_df_histogram7 = tmp_df[tmp_df["hero"] == hero_choosen]
    fig_histogram7 = px.bar(tmp_df_histogram7, x="hero",y="result_hero_damage_per_min_8_value")
    fig_histogram7.update_xaxes(title="Top 80 Percentile Damage Per Min Metric", categoryorder="total descending")

    tmp_df_histogram8 = tmp_df[tmp_df["hero"] == hero_choosen]
    tmp_df_histogram8['average_result_hero_damage_per_min_8_value'] = tmp_df["result_hero_damage_per_min_8_value"].mean()
    fig_histogram8 = px.bar(tmp_df_histogram8, x="average_result_hero_damage_per_min_8_value",
                            y="average_result_hero_damage_per_min_8_value")
    fig_histogram8.update_xaxes(title="Average Top 80 Percentile Damage Per Min Metric", categoryorder="total descending")

    for data in fig_histogram7.data:
        data["width"] = 0.25

    for data in fig_histogram8.data:
        data["width"] = 0.25

    tmp_df_histogram9 = tmp_df[tmp_df["hero"] == hero_choosen]
    fig_histogram9 = px.bar(tmp_df_histogram9, x="hero",y="result_hero_damage_per_min_10_value")
    fig_histogram9.update_xaxes(title="Pro Damage Per Min Metric", categoryorder="total descending")

    tmp_df_histogram10 = tmp_df[tmp_df["hero"] == hero_choosen]
    tmp_df_histogram10['average_result_hero_damage_per_min_10_value'] = tmp_df["result_hero_damage_per_min_10_value"].mean()
    fig_histogram10 = px.bar(tmp_df_histogram10, x="average_result_hero_damage_per_min_10_value",
                             y="average_result_hero_damage_per_min_10_value")
    fig_histogram10.update_xaxes(title="Pro Damage Per Min Metric", categoryorder="total descending")

    for data in fig_histogram9.data:
        data["width"] = 0.25

    for data in fig_histogram10.data:
        data["width"] = 0.25

    # Gold Numbers
        tmp_df_histogram = tmp_df[tmp_df["hero"] == hero_choosen]
    fig_histogram = px.bar(tmp_df_histogram, x="hero",
                           y="result_hero_damage_per_min_2_value")
    fig_histogram.update_xaxes(
        title="Top 20 Percentile Damage Per Min Metric", categoryorder="total descending")

    tmp_df_histogram2 = tmp_df[tmp_df["hero"] == hero_choosen]
    tmp_df_histogram2['average_result_hero_damage_per_min_2_value'] = tmp_df["result_hero_damage_per_min_2_value"].mean()
    fig_histogram2 = px.bar(tmp_df_histogram2, x="average_result_hero_damage_per_min_2_value",
                            y="average_result_hero_damage_per_min_2_value")
    fig_histogram2.update_xaxes(
        title="Average Top 20 Percentile Damage Per Min Metric", categoryorder="total descending")

    for data in fig_histogram.data:
        data["width"] = 0.25

    for data in fig_histogram2.data:
        data["width"] = 0.25

    tmp_df_histogram3 = tmp_df[tmp_df["hero"] == hero_choosen]
    fig_histogram3 = px.bar(tmp_df_histogram3, x="hero",
                            y="result_hero_damage_per_min_4_value")
    fig_histogram3.update_xaxes(
        title="Top 40 Percentile Damage Per Min Metric", categoryorder="total descending")

    tmp_df_histogram4 = tmp_df[tmp_df["hero"] == hero_choosen]
    tmp_df_histogram4['average_result_hero_damage_per_min_4_value'] = tmp_df["result_hero_damage_per_min_4_value"].mean()
    fig_histogram4 = px.bar(tmp_df_histogram4, x="average_result_hero_damage_per_min_4_value",
                            y="average_result_hero_damage_per_min_4_value")
    fig_histogram4.update_xaxes(
        title="Average Top 40 Percentile Damage Per Min Metric", categoryorder="total descending")

    for data in fig_histogram3.data:
        data["width"] = 0.25

    for data in fig_histogram4.data:
        data["width"] = 0.25

    tmp_df_histogram5 = tmp_df[tmp_df["hero"] == hero_choosen]
    fig_histogram5 = px.bar(tmp_df_histogram5, x="hero",
                            y="result_hero_damage_per_min_6_value")
    fig_histogram5.update_xaxes(
        title="Top 60 Percentile Damage Per Min Metric", categoryorder="total descending")

    tmp_df_histogram6 = tmp_df[tmp_df["hero"] == hero_choosen]
    tmp_df_histogram6['average_result_hero_damage_per_min_6_value'] = tmp_df["result_hero_damage_per_min_6_value"].mean()
    fig_histogram6 = px.bar(tmp_df_histogram6, x="average_result_hero_damage_per_min_6_value",
                            y="average_result_hero_damage_per_min_6_value")
    fig_histogram6.update_xaxes(
        title="Average Top 60 Percentile Damage Per Min Metric", categoryorder="total descending")

    for data in fig_histogram5.data:
        data["width"] = 0.25

    for data in fig_histogram6.data:
        data["width"] = 0.25

    tmp_df_histogram7 = tmp_df[tmp_df["hero"] == hero_choosen]
    fig_histogram7 = px.bar(tmp_df_histogram7, x="hero",
                            y="result_hero_damage_per_min_8_value")
    fig_histogram7.update_xaxes(
        title="Top 80 Percentile Damage Per Min Metric", categoryorder="total descending")

    tmp_df_histogram8 = tmp_df[tmp_df["hero"] == hero_choosen]
    tmp_df_histogram8['average_result_hero_damage_per_min_8_value'] = tmp_df["result_hero_damage_per_min_8_value"].mean()
    fig_histogram8 = px.bar(tmp_df_histogram8, x="average_result_hero_damage_per_min_8_value",
                            y="average_result_hero_damage_per_min_8_value")
    fig_histogram8.update_xaxes(
        title="Average Top 80 Percentile Damage Per Min Metric", categoryorder="total descending")

    for data in fig_histogram7.data:
        data["width"] = 0.25

    for data in fig_histogram8.data:
        data["width"] = 0.25

    tmp_df_histogram9 = tmp_df[tmp_df["hero"] == hero_choosen]
    fig_histogram9 = px.bar(tmp_df_histogram9, x="hero",
                            y="result_hero_damage_per_min_10_value")
    fig_histogram9.update_xaxes(
        title="Pro Damage Per Min Metric", categoryorder="total descending")

    tmp_df_histogram10 = tmp_df[tmp_df["hero"] == hero_choosen]
    tmp_df_histogram10['average_result_hero_damage_per_min_10_value'] = tmp_df["result_hero_damage_per_min_10_value"].mean()
    fig_histogram10 = px.bar(tmp_df_histogram10, x="average_result_hero_damage_per_min_10_value",
                             y="average_result_hero_damage_per_min_10_value")
    fig_histogram10.update_xaxes(
        title="Pro Damage Per Min Metric", categoryorder="total descending")

    for data in fig_histogram9.data:
        data["width"] = 0.25

    for data in fig_histogram10.data:
        data["width"] = 0.25


    # Xp Numbers
    tmp_df_histogram = tmp_df[tmp_df["hero"] == hero_choosen]
    fig_histogram11 = px.bar(tmp_df_histogram, x="hero",y="result_xp_per_min_2_value")
    fig_histogram11.update_xaxes(title="Top 20 Percentile XP Per Min", categoryorder="total descending")

    tmp_df_histogram12 = tmp_df[tmp_df["hero"] == hero_choosen]
    tmp_df_histogram12['average_result_xp_per_min_2_value'] = tmp_df["result_xp_per_min_2_value"].mean()
    fig_histogram12 = px.bar(tmp_df_histogram12, x="average_result_xp_per_min_2_value", y="average_result_xp_per_min_2_value")
    fig_histogram12.update_xaxes(title="Average Top 20 Percentile XP Per Min Metric", categoryorder="total descending")

    for data in fig_histogram11.data:
        data["width"] = 0.25

    for data in fig_histogram12.data:
        data["width"] = 0.25

    tmp_df_histogram13 = tmp_df[tmp_df["hero"] == hero_choosen]
    fig_histogram13 = px.bar(tmp_df_histogram13, x="hero",y="result_xp_per_min_4_value")
    fig_histogram13.update_xaxes(title="Top 40 Percentile XP Per Min Metric", categoryorder="total descending")

    tmp_df_histogram14 = tmp_df[tmp_df["hero"] == hero_choosen]
    tmp_df_histogram14['average_result_xp_per_min_4_value'] = tmp_df["result_xp_per_min_4_value"].mean()
    fig_histogram14 = px.bar(tmp_df_histogram14, x="average_result_xp_per_min_4_value", y="average_result_xp_per_min_4_value")
    fig_histogram14.update_xaxes(title="Average Top 40 Percentile XP Per Min Metric", categoryorder="total descending")

    for data in fig_histogram13.data:
        data["width"] = 0.25

    for data in fig_histogram14.data:
        data["width"] = 0.25

    tmp_df_histogram15 = tmp_df[tmp_df["hero"] == hero_choosen]
    fig_histogram15 = px.bar(tmp_df_histogram15, x="hero",y="result_xp_per_min_6_value")
    fig_histogram15.update_xaxes(title="Top 60 Percentile XP Per Min Metric", categoryorder="total descending")

    tmp_df_histogram16 = tmp_df[tmp_df["hero"] == hero_choosen]
    tmp_df_histogram16['average_result_xp_per_min_6_value'] = tmp_df["result_xp_per_min_6_value"].mean()
    fig_histogram16 = px.bar(tmp_df_histogram16, x="average_result_xp_per_min_6_value",y="average_result_xp_per_min_6_value")
    fig_histogram16.update_xaxes(title="Average Top 60 Percentile Damage Per Min Metric", categoryorder="total descending")

    for data in fig_histogram15.data:
        data["width"] = 0.25

    for data in fig_histogram16.data:
        data["width"] = 0.25

    tmp_df_histogram17 = tmp_df[tmp_df["hero"] == hero_choosen]
    fig_histogram17 = px.bar(tmp_df_histogram17, x="hero",y="result_xp_per_min_8_value")
    fig_histogram17.update_xaxes(title="Top 80 Percentile Damage Per Min Metric", categoryorder="total descending")

    tmp_df_histogram18 = tmp_df[tmp_df["hero"] == hero_choosen]
    tmp_df_histogram18['average_result_xp_per_min_8_value'] = tmp_df["result_xp_per_min_8_value"].mean()
    fig_histogram18 = px.bar(
        tmp_df_histogram18, x="average_result_xp_per_min_8_value", y="average_result_xp_per_min_8_value")
    fig_histogram18.update_xaxes(title="Average Top 80 Percentile XP Per Min Metric", categoryorder="total descending")

    for data in fig_histogram17.data:
        data["width"] = 0.25

    for data in fig_histogram18.data:
        data["width"] = 0.25

    tmp_df_histogram19 = tmp_df[tmp_df["hero"] == hero_choosen]
    fig_histogram19 = px.bar(tmp_df_histogram19, x="hero",y="result_xp_per_min_10_value")
    fig_histogram19.update_xaxes(title="Pro XP Per Min Metric", categoryorder="total descending")

    tmp_df_histogram20 = tmp_df[tmp_df["hero"] == hero_choosen]
    tmp_df_histogram20['average_result_xp_per_min_10_value'] = tmp_df["result_xp_per_min_10_value"].mean()
    fig_histogram20 = px.bar(tmp_df_histogram20, x="average_result_xp_per_min_10_value",y="average_result_xp_per_min_10_value")
    fig_histogram20.update_xaxes(title="Pro XP Per Min Metric", categoryorder="total descending")

    for data in fig_histogram19.data:
        data["width"] = 0.25

    for data in fig_histogram20.data:
        data["width"] = 0.25
    
    # # Last Hit Numbers
    # tmp_df_histogram = tmp_df[tmp_df["hero"] == hero_choosen]
    # fig_histogram = px.bar(tmp_df_histogram, x="hero",
    #                        y="result_hero_damage_per_min_2_value")
    # fig_histogram.update_xaxes(
    #     title="Top 20 Percentile Damage Per Min Metric", categoryorder="total descending")

    # tmp_df_histogram2 = tmp_df[tmp_df["hero"] == hero_choosen]
    # tmp_df_histogram2['average_result_hero_damage_per_min_2_value'] = tmp_df["result_hero_damage_per_min_2_value"].mean()
    # fig_histogram2 = px.bar(tmp_df_histogram2, x="average_result_hero_damage_per_min_2_value",
    #                         y="average_result_hero_damage_per_min_2_value")
    # fig_histogram2.update_xaxes(
    #     title="Average Top 20 Percentile Damage Per Min Metric", categoryorder="total descending")

    # for data in fig_histogram.data:
    #     data["width"] = 0.25

    # for data in fig_histogram2.data:
    #     data["width"] = 0.25

    # tmp_df_histogram3 = tmp_df[tmp_df["hero"] == hero_choosen]
    # fig_histogram3 = px.bar(tmp_df_histogram3, x="hero",
    #                         y="result_hero_damage_per_min_4_value")
    # fig_histogram3.update_xaxes(
    #     title="Top 40 Percentile Damage Per Min Metric", categoryorder="total descending")

    # tmp_df_histogram4 = tmp_df[tmp_df["hero"] == hero_choosen]
    # tmp_df_histogram4['average_result_hero_damage_per_min_4_value'] = tmp_df["result_hero_damage_per_min_4_value"].mean()
    # fig_histogram4 = px.bar(tmp_df_histogram4, x="average_result_hero_damage_per_min_4_value",
    #                         y="average_result_hero_damage_per_min_4_value")
    # fig_histogram4.update_xaxes(
    #     title="Average Top 40 Percentile Damage Per Min Metric", categoryorder="total descending")

    # for data in fig_histogram3.data:
    #     data["width"] = 0.25

    # for data in fig_histogram4.data:
    #     data["width"] = 0.25

    # tmp_df_histogram5 = tmp_df[tmp_df["hero"] == hero_choosen]
    # fig_histogram5 = px.bar(tmp_df_histogram5, x="hero",
    #                         y="result_hero_damage_per_min_6_value")
    # fig_histogram5.update_xaxes(
    #     title="Top 60 Percentile Damage Per Min Metric", categoryorder="total descending")

    # tmp_df_histogram6 = tmp_df[tmp_df["hero"] == hero_choosen]
    # tmp_df_histogram6['average_result_hero_damage_per_min_6_value'] = tmp_df["result_hero_damage_per_min_6_value"].mean()
    # fig_histogram6 = px.bar(tmp_df_histogram6, x="average_result_hero_damage_per_min_6_value",
    #                         y="average_result_hero_damage_per_min_6_value")
    # fig_histogram6.update_xaxes(
    #     title="Average Top 60 Percentile Damage Per Min Metric", categoryorder="total descending")

    # for data in fig_histogram5.data:
    #     data["width"] = 0.25

    # for data in fig_histogram6.data:
    #     data["width"] = 0.25

    # tmp_df_histogram7 = tmp_df[tmp_df["hero"] == hero_choosen]
    # fig_histogram7 = px.bar(tmp_df_histogram7, x="hero",
    #                         y="result_hero_damage_per_min_8_value")
    # fig_histogram7.update_xaxes(
    #     title="Top 80 Percentile Damage Per Min Metric", categoryorder="total descending")

    # tmp_df_histogram8 = tmp_df[tmp_df["hero"] == hero_choosen]
    # tmp_df_histogram8['average_result_hero_damage_per_min_8_value'] = tmp_df["result_hero_damage_per_min_8_value"].mean()
    # fig_histogram8 = px.bar(tmp_df_histogram8, x="average_result_hero_damage_per_min_8_value",
    #                         y="average_result_hero_damage_per_min_8_value")
    # fig_histogram8.update_xaxes(
    #     title="Average Top 80 Percentile Damage Per Min Metric", categoryorder="total descending")

    # for data in fig_histogram7.data:
    #     data["width"] = 0.25

    # for data in fig_histogram8.data:
    #     data["width"] = 0.25

    # tmp_df_histogram9 = tmp_df[tmp_df["hero"] == hero_choosen]
    # fig_histogram9 = px.bar(tmp_df_histogram9, x="hero",
    #                         y="result_hero_damage_per_min_10_value")
    # fig_histogram9.update_xaxes(
    #     title="Pro Damage Per Min Metric", categoryorder="total descending")

    # tmp_df_histogram10 = tmp_df[tmp_df["hero"] == hero_choosen]
    # tmp_df_histogram10['average_result_hero_damage_per_min_10_value'] = tmp_df["result_hero_damage_per_min_10_value"].mean()
    # fig_histogram10 = px.bar(tmp_df_histogram10, x="average_result_hero_damage_per_min_10_value",
    #                          y="average_result_hero_damage_per_min_10_value")
    # fig_histogram10.update_xaxes(
    #     title="Pro Damage Per Min Metric", categoryorder="total descending")

    # for data in fig_histogram9.data:
    #     data["width"] = 0.25

    # for data in fig_histogram10.data:
    #     data["width"] = 0.25

    return [
        html.Div([
        html.H2("PERCENTILE METRICS", style={"textAlign": "center"}),
        html.Hr(),
        html.Div([
            html.Div([dcc.Graph(figure=fig_histogram)],
                     className="six columns"),
            html.Div([dcc.Graph(figure=fig_histogram2)],
                     className="six columns"),
        ], className="row"),
        html.Hr(),
            html.Div([
                html.Div([dcc.Graph(figure=fig_histogram3)],
                     className="six columns"),
                html.Div([dcc.Graph(figure=fig_histogram4)],
                     className="six columns"),
            ], className="row"),
        html.Hr(),
            html.Div([
                html.Div([dcc.Graph(figure=fig_histogram5)],
                     className="six columns"),
                html.Div([dcc.Graph(figure=fig_histogram6)],
                     className="six columns"),
            ], className="row"),
        html.Hr(),
            html.Div([
                html.Div([dcc.Graph(figure=fig_histogram7)],
                     className="six columns"),
                html.Div([dcc.Graph(figure=fig_histogram8)],
                     className="six columns"),
            ], className="row"),
        html.Hr(),
        html.Div([
                html.Div([dcc.Graph(figure=fig_histogram9)],
                     className="six columns"),
                html.Div([dcc.Graph(figure=fig_histogram10)],
                     className="six columns"),
            ], className="row"),
            html.Hr(),
            html.Br(),
            html.Div([
                html.Div([dcc.Graph(figure=fig_histogram11)],
                     className="six columns"),
                html.Div([dcc.Graph(figure=fig_histogram12)],
                     className="six columns"),
            ], className="row"),
            html.Hr(),
            html.Div([
                html.Div([dcc.Graph(figure=fig_histogram13)],
                     className="six columns"),
                html.Div([dcc.Graph(figure=fig_histogram14)],
                     className="six columns"),
            ], className="row"),
            html.Hr(),
            html.Div([
                html.Div([dcc.Graph(figure=fig_histogram15)],
                     className="six columns"),
                html.Div([dcc.Graph(figure=fig_histogram16)],
                     className="six columns"),
            ], className="row"),
            html.Hr(),
            html.Div([
                html.Div([dcc.Graph(figure=fig_histogram17)],
                     className="six columns"),
                html.Div([dcc.Graph(figure=fig_histogram18)],
                     className="six columns"),
            ], className="row"),
            html.Hr(),
            html.Div([
                html.Div([dcc.Graph(figure=fig_histogram19)],
                     className="six columns"),
                html.Div([dcc.Graph(figure=fig_histogram20)],
                     className="six columns"),
            ], className="row"),
         html.Hr(),
        #  html.Div([
        #     html.Div([dcc.Graph(figure=fig_histogram21)],
        #              className="six columns"),
        #     html.Div([dcc.Graph(figure=fig_histogram22)],
        #              className="six columns"),
        # ], className="row"),
        # html.Hr(),
        #     html.Div([
        #         html.Div([dcc.Graph(figure=fig_histogram23)],
        #              className="six columns"),
        #         html.Div([dcc.Graph(figure=fig_histogram24)],
        #              className="six columns"),
        #     ], className="row"),
        # html.Hr(),
        #     html.Div([
        #         html.Div([dcc.Graph(figure=fig_histogram25)],
        #              className="six columns"),
        #         html.Div([dcc.Graph(figure=fig_histogram26)],
        #              className="six columns"),
        #     ], className="row"),
        # html.Hr(),
        #     html.Div([
        #         html.Div([dcc.Graph(figure=fig_histogram27)],
        #              className="six columns"),
        #         html.Div([dcc.Graph(figure=fig_histogram28)],
        #              className="six columns"),
        #     ], className="row"),
        # html.Hr(),
        #     html.Div([
        #         html.Div([dcc.Graph(figure=fig_histogram29)],
        #              className="six columns"),
        #         html.Div([dcc.Graph(figure=fig_histogram30)],
        #              className="six columns"),
        #     ], className="row"),
        #     html.Hr(),
        #     html.Div([
        #         html.Div([dcc.Graph(figure=fig_histogram31)],
        #              className="six columns"),
        #         html.Div([dcc.Graph(figure=fig_histogram32)],
        #              className="six columns"),
        #     ], className="row"),
        #     html.Hr(),
        #     html.Div([
        #         html.Div([dcc.Graph(figure=fig_histogram33)],
        #              className="six columns"),
        #         html.Div([dcc.Graph(figure=fig_histogram34)],
        #              className="six columns"),
        #     ], className="row"),
        #     html.Hr(),
        #     html.Div([
        #         html.Div([dcc.Graph(figure=fig_histogram35)],
        #              className="six columns"),
        #         html.Div([dcc.Graph(figure=fig_histogram36)],
        #              className="six columns"),
        #     ], className="row"),
        #     html.Hr(),
        #     html.Div([
        #         html.Div([dcc.Graph(figure=fig_histogram37)],
        #              className="six columns"),
        #         html.Div([dcc.Graph(figure=fig_histogram38)],
        #              className="six columns"),
        #     ], className="row"),
        #     html.Hr(),
        #     html.Div([
        #         html.Div([dcc.Graph(figure=fig_histogram39)],
        #              className="six columns"),
        #         html.Div([dcc.Graph(figure=fig_histogram40)],
        #              className="six columns"),
        #     ], className="row"),
        ])
    ]
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True, port=6969)

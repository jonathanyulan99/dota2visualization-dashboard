from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
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


external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.MORPH]
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

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
        dbc.NavItem(dbc.NavLink("Hero Analyzer", href='')),
        dbc.NavItem(dbc.NavLink("Meta Analyzer", href='')),
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
    fig_histogram.update_xaxes(
        title=f'Gold Per Minute {hero_choosen}', categoryorder="total descending")

    tmp_df_histogram2 = tmp_df[tmp_df["hero"] == hero_choosen]
    tmp_df_histogram2['average_gold_per_min'] = tmp_df["gold_per_min"].mean()
    fig_histogram2 = px.bar(
        tmp_df_histogram2, x="average_gold_per_min", y="average_gold_per_min")
    fig_histogram2.update_xaxes(
        title=f'Average Gold Per Minute for All Heroes', categoryorder="total descending")

    tmp_df_histogram3 = tmp_df.groupby('hero_role')['gold_per_min'].mean()
    tmp_df_histogram3 = pd.DataFrame(tmp_df_histogram3)
    tmp_df_histogram3 = tmp_df_histogram3.reset_index('hero_role')
    fig_histogram3 = px.bar(tmp_df_histogram3, x="hero_role", y='gold_per_min')
    fig_histogram3.update_xaxes(
        title=f'Gold Per Minute per Role', categoryorder="total descending")

    # xp_per_min
    tmp_df_histogram = tmp_df[tmp_df["hero"] == hero_choosen]
    fig_histogram4 = px.bar(tmp_df_histogram, x="hero", y='xp_per_min')
    fig_histogram4.update_xaxes(
        title=f'Xp Per Minute {hero_choosen}', categoryorder="total descending")

    tmp_df_histogram2 = tmp_df[tmp_df["hero"] == hero_choosen]
    tmp_df_histogram2['average_xp_per_min'] = tmp_df["xp_per_min"].mean()
    fig_histogram5 = px.bar(
        tmp_df_histogram2, x="average_xp_per_min", y="average_xp_per_min")
    fig_histogram5.update_xaxes(
        title=f'Average Xp Per Minute for All Heroes', categoryorder="total descending")

    tmp_df_histogram3 = tmp_df.groupby('hero_role')['xp_per_min'].mean()
    tmp_df_histogram3 = pd.DataFrame(tmp_df_histogram3)
    tmp_df_histogram3 = tmp_df_histogram3.reset_index('hero_role')
    fig_histogram6 = px.bar(tmp_df_histogram3, x="hero_role", y='xp_per_min')
    fig_histogram6.update_xaxes(
        title=f'Xp Per Minute per Role', categoryorder="total descending")

    # last_hits
    tmp_df_histogram = tmp_df[tmp_df["hero"] == hero_choosen]
    fig_histogram7 = px.bar(tmp_df_histogram, x="hero", y='last_hits')
    fig_histogram7.update_xaxes(
        title=f'Last Hits per Minute for {hero_choosen}', categoryorder="total descending")

    tmp_df_histogram2 = tmp_df[tmp_df["hero"] == hero_choosen]
    tmp_df_histogram2['average_last_hits'] = tmp_df["last_hits"].mean()
    fig_histogram8 = px.bar(
        tmp_df_histogram2, x="average_last_hits", y="average_last_hits")
    fig_histogram8.update_xaxes(
        title=f'Average Last Hits for all Heroes', categoryorder="total descending")

    tmp_df_histogram3 = tmp_df.groupby('hero_role')['last_hits'].mean()
    tmp_df_histogram3 = pd.DataFrame(tmp_df_histogram3)
    tmp_df_histogram3 = tmp_df_histogram3.reset_index('hero_role')
    fig_histogram9 = px.bar(tmp_df_histogram3, x="hero_role", y='last_hits')
    fig_histogram9.update_xaxes(
        title=f'Last Hits per Minute per Role', categoryorder="total descending")

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
        tmp_df_histogram, path=['hero', 'hero_role', 'last_hits'], values='xp_per_min', color='hero_role')

    # EMPIRICAL CUM DISTRIBUTION
    df_ecdf = df_hero_statistics[df_hero_statistics["hero_role"].isin(
        ["Hard-Carry", "Soft-carry", "Support", "Offlaner/All-rounder"])]
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
                         className="ten columns"),
            ], className="row"),
            html.Hr(),
            html.Div([
                html.Div([dcc.Graph(figure=fig_sburst)], className="eleven columns"), ], className="row"),
            html.Hr(),
        ]),
    ]


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
    tmp_df = df_hero_statistics_updated

    fig = go.Figure()
    tmp_df_hero = tmp_df[tmp_df["hero"] == hero_choosen]
    # for contestant, group in tmp_df_hero:
    #     print(f'Contestant:{contestant} and Group:{group}')
    #     fig.add_trace(go.bar(arg=tmp_df_histogram, x=group['hero'],
    #     y=group["result_hero_damage_per_min_2_value"],name=contestant,
    #     color='contestant',
    #     barmode='group',hovertemplate="Contestant=%s<br>Hero=%%{x}<br>Values=%%{y}<extra></extra>" % contestant))
    # fig.update_layout(legend_title_text="Hero")
    # fig.update_xaxes(title_text="Hero")
    # fig.update_yaxes(title_text="Resulting Hero Damage")
    data_input = []
    layout_bar_group = go.Layout(
        barmode='group', title=f'Gold per Minute for {hero_choosen}')
    for i in range(5):
        x = i
        trace = go.Bar(x=tmp_df_hero["hero"],
                       y=tmp_df_hero[f"result_gold_per_min_{x}_value"],
                       name=f'(Percentile{str("PRO") if i==4 else 0+i*20}%)')
        data_input.append(trace)
        x += 2

    bar_fig = go.Figure(data=data_input, layout=layout_bar_group)

    data_input_2 = []
    layout_bar_group_2 = go.Layout(
        barmode='group', title=f'XP per Minute for {hero_choosen}')
    for i in range(5):
        x = i
        trace = go.Bar(x=tmp_df_hero["hero"],
                       y=tmp_df_hero[f"result_xp_per_min_{x}_value"],
                       name=f'(Percentile{str("PRO") if i==4 else 0+i*20}%)')
        data_input_2.append(trace)
        x += 2

    bar_fig_2 = go.Figure(data=data_input_2, layout=layout_bar_group_2)

    data_input_3 = []
    layout_bar_group_3 = go.Layout(
        barmode='group', title=f'Damage per Minute for {hero_choosen}')
    for i in range(5):
        x = i
        trace = go.Bar(x=tmp_df_hero["hero"],
                       y=tmp_df_hero[f"result_hero_damage_per_min_{x}_value"],
                       name=f'(Percentile{str("PRO") if i==4 else 0+i*20}%)')
        data_input_3.append(trace)
        x += 2

    bar_fig_3 = go.Figure(data=data_input_3, layout=layout_bar_group_3)

    data_input_4 = []
    layout_bar_group_4 = go.Layout(
        barmode='group', title=f'Last Hits per Minute for {hero_choosen}')
    for i in range(5):
        x = i
        trace = go.Bar(x=tmp_df_hero["hero"],
                       y=tmp_df_hero[f"result_last_hits_per_min_{x}_value"],
                       name=f'(Percentile{str("PRO") if i==4 else 0+i*20}%)')
        data_input_4.append(trace)
        x += 2

    bar_fig_4 = go.Figure(data=data_input_4, layout=layout_bar_group_4)

    data_input_5 = []
    layout_bar_group_5 = go.Layout(
        barmode='group', title=f'Kills per Minute for {hero_choosen}')
    for i in range(5):
        x = i
        trace = go.Bar(x=tmp_df_hero["hero"],
                       y=tmp_df_hero[f"result_kills_per_min_{x}_value"],
                       name=f'(Percentile{str("PRO") if i==4 else 0+i*20}%)')
        data_input_5.append(trace)
        x += 2

    bar_fig_5 = go.Figure(data=data_input_5, layout=layout_bar_group_5)

    return [
        html.Div([
            html.H2("PERCENTILE METRICS", style={"textAlign": "center"}),
            html.Hr(),
            html.Div([
                html.Div([dcc.Graph(figure=bar_fig)],
                     className="twelve columns"),
            ], className="row"),
            html.Hr(),
            html.Br(),
            html.Div([
                html.Div([dcc.Graph(figure=bar_fig_2)],
                         className="twelve columns"),
            ], className="row"),
            html.Br(),
            html.Div([
                html.Div([dcc.Graph(figure=bar_fig_3)],
                         className="twelve columns"),
            ], className="row"),
            html.Br(),
            html.Div([
                html.Div([dcc.Graph(figure=bar_fig_4)],
                         className="twelve columns"),
            ], className="row"),
            html.Br(),
            html.Div([
                html.Div([dcc.Graph(figure=bar_fig_5)],
                         className="twelve columns"),
            ], className="row"),
        ])
    ]


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True, port=6969)

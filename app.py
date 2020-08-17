# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit <a href="http://127.0.0.1:8050/">http://127.0.0.1:8050/</a> in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Output, Input, State
import pathlib

DATA_PATH = pathlib.Path(__file__).parent.resolve()
FILENAME = "data/lianjia_nunber_of_ershoufang.csv"
df_number_of_ershoufang = pd.read_csv(DATA_PATH.joinpath(FILENAME), header=0)

app = dash.Dash(__name__,title='房地产Dashboard',external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server # for Heroku deployment


NAVBAR = dbc.Navbar(
    children=[
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src='/assets/logo.jpg', height="30px")),
                    dbc.Col(
                        dbc.NavbarBrand("中国热点城市房价走势图", className="ml-2")
                    ),
                ],
                align="center",
                no_gutters=True,
            ),
            href="https://realestatechina.herokuapp.com/",
        )
    ],
    color="dark",
    dark=True,
    sticky="top",
)

TOP_BIGRAM_COMPS = [
    dbc.CardHeader(html.H5("热点城市房价走势图")),
    dbc.CardBody(
        [
            dcc.Loading(
                id="loading-bigrams-comps",
                children=[
                    dbc.Alert(
                        "Something's gone wrong! Give us a moment, but try loading this page again if problem persists.",
                        id="no-data-alert-bigrams_comp",
                        color="warning",
                        style={"display": "none"},
                    ),
                    dbc.Row(
                        [
                            dbc.Col(html.P("选择城市:"), md=2),
                            dbc.Col(
                                dcc.Dropdown(
                                    id='city-dropdown', 
                                    options=[
                                        {'label': '成都', 'value': 'cd'},
                                        {'label': '武汉', 'value': 'wh'},
                                        {'label': '重庆', 'value': 'cq'},
                                        {'label': '北京', 'value': 'bj'},
                                        {'label': '深圳', 'value': 'sz'},
                                        {'label': '上海', 'value': 'sh'},
                                        {'label': '广州', 'value': 'gz'},
                                        {'label': '杭州', 'value': 'hz'},
                                        {'label': '廊坊', 'value': 'lf'},
                                        {'label': '长沙', 'value': 'cs'},
                                        {'label': '厦门', 'value': 'xm'},
                                        {'label': '郑州', 'value': 'zz'},
                                        {'label': '合肥', 'value': 'hf'},
                                        {'label': '南京', 'value': 'nj'},
                                    ],
                                    value='cd',
                                    multi=False
                                )
                                , md=10  
                            )
                        ]
                    ),
                    dcc.Graph(id="bigrams-comps"),
                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]

@app.callback(
    Output("bigrams-comps", "figure"),
    [Input("city-dropdown", "value")],
)
def comp_bigram_comparisons(display_city):
    temp_df = df_number_of_ershoufang[df_number_of_ershoufang.city == display_city]
    fig = px.area(
        temp_df,
        title=display_city + " 二手房挂牌数量",
        x="update_time",
        y="number",
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Bold,
        labels={"update_time": "时间", "number": "数量"},
        hover_data="",
    )
    fig.update_layout(legend=dict(x=0.1, y=1.1), legend_orientation="h")
    fig.update_yaxes(title="", showticklabels=False)
    fig.data[0]["hovertemplate"] = fig.data[0]["hovertemplate"][:-14]
    return fig

BODY = dbc.Container(
    [
        dbc.Row([dbc.Col(dbc.Card(TOP_BIGRAM_COMPS)),], style={"marginTop": 30}),
    ],
    className="mt-12",
)


app.layout = html.Div(children=[NAVBAR, BODY])

if __name__ == '__main__':
    app.run_server(debug=True)
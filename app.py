# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit <a href="http://127.0.0.1:8050/">http://127.0.0.1:8050/</a> in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd


PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

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
                    dcc.Graph(id="bigrams-comps"),
                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]

BODY = dbc.Container(
    [
        dbc.Row([dbc.Col(dbc.Card(TOP_BIGRAM_COMPS)),], style={"marginTop": 30}),
    ],
    className="mt-12",
)


app.layout = html.Div(children=[NAVBAR, BODY])

if __name__ == '__main__':
    app.run_server(debug=True)
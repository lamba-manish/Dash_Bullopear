from dash import dcc, html
import plotly.graph_objs as go
from plot import PlotPlotly
import pandas as pd
from dash.dependencies import Input, Output
from fetch import Fetch
url='https://archives.nseindia.com/content/fo/fo_mktlots.csv'
df=pd.read_csv(url)
fno_list_temp=list(df.iloc[5:,1])
fno_list=[]
for item in fno_list_temp:
    stripped_item=item.strip()
    # stripped_item = stripped_item.replace('&','%26')
    fno_list.append(stripped_item)

other_securities=['NIFTY','BANKNIFTY', 'FINNIFTY', 'MIDCPNIFTY', 'USDINR', 'CRUDEOIL', 'NATURALGAS']
options = sorted(fno_list + other_securities, key=lambda x: x in other_securities, reverse=True)

def get_left_menu():
    return html.Div(
        className='menu',
        style={
            'float': 'left',
            'width': '15%',
            'height': '100%',
            'position': 'fixed',
            'overflow-y': 'scroll',
            'padding-top': '50px'
        },
        children=[
            html.Div([html.P(html.Label(html.H3('Select Security'))),dcc.Dropdown(id='security-dropdown',options=[{'label': option, 'value': option} for option in options
            ], value=options[0]),
        ]),html.Div([html.P(html.Label(html.H3('Select Expiry'))),dcc.Dropdown(id='select-expiry')]),
        ]
        
    )



def get_navbar():
    return html.Div(
        className='navbar',
        style={
            'backgroundColor': '#fff',
            'padding': '10px',
            'position': 'fixed',
            'width': '145%',
            'top': '-4px',
            'left': '-96px',
            'zIndex': 1000
        },
        children=[
            html.A(
                'My App',
                href='/',
                className='navbar-brand',
                style={
                    'color': 'white',
                    'fontSize': '30px',
                    'fontWeight': 'bold',
                    'textDecoration': 'none',
                    'cursor': 'pointer'
                }
            ),
            html.Ul(
                children=[
                    html.Li(html.A('Home', href='/home'), style={'display': 'inline-block', 'marginRight': '20px'}),
                    html.Li(html.A('About', href='/about'), style={'display': 'inline-block', 'marginRight': '20px'}),
                    html.Li(html.A('Contact', href='/contact'), style={'display': 'inline-block', 'marginRight': '20px'})
                ],
                className='navbar-nav',
                style={
                    'display': 'contents',
                    'listStyleType': 'none',
                    'margin':'0px 10px', 'padding':'8px 12px',
                    'color':'#333','text-decoration':'none','font-size':'18px',
                    'position': 'absolute',
                    'right': '20px',
                    'top': '20px'
                }
            ),html.Hr(style={'margin-top': '16px'})
        ]
    )



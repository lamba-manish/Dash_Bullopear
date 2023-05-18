from dash import dcc, html
from plot import *

def get_bar_plot(security='NIFTY', expiry=None):
    if security in ['CRUDEOIL', "NATURALGAS"]:
        data=PlotPlotly(security, expiry)
        fig_oi=data.plot_Open_Interest()
        fig_oi_change=data.plot_Open_Interest_Change()
        fig1=dcc.Graph(id='bar_plot', figure=fig_oi)
        fig2=dcc.Graph(id='bar_plot2', figure=fig_oi_change)
        return fig1, fig2
    else:
        data = PlotPlotly(security, expiry)
        fig_oi=data.plot_Open_Interest()
        fig_oi_change=data.plot_Open_Interest_Change()
        fig1=dcc.Graph(id='bar_plot', figure=fig_oi)
        fig2=dcc.Graph(id='bar_plot2', figure=fig_oi_change)
        return fig1, fig2

def fno_list():
    url='https://archives.nseindia.com/content/fo/fo_mktlots.csv'
    df=pd.read_csv(url)
    fno_list_temp=list(df.iloc[5:,1])
    fno_list=[]
    for item in fno_list_temp:
        stripped_item=item.strip()
        # stripped_item = stripped_item.replace('&','%26')
        fno_list.append(stripped_item)
    other_securities=['NIFTY','BANKNIFTY', 'FINNIFTY', 'MIDCPNIFTY', 'SENSEX', 'BANKEX', 'SX50', 'USDINR', 'CRUDEOIL', 'NATURALGAS']
    options = sorted(fno_list + other_securities, key=lambda x: x in other_securities, reverse=True)
    return options
fno_list=fno_list()


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
            html.Div([html.P(html.Label(html.H3('Select Security'))),dcc.Dropdown(id='security-dropdown',options=[{'label': option, 'value': option} for option in fno_list
            ], value=fno_list[0]),
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
                    html.Li(html.A('Open Interest', href='/openinterest'), style={'display': 'inline-block', 'marginRight': '20px', }),
                    html.Li(html.A('Bse Options', href='/bse_options'), style={'display': 'inline-block', 'marginRight': '20px'}),
                    html.Li(html.A('PWOI', href='/pwoi'), style={'display': 'inline-block', 'marginRight': '20px'})
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


def oi_layout():
    return html.Div(
        className='container',
        children=[
            get_navbar(),
            html.Div(
                children=[
                    get_left_menu(),

                    html.Div(
                        id='bar-plot',
                        className='content',
                        style={
                            'marginLeft': '20%',
                            'padding': '63px 10px 10px 10px',
                            'textAlign': 'center'
                        },
                        children=[
                            html.H1('Open Interest'),
                            get_bar_plot()[0]
                        ]
                    ),
                    html.Div(
                        id='bar-plot2',
                        className='content',
                        style={
                            'marginLeft': '20%',
                            'padding': '50px 10px 10px 10px',
                            'textAlign': 'center'
                        },
                        children=[
                            html.H1('Open Interest Change'),
                            get_bar_plot()[1]
                        ]
                    )
                ]
            )
        ]
    )
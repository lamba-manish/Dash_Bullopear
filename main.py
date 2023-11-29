import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from plot import PlotPlotly
import pandas as pd
from oi_oic import *
from pwoi import *
app = dash.Dash(__name__)
app.title='Bullopear'
oi_oichange=oi_layout()
# about = html.Div([get_navbar(),html.Br(),html.Br(),
#                   html.Div(children=[html.H1('about this web')],style={'margin-top':'30px'})
#                    ,html.H1('About page')],)
bse_options=html.Div([get_navbar(), html.Br(), html.Br(), html.Div(children=get_left_menu())])
pwoi = html.Div([get_navbar(),html.Br(),html.Br(),
                  html.Div(children=get_left_menu())],)
# menu=html.Div([dcc.Link('oi_oichange', href='/openinterest'),
#                dcc.Link('aboutt', href='/about')])
app.layout = html.Div([dcc.Location(id='url', refresh=False),html.Div(id='page-content')])
@app.callback(Output('page-content','children'),[Input('url', 'pathname')])
def display_page(pathname):
    if pathname=='/openinterest':
        return oi_oichange
    elif pathname=='/':
        return oi_oichange
    elif pathname=='/bse_options':
        return bse_options
    elif pathname=='/pwoi':
        return pwoi


@app.callback(Output('bar-plot', 'children'),Output('bar-plot2','children'),Input('security-dropdown', 'value'),Input('select-expiry', 'value'))
def update_bar_plot(security,expiry):
    fig1,fig2 = get_bar_plot(security=security, expiry=expiry)
    return fig1,fig2

@app.callback(Output('select-expiry', 'options'),Output('select-expiry', 'value'),Input('security-dropdown', 'options'),Input('security-dropdown', 'value'))
def update_expiry_dropdown(options, security_option):
    expiry_dates = Fetch(security_option).return_expiry_dates()
    options = [{'label': date, 'value': date} for date in expiry_dates]    
    default_value = options[0]['value']
    return options, default_value

app.config.suppress_callback_exceptions = True
app.favicon = None

if __name__ == '__main__':
    app.run_server(debug=True,threaded=True, port=8000)

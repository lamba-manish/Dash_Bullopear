import dash
from dash import html, dcc
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

page1_layout = html.Div([
    html.H1('Page 1'),
    html.P('This is the content of page 1.')
])

page2_layout = html.Div([
    html.H1('Page 2'),
    html.P('This is the content of page 2.')
])

page3_layout = html.Div([
    html.H1('Page 3'),
    html.P('This is the content of page 3.')
])

menu = html.Div([
    dcc.Link('Page 1', href='/page-1'),
    dcc.Link('Page 2', href='/page-2'),
    dcc.Link('Page 3', href='/page-3')
])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    menu,
    html.Br(),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),[Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page1_layout
    elif pathname == '/page-2':
        return page2_layout
    elif pathname == '/page-3':
        return page3_layout
    else:
        # if the URL is not recognized, display a 404 error
        return html.H1('404 - Page not found')

# run the app
if __name__ == '__main__':
    app.run_server(debug=True)

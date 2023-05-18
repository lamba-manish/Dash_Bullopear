from dash import html, dcc
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



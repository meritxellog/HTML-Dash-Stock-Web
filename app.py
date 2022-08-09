import dash
# import dash_core_components as dcc
# import dash_html_components as html
from datetime import date
from dash import Dash, dcc, html, Input, Output,State

import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

def blank_figure():
    fig = go.Figure(go.Scatter(x=[], y = []))
    fig.update_layout(template = None)
    fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.layout.plot_bgcolor = 'rgba(0,0,0,0)'
    fig.layout.paper_bgcolor = 'rgba(0,0,0,0)'
    return fig


app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.Div(
        [
            html.P("StockCheck App",
            className ="start"),
            html.Div([# Stock code input
                html.P("Input stock code:",style={'text-align':'left',
                'padding-left':'7vw','width':'20vw',
                'margin-bottom': '0vw'},className = "inputs"),
                dcc.Input("AAPL",id="stock-name", type='text',placeholder="AAPL"),
                html.Button('Submit', id='submit-val', n_clicks=0,className='button'),
            ],className="inputs"),
            html.Div([# Date range picker input
                dcc.DatePickerRange(
                    id='my-date-picker-range',
                    min_date_allowed=date(1995, 8, 5),
                    max_date_allowed=date(2022, 8, 5),
                    initial_visible_month=date(2022, 8, 5),
                    end_date=date(2022, 8, 5),
                    start_date=date(2021,8,1),
                    style = {'background':'rgb(230, 237, 247)'}
                )
            ],className="inputs"),
            html.Div([
                # Stock price button
                html.Button('Stock price', id='stockprice', n_clicks=0,className='button'),
                # Indicators button
                html.Button('Indicators', id='indicators', n_clicks=0,className='button'),
                # Number of days of forecast input
                html.Br(),
                dcc.Input(id="forecast_days"),
                # Forecast button
                html.Button('Forecast', id='submit-forecast-days', n_clicks=0,className='button')
            ],className="inputs")
        ],
        className = "container"
    ),
    html.Div([
            html.Div(
            [
                # html.Img(src='data:image/png;base64,{}'.format(encode_logo),id = 'logo')
                html.P("",id='Titulo',style={'color':'black','font-size':'24px'}),
                html.Br(),
                html.P("Insert a valid Stock code",id = "description",className = "description_ticker",style = {'margin-bottom:':'5vw'})
            ],
            className = "header"
            ),
            html.Br(),
            html.Div([
            # Stock price plot
            dcc.Graph( id = "graphs-content", figure = blank_figure())
            ],className = "plotBorder",id = "test-div"),
            # html.Div([
            # # Indicator plot
            # dcc.Graph( id = "graphs-indicator",figure = blank_figure())
            # ], id="main-content"),
            html.Div([
            # Forecast plot
            ], id="forecast-content")
        ],
        className = "content",style = {'background-color':'#43bccd'})   
],style = {'background-color':'#43bccd'})

@app.callback(
    [Output(component_id='Titulo',component_property='children'),
    Output('description','children')],
    Input('submit-val', 'n_clicks'),
    State('stock-name', 'value')
)
def update_data(n_clicks,value):
    if n_clicks>0:
        ticker = yf.Ticker(value)
        inf = ticker.info
        df = pd.DataFrame().from_dict(inf,orient="index").T
        return1 = inf["longBusinessSummary"]
    # return arg1, df
        return '{}'.format(inf["shortName"]),'{}'.format(return1)
    else:
        return dash.no_update




def get_stock_price_fig(df):
    fig = px.line(df,x = 'Date',y = ['Open','Close'], title = 'Opening Price vs Date',template='plotly_white')
    # fig.add_scatter(x=df['Date'], y=df['Close'], mode='lines',name='Close Price') 
    # fig.layout.plot_bgcolor = '#fff'
    # fig.layout.paper_bgcolor = '#f4f8fb'
    return fig

def get_more_fig(df):
    df['EWA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
    fig = px.scatter(df,
    x= 'Date',
    y= 'EWA_20',
    title="Exponential Moving Average vs Date",color_discrete_sequence=['rgb(31, 57, 109)'])
    fig.add_scatter(x= df['Date'],
    y= df['EWA_20'],mode='lines',line=dict(color="rgb(31, 57, 109)"))
    return fig


@app.callback(
    Output('graphs-content','figure'),
    [
        Input('my-date-picker-range', 'start_date'),
        Input('my-date-picker-range', 'end_date'),
        Input('stockprice', 'n_clicks'),
        Input('indicators', 'n_clicks')
    ],
    State('stock-name', 'value')
)
def update_plot_stock(start_date,end_date,stock_n_clicks,indicators_n_clicks,value):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    print(changed_id)
    df =  yf.download(value,start=start_date,end=end_date)# input paramter,start_date str,end_date str):
    df.reset_index(inplace=True)
    df.Date = pd.to_datetime(df.Date)
    df.Open = pd.to_numeric(df.Open)
    if 'stockprice.n_clicks' in changed_id:
        fig = get_stock_price_fig(df = df)
        return fig
    if 'indicators.n_clicks' in changed_id:
        fig = get_more_fig(df = df)
        return fig
    else:
        return dash.no_update
        
    
@app.callback(
    Output('test-div','className'),
    [Input('stockprice', 'n_clicks'),
    Input('indicators', 'n_clicks')])
def update_style(stock_click,ind_click):
    if (stock_click != 0) | (ind_click != 0):
        return "plotBorder2" 
    else:
        return "plotBorder"


""" @app.callback(
    Output('graphs-indicator','figure'),
    [
        Input('my-date-picker-range', 'start_date'),
        Input('my-date-picker-range', 'end_date'),
        Input('indicators', 'n_clicks')
    ],
    State('stock-name', 'value')
)
def update_plot_indicator(start_date,end_date,n_clicks,value):
    if n_clicks>0:
        df =  yf.download(value,start=start_date,end=end_date)# input paramter,start_date str,end_date str):
        df.reset_index(inplace=True)
        print(df.iloc[:,0])
        df.Date = pd.to_datetime(df.Date)
        df.Open = pd.to_numeric(df.Open)
        fig = get_more_fig(df = df)
        return fig # plot the graph of fig using dcc function
    else:
        return dash.no_update """

if __name__ == '__main__':
    app.run_server(debug=True)
import dash
# import dash_core_components as dcc
# import dash_html_components as html
from datetime import date
from dash import Dash, dcc, html, Input, Output,State

import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px


app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.Div(
        [
            html.P("Welcome to the Stock Dash App!",
            className ="start"),
            html.Div([# Stock code input
                html.P("Input stock code:",style={'text-align':'left','margin-left':'7vw'}),
                dcc.Input(id="stock-name", type='text'),
                html.Button('Submit', id='submit-val', n_clicks=0,className='button'),
            ],className="inputs"),
            html.Div([# Date range picker input
                dcc.DatePickerRange(
                    id='my-date-picker-range',
                    min_date_allowed=date(1995, 8, 5),
                    max_date_allowed=date(2022, 8, 5),
                    initial_visible_month=date(2022, 8, 5),
                    end_date=date(2022, 8, 5),
                    start_date=date(2019,8,1),
                    style = {'background':'rgb(230, 237, 247)'}
                )
            ],className="inputs"),
            html.Div([
                # Stock price button
                html.Button('Stock price', id='stockprice', n_clicks=0,className='button'),
                # Indicators button
                html.Button('Indicators', id='indicators', n_clicks=0,className='button'),
                # Number of days of forecast input
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
                html.P(id='Titulo',style={'color':'black','font-size':'24px'})
            ],
            className = "header"
            ),
            html.P(id = "description",className = "description_ticker"),
            html.Div([
            # Stock price plot
            dcc.Graph( id = "graphs-content")
            ]),
            html.Div([
            # Indicator plot
            dcc.Graph( id = "graphs-indicator")
            ], id="main-content"),
            html.Div([
            # Forecast plot
            ], id="forecast-content")
        ],
        className = "content")   
])

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




def get_stock_price_fig(df):
    print(df)
    fig = px.line(df,x = 'Date',y = 'Open', title = 'Opening Price vs Date') 
    return fig

def get_more(df):
    df['EWA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
    fig = px.scatter(df,
    x= 'Date',
    y= 'EWA_20',
    title="Exponential Moving Average vs Date")
    # fig.update_traces(mode= # appropriate mode)
    return fig


@app.callback(
    Output('graphs-content','figure'),
    [
        Input('my-date-picker-range', 'start_date'),
        Input('my-date-picker-range', 'end_date'),
        Input('stockprice', 'n_clicks')
    ],
    State('stock-name', 'value')
)
def update_plot_stock(start_date,end_date,n_clicks,value):
    if n_clicks>0:
        df =  yf.download(value,start=start_date,end=end_date)# input paramter,start_date str,end_date str):
        df.reset_index(inplace=True)
        print(df.iloc[:,0])
        df.Date = pd.to_datetime(df.Date)
        df.Open = pd.to_numeric(df.Open)
        fig = get_stock_price_fig(df = df)
    return fig# plot the graph of fig using dcc function
    

@app.callback(
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
        fig = get_more(df = df)
    return fig# plot the graph of fig using dcc function

if __name__ == '__main__':
    app.run_server(debug=True)
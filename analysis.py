from dash import html, dcc, Dash, Input, Output, callback
import pandas as pd
import plotly.express as px

df = pd.read_parquet('cpu.parquet')

# sub dataframes
launch_date_df = pd.read_parquet('launch_date.parquet')

# app
app = Dash(__name__)

app.layout = html.Div([
    html.H1("CPU analysis"),
    # drop down
    dcc.Dropdown(id = 'series', options=[
        {'label' : 'Intel core i3', 'value' : 'i3'},
        {'label' : 'Intel core i5', 'value' : 'i5'},
        {'label' : 'Intel core i7', 'value' : 'i7'},
        {'label' : 'Intel core i9', 'value' : 'i9'}
    ], value = 'i3', multi = False, style = {'width':'70%'}),

    # pie charts 
    html.Div(id = 'pie-charts', style = {'display':'flex', 'height' : '100%'}, children = [
        # status pie chart
        dcc.Graph(id = 'pie-status-chart', style = {'width':'50%'}),

        # smart cache chart
        dcc.Graph(id = 'pie-smart-cache-chart', style = {'width':'50%'})
    ]),

    # scatter charts
    html.Div(id = 'bar chart', children = [
        dcc.Graph(id = 'bar-cpu-launch', style = {'width' : '50%'})
    ])

],id = 'container')

@callback(
    [
        Output(component_id = 'pie-status-chart', component_property = 'figure'),
        Output(component_id = 'pie-smart-cache-chart', component_property = 'figure'),
        Output(component_id = 'bar-cpu-launch', component_property = 'figure'),
    ],
    [
        Input(component_id = 'series', component_property = 'value'),
    ]
)
def update(cpu_series):
    # calculating series wise data set only once
    df_series = df.loc[df['series'] == cpu_series]
    return (
        # pie charts 
        px.pie(df_series, names = 'status', hole = 0.5, title = 'status of CPUs', color_discrete_sequence=['LightSkyBlue', 'SlateGray', 'MidnightBlue']),

        px.pie(df_series, names='smart cache', hole = 0.5, title = 'smart cache ratio', color_discrete_sequence=['SeaGreen', 'SlateGray']),

        # line chart
        px.bar(launch_date_df, x = 'year', y = cpu_series, title = 'CPU lauch data')
    )

if __name__ == "__main__":
    app.run(debug = True)
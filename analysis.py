from dash import html, dcc, Dash, Input, Output, callback
import pandas as pd
import plotly.express as px

df = pd.read_parquet('cpu.parquet')

# sub dataframes
launch_date_df = pd.read_parquet('launch_date.parquet')

core_count_df = pd.read_parquet('core_count_df.parquet')

TDP_df = pd.read_parquet('TDP_df.parquet')

# app
app = Dash(__name__)

app.layout = html.Div(id = 'container', children = [
    html.H1("CPU analysis"),
    # drop down
    dcc.Dropdown(id = 'series', options=[
        {'label' : 'Intel core i3', 'value' : 'i3'},
        {'label' : 'Intel core i5', 'value' : 'i5'},
        {'label' : 'Intel core i7', 'value' : 'i7'},
        {'label' : 'Intel core i9', 'value' : 'i9'}
    ], value = 'i3', multi = False, style = {'width':'70%'}),

    # pie charts 
    html.Div(id = 'pie-charts', style = {'display':'flex'}, children = [
        # status pie chart
        dcc.Graph(id = 'pie-status-chart', style = {'width':'50%'}),

        # smart cache chart
        dcc.Graph(id = 'pie-smart-cache-chart', style = {'width':'50%'})
    ]),

    # bar charts
    html.Div(id = 'bar charts', children = [
        dcc.Graph(id = 'bar-cpu-launch', style = {'width' : '50%'})
    ]),

    # line chart
    html.Div(id = 'line charts', style = {'display':'flex'}, children = [
        # generation v/s core count chart
        dcc.Graph(
            id = 'line-gen-core_count',
            style = {'width' : '50%'},
            figure = px.line(core_count_df ,x = 'generation', y = ['min core count','max core count'], markers = True, color_discrete_sequence = ['LightSkyBlue','SlateGray'], title='generation and core count'), 
        ),

        # generation v/s TDP chart
        dcc.Graph(
            id = 'line-gen-TDP',
            style = {'width' : '50%'},
            figure = px.line(TDP_df ,x = 'generation', y = ['min TDP','max TDP'], markers = True, color_discrete_sequence = ['LightSkyBlue','SlateGray'], title='generation and TDP'), 
        ),    
    ])

])

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
    # calculating series wise data set
    df_series = df.loc[df['series'] == cpu_series]
    return (
        # pie charts 
        px.pie(df_series, names = 'status', hole = 0.5, title = 'status of CPUs', color_discrete_sequence=['LightSkyBlue', 'SlateGray', 'MidnightBlue']),

        px.pie(df_series, names='smart cache', hole = 0.5, title = 'smart cache ratio', color_discrete_sequence=['CornflowerBlue', 'LightGreen']),

        # bar chart
        px.bar(launch_date_df, x = 'year', y = cpu_series, title = 'CPU lauch data')
    )
# run the dash app
if __name__ == "__main__":
    app.run(debug = True)
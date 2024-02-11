from dash import html, dcc, Dash, Input, Output, callback
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
load_dotenv()
from os import environ

df = pd.read_parquet('data/cpu.parquet')

# sub dataframes
launch_date_df = pd.read_parquet('data/launch_date.parquet')

core_count_df = pd.read_parquet('data/core_count_df.parquet')

TDP_df = pd.read_parquet('data/TDP_df.parquet')

# app
app = Dash(__name__)
app.layout = html.Div(className = 'container', children = [
    # app header
    html.Header(className= 'header', children = [
        html.Link(rel='stylesheet', href='assets/css/style.css'),
        html.Script(src = "https://kit.fontawesome.com/897c2f2548.js", crossOrigin = 'anonymous')
    ]),

    # app main content
    html.Main(className = 'main', children = [
        # heading 
        html.Div(id = 'header', children = [
            html.Img(src='assets/images/logo.png'),
            html.H1('CPU Analysis')
        ]),
        # line charts
        html.Div(id = 'line-charts-sep', style = {'display':'flex'}, children = [
            # generation v/s core count chart
            dcc.Graph(
                id = 'line-gen-core-count',
                style = {'width' : '50%'},
                figure = px.line(
                    core_count_df ,
                    x = 'generation',
                    y = ['min core count','max core count','avg core count'],
                    markers = True,
                    color_discrete_sequence = ['#B3B3B4', '#5D5D5D','#446CF1'], 
                    title='generation v/s core count'
                ), 
            ),

            # generation v/s TDP chart
            dcc.Graph(
                id = 'line-gen-TDP',
                style = {'width' : '50%'},
                figure = px.line(
                    TDP_df,
                    x = 'generation',
                    y = ['min TDP','max TDP', 'avg TDP'],
                    markers = True, 
                    color_discrete_sequence = ['#B3B3B4', '#5D5D5D','#446CF1'], 
                    title='generation v/s TDP'
                ), 
            ),    
        ]),

        # break
        html.Hr(),
        html.H3('select the series of CPU'),

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

        # line chart
        html.Div(id = 'line-charts-drop', children = [
            dcc.Graph(id = 'line-cpu-launch', style = {'width' : '50%'})
        ])
    ]),

    # app footer
    html.Footer(className = 'footer', children = [
        html.Div(className = "data", children = [
            html.Div(className = 'social', children = [
                html.Span(className = 'label', children= 'follow me on'),
                html.Div(className = 'url', children = [
                    html.Span([html.I(className='icon-svg', children=[
                        html.Embed(src = 'assets/svg/github.svg')
                    ]), html.A('github', href = 'https://github.com/himank670429')]),

                    html.Span([html.I(className='icon-svg', children=[
                        html.Embed(src = 'assets/svg/linkedin.svg')
                    ]), html.A('linkedin', href = 'https://www.linkedin.com/in/himank-singh-65b411249/')]),

                    html.Span([html.I(className='icon-svg', children=[
                        html.Embed(src = 'assets/svg/instagram.svg')
                    ]), html.A('intagram', href = 'https://www.instagram.com/himank_singh9/')]),
                ])
            ]),

            html.Div(className = 'source', children= [
                html.Span(className = 'label', children= 'Data Source'),

                html.Span([html.I(className='icon-svg', children=[
                    html.Embed(src = 'assets/svg/intel.svg')
                ]), html.A('intel offcial website', href = 'https://www.intel.in/content/www/in/en/homepage.html', target="_blank")])
            ]),
        ]),

        html.Span(className = 'copyright', children = 'Copyright © 2023 CPU Analysis Dashboard'),
        
    ]),
])

@callback(
    [
        Output(component_id = 'pie-status-chart', component_property = 'figure'),
        Output(component_id = 'pie-smart-cache-chart', component_property = 'figure'),
        Output(component_id = 'line-cpu-launch', component_property = 'figure'),
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
        px.pie(
            df_series,
            names = 'status', 
            hole = 0.5, 
            title = 'status of CPUs', 
            color_discrete_sequence=['#00FFFF', '#017AFF', '#191970']
        ),

        px.pie(
            df_series, 
            names='smart cache', 
            hole = 0.5, 
            title = 'smart cache ratio', 
            color_discrete_sequence=['#3261B4', '#ADB7BA']
        ),

        # line chart
        px.line(
            launch_date_df, 
            x = 'year', 
            y = [cpu_series], 
            title = 'CPU lauch data', 
            markers = True,
            color_discrete_sequence=['#848BDD']
        )
    )

# run the dash app
if __name__ == "__main__":
    app.run(debug = (environ.get('DEBUG')=='True'))
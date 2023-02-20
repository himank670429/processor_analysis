from dash import html, dcc, Dash, Input, Output, callback
import pandas as pd
import plotly.express as px

df = pd.read_json('cpu.json')

app = Dash(__name__)

app.layout = html.Div([
    html.H1("CPU analysis"),
    html.Div(children = [
        dcc.Dropdown(id = 'series', options=[
            {'label' : 'Intel core i3', 'value' : 'i3'},
            {'label' : 'Intel core i5', 'value' : 'i5'},
            {'label' : 'Intel core i7', 'value' : 'i7'},
            {'label' : 'Intel core i9', 'value' : 'i9'}
        ], value='i3', multi=False,style = {'width':'70%'}),

        dcc.Graph(id = 'pie chart', style = {'width':'50%'})
    ], id = 'pei-chart-vis', style = {'display':'grid'}) 
])

@callback(
    Output(component_id = 'pie chart', component_property = 'figure'),
    Input(component_id = 'series', component_property = 'value')
)
def update_graph(cpu_series):
    filtered_df = df.loc[df['series'] == cpu_series]
    return px.pie(filtered_df, names = 'status', hole = 0.5)

if __name__ == "__main__":
    app.run(debug=True)
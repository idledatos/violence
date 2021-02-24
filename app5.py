import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import datetime as dt



data = pd.read_csv("dashapp.csv",index_col=0)
data.index=pd.to_datetime(data.index)


# Initialise the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
server = app.server

# Define the app
app.layout = dbc.Container([
					dbc.Row(html.H1("|| IDLE || El Efecto de la Pandemia en Los Reportes de Violencia Doméstica"), justify='center'),
					#dbc.Row(html.H1("Evaluación de los reportes de violencia en CABA"),justify="center"),
					dbc.Row(html.P("Comparamos los reportes de violencia doméstica del 2020 con los que hubieramos esperado según nuestros modelos estadísticos", style={'color': 'white', 'fontSize': 16}),justify="center"),
					#dbc.Row(html.P(""),justify="center"),
					dbc.Row([
					dbc.Col([
# dropdown  y  checklist columna izquierda
						html.H4("Modelo estadístico", style={'color': 'white', 'fontSize': 14,'justify':'center'}),
                        dcc.Checklist(

                        id='Kind', 
                        value=['Observed','OLS'],
                        options=[{'label': 'Theory Driven', 'value': 'OLS'},
						{'label': 'Data Driven', 'value': 'FB'},
						{'label': 'Observado', 'value': 'Observed','disabled':False}]),                         
                        dbc.Row(html.H4("Variable",style={'color': 'white', 'fontSize': 14}),justify="center"),
                        dcc.Dropdown(
                        id='variable', clearable=False, 
                        value= 'calls', 
                        options=[
                        {'label': 'Todas las llamadas', 'value': 'calls'},
						{'label': 'Por violencia física', 'value': 'Física'},
						{'label': 'Por violencia psicológica', 'value': 'Psicológica'},
						{'label': 'Hechas por la comisaría', 'value': 'Comisaría'},
						{'label': 'Hechas por la víctima', 'value': 'Víctima'},
						])],
                        width=3),
#Indicators columna derecha uno al lado del otro
					dbc.Col([dbc.Row([
							dbc.Col(dcc.Graph(id='graph2'),style={"height": "100%"}),
							dbc.Col(dcc.Graph(id='graph3'),style={"height": "100%"})]),
					html.P('Elija la cantidad de días desde el comienzo de ASPO para ver el efecto'),
					dcc.Slider(
								id='slider',	
							    min=0,
							    max=287,
							    step=1,
							    marks={ 0 : '0',
							    		100: '100 días de cuarentena',
							    		200: '200 días de cuarentena',
							    		287: 'Efecto total'},
							    value=0 )])]),			
#Series fila inferior
dbc.Row(dcc.Graph(id='graph'),justify='center',  style={"height": "100%", 'width':"100%", 'marginBottom': 0, 'marginTop': 0})])


@app.callback(
    Output('graph', 'figure'),
    [Input("Kind", "value"),
    Input("variable", "value")]
)

def update_graph (Kind,variable): 
	fig=go.Figure()
	fig.update_layout(autosize=True)
	fig.layout.template = 'plotly_dark'
	
	if type(Kind)!=list:
		Kind=[Kind]
	if type(variable)!=list:
		variable=[variable]	
	for i in Kind:
		for e in variable:
			df=data[data['Kind']==i]
			df=df[df['variable']==e]
			fig.add_trace(go.Scatter(x=df.index,y=df.Number,name=i+"-"+e))
	return fig.update_layout(
		{'plot_bgcolor': 'rgba(10, 15, 30, 90)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)'}, 
        title_font_family="Courier New, monospace",
	    title_font_color="white",
	    title_font_size=18)

@app.callback(
    Output('graph2', 'figure'),
    [Input("Kind", "value"),
    Input("variable", "value"),
    Input('slider', 'value')]
)

def update_graph2 (Kind,variable,slider): 	
	fig2 = go.Figure()
	fig2.update_layout(width=300,height=250)
	fig2.layout.template = 'plotly_dark'
	ld=pd.to_datetime("20-03-20")
	date_list = [ld + dt.timedelta(days=x) for x in range(slider)]
	if type(Kind)!=list:
		Kind=[Kind]
	if type(variable)!=list:
		variable=[variable]	
	for i in Kind:
		for e in variable:
			df=data[data['Kind']==i]
			df=df[df['variable']==e]
			estimated=df[df.index>="20-03-20"]
			estimated=df[df.index.isin(date_list)]
			estimated=estimated['Number'].sum()
			aux=data[data['variable']==e]
			aux=aux[aux['Kind']=='Observed']
			aux=aux[aux.index>="20-03-20"]
			aux=aux[aux.index.isin(date_list)]
			reference=aux['Number'].sum()


	return fig2.add_trace(go.Indicator(	
	title = {"text": "Efecto " + str(slider) +" días " + i},
	title_font_size=16,
    mode = "number",
    value = reference-estimated,
    domain = {'x': [0.5, 0.5], 'y': [1, 0]},))

@app.callback(
    Output('graph3', 'figure'),
    [Input("Kind", "value"),
    Input("variable", "value"),
    Input('slider', 'value')]
)

def update_graph3 (Kind,variable,slider): 	
	fig2 = go.Figure()
	fig2.update_layout(width=300,height=250)
	fig2.layout.template = 'plotly_dark'
	ld=pd.to_datetime("20-03-20")
	date_list = [ld + dt.timedelta(days=x) for x in range(slider)]
	if type(Kind)!=list:
		Kind=[Kind]
	if type(variable)!=list:
		variable=[variable]	
	for i in Kind:
		for e in variable:
			df=data[data['Kind']==i]
			df=df[df['variable']==e]
			estimated=df[df.index>="20-03-20"]
			estimated=df[df.index.isin(date_list)]
			estimated=estimated['Number'].sum()
			aux=data[data['variable']==e]
			aux=aux[aux['Kind']=='Observed']
			aux=aux[aux.index>="20-03-20"]
			aux=aux[aux.index.isin(date_list)]
			reference=aux['Number'].sum()


	return fig2.add_trace(go.Indicator(	
	title = {"text": "Efecto " + str(slider)+" días "  + i},
	title_font_size=16,
    mode = "delta",
    value = reference,
    domain = {'x': [0.5, 0.5], 'y': [1, 0]},
    delta = {'reference': estimated, 'relative': True, 'position' : "bottom"}))

# Run the app
if __name__ == '__main__':
    app.run_server(port=8000, host='127.0.0.1',debug=True)

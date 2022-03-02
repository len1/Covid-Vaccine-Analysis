import dash
from dash.dash import Dash
from dash_core_components import Graph  # pip install dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input

import dash_table

from dash_extensions import Lottie  # pip install dash-extensions
import dash_bootstrap_components as dbc
from dash_html_components.Figure import Figure
# pip install dash-bootstrap-components
from dash_html_components.Title import Title
from pandas.io.formats import style
import plotly.express as px  # pip install plotly
import plotly.graph_objs as go
import pandas as pd  # pip install pandas
from dash_bootstrap_templates import load_figure_template


app = dash.Dash(__name__)

url_vaccinces = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv'
vaccine_data = pd.read_csv(url_vaccinces)

# Fix the date for vaccination data
vaccine_data['date'] = pd.to_datetime(vaccine_data['date'])

# Remove null values
vaccine_data['daily_vaccinations'] = vaccine_data['daily_vaccinations'].fillna(
    0)
vaccine_data['people_fully_vaccinated'] = vaccine_data['people_fully_vaccinated'].fillna(
    0)
vaccine_data['people_vaccinated'] = vaccine_data['people_vaccinated'].fillna(0)
vaccine_data['total_vaccinations'] = vaccine_data['total_vaccinations'].fillna(
    0)
vaccine_data['total_boosters'] = vaccine_data['total_boosters'].fillna(0)


vaccine_data_1 = vaccine_data.groupby(['date', 'location', 'iso_code'])[['daily_vaccinations', 'people_fully_vaccinated',
                                                                        'people_vaccinated', 'total_vaccinations', 'total_boosters']].sum().reset_index()

total_vaccinated = vaccine_data_1[vaccine_data_1['location']
                                  == 'World']['people_fully_vaccinated'].iloc[-1]

new_fully_vaccinated = vaccine_data_1[vaccine_data_1['location'] == 'World']['people_fully_vaccinated'].iloc[-1] - \
    vaccine_data_1[vaccine_data_1['location'] ==
                   'World']['people_fully_vaccinated'].iloc[-2]

total_boosters = vaccine_data_1[vaccine_data_1['location']
                                == 'World']['total_boosters'].iloc[-1]

new_boosters = vaccine_data_1[vaccine_data_1['location'] == 'World']['total_boosters'].iloc[-1] - \
    vaccine_data_1[vaccine_data_1['location']
                   == 'World']['total_boosters'].iloc[-2]

population_df = pd.read_csv(
    "/Users/leonardkgoadi/VSCodeProjects/covidVaccineAnalysis/population_data.csv", delimiter=";")
population_df.rename(
    columns={'Country Code': 'iso_code', '2020': 'population'}, inplace=True)
population_df.drop(columns=['Unnamed: 3'], axis=1, inplace=True)
vaccine_data_1_population = pd.merge(
    left=vaccine_data_1, right=population_df, how='left', on='iso_code')

world_population = 7913852200

percent_global_vaccinated = (total_vaccinated/world_population) * 100

summary_df = vaccine_data_1[['date','location','daily_vaccinations', 'people_fully_vaccinated', 'total_boosters', 'total_vaccinations']]

summary_df.rename(columns={"date": "Date", "location": "Country", "daily_vaccinations": "Daily Vaccinations",
                           "people_fully_vaccinated": "Fully Vaccinated", "total_boosters": "Total Boosters",
                           "total_vaccinations": "Total Vaccinations"}, inplace=True)

summary_df['Date'] = pd.to_datetime(summary_df['Date']).dt.date

# ------------------------------------------------------------------------------
# DBC COMPONENTS

total_vaccinated_card = dbc.Card([
    dbc.CardHeader(html.H4("Worldwide Fully Vaccinated",
                           style={'text-align': 'center',
                                  'color': 'darkblue'})),

    dbc.CardBody([
        html.P(f"{total_vaccinated:,.0f}",
               style={'textAlign': 'center',
                      'color': 'green',
                      'margin': 'auto',
                      'fontSize': 20}),

    ])

], color='#F0F8FF', style={'width': '15rem', 'box-shadow': '6px 6px 6px #1f2c56'}, inverse=True)


percentage_vaccinated_card = dbc.Card([
    dbc.CardHeader(html.H4("% Vaccinated Fully Worldwide", style={
        'text-align': 'center', 'color': 'darkblue'})),

    dbc.CardBody([
        html.P(f"{percent_global_vaccinated:.0f}%",
               style={'textAlign': 'center',
                      'color': 'green',
                      'margin': 'auto',
                      'fontSize': 20}),

    ])

], color='#F0F8FF', style={'width': '15rem', 'box-shadow': '6px 6px 6px #1f2c56'}, outline=True, inverse=True)

new_vaccinated_card = dbc.Card([
    dbc.CardHeader(html.H4("New Worldwide Vaccinations",
                           style={'text-align': 'center',
                                  'color': 'darkblue'})),

    dbc.CardBody([
        html.P(f"{new_fully_vaccinated:,.0f}",
               style={'textAlign': 'center',
                      'color': 'green',
                      'margin': 'auto',
                      'fontSize': 20}),

    ])

], color='#F0F8FF', style={'width': '15rem', 'box-shadow': '6px 6px 6px #1f2c56'}, inverse=True)

total_boosters_card = dbc.Card([
    dbc.CardHeader(html.H4("Worldwide Total Boosters",
                           style={'text-align': 'center',
                                  'color': 'darkblue'})),

    dbc.CardBody([
        html.P(f"{total_boosters:,.0f}",
               style={'textAlign': 'center',
                      'color': 'green',
                      'margin': 'auto',
                      'fontSize': 20}),

    ])

], color='#F0F8FF', style={'width': '15rem', 'box-shadow': '6px 6px 6px #1f2c56'}, inverse=True)

new_boosters_card = dbc.Card([
    dbc.CardHeader(html.H4("New Worldwide Boosters",
                           style={'text-align': 'center',
                                  'color': 'darkblue'})),

    dbc.CardBody([
        html.P(f"{new_boosters:,.0f}",
               style={'textAlign': 'center',
                      'color': 'green',
                      'margin': 'auto',
                      'fontSize': 20}),

    ])

], color='#F0F8FF', style={'width': '15rem', 'box-shadow': '6px 6px 6px #1f2c56'}, inverse=True)





# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([
    html.H1("Vaccination Overview", style={'text-align': 'center'}),

    dbc.Row([

        dbc.Col([

            html.H6('Last Updated: ' + str(vaccine_data_1['date'].iloc[-1].strftime('%B %d, %Y')) + ' 00:01 (UTC)',
                    style={'color': 'orange', 'fontSize': 15})



        ])

    ], style={'justify': 'start'}),


    dbc.Row([
        dbc.Col([total_vaccinated_card], style={
                'display': 'inline-block'}),
        dbc.Col([percentage_vaccinated_card], style={
                'display': 'inline-block'}),
        dbc.Col([new_vaccinated_card], style={
                'display': 'inline-block'}),
        dbc.Col([total_boosters_card], style={
                'display': 'inline-block'}),
        dbc.Col([new_boosters_card], style={
                'display': 'inline-block'}),





    ], style={'justify-content': 'space-evenly', 'display': 'flex'}),

    html.Br(),
    html.Br(),
    html.Br(),




    html.Div([


        dcc.Dropdown(id="slct_country",
                     multi=False,
                     value='South Africa',
                     style={'width': "60%"},
                     options=[{'label': c, 'value': c}
                              for c in (vaccine_data_1['location'].unique())],

                     ),

        dcc.Graph(id='stacked_area'),


        html.Br(),


    ], style={'width': '50%', 'display': 'inline-block'}),

    html.Div([


        dcc.Dropdown(id="slct_country2",
                     multi=False,
                     value='South Africa',
                     style={'width': "60%"},
                     options=[{'label': c, 'value': c}
                              for c in (vaccine_data_1['location'].unique())],

                     ),

        dcc.Graph(id="daily_graph")

    ], style={'width': '50%', 'display': 'inline-block'}),
    
    html.Div([
        dash_table.DataTable(
        data=summary_df.sort_values("Fully Vaccinated", ascending=False).to_dict('records'),
        columns=[{'id': c, 'name': c, 'type': 'numeric', 'format': {'specifier': ','}} for c in summary_df.columns],
        fixed_rows={"headers": True},
        sort_action="native",
        style_table={
            "minHeight": "600px",
            "height": "600px",
            "width": "1400px",
            "overflowY": "scroll",
            "overflowX": "scroll"
        },
        style_header={
            "textAlign": "center",
            "fontSize": 14,
            "backgroundColor": "#C9FFE5"
        },
        style_data={
            "fontSize": 12
        },
        style_data_conditional=[{
            "if": {"row_index": "odd"},
            "backgroundColor": "#F0F8FF"
        },
        
        {
            'if': {
                'filter_query': '{{Daily Vaccinations}} = {}'.format(summary_df['Daily Vaccinations'].max()),
            },
            'backgroundColor': '#0048BA',
            'color': 'white'
        },
                
            ]
        
)
    ], style={'justify-content': 'space-evenly', 'display': 'flex'}),
    
    
    
    


], id="main_container")


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    Output(component_id='stacked_area', component_property='figure'),
    [Input(component_id='slct_country', component_property='value')]
)
def update_graph(option_slctd):

    vaccine_data_1_df = vaccine_data_1.copy()
    vaccine_data_1_df = vaccine_data_1_df[vaccine_data_1_df['location']
                                          == option_slctd]

    fig = go.Figure()

    # Create the Area Chart Object
    obj1 = go.Scatter(
        name="Fully Vaccinated",
        x=vaccine_data_1_df['date'],
        y=vaccine_data_1_df['people_fully_vaccinated'],
        #mode = 'lines',
        #line=dict(width=5, color='green'),
        stackgroup='one'
    )

    obj2 = go.Scatter(
        name="vaccinated",
        x=vaccine_data_1_df['date'],
        y=vaccine_data_1_df['people_vaccinated'],
        #mode = 'lines',
        #line=dict(width=1, color='green'),
        stackgroup='one'
    )

    fig.add_trace(obj1)
    fig.add_trace(obj2)

    fig.update_layout(
        title="Cumulative Vaccinations by Dose",
        title_font_size=20, legend_font_size=20
    )

    return fig


@app.callback(
    Output(component_id='daily_graph', component_property='figure'),
    [Input(component_id='slct_country2', component_property='value')]
)
def update_daily_graph(country_slctd):
    vaccine_data_2_df = vaccine_data_1.copy()
    vaccine_data_2_df = vaccine_data_2_df[vaccine_data_2_df['location']
                                          == country_slctd]

    fig2 = go.Figure()

    obj6 = go.Scatter(
        x=vaccine_data_2_df['date'],
        y=vaccine_data_2_df['daily_vaccinations'],

    )
    fig2.add_trace(obj6)

    fig2.update_layout(
        title="Daily Vaccinations",
        title_font_size=20, legend_font_size=20
    )

    return fig2


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=False, host='127.0.0.1', port=8051)

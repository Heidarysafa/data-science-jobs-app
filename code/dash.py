# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 21:43:28 2021

@author: mojtaba heidarysafa
"""


#from app_sub import top_skill_list,us_state_abbrev,list_of_us_codes, modify_start_end_date
import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output, State
import plotly.express as px
from datetime import datetime as dt


import pandas as pd
import time
import pymysql #version 0.9.2

from pandas.tseries.offsets import DateOffset

list_of_us_codes = ['AK', 'AL', 'AR', 'AS', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'GU', 'HI',
                    'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MP',
                    'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI',
                    'SC', 'SD', 'TN', 'TX', 'UM', 'UT', 'VA', 'VI', 'VT', 'WA', 'WI', 'WV', 'WY']
us_state_abbrev = {
    'AL': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VT': 'Vermont',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming',
}



###### count plot prep weeks
def modify_start_end_date(date, forward=True):
    '''
    :param date: datetime for the date to modify
    :param forward: a boolean that specified if the date is moving forward
    to the beginning next week or back to the end of previous week
    :return: modified datetime
    '''
    if forward:
        if date.weekday() != 0:
            offset = 7 - date.weekday()
            start_date = date + DateOffset(offset)
            return start_date
        else:
            return date
    else:
        # modify the end date of dataframe to the end of last week
        if date.weekday() != 0:
            offset = date.weekday()
            end_date = date - DateOffset(offset + 1)
            return end_date
        else:
            return date

'''
###### in case of connecting to 
host = "your_database_on_amazon.....rds.amazonaws.com"

port =int(3306)
dbname="job_posts"
user="yourusername"
password="yourpassword"
##### create connection with parameters you need
conn = pymysql.connect(host, user=user, port=port, passwd=password, db=dbname)
start ="""2020-04-10"""
end = """2020-05-10"""
#init_querry = 'SELECT posted_date,state,term,count(job_title) as count, %s from dash_table  group by posted_date, state, term '% querry
init_querry = 'SELECT * from dash_grouped_data'
skillset_sql = pd.read_sql(init_querry, con=conn)
conn.close()
'''
skillset_sql = pd.read_csv('grouped_april_final_for_dash.csv')
skillset_sql['posted_date'] = skillset_sql['posted_date'].apply(lambda x:dt.strptime(x,'%Y-%m-%d'))
def manipulate_skillset(All_skills):
    # data manipulation for bar chart
    all_skills = All_skills.iloc[:,2:].sum(axis=0).sort_values(ascending= False).to_frame()
    all_skills.reset_index(inplace = True)
    all_skills.rename(columns={"index": "Skills", 0: "Counted Ads"},inplace = True)
    all_skills.set_index('Skills', inplace =True)
    return all_skills



app = dash.Dash(__name__)
server = app.server
app.layout = html.Div(className="container scalable", children=[

    html.Div(
        id="banner",
        className="banner",
        children=[
            html.H2("US Data Science Job Market Dashboard   V.1.1"),
            html.Img(src=app.get_asset_url("dsi.jpg")),
        ]),

    html.Div(
        id="dropdown-select-outer",
        children=[
            html.Div(
                [
                    html.P("Job Title"),
                    dcc.Dropdown(
                        id="dropdown-select",
                        options=[
                            {"label": "Data Scientist", "value": "data scientist"},
                            {"label": "Machine Learning Engineer", "value": "machine learning engineer"},
                            {"label": "Data Analyst", "value": "data analyst"},
                            {"label": "All", "value": "all"},
                        ],
                        value="data scientist",
                    ),
                ],
                className="selector",
            ),
            html.Div(
                [
                    html.P("Select Date Range"),
                    dcc.DatePickerRange(
                        id="date-picker-range",
                        min_date_allowed=dt(2020, 4, 20),
                        max_date_allowed=dt(
                            2021, 4, 10
                        ),  # set maximum limit according to local casting
                        initial_visible_month=dt(2020, 4, 20),
                        minimum_nights=3,
                        display_format="MMM Do, YY",
                        start_date=dt(2020, 4, 20),
                        end_date=dt(2020, 10, 30),
                    ),
                ],
                id="date-picker-outer",
                className="selector",
            ),
            html.Div(
                [
                    html.Button(
                        "reset states",
                        id="reset-button",
                        n_clicks=0,
                        n_clicks_timestamp=0,
                        style={'background-color': '#f07400'}
                    )
                ],
                title="Click to reset  graphs back to default (all states).",
                className="selector_button",
            )

        ]

    ),

    html.Div(id='output_container', children=[]),
    html.Br(),
    html.Div(className='eight columns', children=[
        html.H3(id='selected_state', style={'text-align': 'center'})]
             ),
    html.Div(id='map-container', className="eight columns",
             children=dcc.Loading(dcc.Graph(id='my_US_map', figure={}), type='circle')),
    html.Div(id='map-container2', className="four columns", children=dcc.Loading(

        children=dcc.Graph(id='skill-plot', figure={}))),
    html.Br(),
    html.Div(id='container', className="twelve columns",
             children=dcc.Loading(dcc.Graph(id='count_plot', figure={}), type='circle')
             ),
    html.Div(
        id="footer",
        className="footer",
        children=[
            html.H4("Last update on: April 2021"),
            html.H4("University of Virginia"),
            html.H6("Developed by: M. Heidarysafa"),
        ]),

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(

    Output(component_id='my_US_map', component_property='figure'),
    [Input(component_id='dropdown-select', component_property='value'),
     Input("date-picker-range", "start_date"),
     Input("date-picker-range", "end_date"),
     ]
)
def update_graph(option_slctd, start_d, end_d):
    print(option_slctd)
    print(type(option_slctd))
    time.sleep(1)
    # filter data in the date picker range
    # !!! overide the main job_skills with this to reduce repeteation when calling sql
    skillset_sql_map = skillset_sql[(skillset_sql['posted_date'] >= pd.Timestamp(start_d).to_pydatetime()) & (
                skillset_sql['posted_date'] < pd.Timestamp(end_d).to_pydatetime())]

    # map_data_df = skillset_sql_map.iloc[:,0:3]
    # map_data_df = map_data.to_frame()
    # map_data_df.reset_index(inplace = True)
    # map_data_df['state_name'] = map_data_df['state'].map(us_state_abbrev)
    # map_data_df.rename(columns ={'description':'count'}, inplace =True)
    if option_slctd != 'all':
        skillset_sql_map = skillset_sql_map[(skillset_sql_map["term"] == option_slctd)]
        skillset_sql_map.groupby(['posted_date', 'state'])['count'].sum().reset_index()
        skillset_sql_map.drop('posted_date', axis=1, inplace=True)
        map_data = skillset_sql_map.groupby(['state'])['count'].sum()
    else:
        skillset_sql_map.groupby(['posted_date', 'state'])['count'].sum().reset_index()
        skillset_sql_map.drop('posted_date', axis=1, inplace=True)
        map_data = skillset_sql_map.groupby(['state'])['count'].sum()

    map_data_df = map_data.to_frame()
    map_data_df.reset_index(inplace=True)
    map_data_df['state_name'] = map_data_df['state'].map(us_state_abbrev)
    # map_data_df.rename(columns ={'description':'count'}, inplace =True)

    dff = map_data_df

    # Plotly Express
    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state',  # careful changing this will cause not showing states
        scope="usa",
        color='count',
        hover_data=['state_name', 'count'],
        color_continuous_scale=px.colors.sequential.Bluyl,
        labels={'number of jobs: description'}
        # template='plotly_dark'
    )
    return fig


# this will reflect the effect of clicking on the us map by selecting the state
@app.callback(
    Output(component_id='selected_state', component_property='children'),
    [Input(component_id='my_US_map', component_property='clickData'),
     Input("reset-button", "n_clicks_timestamp")]
)
def get_state(clickData, reset_click):
    state = 'No State'
    now = time.time() * 1000
    if clickData is not None:
        state = clickData["points"][0]['location']
    if int(now) - int(reset_click) < 3000 and int(reset_click) > 0:
        state = "US"
    return 'You have selected: {}'.format(state)


# update the skill plot after changes on map, field
@app.callback(
    Output(component_id='skill-plot', component_property='figure'),
    [Input(component_id='my_US_map', component_property='clickData'),
     Input(component_id='dropdown-select', component_property='value'),
     Input("date-picker-range", "start_date"),
     Input("date-picker-range", "end_date"),
     Input("reset-button", "n_clicks_timestamp")
     ]
)
def plot_top_skills(clickData, value, start_d, end_d, reset_click):
    time.sleep(1)
    now = time.time() * 1000
    skillset_sql_skill = skillset_sql[(skillset_sql['posted_date'] >= pd.Timestamp(start_d).to_pydatetime()) & (
                skillset_sql['posted_date'] < pd.Timestamp(end_d).to_pydatetime())]

    ####prepare skills for bar chart
    skillset = skillset_sql_skill.drop(['count', 'posted_date'], axis=1)
    if value == 'all':

        skillset = skillset
    else:
        skillset = skillset[skillset['term'] == value]
    if int(now) - int(reset_click) < 3000 and int(reset_click) > 0:

        skill = manipulate_skillset(skillset)
        fig = px.bar(skill[:20].iloc[::-1], x="Counted Ads")
        return fig
    elif clickData and (clickData["points"][0]["location"] in list_of_us_codes):
        skillset = skillset_sql_skill.drop(['count', 'posted_date'], axis=1)
        state = clickData["points"][0]["location"]
        if value == 'all':
            state_skillset = skillset[skillset['state'] == state]
        else:

            state_skillset = skillset[(skillset['term'] == value) & (skillset['state'] == state)]
        skill = manipulate_skillset(state_skillset)
        fig = px.bar(skill[:20].iloc[::-1], x="Counted Ads")
        return fig


    else:

        skill = manipulate_skillset(skillset)
        fig = px.bar(skill[:20].iloc[::-1], x="Counted Ads")

        return fig


# creating count presentation plot

@app.callback(
    Output(component_id='count_plot', component_property='figure'),
    [Input(component_id='my_US_map', component_property='clickData'),
     Input(component_id='dropdown-select', component_property='value'),
     Input("date-picker-range", "start_date"),
     Input("date-picker-range", "end_date"),
     Input("reset-button", "n_clicks_timestamp")
     ]
)
def update_count_plot(clickData, value, start_d, end_d, reset_click):
    time.sleep(1)
    w_start_d = modify_start_end_date(pd.Timestamp(start_d).to_pydatetime(), forward=True)

    w_end_d = modify_start_end_date(pd.Timestamp(end_d).to_pydatetime(), forward=False)

    skillset_sql_count = skillset_sql[(skillset_sql['posted_date'] >= pd.Timestamp(w_start_d).to_pydatetime()) & (
                skillset_sql['posted_date'] < pd.Timestamp(w_end_d).to_pydatetime())]

    now = time.time() * 1000
    # count_data = skillset_sql_count.groupby(['posted_date','state','term'])['count'].sum().reset_index()
    count_week = skillset_sql_count.groupby([pd.Grouper(key='posted_date', freq='1w'), 'state', 'term'])['count'] \
        .sum().reset_index()
    count_week.rename(columns={'posted_date': 'week'}, inplace=True)
    count_week['week'] = count_week['week'].apply(lambda x: x.date())
    count_week.set_index('week', inplace=True)
    if int(now) - int(reset_click) < 3000 and int(reset_click) > 0:
        if value == 'all':
            final_plot_data = count_week.groupby('week')['count'].sum()
        else:
            final_plot_data = count_week[(count_week['term'] == value)].groupby('week')['count'].sum()
    elif clickData:
        state = clickData["points"][0]["location"]
        if value == 'all':
            final_plot_data = count_week[count_week['state'] == state].groupby('week')['count'].sum()
        else:
            final_plot_data = count_week[(count_week['state'] == state) & (count_week['term'] == value)]['count']

    else:
        if value == 'all':
            final_plot_data = count_week.groupby('week')['count'].sum()
        else:
            final_plot_data = count_week[(count_week['term'] == value)].groupby('week')['count'].sum()
    fig = px.bar(final_plot_data)
    return fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(port =4070, debug =True)

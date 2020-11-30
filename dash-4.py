# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 15:38:37 2020

@author: mh4pk
"""

import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output, State
import plotly.express as px
from datetime import datetime as dt

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

import pandas as pd
import time
from pandas.tseries.offsets import DateOffset

jobs_and_skills = pd.read_csv('jobs_and_skills_V2.csv')

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
top_skill_list = ['machine learning', 'python', 'sql', 'programming', 'excel','statistics','cloud','data analysis','algorithms',
                 'r','databases', 'mathematics', 'java','visualization', 'tableau', 'aws', 'spark', 'dashboards', 'sas', 'deep learning',
                  'c++' ,'hadoop', 'tensorflow', 'etl', 'scala', 'computer vision','nlp', 'nosql','hive','matlab', 'pytorch', 'keras','powerbi',
                  'google cloud', 'spss', 'time series','version control','.net', 'reinforcement learning', 'anomaly detection', 'mxnet', 
                  'decision trees', 'bioinformatics','caffe', 'feature engineering','information retrieval', 'stata','text mining','pyspark']
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
            offset = 7-date.weekday()
            start_date = date + DateOffset(offset)
            return start_date
        else:
            return date
    else:
    # modify the end date of dataframe to the end of last week
        if date.weekday() != 0:
            offset = date.weekday()
            end_date = date - DateOffset(offset+1)
            return end_date
        else:
            return date
                
##### skill bar charts data preparation 
skillset = jobs_and_skills.groupby(['state','term'])[top_skill_list].sum().reset_index()
def manipulate_skillset(All_skills):
    # data manipulation for bar chart
    all_skills = All_skills.iloc[:,2:].sum(axis=0).sort_values(ascending= False).to_frame()
    all_skills.reset_index(inplace = True)
    all_skills.rename(columns={"index": "Skills", 0: "Counted Ads"},inplace = True)
    all_skills.set_index('Skills', inplace =True)
    return all_skills
### following portion modifies data for the main map
jobs_and_skills = jobs_and_skills[jobs_and_skills['state'].isin(list_of_us_codes)]
global subset_jobs_state
subset_jobs_state = subset_jobs_state = jobs_and_skills[(jobs_and_skills['posted_date']>= '2020-04-10')
                                                                 & (jobs_and_skills['posted_date']< '2020-05-20')]
jobs_and_skills['posted_date'] = jobs_and_skills['posted_date'].apply(lambda x:dt.strptime(x,'%Y-%m-%d'))
#jobs_and_skills_state_fix.rename(columns ={'state':'state_code'}, inplace =True)

# map_data = jobs_and_skills_state_fix.groupby(['state_code','term','posted_date'])['description'].count()
# map_data_df = map_data.to_frame()
# map_data_df.reset_index(inplace = True)
# map_data_df['state'] = map_data_df['state_code'].map(us_state_abbrev)
# map_data_df.rename(columns ={'description':'count'}, inplace =True)

# external_stylesheets = [
#     'https://codepen.io/chriddyp/pen/bWLwgP.css',
#     {
#         'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
#         'rel': 'stylesheet',
#         'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
#         'crossorigin': 'anonymous'
#     }
#]

app = dash.Dash(__name__)
app.layout = html.Div(className="container scalable",children =[
    
    
    html.Div(
            id="banner",
            className="banner",
            children=[
                html.H2("US Data Science Job Market Dashboard   V.1.0"),
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
                                    min_date_allowed=dt(2020, 4, 1),
                                    max_date_allowed=dt(
                                        2020, 12, 31
                                    ),  # set maximum limit according to local casting
                                    initial_visible_month=dt(2020, 4, 1),
                                    minimum_nights=3,
                                    display_format="MMM Do, YY",
                                    start_date=dt(2020, 4, 1),
                                    end_date=dt(2020, 4, 30),
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
                                style = {'background-color': '#f07400'}
                            )
                        ],
                        title="Click to reset  graphs back to default (all states).",
                        className="selector_button",
                    )
                        
                        ]
                    
                    
                    ),


    html.Div(id='output_container', children=[]),
    html.Br(),
    html.Div(id ='map-container',className="eight columns",
    children = dcc.Loading(dcc.Graph(id='my_US_map', figure={}), type = 'circle')),
    html.Div(id ='map-container2',className="four columns", children = dcc.Loading(
    
    children = dcc.Graph(id='skill-plot', figure={}))),
    html.Div(className = 'twelve columns',children = [
    html.H3(id = 'selected_state', style={'text-align': 'center'})]
              ),
    html.Div(id ='container',className="twelve columns",
    children = dcc.Loading(dcc.Graph(id='count_plot', figure={}), type = 'circle'))
    
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
    # filter data in the date picker range
    global subset_jobs_state
    subset_jobs_state = jobs_and_skills[(jobs_and_skills['posted_date']>= start_d)
                                                                 & (jobs_and_skills['posted_date']< end_d)]
    map_data = subset_jobs_state.groupby(['state','term'])['description'].count()

    map_data_df = map_data.to_frame()
    map_data_df.reset_index(inplace = True)
    map_data_df['state_name'] = map_data_df['state'].map(us_state_abbrev)
    map_data_df.rename(columns ={'description':'count'}, inplace =True)
    if option_slctd != 'all':
        dff = map_data_df[(map_data_df["term"] == option_slctd) ]
    else:
        map_data = subset_jobs_state.groupby(['state'])['description'].count()

        map_data_df = map_data.to_frame()
        map_data_df.reset_index(inplace = True)
        map_data_df['state_name'] = map_data_df['state'].map(us_state_abbrev)
        map_data_df.rename(columns ={'description':'count'}, inplace =True)
        
        dff = map_data_df
    
    # Plotly Express
    fig = px.choropleth(
        data_frame = dff,
        locationmode='USA-states',
        locations='state',# careful changing this will cause not showing states
        scope="usa",
        color='count',
        hover_data=['state_name','count'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'number of jobs: description'},
        template='plotly_dark'
    )
    return  fig


# this will reflect the effect of clicking on the us map by selecting the state
@app.callback(
    Output(component_id='selected_state', component_property='children'),
    [Input(component_id='my_US_map', component_property='clickData'),
     Input("reset-button", "n_clicks_timestamp")]
)
def get_state (clickData,reset_click):
    state =None
    now = time.time() * 1000
    if clickData is not None:
        state = clickData["points"][0]['location']
    if int(now) - int(reset_click) <500 and int(reset_click) > 0:
        state ="US"
    return 'you have selected: {}'.format(state)
    
   
        

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
def plot_top_skills(clickData, value,start_d, end_d,reset_click):
    # subset_jobs_and_skills = jobs_and_skills[(jobs_and_skills['posted_date']>= start_d)
    #                 & (jobs_and_skills['posted_date']< end_d)]
    now = time.time() * 1000
    
    ####prepare skills for bar chart
    skillset = subset_jobs_state.groupby(['state','term'])[top_skill_list].sum().reset_index()
    if value == 'all':
        
        skillset = skillset
    else:
        skillset = skillset[skillset['term'] == value]
    if int(now) - int(reset_click) <500 and int(reset_click) > 0:
        
        skill = manipulate_skillset(skillset) 
        fig = px.bar(skill[:20], x="Counted Ads")
        return fig
    elif clickData and (clickData["points"][0]["location"] in list_of_us_codes):
        skillset = subset_jobs_state.groupby(['state','term'])[top_skill_list].sum().reset_index()
        state =   clickData["points"][0]["location"]
        if value == 'all':
            state_skillset = skillset[skillset['state']==state]
        else:
        
            state_skillset = skillset[(skillset['term'] == value) & (skillset['state']==state)]
        skill = manipulate_skillset(state_skillset) 
        fig = px.bar(skill[:20], x="Counted Ads")
        return fig
    

    else:
       
       skill = manipulate_skillset(skillset) 
       fig = px.bar(skill[:20], x="Counted Ads")
       
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
def update_count_plot(clickData, value,start_d, end_d,reset_click):
    w_start_d=modify_start_end_date(pd.Timestamp(start_d).to_pydatetime(),forward = True)
    print(w_start_d)
    w_end_d = modify_start_end_date(pd.Timestamp(end_d).to_pydatetime(),forward = False)
    #jobs_and_skills = jobs_and_skills[jobs_and_skills['state'].isin(list_of_us_codes)]
    
    subset_jobs_and_skills = jobs_and_skills[(jobs_and_skills['posted_date']>= w_start_d)
                    & (jobs_and_skills['posted_date']< w_end_d)]
    now = time.time() * 1000
    count_data = subset_jobs_and_skills.groupby(['posted_date','state','term'])['description'].count().reset_index()
    count_week = count_data.groupby([pd.Grouper(key='posted_date', freq='1w'),'state','term'])['description']\
    .sum().reset_index()
    count_week.rename(columns={'posted_date':'week','description':'count'}, inplace =True)
    count_week['week'] = count_week['week'].apply(lambda x:x.date())
    count_week.set_index('week',inplace = True)
    if clickData:
        state =   clickData["points"][0]["location"]
        if value =='all':
            final_plot_data = count_week[count_week['state']== state].groupby('week')['count'].sum()
        else:
            final_plot_data = count_week[(count_week['state']== state)&(count_week['term']== value)]['count']
        
    else:
        if value =='all':
            final_plot_data = count_week.groupby('week')['count'].sum()
        else:
            final_plot_data = count_week[(count_week['term']== value)].groupby('week')['count'].sum()
    fig = px.bar(final_plot_data)
    return fig

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(port =4080, debug =True)

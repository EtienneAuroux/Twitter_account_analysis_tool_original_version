# -*- coding: utf-8 -*-
"""
Project: Twitter Account Analysis Tool
Started in february 2022
@author: Etienne Auroux
"""

##Installation

##Modules
from support_functions import date_format, twitter_scrapper, engagement_metrics, top_five, analytics
import plotly.graph_objects as go
import dash
from dash import html, dcc
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import datetime
from whitenoise import WhiteNoise
import os
import webbrowser
from threading import Timer

##Layout of the webpage
default_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css']
app=dash.Dash(__name__,external_stylesheets=[default_stylesheets,dbc.themes.BOOTSTRAP]) #initialising dash app
server=app.server
server.wsgi_app = WhiteNoise(server.wsgi_app,root=os.path.join(os.path.dirname(__file__), 'static'),prefix='static/')

app.layout=html.Div(id='parent',children=[
    dcc.Store(id='data_storage',storage_type='local'),
    html.Img(id='header_icon',className='header_avatar',src=r'static\app_icon.png',style={'display':'inline-block'}),
    html.H1('Twitter analysis tool',className='header_main'),
    html.Div(id='header',className='row',children=[
        html.Div(id='left_column',className='left',children=[
            html.Div(id='left_column_top',className='block input_block',children=[
                html.H3('Input parameters',className='header header_column'),
                html.P('Username:',className='text_P text_username'),
                dcc.Input(id='input_username',className='input_field input_username',type='text'),
                html.P('(account name, it is everything after the @)',className='text_P annotation_username'),
                html.Div(id='date_range',children=[
                    html.Div(id='since_date',className='date_field',children=[
                        html.P('Since: ',className='text_P text_since'),
                        dcc.Input(id='input_date1',className='input_field input_since',type='text'),
                        html.P('(YYYY-MM-DD)',className='text_P annotation_since')
                        ]),
                    html.Div(id='until_date',className='date_field',children=[
                        html.P('Until: ',className='text_P text_until'),
                        dcc.Input(id='input_date2',className='input_field input_until',type='text'),
                        html.P('(YYYY-MM-DD)',className='text_P annotation_until')
                        ]),
                    ]),
                dbc.Button('Submit request',id='submit_button',className='button_submit',n_clicks=0),
                dbc.Button('Reset',id='reset_button',className='button_reset',n_clicks=0)
                ]),
            dbc.Collapse(id='hide_error',children=[
                html.Div(id='middle_column_top',className='block error_block_date',children=[
                    html.H3('Error',className='header_error',id='error_heading'),
                    html.Img(id='error_icon',className='error_img',src=r'static\error_icon.png'),
                    html.P(id='error_cause',className='error_message'),
                    ])
                ],is_open=False),
            dbc.Collapse(id='hide_error2',children=[
                html.Div(id='middle_column_middle',className='block error_block_user',children=[
                    html.H3('Error',className='header_error',id='error_heading2'),
                    html.Img(id='error_icon2',className='error_img',src=r'static\error_icon.png'),
                    html.P('This username does not exist during this period, click on Reset to retry.',id='error_cause2',className='error_message'),
                    ])
                ],is_open=False),
            dbc.Collapse(id='hide_progress_bar',children=[
                html.Div(id='left_column_middle',className='block progress_block',children=[
                    html.H3('Loading the data',className='header_column',id='loading_message'),
                    dbc.Progress(id='progress',className='progress_bar',value=100,label='(10000 tweets ~ 15 minutes)',striped=True,animated=True)
                    ])
                ],is_open=False),
            dbc.Collapse(id='hide_dropdown',children=[
                html.Div(id='left_column_bottom',className='block choice_block',children=[
                    html.H3('Results',className='header_column'),
                    dcc.Dropdown(['Engagement metrics','Top five tweets','Analytics'],placeholder='What do you want to see?',id='plot_select',className='choice_menu',searchable=False,clearable=False)
                    ])
                ],is_open=False)
            ]),
        html.Div(id='right_column',className='right',children=[
            dbc.Collapse(id='hide_graph',children=[
                html.Div(id='right_column_graph',className='block graph_block',children=[
                    html.H3(style={'textAlign':'center'},id='plot_title',className='header_column'),
                    dcc.Graph(id='metrics',className='graph',figure={})
                    ])
                ],is_open=False),
            dbc.Collapse(id='hide_tweet',children=[
                html.Div(id='right_column_tweet',className='block graph_block',children=[
                    html.H3('Top five tweets for the period',className='header_column',style={'textAlign':'center'}),
                    html.Div(id='tweet1',className='tweet_block first_tweet',children=[
                        html.Div(id='tweet_header1',className='tweet_header',children=[
                            html.Img(id='profile_image1',className='avatar',style={'display':'inline-block'}),
                            html.Div(id='tweet_info1',className='tweet_usernames',children=[
                                html.P(id='public1',className='public_header'),
                                html.P(id='account1',className='account_header')
                                ],style={'display':'inline-block'}),
                            html.Img(id='rank1',className='ranking',src=r'static\rank_1.png',style={'display':'inline-block'})
                            ]),
                        html.P(id='content1',className='tweet_content'),
                        html.Div(id='day_hour1',className='date_infos',children=[
                            html.P(id='hour1',className='text_date',style={'display':'inline-block'}),
                            html.P(' - ',id='spacer1',className='text_date',style={'display':'inline-block'}),
                            html.P(id='day1',className='text_date',style={'display':'inline-block'})
                            ]),
                        html.Div(id='image_block1',className='tweet_picture_block',children=[
                            html.Img(id='tweet_image1',className='tweet_picture')
                            ]),
                        html.Div(id='tweet_counts1',className='tweet_infos',children=[
                            html.Img(id='comment_icon1',className='count_icon',src=r'static\comment_icon.png',style={'display':'inline-block'}),
                            html.P(id='comments1',className='metric_count',style={'display':'inline-block'}),
                            html.Img(id='retweet_icon1',className='count_icon',src=r'static\retweet_icon.png',style={'display':'inline-block'}),
                            html.P(id='retweets1',className='metric_count',style={'display':'inline-block'}),
                            html.Img(id='like_icon1',className='count_icon',src=r'static\like_icon.png',style={'display':'inline-block'}),
                            html.P(id='likes1',className='metric_count',style={'display':'inline-block'})
                            ])
                        ]),
                    html.Br(),
                    html.Div(id='tweet2',className='tweet_block second_tweet',children=[
                        html.Div(id='tweet_header2',className='tweet_header',children=[
                            html.Img(id='profile_image2',className='avatar',style={'display':'inline-block'}),
                            html.Div(id='tweet_info2',className='tweet_usernames',children=[
                                html.P(id='public2',className='public_header'),
                                html.P(id='account2',className='account_header')
                                ],style={'display':'inline-block'}),
                            html.Img(id='rank2',className='ranking',src=r'static\rank_2.png',style={'display':'inline-block'}),
                            html.P(id='content2',className='tweet_content'),
                            html.Div(id='day_hour2',className='date_infos',children=[
                                html.P(id='hour2',className='text_date',style={'display':'inline-block'}),
                                html.P(' - ',id='spacer2',className='text_date',style={'display':'inline-block'}),
                                html.P(id='day2',className='text_date',style={'display':'inline-block'})
                                ])
                            ]),
                        html.Div(id='image_block2',className='tweet_picture_block',children=[
                            html.Img(id='tweet_image2',className='tweet_picture')
                            ]),
                        html.Div(id='tweet_counts2',className='tweet_infos',children=[
                            html.Img(id='comment_icon2',className='count_icon',src=r'static\comment_icon.png',style={'display':'inline-block'}),
                            html.P(id='comments2',className='metric_count',style={'display':'inline-block'}),
                            html.Img(id='retweet_icon2',className='count_icon',src=r'static\retweet_icon.png',style={'display':'inline-block'}),
                            html.P(id='retweets2',className='metric_count',style={'display':'inline-block'}),
                            html.Img(id='like_icon2',className='count_icon',src=r'static\like_icon.png',style={'display':'inline-block'}),
                            html.P(id='likes2',className='metric_count',style={'display':'inline-block'})
                            ])
                        ]),
                    html.Div(id='tweet3',className='tweet_block third_tweet',children=[
                        html.Div(id='tweet_header3',className='tweet_header',children=[
                            html.Img(id='profile_image3',className='avatar',style={'display':'inline-block'}),
                            html.Div(id='tweet_info3',className='tweet_usernames',children=[
                                html.P(id='public3',className='public_header'),
                                html.P(id='account3',className='account_header')
                                ],style={'display':'inline-block'}),
                            html.Img(id='rank3',className='ranking',src=r'static\rank_3.png',style={'display':'inline-block'}),
                            html.P(id='content3',className='tweet_content'),
                            html.Div(id='day_hour3',className='date_infos',children=[
                                html.P(id='hour3',className='text_date',style={'display':'inline-block'}),
                                html.P(' - ',id='spacer3',className='text_date',style={'display':'inline-block'}),
                                html.P(id='day3',className='text_date',style={'display':'inline-block'})
                                ])
                            ]),
                        html.Div(id='image_block3',className='tweet_picture_block',children=[
                            html.Img(id='tweet_image3',className='tweet_picture')
                            ]),
                        html.Div(id='tweet_counts3',className='tweet_infos',children=[
                            html.Img(id='comment_icon3',className='count_icon',src=r'static\comment_icon.png',style={'display':'inline-block'}),
                            html.P(id='comments3',className='metric_count',style={'display':'inline-block'}),
                            html.Img(id='retweet_icon3',className='count_icon',src=r'static\retweet_icon.png',style={'display':'inline-block'}),
                            html.P(id='retweets3',className='metric_count',style={'display':'inline-block'}),
                            html.Img(id='like_icon3',className='count_icon',src=r'static\like_icon.png',style={'display':'inline-block'}),
                            html.P(id='likes3',className='metric_count',style={'display':'inline-block'})
                            ])
                        ]),
                    html.Div(id='tweet4',className='tweet_block fourth_tweet',children=[
                        html.Div(id='tweet_header4',className='tweet_header',children=[
                            html.Img(id='profile_image4',className='avatar',style={'display':'inline-block'}),
                            html.Div(id='tweet_info4',className='tweet_usernames',children=[
                                html.P(id='public4',className='public_header'),
                                html.P(id='account4',className='account_header')
                                ],style={'display':'inline-block'}),
                            html.Img(id='rank4',className='ranking',src=r'static\rank_4.png',style={'display':'inline-block'}),
                            html.P(id='content4',className='tweet_content'),
                            html.Div(id='day_hour4',className='date_infos',children=[
                                html.P(id='hour4',className='text_date',style={'display':'inline-block'}),
                                html.P(' - ',id='spacer4',className='text_date',style={'display':'inline-block'}),
                                html.P(id='day4',className='text_date',style={'display':'inline-block'})
                                ])
                            ]),
                        html.Div(id='image_block4',className='tweet_picture_block',children=[
                            html.Img(id='tweet_image4',className='tweet_picture')
                            ]),
                        html.Div(id='tweet_counts4',className='tweet_infos',children=[
                            html.Img(id='comment_icon4',className='count_icon',src=r'static\comment_icon.png',style={'display':'inline-block'}),
                            html.P(id='comments4',className='metric_count',style={'display':'inline-block'}),
                            html.Img(id='retweet_icon4',className='count_icon',src=r'static\retweet_icon.png',style={'display':'inline-block'}),
                            html.P(id='retweets4',className='metric_count',style={'display':'inline-block'}),
                            html.Img(id='like_icon4',className='count_icon',src=r'static\like_icon.png',style={'display':'inline-block'}),
                            html.P(id='likes4',className='metric_count',style={'display':'inline-block'})
                            ])
                        ]),
                    html.Div(id='tweet5',className='tweet_block fifth_tweet',children=[
                        html.Div(id='tweet_header5',className='tweet_header',children=[
                            html.Img(id='profile_image5',className='avatar',style={'display':'inline-block'}),
                            html.Div(id='tweet_info5',className='tweet_usernames',children=[
                                html.P(id='public5',className='public_header'),
                                html.P(id='account5',className='account_header')
                                ],style={'display':'inline-block'}),
                            html.Img(id='rank5',className='ranking',src=r'static\rank_5.png',style={'display':'inline-block'}),
                            html.P(id='content5',className='tweet_content'),
                            html.Div(id='day_hour5',className='date_infos',children=[
                                html.P(id='hour5',className='text_date',style={'display':'inline-block'}),
                                html.P(' - ',id='spacer5',className='text_date',style={'display':'inline-block'}),
                                html.P(id='day5',className='text_date',style={'display':'inline-block'})
                                ])
                            ]),
                        html.Div(id='image_block5',className='tweet_picture_block',children=[
                            html.Img(id='tweet_image5',className='tweet_picture')
                            ]),
                        html.Div(id='tweet_counts5',className='tweet_infos',children=[
                            html.Img(id='comment_icon5',className='count_icon',src=r'static\comment_icon.png',style={'display':'inline-block'}),
                            html.P(id='comments5',className='metric_count',style={'display':'inline-block'}),
                            html.Img(id='retweet_icon5',className='count_icon',src=r'static\retweet_icon.png',style={'display':'inline-block'}),
                            html.P(id='retweets5',className='metric_count',style={'display':'inline-block'}),
                            html.Img(id='like_icon5',className='count_icon',src=r'static\like_icon.png',style={'display':'inline-block'}),
                            html.P(id='likes5',className='metric_count',style={'display':'inline-block'})
                            ])
                        ])
                    ])
                ],is_open=False)
            ])
        ]),
    html.Div(id='bottom_bar',className='bottom_info',children=[
        html.A("App by Etienne Auroux",id='signature',className='sign_name',href='https://etienneauroux.com', target="_blank")
        ])
    ])

@app.callback(
    [Output('submit_button','n_clicks'),
     Output('input_username','value'),
     Output('input_date1','value'),
     Output('input_date2','value')],
    Input('reset_button','n_clicks')
)
def reset_layout(n_clicks):
    if n_clicks==0:
        raise PreventUpdate
    else:
        return 0, '', '', ''

@app.callback(
    Output('submit_button','disabled'),
    Input('submit_button','n_clicks')
)
def submit_switch(clicks):
    if clicks==0:
        switch=False
    else:
        switch=True
    return switch

@app.callback(
    [Output('hide_error','is_open'),
     Output('error_cause','children')],
    Input('submit_button','n_clicks'),
    [State('hide_error','is_open'),
     State('input_username','value'),
     State('input_date1','value'),
     State('input_date2','value')]
)
def toggle_error(clicks,error,twitter_username,start_date,end_date):
    if clicks==0 and error==True:
        return False, ''
    if clicks and error==False:
        check=date_format(start_date,end_date)
        if check=='Start':
            return True, 'Wrong format for the start date.'
        elif check=='End':
            return True, 'Wrong format for the end date.'
        elif check=='Both':
            return True, 'Wrong format for the dates.'
        elif check=='Start out':
            return True, 'The start date does not exist.'
        elif check=='End out':
            return True, 'The end date does not exist.'
        elif check=='Both out':
            return True, 'The dates do not exist.'
        elif check=='Same':
            return True, 'The dates are the same.'
        else:
            return False, ''
    return error, ''

@app.callback(
    [Output('hide_progress_bar','is_open'),
     Output('data_storage','clear_data')],
    [Input('submit_button','n_clicks'),
     Input('hide_error','is_open')],
    [State('hide_progress_bar','is_open'),
     State('data_storage','clear_data')]
)
def toggle_collapse(clicks,error,is_open,erase_data):
    if clicks==0 and is_open==True:
        return False, True
    if clicks and is_open==False and error==False:
        return True, False
    return is_open, erase_data

@app.callback([Output('data_storage','data'),
               Output('loading_message','children'),
               Output('progress','striped'),
               Output('progress','animated'),
               Output('progress','color'),
               Output('progress','label'),
               Output('hide_error2','is_open')],
              [Input('submit_button','n_clicks'),
               Input ('hide_error','is_open')],
              [State('input_username','value'),
               State('input_date1','value'),
               State('input_date2','value'),
               State('loading_message','children')]
)
def load_data(clicks,error,twitter_username,start_date,end_date,message_bar):
    if clicks==0 and message_bar=='Data acquired!':
        data=None
        message_bar='Loading the data'
        stripes=True
        animation=True
        color_bar='primary'
        label_bar='(10000 tweets ~ 15 minutes)'
        error2=False
    else:
        if error==False and twitter_username!='' and twitter_username!=None and start_date!='' and start_date!=None and end_date!='' and end_date!=None:
            start_scrapping=datetime.datetime.now()
            data=twitter_scrapper(twitter_username,start_date,end_date)
            end_scrapping=datetime.datetime.now()
            time_scrapping=str(end_scrapping-start_scrapping)
            if data=='Uwrong':
                data=None
                message_bar='Loading the data'
                stripes=True
                animation=True
                color_bar='primary'
                label_bar='(10000 tweets ~ 15 minutes)'
                error2=True
            else:
                message_bar='Data acquired!'
                stripes=False
                animation=False
                color_bar='success'
                label_bar='It took '+time_scrapping[:-13]+'h '+time_scrapping[-12:-10]+'min '+time_scrapping[-9:-7]+'s'
                error2=False
        else:
            data=None
            message_bar='Loading the data'
            stripes=True
            animation=True
            color_bar='primary'
            label_bar='(10000 tweets ~ 15 minutes)'
            error2=False
    return data,message_bar, stripes, animation, color_bar, label_bar, error2

@app.callback(
    Output('hide_dropdown','is_open'),
    [Input('loading_message','children'),
     Input('submit_button','n_clicks')],
    State('hide_dropdown','is_open')
)
def toggle_collapse2(message,n_clicks,is_open):
    if message=='Data acquired!' and is_open==False:
        return not is_open
    elif n_clicks==0 and is_open==True:
        return not is_open
    return is_open

@app.callback(Output('plot_title','children'),
              Input('plot_select','value')
)
def graph_title(selected_value):
    if selected_value=='Engagement metrics':
        graph_heading='Engagement metrics'
    elif selected_value=='Analytics':
        graph_heading='Analytics'
    else:
        graph_heading=''
    return graph_heading

@app.callback(
    [Output('metrics','figure')],
    Input('plot_select','value'),
    State('data_storage','data'))
def get_graphs(selected_value,data): #missing all the safety for wrong inputs
    if selected_value=='Engagement metrics':
        fig=engagement_metrics(data[0],data[1],data[7],data[8],data[9],data[10])
        return [go.Figure(data=fig)]
    elif selected_value=='Analytics':
        fig=analytics(data[4],data[7],data[8],data[9],data[10])
        return [go.Figure(data=fig)]
    else:
        return [go.Figure(data={})]
    
@app.callback(
    Output('hide_graph','is_open'),
    [Input('plot_select','value'),
     Input('submit_button','n_clicks')],
    State('hide_graph','is_open')
)
def toggle_collapse3(selected_value,n_clicks,is_open):
    if (selected_value=='Engagement metrics' or selected_value=='Analytics') and is_open==False:
        return not is_open
    elif selected_value=='Top five tweets' and is_open==True:
        return not is_open
    elif n_clicks==0 and is_open==True:
        return not is_open
    return is_open

@app.callback(
    Output('hide_tweet','is_open'),
    [Input('plot_select','value'),
     Input('submit_button','n_clicks')],
    State('hide_tweet','is_open')
)
def toggle_collapse4(selected_value,n_clicks,is_open):
    if selected_value=='Top five tweets' and is_open==False:
        return not is_open
    elif selected_value!='Top five tweets' and is_open==True:
        return not is_open
    elif n_clicks==0 and is_open==True:
        return not is_open
    return is_open

@app.callback(
    Output('plot_select','value'),
    Input('submit_button','n_clicks'),
    State('plot_select','value')
)
def reset_menu(n_clicks,selected_value):
    if n_clicks==0 and selected_value!=None:
        return None

profile_image_array=['profile_image1','profile_image2','profile_image3','profile_image4','profile_image5']
account_array=['account1','account2','account3','account4','account5']
public_array=['public1','public2','public3','public4','public5']
content_array=['content1','content2','content3','content4','content5']
day_array=['day1','day2','day3','day4','day5']
hour_array=['hour1','hour2','hour3','hour4','hour5']
comment_array=['comments1','comments2','comments3','comments4','comments5']
retweet_array=['retweets1','retweets2','retweets3','retweets4','retweets5']
like_array=['likes1','likes2','likes3','likes4','likes5']

for i in range(0,5):
    @app.callback(
        [Output(profile_image_array[i],'src'),
         Output(account_array[i],'children'),
         Output(public_array[i],'children'),
         Output(content_array[i],'children'),
         Output(day_array[i],'children'),
         Output(hour_array[i],'children'),
         Output(comment_array[i],'children'),
         Output(retweet_array[i],'children'),
         Output(like_array[i],'children')],
        Input('plot_select','value'),
        State('data_storage','data')
    )
    def tweet(selected_value,data,i=i):
        if selected_value=='Top five tweets':
            account_name,public_name,profile_picture,top_dates,top_times,top_content,top_url,top_thumbnail,top_reply,top_like,top_retweet=top_five(data[1],data[2],data[4],data[5],data[6],data[7],data[8],data[9],data[13],data[14],data[15])
            return profile_picture,account_name,public_name,top_content[i],top_dates[i],top_times[i],top_reply[i],top_retweet[i],top_like[i]
        else:
            return '','','','','','','','',''        

port=8050
def open_browser():
    webbrowser.open_new("http://localhost:{}".format(port))

if __name__ =='__main__':
    Timer(1, open_browser).start();
    app.run_server(debug=False,port=port,use_reloader=False)

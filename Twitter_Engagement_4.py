# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 10:20:26 2022

@author: ETIENNEA
"""
# import pandas as pd
# file=r'Previous_versions\Data\Tweets_from_elonmusk_2019-12-31_to_2020-03-31.xlsx'
# data_sheet=pd.read_excel(file,sheet_name='Dates_and_Tweets',skiprows=1)
# data_values=data_sheet.values
# content=data_values[:,4]
# reply_count=data_values[:,8]
# like_count=data_values[:,9]
# retweet_count=data_values[:,10]
# quote_count=data_values[:,11]

def engagement_metrics(unixdates,dates,reply_count,like_count,retweet_count,quote_count):
    ##Modules
    import math
    import numpy as np
    import datetime
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    
    ##Plot
    #Calibrating axes
    def calibration_ax(x_data,y_data):
        time_span=x_data[0]-x_data[-1]
        if time_span<300: #5 minutes
            x_lab='Seconds'
        elif time_span>=300 and time_span<14400: #4 hours
            x_lab='Minutes'
            x_norm=60
        elif time_span>=14400 and time_span<345600: #4 days
            x_lab='Hours'
            x_norm=3600
        elif time_span>=345600 and time_span<2419200: #28 days
            x_lab='Days'
            x_norm=86400
        elif time_span>=2419200 and time_span<10886400: #18 weeks
            x_lab='Weeks'
            x_norm=604800
        elif time_span>=10886400 and time_span<125798400: #4 years
            x_lab='Months'
            x_norm=2629757 #Taking 30.437 as average number of days in one month
        else:
            x_lab='Years'
            x_norm=31449600
        x_axis=[]
        for i in range(len(x_data)):
            x_axis=np.append(x_axis,x_data[i]-x_data[-1])
        
        x_lim=[-(1.05*x_axis[0]-x_axis[0]),1.05*x_axis[0]]
        
        x_tick=[]
        x_tick_label=[]
        for i in range(0,10):
            x_tick=np.append(x_tick,i*x_axis[0]/9)
            x_tick_label=np.append(x_tick_label,str(int(x_tick[i])))
            x_tick_label[i]=datetime.datetime.fromtimestamp(x_tick[i]+x_data[-1]).strftime('%d-%m-%Y')
        
        width=np.mean(x_axis)/250
            
        ydata_zeroes=math.floor(math.log(max(y_data),10))
        if ydata_zeroes<3:
            y_lab=''
            y_norm=1
        elif ydata_zeroes>=3 and ydata_zeroes<6:
            y_lab='(in thousands)'
            y_norm=1e3
        elif ydata_zeroes>=6 and ydata_zeroes<9:
            y_lab='(in millions)'
            y_norm=1e6
        else:
            y_lab='(in billions)'
            y_norm=1e9
        y_axis=y_data
        
        y_lim=[0,1.05*max(y_axis)]
        
        y_tick=[]
        y_tick_label=[]
        for i in range(0,5):
            y_tick=np.append(y_tick,round(i*max(y_axis)/4,-3))
            y_tick_label=np.append(y_tick_label,str(y_tick[i]/y_norm))
            if y_tick_label[i][-2:]=='.0':
                y_tick_label[i]=y_tick_label[i][:-2]
        
        return x_lab, x_axis, x_lim, x_tick, x_tick_label, y_lab, y_axis, y_lim, y_tick, y_tick_label, width
    
    #Figure
    metrics=['<b>Number of replies</b>','<b>Number of likes</b>','<b>Number of retweets</b>','<b>Number of quotes</b>']
    hover_text='<b>Date:</b> %{hovertext}<br /><b>Count:</b> %{y}<extra></extra>'
    fig=make_subplots(4,1,shared_xaxes=True,vertical_spacing=0.1,subplot_titles=metrics,row_heights=[0.25,0.25,0.25,0.25]) #,font=dict(size=26)
    
    x_label,x_axis,x_lim,x_tick,x_tick_label,y_label,y_axis,y_lim,y_tick,y_tick_label,width_bars=calibration_ax(unixdates,reply_count)
    fig.add_trace(go.Bar(x=x_axis,y=y_axis,width=width_bars,marker=dict(color='blue'),hovertext=dates,hovertemplate=hover_text),row=1,col=1)
    fig.update_yaxes(title_text=y_label,title_standoff=40,range=y_lim,tickvals=y_tick,ticktext=y_tick_label,ticks='inside',tickwidth=2,ticklen=10,title_font=dict(size=20,family='Gill sans MT'),row=1,col=1)
    
    x_label,x_axis,x_lim,x_tick,x_tick_label,y_label,y_axis,y_lim,y_tick,y_tick_label,width_bars=calibration_ax(unixdates,like_count)
    fig.add_trace(go.Bar(x=x_axis,y=y_axis,width=width_bars,marker=dict(color='red'),hovertext=dates,hovertemplate=hover_text),row=2,col=1)
    fig.update_yaxes(title_text=y_label,title_standoff=8,range=y_lim,tickvals=y_tick,ticktext=y_tick_label,ticks='inside',tickwidth=2,ticklen=10,title_font=dict(size=20,family='Gill sans MT'),row=2,col=1)
    
    x_label,x_axis,x_lim,x_tick,x_tick_label,y_label,y_axis,y_lim,y_tick,y_tick_label,width_bars=calibration_ax(unixdates,retweet_count)
    fig.add_trace(go.Bar(x=x_axis,y=y_axis,width=width_bars,marker=dict(color='green'),hovertext=dates,hovertemplate=hover_text),row=3,col=1)
    fig.update_yaxes(title_text=y_label,title_standoff=20,range=y_lim,tickvals=y_tick,ticktext=y_tick_label,ticks='inside',tickwidth=2,ticklen=10,title_font=dict(size=20,family='Gill sans MT'),row=3,col=1)
    
    x_label,x_axis,x_lim,x_tick,x_tick_label,y_label,y_axis,y_lim,y_tick,y_tick_label,width_bars=calibration_ax(unixdates,quote_count)
    fig.add_trace(go.Bar(x=x_axis,y=y_axis,width=width_bars,marker=dict(color='black'),hovertext=dates,hovertemplate=hover_text),row=4,col=1)
    fig.update_yaxes(title_text=y_label,title_standoff=40,range=y_lim,tickvals=y_tick,ticktext=y_tick_label,ticks='inside',tickwidth=2,ticklen=10,title_font=dict(size=20,family='Gill sans MT'),row=4,col=1)
    
    fig.update_xaxes(title_text='<b>'+x_label+'</b>',range=x_lim,tickvals=x_tick,ticktext=x_tick_label,tickangle=-45,ticks='inside',tickwidth=2,ticklen=10,title_font=dict(size=20,family='Gill sans MT'),row=4,col=1)
   
    fig.update_yaxes(linecolor='#1DA1F2',linewidth=0.5,mirror=True,gridcolor='#D3D3D3',gridwidth=0.5)
    fig.update_xaxes(linecolor='#1DA1F2',linewidth=0.5,mirror=True,title_font_family='Gill sans MT')
    fig.update_layout(height=900,font=dict(size=20),margin={'l':0,'r':0,'b':0,'t':60},showlegend=False)
    fig.update_annotations(font_size=20,x=0,xanchor='left') #to update subplots titles
    fig.layout.annotations[0].update(y=1.01,font_family='Bahnschrift Light')
    fig.layout.annotations[1].update(y=0.735,font_family='Bahnschrift Light')
    fig.layout.annotations[2].update(y=0.46,font_family='Bahnschrift Light')
    fig.layout.annotations[3].update(y=0.185,font_family='Bahnschrift Light')
    fig.layout.plot_bgcolor='white'
    fig.layout.paper_bgcolor='white'
    
    return fig 

def top_five(dates,times,content,media_url,thumbnail_url,reply_count,like_count,retweet_count,account_name,public_name,profile_picture):
    ##Modules
    import numpy as np
    import datetime
    
    ##Arranging data
    if len(like_count)<5:
        top_like_index=np.argsort(like_count)
    else:
        top_like_index=np.argsort(like_count)[-5:]
    
    month_number=[]
    for i in range(len(times)):
        times[i]=datetime.datetime.strptime(times[i],'%H:%M:%S')
        times[i]=times[i].strftime('%I:%M %p')
        dates[i]=datetime.datetime.strptime(dates[i],'%d/%m/%Y')
        month_number=np.append(month_number,dates[i].strftime('%b'))
        dates[i]=dates[i].strftime('%d, %Y')
        dates[i]=month_number[i]+', '+dates[i]
        
    top_dates=np.flip([dates[i] for i in top_like_index],0)
    top_times=np.flip([times[i] for i in top_like_index],0)
    top_content=np.flip([content[i] for i in top_like_index],0)
    top_url=np.flip([media_url[i] for i in top_like_index],0)
    top_thumbnail=np.flip([thumbnail_url[i] for i in top_like_index],0)
    top_reply=np.flip([reply_count[i] for i in top_like_index],0)
    top_like=np.flip([like_count[i] for i in top_like_index],0)
    top_retweet=np.flip([retweet_count[i] for i in top_like_index],0)
    
    return account_name, public_name, profile_picture, top_dates, top_times, top_content, top_url, top_thumbnail, top_reply, top_like, top_retweet

def analytics(content,reply_count,like_count,retweet_count,quote_count):
    ##Modules
    import numpy as np
    import plotly.graph_objects as go
    import re
    import collections
    
    #Arranging data
    #Metrics
    n_tweet=str(len(content))+'<br>tweets'
    
    n_like=str(sum(like_count))+'<br>likes'
    n_reply=str(sum(reply_count))+'<br>replies'
    n_retweet=str(sum(retweet_count))+'<br>retweets'
    n_quote=str(sum(quote_count))+'<br>quotes'
    
    avg_like='~'+str(int(np.average(like_count)))+'<br>likes/tweet'
    avg_reply='~'+str(int(np.average(reply_count)))+'<br>replies/tweet'
    avg_retweet='~'+str(int(np.average(retweet_count)))+'<br>retweets/tweet'
    avg_quote='~'+str(int(np.average(quote_count)))+'<br>quotes/tweet'
    
    max_like='max likes<br>'+str(max(like_count))
    max_reply='max replies<br>'+str(max(reply_count))
    max_retweet='max retweets<br>'+str(max(retweet_count))
    max_quote='max quotes<br>'+str(max(quote_count))
    
    min_like='min likes<br>'+str(min(like_count))
    min_reply='min replies<br>'+str(min(reply_count))
    min_retweet='min retweets<br>'+str(min(retweet_count))
    min_quote='min quotes<br>'+str(min(quote_count))
    
    #Content    
    pattern=r'[^A-Za-z0-9]+'
    word_remove=['too','to','the','a','of','is','are','was','were','been',
                 'I','you','we','they','do','did','done','have','has','had',
                 'if','in','out','above','under','s','for','on','be','will',
                 'it','t','d','but','that','this','with','but','not','as',
                 'so','at','i','from','should','could','or','just','there',
                 'much','many','me','him','her','them','their','our','us',
                 'his','mine']
    
    text_all=''
    for i in range(len(content)):
        content[i]=str(content[i])
        text_all=text_all+content[i]
    word_list=re.sub(pattern,' ',text_all).split()
    for i in range(len(word_list)):
        word_list[i]=word_list[i].lower()
    for word in word_remove:
        while word in word_list:
            word_list.remove(word)
    word_counter=collections.Counter(word_list).most_common()
    
    first_word=word_counter[0][0]+'<br>('+str(word_counter[0][1])+')'
    second_word=word_counter[1][0]+'<br>('+str(word_counter[1][1])+')'
    third_word=word_counter[2][0]+'<br>('+str(word_counter[2][1])+')'
    fourth_word=word_counter[3][0]+'<br>('+str(word_counter[3][1])+')'
    fifth_word=word_counter[4][0]+'<br>('+str(word_counter[4][1])+')'
    
    text_success=''
    for i in range(len(content)):
        if like_count[i]>0.5*max(like_count):
            content[i]=str(content[i])
            text_success=text_success+content[i]
    word_list_success=re.sub(pattern,' ',text_success).split()
    for i in range(len(word_list_success)):
        word_list_success[i]=word_list_success[i].lower()
    for word in word_remove:
        while word in word_list_success:
            word_list_success.remove(word)
    word_counter_success=collections.Counter(word_list_success).most_common()
    
    try:
        first_word_success=word_counter_success[0][0]+'<br>('+str(word_counter_success[0][1])+')'
    except IndexError:
        first_word_success=''
    try:
        second_word_success=word_counter_success[1][0]+'<br>('+str(word_counter_success[1][1])+')'
    except IndexError:
        second_word_success=''
    try:
        third_word_success=word_counter_success[2][0]+'<br>('+str(word_counter_success[2][1])+')'
    except IndexError:
        third_word_success=''
    try:
        fourth_word_success=word_counter_success[3][0]+'<br>('+str(word_counter_success[3][1])+')'
    except IndexError:
        fourth_word_success=''
    try:
        fifth_word_success=word_counter_success[4][0]+'<br>('+str(word_counter_success[4][1])+')'
    except IndexError:
        fifth_word_success=''
        
    #Plot
    myColors=[
        'white','#1DA1F2','#D70040',
        'cornflowerblue','cornflowerblue','cornflowerblue','cornflowerblue',
        'coral','coral',
        'lightpink','lightpink','lightpink','lightpink','lightpink',
        'lightpink','lightpink','lightpink','lightpink','lightpink',
        'lightskyblue','lightskyblue','lightskyblue','lightskyblue',
        'lightskyblue','lightskyblue','lightskyblue','lightskyblue',
        'lightskyblue','lightskyblue','lightskyblue','lightskyblue'
              ]
    myFontColors=[
        'black','white','white',
        'white','white','white','white',
        'black','black',
        'black','black','black','black','black',
        'black','black','black','black','black',
        'black','black','black','black',
        'black','black','black','black',
        'black','black','black','black'
              ]
    
    myFontSize=[
        30,25,25,
        20,20,20,20,
        20,20,20,20,
        15,15,15,15,15,
        15,15,15,15,15,
        15,15,15,15,
        15,15,15,15,
        15,15,15,15
              ]
    
    fig=go.Figure(go.Sunburst(
        labels=[
            n_tweet,'metrics','words',
            n_like,n_reply,n_retweet,n_quote,
            'most used','most successful',
            first_word,second_word,third_word,fourth_word,fifth_word,
            first_word_success,second_word_success,third_word_success,fourth_word_success,fifth_word_success,
            avg_like,avg_reply,avg_retweet,avg_quote,
            max_like,max_reply,max_retweet,max_quote,
            min_like,min_reply,min_retweet,min_quote
            ],
        parents=[
            '',n_tweet,n_tweet,
            'metrics','metrics','metrics','metrics',
            'words','words',
            'most used','most used','most used','most used','most used',
            'most successful','most successful','most successful','most successful','most successful',
            n_like,n_reply,n_retweet,n_quote,
            n_like,n_reply,n_retweet,n_quote,
            n_like,n_reply,n_retweet,n_quote
            ],
        values=[
            1,2,2,
            3,3,3,3,
            3,3,
            4,4,4,4,4,
            4,4,4,4,4,
            4,4,4,4,
            4,4,4,4,
            4,4,4,4
            ],
        # insidetextorientation='tangential',
        hoverinfo='none',
        insidetextfont={'color':myFontColors,'family':'Gill sans MT','size':myFontSize},
        marker={'colors':myColors},
        outsidetextfont={'size':30}
        )) #values are arbitrarily defined so that the plot looks pretty
    
    fig.update_layout(height=900,margin={'l':0,'r':0,'b':0,'t':60},showlegend=False)
    
    return fig
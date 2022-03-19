# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 16:07:50 2022

@author: ETIENNEA
"""
username='elonmusk'
since_date='2019-12-31'
until_date='2020-02-25'


def date_format(start_date,end_date):
    import re
    import datetime
    
    proper_format=re.compile('\d\d\d\d-\d\d-\d\d') 
    #what if it is same date? What if the date is yyyy-15-32? -> it reports a user error.
    if proper_format.match(start_date) is None and proper_format.match(end_date) is not None:
        message='Start'
    elif proper_format.match(end_date) is None and proper_format.match(start_date) is not None:
        message='End'
    elif proper_format.match(start_date) is None and proper_format.match(end_date) is None:
        message='Both'
    else:
        k1=0
        k2=0
        try:
            datetime.datetime.strptime(start_date,'%Y-%m-%d')
        except ValueError:
            k1=1
        try:
            datetime.datetime.strptime(end_date,'%Y-%m-%d')
        except ValueError:
            k2=1
        if k1==1 and k2==0:
            message='Start out'
        elif k1==0 and k2==1:
            message='End out'
        elif k1==1 and k2==1:
            message='Both out'
        else:
            if start_date==end_date:
                message='Same'
            else:
                message='Dates ok'
    return message
    
def user_exist(twitter_username,start_date,end_date):
    import snscrape.modules.twitter as sntwitter
    
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper('from:@'+twitter_username+' + since:'+start_date+' until:'+until_date).get_items()):
        test=tweet.user.username
    try:
        test+'test'
    except UnboundLocalError:
        return 'Uwrong'

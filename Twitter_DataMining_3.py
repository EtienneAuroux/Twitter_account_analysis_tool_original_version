# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 11:09:42 2022

@author: ETIENNEA
"""

##Inputs
username='elonmusk'
since_date='2019-12-31'
until_date='2020-03-31'

def twitter_scrapper(twitter_username,start_date,end_date):
    #Modules
    import numpy as np
    import snscrape.modules.twitter as sntwitter
    
    ##Scrapping Twitter data
    unixdates=[]
    dates=[]
    times=[]
    content=[]
    reply=[]
    ids=[]
    reply_count=[]
    like_count=[]
    retweet_count=[]
    quote_count=[]
    followers=[]
    friends=[]
    thumbnail=[]
    media_url=[]
    reply_username=[]
    
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper('from:@'+twitter_username+' + since:'+start_date+' until:'+end_date).get_items()):
        tweet_time=tweet.date
        dates=np.append(dates,tweet_time.strftime('%d/%m/%Y'))
        times=np.append(times,tweet_time.strftime('%H:%M:%S'))
        unixdates=np.append(unixdates,tweet_time.timestamp())
        content=np.append(content,tweet.content)
        reply=np.append(reply,tweet.inReplyToUser)
        ids=np.append(ids,tweet.id)
        reply_count=np.append(reply_count,tweet.replyCount)
        like_count=np.append(like_count,tweet.likeCount)
        retweet_count=np.append(retweet_count,tweet.retweetCount)
        quote_count=np.append(quote_count,tweet.quoteCount)
        followers=np.append(followers,tweet.user.followersCount)
        friends=np.append(friends,tweet.user.friendsCount)
        if 'http' in tweet.content:
            k=0
            try:
                media_url=np.append(media_url,tweet.media[0].previewUrl)
                thumbnail=np.append(thumbnail,'none')
            except TypeError:
                quoted=tweet
                k=1 #that's a quoted tweet
            except AttributeError:
                original=tweet.media[0]
                k=2 #that's an original tweet
            if k==1:
                media_url=np.append(media_url,quoted.outlinks[0])
                thumbnail=np.append(thumbnail,'none')
            elif k==2:
                media_url=np.append(media_url,original.variants[0].url)
                thumbnail=np.append(thumbnail,original.thumbnailUrl)
        else:
            media_url=np.append(media_url,'no media')
            thumbnail=np.append(thumbnail,'none')
    
    mistake=False
    try:
        account_name=tweet.user.username
    except UnboundLocalError:
        mistake=True
    
    if mistake==False:
        account_name='@'+account_name
        public_name=tweet.user.displayname
        profile_picture=tweet.user.profileImageUrl
        
        for i in range(len(unixdates)):
            if 'http' in content[i]:
                url_start=content[i].find('http')
                content[i]=content[i][:url_start]
            try:
                reply_username=np.append(reply_username,reply[i].username)
            except AttributeError:
                reply_username=np.append(reply_username,'')
        
        return unixdates, dates, times, ids, content, media_url, thumbnail, reply_username, reply_count, like_count, retweet_count, quote_count, followers, friends, account_name, public_name, profile_picture
    else:
        return 'Uwrong'
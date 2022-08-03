# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 16:55:47 2022

@author: Marc Riven
"""

import tweepy
import pandas as pd
import numpy as np

# Installation / Access to Twitter account
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

df = pd.read_csv('')
df

# First, we check which accounts are protected/still exist
username_column = '' # Insert name of column containing user handles here
user_list = df[username_column] 
df['protected'] = np.nan
df['exists'] = np.nan

for uid in user_list:
    try:
        user = api.get_user(screen_name=uid)
        df.loc[df[username_column] == uid, 'protected'] = 'TRUE' if user.protected else 'FALSE'
        df.loc[df[username_column] == uid, 'exists'] = 'TRUE'
    except tweepy.errors.NotFound:
        df.loc[df[username_column] == uid, 'exists'] = 'FALSE'
    except tweepy.errors.Forbidden:
        df.loc[df[username_column] == uid, 'exists'] = 'SUSPENDED'

# Secondly, we check when the latest tweet was for accounts that aren't protected/still exist
df['latest_tweet'] = np.nan
still_exist = df[df['exists'] == 'TRUE'][username_column]

for uid in still_exist: # Filter out by which one still exists etc
    try:
        user = api.get_user(screen_name=uid)
        try: 
            df.loc[df[username_column] == uid, 'latest_tweet'] = api.user_timeline(screen_name=uid)[0].created_at
        except IndexError:
            df.loc[df[username_column] == uid, 'latest_tweet'] = np.nan
    except tweepy.errors.NotFound:
        pass
    except tweepy.errors.Forbidden:
        pass
    except tweepy.errors.Unauthorized:
        pass
    
df.to_csv('')
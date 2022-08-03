# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 12:44:43 2022

@author: Marc Riven
"""

import tweepy
import pandas as pd
import numpy as np
import datetime

# Installation / Access to Twitter account
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

df = pd.read_csv('')

df['Message Status'] = np.nan
df['Follow Status'] = np.nan
df['Timestamp'] = np.nan

username_column = ''

# We want to filter out users we have already sent an invite to in order to
# prevent spam
user_list = df[df['Message Status'] != 'Sent'][username_column]
user_list = df[username_column]

message = ''
timestamp = []

for username in user_list:
    user = api.get_user(screen_name=username)
    try:  # Attempts to send a message
        api.send_direct_message(user.id_str, message)
        df.loc[df[username_column] == username, 'Message Status'] = 'Sent'
        df.loc[df[username_column] == username, 'Follow Status'] = 'Not Needed'
        df.loc[df[username_column] == username, 'Timestamp'] = str(
            datetime.datetime.now())
    except tweepy.errors.Forbidden:  # If we cannot send a message, we attempt
        # to follow the user
        try:
            # Person needs to follow us for us to send them a message
            api.create_friendship(user_id=user.id_str)
            df.loc[df[username_column] == username, 'Message Status'] = 'Not Sent'
            df.loc[df[username_column] == username, 'Follow Status'] = 'Pending'
            df.loc[df[username_column] == username, 'Timestamp'] = str(
                datetime.datetime.now())
        except tweepy.errors.Forbidden:  # Twitter will throw an error if we
            # have already attempted to follow; this is to prevent that
            df.loc[df[username_column] == username, 'Message Status'] = 'Not Sent'
            df.loc[df[username_column] == username, 'Follow Status'] = 'Pending'
            df.loc[df[username_column] == username, 'Timestamp'] = str(
                datetime.datetime.now())

df.to_csv('names.csv', encoding='utf-8', index=False, mode='w+')

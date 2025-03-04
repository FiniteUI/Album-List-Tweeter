import gspread
import dotenv
import os
import config
import asyncio
import twikit
import time
import pytz
import re
from datetime import datetime, timezone

def getCookiePath():
    path = os.path.join(os.getcwd(), 'Data')
    if not os.path.isdir(path):
        os.makedirs(path)

    path = os.path.join(path, 'cookies.json')

    return path

def getDateTimeTimeZone(dt=None, tz='US/Central'):
    if dt == None:
        dt = datetime.now(timezone.utc).astimezone()

    if dt.tzinfo == None:
        utc = pytz.timezone('UTC')
        dt = utc.localize(dt)
    
    tz = pytz.timezone(tz)
    dt = dt.astimezone(tz)

    return dt

async def tweet(content):
    #load twikit client
    tc = twikit.Client()
    logged_in = config.getConfigValue('logged_in', default = False)
    if logged_in:
        tc.load_cookies(getCookiePath())
    else:
        #login
        username = dotenv.get_key('.env', 'TWITTER_USERNAME')
        email = dotenv.get_key('.env', 'TWITTER_EMAIL')
        password = dotenv.get_key('.env', 'TWITTER_PASSWORD')

        await tc.login(auth_info_1 = username, auth_info_2 = email, password = password)

        #save cookies so we don't have to login again
        tc.save_cookies(getCookiePath())
        config.saveConfigValue('logged_in', True)

    #send tweet
    try:
        await tc.create_tweet(content)
    except twikit.errors.DuplicateTweet:
        pass

def run():
    print("Process starting...")
    
    while True:
        print("Checking for new records...")

        #connect to google sheets api, get sheet
        gs = gspread.service_account(filename = 'google-api.json')
        SHEET_KEY = dotenv.get_key('.env', 'SHEET_KEY')
        sheet = gs.open_by_key(SHEET_KEY).sheet1

        #check for new records
        last_row = config.getConfigValue('last_row', default = sheet.row_count - 1)
        if sheet.row_count > last_row:
            #only add one, so if there are multiple new rows the rest will be picked up next process
            row = last_row + 1

            #build tweet
            artist = sheet.cell(row, 2).value
            album = sheet.cell(row, 3).value
            year = sheet.cell(row, 4).value
            link = sheet.cell(row, 6).value
            tweet_text = f'Just listened to the album {album} by {artist} ({year}) for the first time:\n\n{link}'

            #get number of albums this year
            year = datetime.strftime(datetime.now(), '%Y')
            year = re.compile(f'..?/..?/{year}')
            albums = len(sheet.findall(year, in_column=5))
            extra_text = f"\n\nI've listened to {albums} new albums so far this year."
            if (len(tweet_text) + len(extra_text) <= 280):
                tweet_text = tweet_text + extra_text

            #send tweet
            print(f"New record found, sending tweet...")
            asyncio.run(tweet(tweet_text))
            
            #save config data
            config.saveConfigValue('tweets_sent', config.getConfigValue('tweets_sent', default = 0) + 1)
            config.saveConfigValue('last_row', row)
            config.saveConfigValue('last_tweet', str(getDateTimeTimeZone()))

            print("Process complete.")

        #save process time
        config.saveConfigValue('last_process', str(getDateTimeTimeZone()))

        #now we wait
        print("Waiting...")
        time.sleep(int(dotenv.get_key('.env', 'INTERVAL_SECONDS')))

#run program
if __name__ == '__main__':
    run()













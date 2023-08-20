##[ IMPORTS ]##
import os
import requests
import json
import webbrowser
import traceback
from selenium import webdriver
from termcolor import colored, cprint
from os.path import dirname, join
session = requests.Session()
session.cookies["CONSENT"] = "YES+cb.20210328-17-p0.en-GB+FX+"
session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'

file_list = os.listdir(dirname(__file__) + "./assets/streamers")

cprint("What list of streamers would you like to scan?", 'blue')
print("-----------------------")
for index, file_name in enumerate(file_list, start=1):
    print(f"{index}. {file_name}")
print("-----------------------")

selection = input("Enter the number corresponding to the file (or 'q' to quit): ")
if selection.isdigit() and 1 <= int(selection) <= len(file_list):
    chosen_file = file_list[int(selection) - 1]
    cprint(f"You selected: {chosen_file}", 'blue')
elif selection.lower() == 'q':
    print("Exiting the program.")
else:
    print("Invalid selection.")

# = # = # = # = # = #

config = json.load(open(join(dirname(__file__), "./config.json")))
languages = json.load(open(join(dirname(__file__), "./assets/languages.json"), encoding="utf8"))
streamers = json.load(open(join(dirname(__file__), "./assets/streamers/"+chosen_file)))

def twitch_is_live(link):
    if config['Services']['Twitch']['simple_method']:
        try:
            r = requests.get(link)
            if "isLiveBroadcast" in r.content.decode('utf-8'):
                cprint(f'[#] {link} is live.', 'green')
                if config['Settings']['Open_In_Browser']:
                    webbrowser.open(link)
            else:
                cprint(f'[X] {link} is not live.', 'red')
        except:
            traceback.print_exc()
    if config['Services']['Twitch']['api_method']:
        # SEARCH ACCOUNT #
        filtered_name = link.replace("https://www.twitch.tv/", "")
        try:
            stream = requests.get('https://api.twitch.tv/helix/streams?user_login=' + filtered_name, headers=headers)
            stream_data = stream.json();

            if len(stream_data['data']) == 1:
                # FOUND STREAM INFORMATION #
                game = stream_data['data'][0]['game_name']
                viewcount = str(stream_data['data'][0]['viewer_count'])
                language = stream_data['data'][0]['language']

                # FIND LANGUAGE #
                for x in languages:
                    if x == language:
                        real_language = languages[x]['name']

                # OUTPUT #
                cprint(f'[#] {link} is currently live. \n[#] <{real_language}> [{game}] to {viewcount} viewer(s)', 'green')
                if config['Open_In_Browser']:
                    webbrowser.open(link)
            else:
                print(f'[X] {link} is not live', 'red')
        except:
            traceback.print_exc()

def youtube_is_live(link):
    try:
        page = session.get(link)
        if 'Started streaming' in page.content.decode('utf-8'):
            cprint(f'[#] {link} is streaming.', 'green')
            # livestreams.append(link)
            if config['Open_In_Browser']:
                webbrowser.open(link)
        else:
            cprint(f'[X] {link} is not streaming.', 'red')
    except:
        traceback.print_exc()

def kick_is_live(link):
    filtered_name = link.replace("https://kick.com/", "")
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--enable-javascript")
        chrome_options.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=chrome_options)
        api = driver.get(f"https://kick.com/api/v1/channels/{filtered_name}")
        api_response = driver.page_source
        if "\"is_live\":true" in api_response:
            cprint(f'[#] {link} is live.', 'green')
            if config['Open_In_Browser']:
                webbrowser.open(link)
        else:
            cprint(f'[X] {link} is not live', 'red')
    except:
        traceback.print_exc()

def is_live(link):
    if "youtube.com" in link:
        youtube_is_live(link)
    elif "twitch.tv" in link:
        twitch_is_live(link)
    elif "kick.com" in link:
        kick_is_live(link)

if config['Services']['Twitch']['api_method'] == True:
    try:
        r = requests.post('https://id.twitch.tv/oauth2/token', {
            'client_id': config['Services']['Twitch']['Authentication']['client_id'],
            'client_secret': config['Services']['Twitch']['Authentication']['client_secret'],
            "grant_type": 'client_credentials'
        })
        headers = {
            'Client-ID': config['Services']['Twitch']['Authentication']['client_id'],
            'Authorization': 'Bearer ' + r.json()['access_token']
        }
    except KeyError:
        cprint('Please input a client_id & client_secret while using API Method.', 'light_red')
        quit()

for category in streamers:
    try:
        cprint(f'\n{category}', 'white')
        if len(streamers[category]) != 0:
            for stream in streamers[category]:
                is_live(stream)
    except KeyError:
        print('Something went wrong!?', 'light_red')
        quit()
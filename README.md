# FindWhoisLive
Track your favorite YouTube & Twitch streamers' live status effortlessly with this Python script.   
Just input their usernames in a JSON file, and stay alerted whenever they're live.  
Never miss another stream again!  

**Requires latest version of Python.**

### Features

- Supports multiple platforms such as **YouTube**, **Twitch** & **Kick**
- Utilizes the **Twitch** API to provide additional details about their stream.
- Utilizes the **Kick** API to provide additional details about their stream. (**SOON**)
- Automatically open active streamers in browser.

## Installation:
Go to [python.org](https://www.python.org/downloads/) and download the latest python release.  
Go to [findwhoislive releases](https://github.com/Unreal1739/findwhoislive/releases/latest/) and download the latest release.  
Go to [ChromeDriver @ Chromium.org](https://chromedriver.chromium.org/downloads) and download the latest chromedriver.exe (**OPTIONAL, REQUIRED FOR KICK**)  
Unzip the compressed file into a directory of your choice.  
Drag and drop the downloaded ChromeDriver into the same folder as the script. (**OPTIONAL, REQUIRED FOR KICK**)  
Open ``setup.bat``, this will download what you need for the program to run.  
Configure ``config.json`` and ``assets/streamers/streamers.json`` to your liking then use ``run.bat``.  

## Configuration
Not updated.

## Adding your own streamers.  
To make your own categories, you need slight json file syntax knowledge.  
You can use [JsonChecker](https://jsonchecker.com/) to check for errors in your file.
### assets/streamers/my_favourite_streamers.json
```
{
  "category_name": [
    "streamer's link",
    "streamer's link 2"
  ]
}
```

# Song-DL
Project involves implementing a graphical user interface (GUI) that allows user to download songs from Youtube Music links. The project was written in Python 3 and utilizes Python's scripting capabilities and various technology listed below. The goal of this ongoing project is continue on a personal idea of replicating a music playing system such as Windows Media Player and Spotify.

**NOTE:** I have no intention of trying to commercialize this project, rather its a personal project to show that through Python scripting and using free open-source technology its possible to replicate online music streaming platforms. 

# Requirements
1. Python 3.x (Original project was ran in Python 3.9)
2. Selenium
3. BeautifulSoup
5. yt-dlp
6. FFmpeg
7. Windows OS (Linux support coming soon.)

# Installation

## Python 3.x.
Python can be installed from [Python's website](https://www.python.org/).

**NOTE:** While the original project was built in an IDE (Pycharm), the python scripts above can still be run via a command-line interface regardless of having an IDE.

## Selenium, BeautifulSoup, yt-dlp
All of the packages listed can be installed by Python's package installer **PIP**.

### PIP
If you don't have it already, you can follow the [installation guide](https://pip.pypa.io/en/stable/installation/) to install PIP.

### Selenium
```
pip install -U selenium
```
### BeautifulSoup
```
pip install beautifulsoup4
```
### yt-dlp
```
pip install -U yt-dlp
```

## FFmpeg
While FFmpeg does have its own PyPI package that is installed through PIP, for this project FFmpeg was used directly as a command on the terminal.
The main reason for not using the package version, was the bare or lack of sufficient documentation on how to use FFmpeg in Python.

You can get FFmpeg from it's [main website](https://ffmpeg.org/download.html). For this project specifically, gyan-dev's version of FFmpeg was utilized, which you can get [here](https://www.gyan.dev/ffmpeg/builds/) and make sure to download the **essentials** version of it and not the full version.

For setup, make sure you have a Windows PATH linking to the FFmpeg's **bin** folder.
You can follow these steps:
1. Either via control panel (Control Panel > System and Security > System > Look for "Advanced System Settings"
 or looking in the Windows' search bar "Edit the system environment variable". 
2. This will popup the "System Properties" window and from there you can click on Environment Variables under the Advanced tab to change the environment variables.
3. From here you can click on Path under User Variables and click Edit to edit it and then add the absolute path to where your FFmpeg's bin folder is. After that you are all set to OK everything and close out those windows.

# Setup
Upon pulling the files in this repository, to start the program you want to run the **sd_interface.py** file in your choice of Python IDE or command-line interface.

# Guide to using SongDownloader (Song-DL)
## How it works!
The application takes Youtube Music song links (not video links as Youtube Music may provides link to a music video). Upon collecting links it goes through the links the program downloads the song using yt-dlp as temp files. Then using Selenium, the program access the links provided and grabs the HTML source code, which is analyzed by BeautifulSoup to gather metadata relevant to the song(s) being downloaded. After the retrieval of metadata, the program uses FFmpeg with the temp song files and inserts the proper metadata relevant to the song(s) and outputting all the final song files wanted in the playlist folder which is created on the desktop of the user's device.

## User Interaction
On the GUI, the user has 3 entry/text boxes that they can fill out.
1) Song Links
- Ensure you have the correct Youtube Music links for the track and not for the music video when adding links. For adding multiple links, you can separate each link with a comma and also make sure to **not add** any spaces between links or after commas.
### HOW IT SHOULD LOOK
```
DO: link1,link2
DO NOT: link1, link2
```
2) Removing Link #
- This form/box only works to remove links you have already added. Upon adding links you will see a index number that marks what number the link is in the order it was added. If you want to remove a link you input the value that indexes that link. **NOTE** you can't remove multiple links at the same time and that every time you remove a link the the link index number updates for every link in the current list. 

3) Playlist Name/Folder Name
- This is important as the name enter will be the name of the folder that will be created on your desktop upon starting the download process for all the music you intend to download. 

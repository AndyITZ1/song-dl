# Selenium + BS4
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time
import os


def remove_illegal_char(name):
    illegal_chars = ['<', '>', ':', '\"', '/', '\\', '|', '?', '*', '＜', '＞']
    for char in illegal_chars:
        name = name.replace(char, '_')
    name = name.replace(" ", '_')
    return name


class MetaDataCollector:

    def __init__(self):
        self.options = FirefoxOptions()
        self.options.add_argument("--headless")
        self.service = Service('./geckodriver.exe')
        self.driver = None
        self.album_covers = []
        self.music_folder = os.path.join(os.path.expanduser("~"), 'Music\\temp\\')

    def run(self):
        self.driver = webdriver.Firefox(service=self.service, options=self.options)

    def get_metadata(self, url):
        if not os.path.isdir(self.music_folder):
            os.makedirs(f'{self.music_folder}')
        self.driver.get(url)
        time.sleep(5)
        page = self.driver.page_source
        soup = BeautifulSoup(page, 'html.parser')
        yt_content = soup.find('div', class_="content-info-wrapper style-scope ytmusic-player-bar")
        if yt_content:
            album_cover = soup.find('img', class_="style-scope yt-img-shadow")['src']
            song_name = yt_content.find('yt-formatted-string', class_="title style-scope ytmusic-player-bar")['title']
            song_data = yt_content.find('yt-formatted-string',
                                        class_="byline style-scope ytmusic-player-bar complex-string")
            # [artist, album_name, release year]
            yt_meta = song_data['title'].split(' • ')
            # Filter out illegal characters
            song_name = remove_illegal_char(song_name)
            yt_meta[1] = remove_illegal_char(yt_meta[1])
            yt_meta[0] = remove_illegal_char(yt_meta[0])
            print(song_name)
            print(yt_meta)
            if album_cover not in self.album_covers:
                self.album_covers.append(album_cover)
                os.system(f'curl -J -o'
                          f' "{self.music_folder}{yt_meta[1]}_{yt_meta[0]}.jpg" {album_cover}')
            return [f'{self.music_folder}{yt_meta[1]}_{yt_meta[0]}.jpg',
                    song_name, yt_meta[0], yt_meta[1], yt_meta[2]]

    def finish(self):
        self.driver.close()

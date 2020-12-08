#!/usr/bin/env python3

import requests
import re
from bs4 import BeautifulSoup
import tqdm
import os

def get_filename_from_cd(cd):
    """
    Get filename from content-disposition
    """
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0][1:-1]

DOWNLOAD_PATH = 'downloaded'

if __name__ == '__main__':
    # crawling genres
    search_url = 'https://audionautix.com'
    search = requests.get(search_url)
    html = search.text
    soup = BeautifulSoup(html, 'html.parser')

    search_res = soup.select('body > div.main-content-area > div > div > div > div > div.content-left > div > ul > li')

    genre_dirs = []
    download_URLs = []
    # for each genre get download URLs for music
    for genre in search_res:
        genre_name = genre.text.strip().replace('/', '_')
        genre_link = genre.find('a').attrs['href']

        genre_dir = os.path.join(DOWNLOAD_PATH,genre_name)
        os.makedirs(genre_dir, exist_ok=True)
        
        search = requests.get(search_url + genre_link)
        html = search.text
        soup = BeautifulSoup(html, 'html.parser')
        song_search_res = soup.select('body > div.main-content-area > div > div > div > div > div.content-middle > div.search-songs > div > div > div > div > div > div > div.songs > div.song-download > a')

        for song in song_search_res:
            genre_dirs.append(genre_dir)
            download_URLs.append(search_url + song.attrs['href'])


    for genre_dir, download_URL in tqdm.tqdm(zip(genre_dirs, download_URLs)):
        r = requests.get(download_URL)
        filename = download_URL[download_URL.find('/Music/')+7:]
        download_path = os.path.join(genre_dir, filename)
        tqdm.tqdm.write(download_path)
        with open(download_path, 'wb') as f:
            f.write(r.content)


import requests
import pandas as pd
from bs4 import BeautifulSoup

def extract_lyrics(song_url):
    # Send request to the song URL
    response = requests.get(song_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    title_tag = soup.find('h1', class_="title is-size-3")
    if title_tag:
        title_text = title_tag.text.strip()
        print(title_text)
        song_title = title_text.split('-')[0]
    else:
        song_title = "", ""
    
    lyrics_div = soup.find('div', class_="has-text-centered-mobile is-size-5-desktop")

    if lyrics_div:
        lyrics = lyrics_div.get_text(separator="\n").strip()
        lyrics = lyrics.split("เนื้อเพลง")[0].strip()
        lyrics = lyrics.replace(' ', '').replace('\n', '').replace('\r', '')
    else:
        lyrics = ""
    return song_title, lyrics

def get_song_df(artist_name):
    base_url = f"https://www.siamzone.com/music/thailyric/เนื้อเพลง-{artist_name}"
    main_url = "https://www.siamzone.com"

    # Send a request to the main page and parse it
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    song_links = soup.find_all('a', href=True)

    songs_data = []

    # Loop through each song link and extract details
    for link in song_links:
        if link['href'].startswith('/music/thailyric/'):
            song_url = main_url + link['href']
            print(f"Extracting {song_url}")
            song_title, lyrics = extract_lyrics(song_url)
            if song_title and lyrics:
                songs_data.append([song_title, lyrics])
    df = pd.DataFrame(songs_data, columns=['Song', 'Lyrics'])
    df['Artist'] = artist_name
    df['Song'] = df['Song'].str.replace('เนื้อเพลง ','')
    return df
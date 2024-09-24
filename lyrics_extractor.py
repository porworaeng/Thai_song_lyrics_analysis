import requests
import pandas as pd
from bs4 import BeautifulSoup

def extract_lyrics(song_url):
    # Send request to the song URL
    response = requests.get(song_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the song title and artist (from the <h1> tag)
    title_tag = soup.find('h1', class_="title is-size-3")
    if title_tag:
        title_text = title_tag.text.strip()
        # Split the title text at the hyphen to get song and artist
        song_title, artist = map(str.strip, title_text.split('-'))
    else:
        song_title, artist = "", ""
    
    # Extract the lyrics (from the specific <div> tag you provided)
    lyrics_div = soup.find('div', class_="has-text-centered-mobile is-size-5-desktop")
    lyrics = lyrics_div.get_text(separator="\n").strip().replace(' ','').replace('\n','').replace('\r','') if lyrics_div else ""
    
    return song_title, artist, lyrics

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
            song_title, artist, lyrics = extract_lyrics(song_url)
            if song_title and lyrics:
                songs_data.append([song_title, artist, lyrics])
    df = pd.DataFrame(songs_data, columns=['Song', 'Artist', 'Lyrics'])
    df['Artist'] = artist_name
    df['Song'] = df['Song'].str.replace('เนื้อเพลง ','')
    return df
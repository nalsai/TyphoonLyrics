import os
from flask import Flask, request, render_template, redirect, url_for
import syncedlyrics
from tinytag import TinyTag

app = Flask(__name__)

# Supported music file extensions
MUSIC_EXTENSIONS = ('.flac', '.opus', '.ogg', '.mp3', '.wav', '.m4a', '.aac', '.alac', '.wma', '.aiff', '.aif', '.aifc')

def find_music_files(directory):
    """Recursively find all music files in the given directory and its subdirectories."""
    music_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(MUSIC_EXTENSIONS):
                music_files.append(os.path.join(root, file))
    return music_files

def download_lyrics_for_music_files(music_files):
    """Download lyrics for the given list of music files."""
    for music_file in music_files:
        try:
            tag = TinyTag.get(music_file)

            lyrics = syncedlyrics.search("["+tag.title+"] ["+tag.artist+"]") 
            # TODO: try different search queries
            # TODO: add karoke lyrics and translation support
            if lyrics:
                lyric_file = music_file + '.lrc'
                with open(lyric_file, 'w', encoding='utf-8') as f:
                    f.write(lyrics)
                print(f"Lyrics downloaded for: {music_file}")
            else:
                print(f"No lyrics found for: {music_file}")
        except Exception as e:
            print(f"Error downloading lyrics for {music_file}: {e}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        directory = request.form['directory']
        if os.path.isdir(directory):
            music_files = find_music_files(directory)
            download_lyrics_for_music_files(music_files)
            return redirect(url_for('success'))
        else:
            return render_template('index.html', error="Invalid directory. Please try again.")
    return render_template('index.html')

@app.route('/success')
def success():
    return "Lyrics downloaded successfully!"

if __name__ == '__main__':
    app.run(debug=True)

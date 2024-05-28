import os
import threading
from flask import Flask, request, jsonify, render_template
import syncedlyrics
from tinytag import TinyTag

app = Flask(__name__)

MUSIC_EXTENSIONS = (".mp3", ".flac", ".wav", ".m4a")

file_states = {}
working_directory = ""
downloading = False

# Configuration
delete_lyric_txt = True
refresh_existing_lyrics = False


def remove_prefix(text, prefix):
    """Remove the given prefix from the text."""
    if text.startswith(prefix):
        return text[len(prefix) :]
    return text


def find_music_files(directory):
    """Recursively find all music files in the given directory and its subdirectories."""
    music_files = []
    global working_directory
    working_directory = directory
    print(working_directory)
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(MUSIC_EXTENSIONS):
                full_file_path = os.path.join(root, file)
                file_path = remove_prefix(full_file_path, working_directory)
                music_files.append(file_path)

                path_without_extension = os.path.splitext(full_file_path)[0]
                lyric_file = path_without_extension + ".lrc"
                if os.path.exists(lyric_file):
                    file_states[file_path] = "Lyrics already present"
                else:
                    file_states[file_path] = "Pending"
    return music_files


def download_lyrics_for_music_files(music_files):
    """Download lyrics for the given list of music files."""
    for music_file in music_files:
        global downloading
        downloading = True

        try:
            if (
                refresh_existing_lyrics
                and file_states[music_file] == "Lyrics already present"
            ):
                file_states[music_file] = "Pending"
            if file_states[music_file] != "Pending":
                continue

            path = working_directory + music_file
            tag = TinyTag.get(path)

            lyrics = syncedlyrics.search("[" + tag.title + "] [" + tag.artist + "]")
            """
            TODO:
            - use save_path to save the lyrics?
            - make sure the lyrics are for the correct song
            - compare different search results and select the best one, allow user to select a different one
            - add karoke lyrics and translation support
            - add option to allow for plain text lyrics
            """
            if lyrics:
                path_without_extension = os.path.splitext(path)[0]
                lyric_file = path_without_extension + ".lrc"
                with open(lyric_file, "w", encoding="utf-8") as f:
                    f.write(lyrics)
                file_states[music_file] = "Downloaded"

                lyric_txt_file = path_without_extension + ".txt"
                if os.path.exists(lyric_txt_file) and delete_lyric_txt:
                    os.remove(lyric_txt_file)
            else:
                file_states[music_file] = "No lyrics found"
        except Exception as e:
            file_states[music_file] = f"Error: {str(e)}"

        downloading = False


@app.route("/")
def index():
    return render_template("index.html", downloading= "true" if downloading else "false")


@app.route("/files", methods=["POST"])
def get_files():
    directory = request.json.get("directory")
    if os.path.isdir(directory):
        music_files = find_music_files(directory)
        return jsonify({"files": music_files, "states": file_states})
    else:
        return jsonify({"error": "Invalid directory."}), 400


@app.route("/download_lyrics", methods=["POST"])
def start_download():
    music_files = request.json.get("files")
    if music_files:
        threading.Thread(
            target=download_lyrics_for_music_files, args=(music_files,)
        ).start()
        return jsonify({"status": "Download started"})
    else:
        return jsonify({"error": "No files provided."}), 400


@app.route("/states", methods=["GET"])
def get_states():
    return jsonify(file_states)


if __name__ == "__main__":
    app.run(debug=True)

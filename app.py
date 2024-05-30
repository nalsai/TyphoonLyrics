import os
import threading
from flask import Flask, request, jsonify, render_template
import syncedlyrics
from tinytag import TinyTag

app = Flask(__name__)

MUSIC_EXTENSIONS = (
    ".flac",
    ".opus",
    ".ogg",
    ".mp3",
    ".wav",
    ".m4a",
    ".aac",
    ".alac",
    ".wma",
    ".aiff",
    ".aif",
    ".aifc",
)

file_states = {}
working_directory = ""
downloading = False

# Configuration
delete_lyrics_txt = True


def remove_prefix(text, prefix):
    """Remove the given prefix from the text."""
    if text.startswith(prefix):
        return text[len(prefix) :]
    return text


def find_music_files(directory):
    """Recursively find all music files in the given directory and its subdirectories."""
    global working_directory
    working_directory = directory
    print(working_directory)
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(MUSIC_EXTENSIONS):
                full_file_path = os.path.join(root, file)
                file_path = remove_prefix(full_file_path, working_directory)

                path_without_extension = os.path.splitext(full_file_path)[0]
                lyric_file = path_without_extension + ".lrc"
                if os.path.exists(lyric_file):
                    file_states[file_path] = "Lyrics already present"
                else:
                    file_states[file_path] = "Pending"


def download_lyrics_for_music_files(music_files):
    """Download lyrics for the given list of music files."""

    # remove all files that are not in the list
    for music_file in list(file_states.keys()):
        if music_file not in music_files:
            del file_states[music_file]

    for music_file in music_files:
        global downloading
        downloading = True

        try:
            if file_states[music_file] != "Pending":
                continue

            file_states[music_file] = "Downloading..."

            path = working_directory + music_file
            tag = TinyTag.get(path)

            lyrics = syncedlyrics.search("[" + tag.title + "] [" + tag.artist + "]")
            # TODO: use save_path to save the lyrics?

            if lyrics:
                path_without_extension = os.path.splitext(path)[0]
                lyric_file = path_without_extension + ".lrc"
                with open(lyric_file, "w", encoding="utf-8") as f:
                    f.write(lyrics)
                file_states[music_file] = "Downloaded"

                lyrics_txt_file = path_without_extension + ".txt"
                if os.path.exists(lyrics_txt_file) and delete_lyrics_txt:
                    os.remove(lyrics_txt_file)
            else:
                file_states[music_file] = "No lyrics found"
        except Exception as e:
            file_states[music_file] = f"Error: {str(e)}"

        downloading = False


@app.route("/")
def index():
    return render_template("index.html", downloading="true" if downloading else "false")


@app.route("/files", methods=["POST"])
def get_files():
    directory = request.json.get("directory")
    if os.path.isdir(directory):
        find_music_files(directory)
        return jsonify({"states": file_states})
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

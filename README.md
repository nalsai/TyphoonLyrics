# TyphoonLyrics

TyphoonLyrics is a frontend for the [syncedlyrics](https://github.com/moehmeni/syncedlyrics).
It uses a simple Flask web server for easy usage locally or directly on your media server.
The goal of this project is to allow users to easily download the appropriate .lrc file for every music file they have.

Thanks to syncedlyrics supporting a wide array of [providers](https://github.com/moehmeni/syncedlyrics?tab=readme-ov-file#providers),
TyphoonLyrics can find lyrics for almost any song that has synced lyrics available.

## TODO

- make sure the lyrics are for the correct song (check name, track, album? and duration)
- add option to allow for plain text lyrics in case no synced lyrics are available
- cache which tracks have had no lyrics found, so we don't search for the same file multiple times in case the run is interrupted
- compare different search results and select the best one, allow user to select a different one

## Installation

To install and run TyphoonLyrics, follow these steps:

1. Clone the repository:

    ```sh
    git clone https://github.com/nalsai/TyphoonLyrics.git
    cd TyphoonLyrics
    ```

2. Install the required dependencies:

    ```sh
    pip install Flask tinytag syncedlyrics
    ```

3. Start the web server:

    ```sh
    python app.py
    ```

## Usage

Once the web server is running, you can access TyphoonLyrics by opening your browser and navigating to `http://localhost:5000`.
From there, you can input the path to search for music files and download the lyrics.
The files need to be tagged with the correct title and artist for the search to work correctly.

## License

This project is licensed under the [MIT License](LICENSE).

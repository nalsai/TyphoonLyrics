# SyncedLyrics-UI

> [!CAUTION]
> This project is still in development and not yet ready for use.

SyncedLyrics-UI is a frontend for the [syncedlyrics](https://github.com/moehmeni/syncedlyrics) Python library and CLI.
It provides a web server for easy usage, both locally and directly on your media server.
The goal of this project is to allow users to easily download the appropriate .lrc file for every music file they have.

Thanks to syncedlyrics supporting a wide array of [providers](https://github.com/moehmeni/syncedlyrics?tab=readme-ov-file#providers),
SyncedLyrics-UI can find lyrics for almost any song that has synced lyrics available.

## Installation

To install and run Syncedlyrics-UI, follow these steps:

1. Clone the repository:

    ```shell
    git clone https://github.com/your-username/syncedlyrics-ui.git
    ```

2. Install the required dependencies:

    ```shell
    pip install Flask tinytag syncedlyrics
    ```

3. Start the web server:

    ```shell
    python app.py
    ```

## Usage

Once the web server is running, you can access SyncedLyrics-UI by opening your browser and navigating to `http://localhost:5000`.
From there, you can search for music files and download the corresponding .lrc files.

## License

This project is licensed under the [MIT License](LICENSE).

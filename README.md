[![img release](https://img.shields.io/github/commit-activity/m/MUSIC-Ecosystem-Team/MUSIC-server.svg?sanitize=true&color=blue)](#)
[![img last commit](https://img.shields.io/github/last-commit/MUSIC-Ecosystem-Team/MUSIC-server.svg)](#)
[![img last release](https://img.shields.io/github/release/MUSIC-Ecosystem-Team/MUSIC-server.svg?color=red)](#)
[![img last release](https://img.shields.io/twitter/follow/Ooggle_.svg?style=social)](https://twitter.com/Ooggle_)

# MUSIC!
Music server and music players for personal use and self-hosted experience.   
Listen your music everywhere without using a single MB of storage.

![logo](music.png)

## Current development progression
MUSIC! server: Most of the mandatory endpoints have been done.    
MUSIC! Android player: research stage.   
MUSIC! Web player: currently developed by MeatReed [here](https://github.com/MUSIC-Ecosystem-Team/MUSIC-node-website).   

For now, it will support mp3, flac, ogg and m4a formats. Maybe i will add more in the future. Also, everything is WIP for the moment.

To view the server API progress, feel free to visit [the dedicated page](https://github.com/MUSIC-Ecosystem-Team/MUSIC-server/wiki/).

## Usage

You need at least `python3` and `pip`:   
```bash
git clone https://github.com/MUSIC-Ecosystem-Team/MUSIC-server && cd MUSIC-server
python3 -m pip install -r requirements.txt
cd src
python3 ./server.py
```
*On WSL, you may need to use `sudo` with the last command*

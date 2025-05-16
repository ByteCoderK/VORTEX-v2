import random 
import os

def play_music():
    music_dir = "F:\\STRORAGE\\OneDrive\\Desktop\\Python\\AI\\DataBase\\music"
    try:
        songs = os.listdir(music_dir)
        rd = random.choice(songs)
        os.startfile(os.path.join(music_dir, rd))
        return "Playing your favorite tunes."
    except Exception as e:
        return "Apologies, Master. I'm unable to play music at the moment."
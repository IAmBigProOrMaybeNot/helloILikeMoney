from moviepy.editor import *
import os
import random
from Config import Config


class Music:
    def __init__(self, musicFolder):
        self.fps = int(Config.getConfig("VIDEO","FPS",60))
        self.music = self.convertPathsToAudioClips(
            self.loadMusics(musicFolder))

    def bestFit(self, lengthInFps):
        musicList = []
        
        while self.calculateLengthOfMusicInList(musicList) < lengthInFps/self.fps:
            musicList.append(random.choice(self.music))

        untrimmedAudioClip = concatenate_audioclips(musicList)
        trimmedAudioClip = untrimmedAudioClip.subclip(0,lengthInFps/self.fps)
        return trimmedAudioClip

    def calculateLengthOfMusicInList(self, l):
        total = 0
        for item in l:
            total += item.duration
        return total

    def loadMusics(self, musicFolder):
        musicFilePaths = []
        for music in os.listdir(musicFolder):
            if ".mp3" not in music:
                continue
            print(music)

            suffix = music[music.index("."):]
            if suffix == ".mp3":
                musicFilePaths.append(os.path.join(musicFolder, music))
        return musicFilePaths

    def convertPathsToAudioClips(self, musicFilePaths):
        result = []
        for music in musicFilePaths:
            result.append(AudioFileClip(music))

        return result

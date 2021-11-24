import pygame, json

class SoundManager():
    def __init__(self):
        pygame.mixer.init()
        with open('settings.json', 'r') as f:
            data = json.load(f)
            self.master_volume = data['volumes']['master']
            self.music_volume = data['volumes']['music']
            self.sound_volume = data['volumes']['sound']
        self.sounds = {
            'coin_pickup_1': pygame.mixer.Sound('assets\\audio\\sounds\\Gameplay\\5. Collectibles\\Collectibles_1.wav'),
            'coin_pickup_2': pygame.mixer.Sound('assets\\audio\\sounds\\Gameplay\\5. Collectibles\\Collectibles_2.wav'),
            'coin_pickup_3': pygame.mixer.Sound('assets\\audio\\sounds\\Gameplay\\5. Collectibles\\Collectibles_6.wav'),
            'hit_1': pygame.mixer.Sound('assets\\audio\\sounds\\Gameplay\\4. Impact\\Hit_2.wav'),
            'hit_2': pygame.mixer.Sound('assets\\audio\\sounds\\Gameplay\\4. Impact\\Hit_4.wav'),
            'slash_1': pygame.mixer.Sound('assets\\audio\\sounds\\Gameplay\\4. Impact\\Metal_woosh_1.wav'),
            'slash_2': pygame.mixer.Sound('assets\\audio\\sounds\\Gameplay\\4. Impact\\Metal_woosh_2.wav'),
            'click_1': pygame.mixer.Sound('assets\\audio\\sounds\\UI\\2. Clicks\\Click_5.wav'),
            'click_2': pygame.mixer.Sound('assets\\audio\\sounds\\UI\\2. Clicks\\Click_6.wav'),
            'deathsound': pygame.mixer.Sound('assets\\audio\\sounds\\deathsound.mp3'),
            'deathsound_2': pygame.mixer.Sound('assets\\audio\\sounds\\deathsound_2.mp3')
        }
        self.music = {
            'stray_cat': 'assets\\audio\\music\\Monolith OST 320\\33 Stray Cat (Alternate).mp3',
            'rivaling_force': 'assets\\audio\\music\\Monolith OST 320\\17 Rivaling Force.mp3'
        }
    def setMasterVolume(self, volume):
        self.master_volume = volume
        pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
    def setMusicVolume(self, volume):
        self.music_volume = volume
        pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
    def setSoundVolume(self, volume):
        self.sound_volume = volume
    def playSound(self, name):
        self.sounds[name].set_volume(self.sound_volume * self.master_volume)
        self.sounds[name].play()
    def playMusic(self, name):
        pygame.mixer.music.load(self.music[name])
        pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
        pygame.mixer.music.play(-1)
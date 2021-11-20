import pygame
class SoundManager():
    def __init__(self):
        pygame.mixer.init()
        self.soundVolume = 0.4
        self.musicVolume = 0.2
        self.sounds = {
            'coin_pickup_1': pygame.mixer.Sound('assets\\audio\\sounds\\Gameplay\\5. Collectibles\\Collectibles_1.wav'),
            'coin_pickup_2': pygame.mixer.Sound('assets\\audio\\sounds\\Gameplay\\5. Collectibles\\Collectibles_2.wav'),
            'coin_pickup_3': pygame.mixer.Sound('assets\\audio\\sounds\\Gameplay\\5. Collectibles\\Collectibles_6.wav'),
            'hit_1': pygame.mixer.Sound('assets\\audio\\sounds\\Gameplay\\4. Impact\\Hit_2.wav'),
            'hit_2': pygame.mixer.Sound('assets\\audio\\sounds\\Gameplay\\4. Impact\\Hit_4.wav'),
            'slash_1': pygame.mixer.Sound('assets\\audio\\sounds\\Gameplay\\4. Impact\\Metal_woosh_1.wav'),
            'slash_2': pygame.mixer.Sound('assets\\audio\\sounds\\Gameplay\\4. Impact\\Metal_woosh_2.wav')
        }
        self.music = {
            'stray_cat': 'assets\\audio\\music\\Monolith OST 320\\33 Stray Cat (Alternate).mp3',
            'rivaling_force': 'assets\\audio\\music\\Monolith OST 320\\17 Rivaling Force.mp3'
        }
    def playSound(self, name):
        self.sounds[name].set_volume(self.soundVolume)
        self.sounds[name].play()
    def playMusic(self, name):
        pygame.mixer.music.load(self.music[name])
        pygame.mixer.music.set_volume(self.musicVolume)
        pygame.mixer.music.play(-1)
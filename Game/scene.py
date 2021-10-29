class Scene:
    def __init__(self):
        pass
    def input(self):
        pass
    def update(self):
        pass
    def draw(self):
        pass

class MainMenu(Scene):
    def input(self):
        print(1)
    def update(self):
        pass
    def draw(self):
        pass

class Game(Scene):
    pass

class SceneManager:
    def __init__(self):
        self.scenes = []
    def input(self):
        if len(self.scenes) > 0:
            self.scenes[-1].input()
    def update(self):
        if len(self.scenes) > 0:
            self.scenes[-1].update()
    def draw(self):
        if len(self.scenes) > 0:
            self.scenes[-1].draw()
    def push(self, scene):
        self.scenes.append(scene)
    def pop(self):
        self.scenes.pop()
    def set(self, scene):
        self.scenes = [scene]
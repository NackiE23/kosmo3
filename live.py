from pygame import image
from pygame.sprite import Sprite, Group


class Live(Sprite):

    def __init__(self, screen, amount=0):
        super(Live, self).__init__()
        self.screen = screen
        self.amount = amount
        self.image = image.load("assets/images/kosmo_live.png")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.center = float(self.rect.centerx)
        self.rect.bottom = self.screen_rect.bottom

    def draw(self):
        self.lives = Group()
        for lives_number in range(self.amount):
            live = Live(self.screen)
            live.rect.x = 15 + lives_number * live.rect.width
            live.rect.y = 20
            self.lives.add(live)
        self.lives.draw(self.screen)

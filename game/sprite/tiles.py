import pygame
     
class TileSprite(pygame.sprite.Sprite):

    # state
    # 0: idle
    # 1: move
    # 2: attack
    # 3: die
    def __init__(self, size, position, movement, group, hp, power, name, images, game):

        super(TileSprite, self).__init__()

        self.game = game
        self.name = name
        self.state = 0
        self.hp = hp
        self.hp_max = hp
        self.power = power
        self.movement = movement
        self.group = group
        self.images = images        
        self.rect = pygame.Rect(position, size)
        self.img_index = 0
        self.img_index_start = 0
        self.img_index_end = 0
        self.image = self.images[self.img_index]  
        
        self.animation_time = 1

        # mt와 결합하여 animation_time을 계산할 시간 초기화
        self.current_time = 0
        self.current_attack_time = 0

    def move(self):
        dx, dy = self.movement
        self.rect.x += dx
        self.rect.y += dy

    def update(self, mt, game):
        self.image = self.images[0]

    def draw(self):
        pass
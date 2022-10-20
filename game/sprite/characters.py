from game.code import SCREEN_WIDTH
import pygame

# 기본 오브젝트 클래스
class BaseObject:
    def __init__(self, size, position, movement, group, hp, power, name, profile, images, game):
        self.game = game
        self.name = name
        self.profile = profile
        self.state = 1
        self.hp = hp
        self.hp_max = hp
        self.power = power
        self.movement = movement
        self.now_movement = movement
        self.group = group
        self.type = 1
        self.images = images
    
    def move(self):
        dx, dy = self.now_movement
        self.rect.x += dx
        self.rect.y += dy
        if self.rect.x <= -30:
            self.direction = 'right'
            self.now_movement = (-self.now_movement[0],0)            
        elif self.rect.x >= SCREEN_WIDTH - 100:
            self.direction = 'left'
            self.now_movement = (-self.now_movement[0],0)

    def update(self, mt, game):
        pass

    def draw(self, mt):
        pass
    
    def draw_back(self):
        pass

    def damaged(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.destroy_self()

    def destroy_self(self):
        self.kill()

class DogSprite(pygame.sprite.Sprite, BaseObject):

    # state
    # 0: idle
    # 1: walk
    # 2: run
    # 3: jump
    # 4: slide
    # 5: hurt
    # type
    # 1: character
    # 2: structure(castle)
    # 3: skill
    def __init__(self, size, position, direction, movement, state, group, hp, power, name, profile, images, game):

        super(DogSprite, self).__init__()

        self.game = game
        self.name = name        
        self.profile = profile
        self.state = state
        self.hp = hp
        self.hp_max = hp
        self.power = power
        self.direction = direction
        self.movement = movement
        self.now_movement = movement
        self.motion_time = 0            # 특정 이벤트에 의해 state, movement가 설정되고 해당 애니메이션을 보이는 시간
        self.now_motion_time = 0
        self.group = group
        self.type = 1
        self.chat = None                # 관리자 채팅        
        self.images = images
          
        # rect 만들기
        self.rect = pygame.Rect(position, size)
  
        base_idx = 0
        if self.direction == 'left':
            base_idx = 57
        
        if self.state == 0:             # idle
            self.img_index_start = base_idx + 0
            self.img_index_end = base_idx + 9
        elif self.state == 1:           # walk
            self.img_index_start = base_idx + 10
            self.img_index_end = base_idx + 19
        elif self.state == 2:           # run
            self.img_index_start = base_idx + 20
            self.img_index_end = base_idx + 27
        elif self.state == 3:           # jump
            self.img_index_start = base_idx + 28
            self.img_index_end = base_idx + 36
        elif self.state == 4:           # slide
            self.img_index_start = base_idx + 37
            self.img_index_end = base_idx + 46
        elif self.state == 5:           # hurt
            self.img_index_start = base_idx + 47
            self.img_index_end = base_idx + 56

        self.img_index = self.img_index_start
        self.image = self.images[self.img_index]  # 'image' is the current image of the animation.

        # 1초에 보여줄 1장의 이미지 시간을 계산, 소수점 3자리까지 반올림
        #self.animation_time = round(100 / len(self.images * 100), 2)
        img_len = self.img_index_end - self.img_index_start + 1
        self.animation_time = round(100 / (img_len * 150), 2)
        self.chat_animation_time = 4
        self.chat_animation_now = 0

        # mt와 결합하여 animation_time을 계산할 시간 초기화
        self.current_time = 0
        self.current_attack_time = 0

    def update(self, mt, game):
        # update를 통해 캐릭터의 이미지가 계속 반복해서 나타나도록 한다.
        
        self.move()
        
        base_idx = 0
        if self.direction == 'left':
            base_idx = 57
        
        if self.state == 0:             # idle
            self.img_index_start = base_idx + 0
            self.img_index_end = base_idx + 9
        elif self.state == 1:           # walk
            self.img_index_start = base_idx + 10
            self.img_index_end = base_idx + 19
        elif self.state == 2:           # run
            self.img_index_start = base_idx + 20
            self.img_index_end = base_idx + 27
        elif self.state == 3:           # jump
            self.img_index_start = base_idx + 28
            self.img_index_end = base_idx + 36
        elif self.state == 4:           # slide
            self.img_index_start = base_idx + 37
            self.img_index_end = base_idx + 46
        elif self.state == 5:           # hurt
            self.img_index_start = base_idx + 47
            self.img_index_end = base_idx + 56

        if self.img_index < self.img_index_start or self.img_index > self.img_index_end:
            self.img_index = self.img_index_start

        # loop 시간 더하기
        self.current_time += mt

        # loop time 경과가 animation_time을 넘어서면 새로운 이미지 출력 
        if self.current_time >= self.animation_time:
            self.current_time = 0
        
            self.img_index += 1
            if self.img_index > self.img_index_end:
                self.img_index = self.img_index_start
            #print("start:[%d]/end:[%d]"%(self.img_index_start, self.img_index_end))               
            #print("[Now Dog Image IDx]:%d"%self.img_index)
            self.image = self.images[self.img_index]
            #print("%d[Now Dog Image Number]:%d"%(len(self.images), self.img_index))
        
        self.check_motion_time(mt)

    def check_motion_time(self, mt):
        self.now_motion_time += mt
        if self.now_motion_time >= self.motion_time:
            self.now_movement = (0, 0)
            self.state = 0
            self.motion_time = 0
            self.now_motion_time = 0

    def draw(self, mt):
        # 채팅 출력
        if self.chat != None:
            
            msg = self.chat
            if len(msg) >= 25:
                msg = msg[0:25] + '...'
            chat = self.game.main_font_15.render(msg, True, self.game.COLOR_BLACK)
            chat_rect = chat.get_rect()
            chat_size = chat_rect.size
            # 채팅창
            chat_back_rect = pygame.draw.rect(self.game.SCREEN, self.game.COLOR_WHITE, [self.rect.x, self.rect.y - 30, chat_size[0] + 20, chat_size[1] + 10])
            chat_rect.centerx = chat_back_rect.centerx
            # 채팅 메시지
            self.game.SCREEN.blit(chat, (self.rect.x + 10, chat_back_rect.y + 3))
            self.chat_animation_now += mt
            if self.chat_animation_now >= self.chat_animation_time:
                self.chat = None
                self.chat_animation_now = 0
        
        # # 닉네임 출력        
        # if self.name != 'left_soldier' and self.name != 'right_soldier' and self.name != 'dead_soldier':
        #     nickname_text = self.game.main_font_13.render(self.name, True, self.game.COLOR_BLACK)
        #     nickname_text_rect = nickname_text.get_rect()
        #     nickname_text_size = nickname_text_rect.size            
        #     nickname_text_rect.centerx = self.rect.centerx            
        #     self_size_y = self.rect.size[1]
        #     self.game.SCREEN.blit(nickname_text, (nickname_text_rect.x, self.rect.y + self_size_y + 2))

    def collide_enemy(self, mt, enemy_group, game):
        pass
    
    def destroy_self(self):
        pass


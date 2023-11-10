import pygame
import pygame.mixer
import asyncio
import time
import io
import datetime
import json
import random
import requests
import os
import sys
import websockets
from game.dataload import *
from game.sprite import ui
from game.sprite import characters
from game.code import *
from urllib.request import urlopen
from PIL import Image, ImageDraw
import numpy as np
import emoji 
#import unicode



# 게임 플레이 설정

class Game:
    def __init__(self):
        # 게임 초기화
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("TIKTOK WORD GAME")        

        #print(pygame.font.get_fonts())  # 사용 가능한 시스템 폰트 목록 출력 - 한글 지원x
        
        # 상태 변수 설정
        # ready
        self.is_end_ready_animation = False
        self.is_set_candidate = False 
        self.is_set_tiles = False
        # start
        self.is_set_timer = False
        # over
        self.is_end_over_animation = False
        self.is_update_rank = False
        self.is_clear_game_data = False
        
        self.state = GAME_STATE_INIT
        
        # 게임 환경 설정
        self.SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #화면 크기 설정
        self.clock = pygame.time.Clock() 
        self.FPS = FPS
        self.COLOR_BLUE = (24, 154, 211)
        self.COLOR_BLACK = (0, 0, 0)
        self.COLOR_WHITE = (255, 255, 255)
        self.COLOR_YELLOW = (255, 228, 0)
        self.COLOR_YELLOW_LEMON = (255, 255, 159)
        self.COLOR_ORANGE_PEEL = (255, 159, 0)
        self.COLOR_BLUE_LIGHT = (103, 153, 255)
        self.COLOR_BLUE_DEEP = (1, 0, 255)
        self.COLOR_BLUE_DARK = (0, 34, 102)
        self.COLOR_GREEN_LIGHT = (183, 240, 177)
        self.COLOR_GREEN_DEEP = (47, 157, 39)
        self.COLOR_PURPLE = (95, 0, 255)
        self.COLOR_PURPLE_LIGHT = (150, 120, 182)
        self.COLOR_PURPLE_DARK = (120, 85, 157)
        self.COLOR_RED_LIGHT = (255, 167, 167)
        self.COLOR_GREY_LIGHT = (213, 213, 213)
        self.COLOR_BROWN = (136, 101, 78)
        self.COLOR_BROWN_DARK = (69, 48, 10)
        self.COLOR_JELLY_BEAN_BLUE = (68, 121, 142)
        
        self.main_font_60 = pygame.font.Font("game/res/font/NanumBarunGothicBold.ttf", 60)
        self.main_font_40 = pygame.font.Font("game/res/font/NanumBarunGothicBold.ttf", 40)   
        self.main_font_30 = pygame.font.Font("game/res/font/NanumBarunGothicBold.ttf", 30)   
        self.main_font_25 = pygame.font.Font("game/res/font/NanumBarunGothicBold.ttf", 25)   
        self.main_font_20 = pygame.font.Font("game/res/font/NanumBarunGothicBold.ttf", 20) 
        self.main_font_15 = pygame.font.Font("game/res/font/NanumBarunGothicBold.ttf", 15)
        self.main_font_13 = pygame.font.Font("game/res/font/NanumBarunGothicBold.ttf", 13) 
        self.main_font_11 = pygame.font.Font("game/res/font/NanumBarunGothicBold.ttf", 11) 

        self.sebang_font_30_bold = pygame.font.Font("game/res/font/SEBANGGothicBold.ttf", 30)
        self.sebang_font_27_bold = pygame.font.Font("game/res/font/SEBANGGothicBold.ttf", 27) 
        self.sebang_font_25_bold = pygame.font.Font("game/res/font/SEBANGGothicBold.ttf", 25)
        self.sebang_font_22_bold = pygame.font.Font("game/res/font/SEBANGGothicBold.ttf", 22) 
        self.sebang_font_20_bold = pygame.font.Font("game/res/font/SEBANGGothicBold.ttf", 20) 
        self.sebang_font_18_bold = pygame.font.Font("game/res/font/SEBANGGothicBold.ttf", 18) 
        self.sebang_font_15_bold = pygame.font.Font("game/res/font/SEBANGGothicBold.ttf", 15) 
        self.sebang_font_30 = pygame.font.Font("game/res/font/SEBANGGothic.ttf", 30)
        
        self.sebang_font_20 = pygame.font.Font("game/res/font/SEBANGGothic.ttf", 20) 
        self.sebang_font_15 = pygame.font.Font("game/res/font/SEBANGGothic.ttf", 15)  
        self.sebang_font_11 = pygame.font.Font("game/res/font/SEBANGGothic.ttf", 11) 

        # sprite group 설정
        self.sprite_group = pygame.sprite.Group()
        self.tile_group = pygame.sprite.Group()
        self.ui_group = pygame.sprite.Group()

        self.tile_size = (50, 50)
        self.donation_size = (SCREEN_WIDTH / 7, SCREEN_WIDTH / 7)
        self.right_profile_size = (SCREEN_WIDTH / 6, SCREEN_WIDTH / 6)
        self.npc_dog_size = (130, 130)

        # 리소스 불러오기
        import_dog_images(self.npc_dog_size)
        import_cat_images(self.npc_dog_size)
        
        print("[dog_images size]:%d"%len(dog_images))

        # 효과음 로드
        self.sound_map = import_sound()
        
        #text = main_font.render("Test Text", True, COLOR_BLACK)     # 문자열, antialias, 글자색

        self.message_queue = []     # 웹소켓 전송 메시지큐
        self.donation_queue = []    # 도네이션 큐
        self.right_user_queue = []  # 정답자 큐

        ### 시간 관련 변수 ###
        self.npc_move_term = 500       # NPC 자동 움직임 시간 간격
        self.game_timer_term = 60 * 2  # 게임 플레이 제한 시간 - 240초 => 4분
        self.bonus_time = 0            # 남은 보너스 시간  
        self.bonus_start_time = 0      # 보너스 시작 시간

        
        # 게임 플레이 변수
        self.websocket = None
        self.is_ws_connected = False

        self.ready_animation_time = 0   # ready animation 시작 시간
        self.ready_animation_before_time = 0    # 이전 시간 
        self.ready_animation_term = 0   # 시작부터 변경된 누적 시간 - 일정 간격으로 초기화
        self.over_animation_time = 0
        self.goal_like_cnt = 0          # 보너스 목표 좋아요 개수
        self.now_goal_like_cnt = 0      # 현재 보너스 좋아요 개수


        self.consonant = ['ㄱ','ㄴ','ㄷ','ㄹ','ㅁ','ㅂ','ㅅ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']
        self.random_consonant = None
        
        # npc 초기화        
        self.npc_dog = characters.DogSprite(size=self.npc_dog_size, position=RIGHT_SPAWN_POSITION, direction='left', movement=(0,0), state=0, group='npc', 
                                            hp=100, power=1, name='PangDog', profile=None, images=dog_images, game=self)        
        self.sprite_group.add(self.npc_dog)

        # self.npc_cat = characters.DogSprite(size=self.npc_dog_size, position=LEFT_SPAWN_POSITION, direction='right', movement=(0,0), state=0, group='npc', 
        #                                     hp=100, power=1, name='PangCat', profile=None, images=cat_images, game=self)        
        # self.sprite_group.add(self.npc_cat)
        

        self.coin_map = {}
        self.like_map = {}
        self.share_map = {}

        self.top_ranks = []

        self.now_word = None
        self.send_word = None
        self.now_hint_idx = -1
        self.max_hint_count = 0
        self.now_hint_count = 0
        self.hint_height = SCREEN_HEIGHT * 0.34
        
        self.last_right_user = None

        self.draw_ready = False
        self.draw_result = False
        self.print_user_state = True        
        self.state = GAME_STATE_READY

        self.total_msg_count = 0
       
        self.candidates = []            # 단어 후보
        self.selected_candidates = []   # 한 번 나온 단어
        
        # word 로드
        self.load_word_data("game/data/words.txt")   
        self.load_word_data("game/data/words_entertainment.txt")   
        self.load_word_data("game/data/words_animal.txt")   
        self.load_word_data("game/data/words_food.txt")
        #self.load_word_data("game/data/words_slang.txt")    


        # 랭킹 정보 로드 => 그날의 랭킹 데이터가 있다면 로드
        self.rank = {}
        try:
            now = time.localtime()
            tody_str = time.strftime('%Y%m%d', now)     
            f = open("game/data/rank/user_rank_%s.txt" % tody_str, 'r', encoding='UTF-8')
            while True:
                line = f.readline()
                if not line: break                        
                obj = json.loads(line)
                self.rank[obj.get('user_id')] = obj    
                self.top_ranks.append(obj)        
                #print("[LOAD RANK]: %s => %d %d " % (obj.get('name'), obj.get('win'), obj.get('lose')))
            print("[[ Complete load user rank data. ]]")
            f.close()
        except FileNotFoundError as e:
            pass              


        print("[[ END INIT GAME ]]")

    def load_word_data(self, path):        
        # 두 개의 리스트 합치기
        # list1 = [10, 22, 19]
        # list2 = [2, 9, 3]
        # list3 = list1 + list2
               
        #f = open("game/data/words.txt", 'r', encoding='UTF-8')
        f = open(path, 'r', encoding='UTF-8')
        count = 0
        while True:
            line = f.readline()
            if not line: break 
            line = line.replace("\n", "")   
            if line == None or line == "":
                continue        
            obj = json.loads(line)     
                   
            if obj['word'] == "" or obj['consonant'] == "":
                continue
            
            self.candidates.append(obj)
            #print("[LOADED DATA COUNT]:%d"%count)
            count += 1
        print("[[ Complete load words data. ]]: %d" % count)    
        f.close()

    async def animation(self):
       
        current_time = 0
        while True:
            #print('animation/game_state:[%d]' % self.state)
            last_time, current_time = current_time, time.time()
            await asyncio.sleep(1 / FPS - (current_time - last_time))  # tick
            
            mt = self.clock.tick(FPS) / 1000 # 1000을 나누어줘서 초단위로 변경하여 반환
            
            # ================================== READY ==================================
            if self.state == GAME_STATE_READY:
                # 다음 단어 선정
                # 랜덤 함수 사용     
                if self.is_set_candidate == False:
                    tmp_arr = list(range(len(self.candidates)))
                    idx = random.randint(0, len(tmp_arr) - 1)
                    self.now_word = self.candidates[idx]

                    self.selected_candidates.append(self.now_word)
                    del self.candidates[idx]

                    # 남은 단어 후보가 10개 이하라면 이미 나온 단어들을 다시 후보로 넣어준다.
                    if len(self.candidates) < 10:
                        self.candidates.extend(self.selected_candidates)
                        self.selected_candidates = []
                    
                    # 서버에 전송할 현재 단어 설정                    
                    self.send_word = self.now_word['word']
                    
                    # 힌트 개수 카운트                 
                    hint_count = 0
                    hints = self.now_word['hints']
                    
                    for hint in hints:
                        if hint != "" and len(hint) > 0:
                            hint_count += 1
                    self.max_hint_count = hint_count
                    self.now_hint_count = hint_count
                    self.now_hint_idx = -1
                    del tmp_arr[idx]
                    self.is_set_candidate = True
                    print("[[ Set Candidates ]]:%s" % self.now_word.get('word'))


                if self.is_set_tiles == False:
                    # ui 구성
                    #self.set_tiles()
                    self.is_set_tiles = True                    
                    self.ready_animation_time = pygame.time.get_ticks()
                    print("[[ Set Tiles ]]")
                
                # 모든 처리가 완료되면 game state START로 변경
                if self.is_set_tiles and self.is_set_candidate:
                    #self.state = GAME_STATE_START
                    self.draw_ready = True        
                    # TODO: 해당 if문 주석 바꿔야할듯, 기존에는 state START로 설정했는데
                    # 현재는 ready 상태로 만드는 것으로 보임
                    # nodejs 서버에 연결되지 않으면 여기서 더이상 진행되지 않는 것으로 보임 
                    

            
            # ================================== START ==================================
            if self.state == GAME_STATE_START:
                # is_set_timer = False
                # 타이머 시작
                # 모든 처리가 완료되면 game state PLAYING으로 변경
                self.start_ticks = pygame.time.get_ticks()
                self.state = GAME_STATE_PLAYING
                print("[[ SET TIMER ]]")
                print("[[ Complete Start Process ]]")
               


            
            # ================================== PLAYING ==================================
            if self.state == GAME_STATE_PLAYING:
                # TODO: NPC 자동 이동
                pass           

            # ==========================================================================


            # ================================== OVER ==================================
            if self.state == GAME_STATE_OVER:
                #print("[[ GAME OVER ]]")
                #print("%s:[%s] / %s:[%s]" % (self.left_castle.name, self.left_castle.hp, self.right_castle.name, self.right_castle.hp))     
                
                # 정답 처리 => 정답자 스코어 증가 
                if self.is_update_rank == False:                    
                    if self.last_right_user != None:
                        print("[정답자] => %s" % self.last_right_user)
                        if self.last_right_user['user_id'] in self.rank:
                            update_rank = self.rank[self.last_right_user['user_id']]
                            update_rank['right_count'] += 1
                            update_rank['nickname'] = self.last_right_user['nickname']

                            now_time = time.time()
                            update_rank['right_update_time'] = now_time
                            
                            self.rank[update_rank['user_id']] = update_rank
                            self.update_rank(update_rank)
                        else:
                            new_rank = self.last_right_user
                            new_rank['right_count'] = 1

                            now_time = time.time()
                            print(now_time)

                            now_time = time.time()
                            new_rank['right_update_time'] = now_time

                            self.rank[new_rank['user_id']] = new_rank
                            self.update_rank(new_rank)

                        #self.last_right_user = None

                self.is_update_rank = True
                self.draw_result = True

                # 상태 확인을 위한 모든 전역 변수 확인 후 적절하게 초기화
                # 모든 작업 완료 후 game state READY로 변경
                if self.is_clear_game_data == False:
                    #self.sprite_group.empty()
                    self.is_end_ready_animation = False
                    self.is_set_candidate = False
                    self.is_set_tiles = False   
                    self.is_set_timer = False

                    self.is_clear_game_data = True
                    print("[Clear Game Data]")

                if self.is_end_over_animation and self.is_update_rank and self.is_clear_game_data:
                    self.is_end_over_animation = False
                    self.is_update_rank = False
                    self.is_clear_game_data = False
                    self.state = GAME_STATE_READY
                    print("[[ Complete Game Over Process ]]")


            # <화면 그리기>
            # 모든 Sprite update
            self.sprite_group.update(mt, self)         
            
            # 배경색
            self.SCREEN.fill(self.COLOR_PURPLE_LIGHT) 

            # 설명 UI
            desc_rect_x = SCREEN_WIDTH * 0.04
            desc_rect_y = desc_rect_x
            desc_rect_width = SCREEN_WIDTH * 0.43
            # desc_rect_fill = pygame.draw.rect(self.SCREEN, (255, 255, 228), [desc_rect_x+3, desc_rect_y+3, desc_rect_width-6, desc_rect_width * 0.6 - 6], 
            #                             border_radius=0, border_top_left_radius=5, border_top_right_radius=5, border_bottom_left_radius=5, border_bottom_right_radius=5)
            # desc_rect_border = pygame.draw.rect(self.SCREEN, (153, 56, 0), [desc_rect_x, desc_rect_y, desc_rect_width, desc_rect_width * 0.6], 
            #                             width=3, border_radius=0, border_top_left_radius=10, border_top_right_radius=10, border_bottom_left_radius=10, border_bottom_right_radius=10)

            # 채팅으로 정답을 맞혀보세요            
            # text_join_desc = self.main_font_30.render("채팅으로 정답을 맞혀보세요", True, self.COLOR_GREY_LIGHT)
            # text_join_desc_rect = text_join_desc.get_rect()
            # text_join_desc_rect.centerx = SCREEN_WIDTH / 2
            # self.SCREEN.blit(text_join_desc, (text_join_desc_rect.x, SCREEN_HEIGHT * 0.2))
           


            # 하단 배경
            chat_back_rect = pygame.draw.rect(self.SCREEN, self.COLOR_YELLOW_LEMON, [0, LAND_BOTTOM_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - LAND_BOTTOM_HEIGHT])

            # 힌트 설명 텍스트
            hint_desc_text = self.sebang_font_27_bold.render('장미 1개 = 1 힌트', True, self.COLOR_BROWN_DARK)
            hint_desc_text_rect = hint_desc_text.get_rect()
            hint_desc_text_rect.x = SCREEN_WIDTH * 0.10
            
            # 힌트 설명 테두리
            hint_desc_rect_border = pygame.draw.rect(self.SCREEN, self.COLOR_ORANGE_PEEL, 
                                        [hint_desc_text_rect.x - 30, (LAND_BOTTOM_HEIGHT + (SCREEN_HEIGHT * 0.03)) - (hint_desc_text_rect.size[1] * 0.2), hint_desc_text_rect.size[0] * 1.2, hint_desc_text_rect.size[1] * 1.4], 
                                        width=3, border_radius=0, border_top_left_radius=10, border_top_right_radius=10, border_bottom_left_radius=10, border_bottom_right_radius=10)

            self.SCREEN.blit(hint_desc_text, (hint_desc_text_rect.x - 10, LAND_BOTTOM_HEIGHT + (SCREEN_HEIGHT * 0.03)))



            # 보너스 타임에서 하트 목표치 출력
            # 보너스 시간 계산
            if self.bonus_time > 0:
                now_time = pygame.time.get_ticks()
                tmp_interval = now_time - self.bonus_start_time            
                #print("[진행된 보너스 시간]:%s"%(tmp_interval/1000))

                like_goal_text = self.sebang_font_18_bold.render('다음 힌트까지: %s/%s 좋아요'%(self.now_goal_like_cnt, self.goal_like_cnt), True, self.COLOR_WHITE)
                like_goal_text_rect = like_goal_text.get_rect()
                #like_goal_text_rect.x = SCREEN_WIDTH * 0.10
                                
                # 힌트 설명 테두리
                # like_goal_rect_border = pygame.draw.rect(self.SCREEN, self.COLOR_RED_LIGHT, 
                #                             [like_goal_text_rect.x - 30, (LAND_BOTTOM_HEIGHT + (SCREEN_HEIGHT * 0.09)) - (like_goal_text_rect.size[1] * 0.2), like_goal_text_rect.size[0] * 1.2, like_goal_text_rect.size[1] * 1.4], 
                #                             width=3, border_radius=0, border_top_left_radius=10, border_top_right_radius=10, border_bottom_left_radius=10, border_bottom_right_radius=10)

                # self.SCREEN.blit(like_goal_text, (like_goal_text_rect.x - 10, LAND_BOTTOM_HEIGHT + (SCREEN_HEIGHT * 0.09)))

                like_goal_text_rect.centerx =SCREEN_WIDTH / 2
                like_goal_rect_border = pygame.draw.rect(self.SCREEN, self.COLOR_RED_LIGHT, 
                                            [like_goal_text_rect.x - 30, SCREEN_HEIGHT * 0.15 - (like_goal_text_rect.size[1] * 0.32), like_goal_text_rect.size[0] * 1.2, like_goal_text_rect.size[1] * 1.8], 
                                            width=3, border_radius=0, border_top_left_radius=10, border_top_right_radius=10, border_bottom_left_radius=10, border_bottom_right_radius=10)

                self.SCREEN.blit(like_goal_text, (like_goal_text_rect.x - 10, SCREEN_HEIGHT * 0.15))
                
                if (tmp_interval/1000) >= self.bonus_time:
                    self.bonus_time = 0
                    self.bonus_start_time = 0
                    self.now_goal_like_cnt = 0
                    self.goal_like_cnt = 0                    
                    self.op_npc('보너스 시간이 종료되었습니다.', NPC_DOG_STATE_HURT, 'left', (0,0), 2)
                    print("보너스 시간 종료")
            

           
            # 랭킹 정보 출력            
            rank_x = (SCREEN_WIDTH * 0.6) - (SCREEN_WIDTH * 0.14)
            rank_y = (LAND_BOTTOM_HEIGHT + (SCREEN_HEIGHT * 0.03)) - (hint_desc_text_rect.size[1] * 0.2)
            #rank_y = hint_desc_rect_border.y     
            for idx, rank in enumerate(self.top_ranks):       

                if idx == 7:
                    break         
                
                rank_text_rect = None
                name = rank['nickname']
                
                if (idx == 0 or idx == 1) and len(name) > 9:
                    name = name[0:9] + '..'
                elif len(name) > 12:
                    name = name[0:12] + '..'

                name_str = "%s  %d Win"%(name, rank['right_count'])
                if idx == 0:
                    rank_text = self.sebang_font_22_bold.render("%dst"%(idx+1), True, self.COLOR_BROWN)
                    rank_text_rect = rank_text.get_rect()

                    rank_name_text = self.sebang_font_22_bold.render(name, True, self.COLOR_JELLY_BEAN_BLUE)
                    rank_name_text_rect = rank_name_text.get_rect()
                    rank_name_text_rect.x = rank_text_rect.x + 15

                    rank_count_text = self.sebang_font_20_bold.render("%d Win" %(rank['right_count']), True, self.COLOR_JELLY_BEAN_BLUE)
                    rank_count_text_rect = rank_count_text.get_rect()
                    rank_count_text_rect.x = rank_name_text_rect.x + 15

                    self.SCREEN.blit(rank_text, (rank_x, rank_y))
                    self.SCREEN.blit(rank_name_text, (rank_x + rank_text_rect.size[0] + 15, rank_y))
                    self.SCREEN.blit(rank_count_text, (rank_x + rank_text_rect.size[0] + 15 + rank_name_text_rect.size[0] + 10, rank_y + 5))
                elif idx == 1:
                    rank_text = self.sebang_font_18_bold.render("%dnd"%(idx+1), True, self.COLOR_GREEN_DEEP)
                    rank_text_rect = rank_text.get_rect()

                    rank_name_text = self.sebang_font_18_bold.render(name_str, True, self.COLOR_JELLY_BEAN_BLUE)
                    rank_name_text_rect = rank_name_text.get_rect()
                    rank_name_text_rect.x = rank_text_rect.x + 15

                    self.SCREEN.blit(rank_text, (rank_x, rank_y))
                    self.SCREEN.blit(rank_name_text, (rank_x + rank_text_rect.size[0] + 15, rank_y))
                elif idx == 2:
                    rank_text = self.sebang_font_18_bold.render("%drd"%(idx+1), True, self.COLOR_PURPLE)
                    rank_text_rect = rank_text.get_rect()

                    rank_name_text = self.sebang_font_18_bold.render(name_str, True, self.COLOR_JELLY_BEAN_BLUE)
                    rank_name_text_rect = rank_name_text.get_rect()
                    rank_name_text_rect.x = rank_text_rect.x + 15

                    self.SCREEN.blit(rank_text, (rank_x, rank_y))
                    self.SCREEN.blit(rank_name_text, (rank_x + rank_text_rect.size[0] + 15, rank_y))
                else:
                    rank_text = self.sebang_font_18_bold.render("%dth"%(idx+1), True, self.COLOR_JELLY_BEAN_BLUE)
                    rank_text_rect = rank_text.get_rect()
                    #rank_text_rect.x = SCREEN_WIDTH * 0.6

                    rank_name_text = self.sebang_font_18_bold.render(name_str, True, self.COLOR_JELLY_BEAN_BLUE)
                    rank_name_text_rect = rank_name_text.get_rect()
                    rank_name_text_rect.x = rank_text_rect.x + 15

                    self.SCREEN.blit(rank_text, (rank_x, rank_y))
                    self.SCREEN.blit(rank_name_text, (rank_x + rank_text_rect.size[0] + 15, rank_y))
                    
                rank_y += rank_text_rect.size[1] + (SCREEN_HEIGHT * 0.01)



            # ================================== READY ==================================
            if self.state == GAME_STATE_READY and self.draw_ready == True:
                
                now_ready_animation_time = pygame.time.get_ticks()                
                #animation_time = int((now_ready_animation_time - self.ready_animation_time) / 1000)
                animation_time = (now_ready_animation_time - self.ready_animation_time) / 1000

                #print("[now_ready_animation_time]: %s" % now_ready_animation_time)
                #print("[ready_animation_time]: %s" % self.ready_animation_time)

                self.ready_animation_term += now_ready_animation_time - self.ready_animation_before_time
                self.ready_animation_before_time = now_ready_animation_time                

                #print("[animation_term]: %s" % (self.ready_animation_term))
                

                # 랜덤 자음 출력하기
                random_len = len(self.now_word['word'])
                #self.random_consonant
                if self.ready_animation_term >= 100:
                    self.random_consonant = ""
                    self.ready_animation_term = 0
                    for i in range(0,random_len):
                        rand_idx = random.randint(0, len(self.consonant) - 1)
                        self.random_consonant += self.consonant[rand_idx]
                                    
                self.print_random_consonant()

                # TODO 중요: 랜덤 대기 시간이 2초 이상이고, 서버와의 연결이 정상적이었다면 으로 조건 변경 
                # 서버와의 연결이 지연 되었을 때 어떻게 처리되고 있는지 확인 필요
                # 아래의 코드에서 서버와의 상태를 확인하는 조건을 추가해야할 듯 
                #print("[animation_time]: %s" % (animation_time))
                if int(animation_time) >= 2 and self.is_ws_connected == True:
                    self.ready_animation_time = 0
                    #print("[[ ReSet Reday Animation Time 0 ]]")
                    self.state = GAME_STATE_START
                    #print("[[ Set State Start ]]")
                    #self.is_end_ready_animation = False
                    self.draw_ready = False
                    print("[[ Complete Ready Process ]]")


            # if self.state == GAME_STATE_OVER and self.draw_result == True:
            #     # 게임 결과 애니메이션 출력
            #     # TODO: sparkle
            #     now_over_animation_time = pygame.time.get_ticks()                
            #     animation_time = int((now_over_animation_time - self.over_animation_time) / 1000)
                
            #     if self.last_right_user != None:
            #         self.print_word_result()
                

            #     if animation_time == 2:
            #         self.is_end_over_animation = True
            #         self.over_animation_time = 0
            #         self.last_right_user = None
                    # self.draw_result = False
                



            # ================================== START ==================================
            if self.state == GAME_STATE_START:
                pass


            # ================================== PLAYING ==================================
            if self.state == GAME_STATE_PLAYING:
                
                # game play timer
                play_time_sec = int((pygame.time.get_ticks() - self.start_ticks) / 1000)                
                last_time = self.game_timer_term - play_time_sec
                min = int(last_time / 60)
                sec = int(last_time % 60)

                if min == 0 and sec == 0:
                    self.state = GAME_STATE_OVER
                    self.over_animation_time = pygame.time.get_ticks()

                min_str = "0%d"%min if min < 10 else "%d"%min
                sec_str = "0%d"%sec if sec < 10 else "%d"%sec
                timer_str = "%s : %s" % (min_str, sec_str)
                #print("남은 시간 %s" % timer_str)

                timer_text = self.sebang_font_30_bold.render(timer_str, True, self.COLOR_BLACK)
                timer_text_rect = timer_text.get_rect()
                timer_text_rect.centerx = int(SCREEN_WIDTH * 0.85)
                self.SCREEN.blit(timer_text, (timer_text_rect.x, SCREEN_HEIGHT * 0.1))


                # 힌트 출력 
                # 현재 워드의 힌트 리스트에서 현재 힌트 idx 위치에 사용 가능한 힌트가 있다면
                # <남은 힌트: a개>
                # coin 후원 받으면 힌트 출력
                # <힌트 있음> 아래에 힌트1. ㅁㅁㅁㅁㅁ 힌트2. ㅁㅁㅁㅁ 이런 형식으로 출력
                for idx, hint in enumerate(self.now_word['hints']):
                    if idx <= self.now_hint_idx and hint != "" and len(hint) > 0:
                        hint_text = self.main_font_20.render('힌트%d: %s'%(idx+1, hint), True, self.COLOR_GREY_LIGHT)
                        hint_text_rect = hint_text.get_rect()
                        hint_text_rect.centerx = int(SCREEN_WIDTH * 0.5)
                        self.SCREEN.blit(hint_text, (hint_text_rect.x, self.hint_height + (SCREEN_HEIGHT * 0.03 * idx)))
                    elif idx > self.now_hint_idx and hint != "" and len(hint) > 0:
                        blind_hint = "ㅁ" * len(hint)
                        hint_text = self.main_font_20.render('힌트%d: %s'%(idx+1, "ㅁㅁㅁㅁ"), True, self.COLOR_GREY_LIGHT)
                        hint_text_rect = hint_text.get_rect()
                        hint_text_rect.centerx = int(SCREEN_WIDTH * 0.5)
                        self.SCREEN.blit(hint_text, (hint_text_rect.x, self.hint_height + (SCREEN_HEIGHT * 0.03 * idx)))
                        

                self.now_hint_count = self.max_hint_count - (self.now_hint_idx + 1)
                hint_cnt_text = self.main_font_25.render('[ 남은 힌트: %d개 ]'%self.now_hint_count, True, self.COLOR_GREY_LIGHT)
                hint_cnt_text_rect = hint_cnt_text.get_rect()
                hint_cnt_text_rect.centerx = int(SCREEN_WIDTH * 0.5)
                #self.SCREEN.blit(hint_cnt_text, (hint_cnt_text_rect.x, SCREEN_HEIGHT * 0.36))
                self.SCREEN.blit(hint_cnt_text, (hint_cnt_text_rect.x, SCREEN_HEIGHT * 0.3))
                
                
                self.print_word_ui()


            # ================================== OVER ==================================            
            if self.state == GAME_STATE_OVER and self.draw_result == True:
                # 게임 결과 애니메이션 출력
                # TODO: sparkle
                now_over_animation_time = pygame.time.get_ticks()                
                animation_time = int((now_over_animation_time - self.over_animation_time) / 1000)
                
                if self.last_right_user != None:
                    self.print_word_result()                

                if animation_time == 2 or self.last_right_user == None:
                    self.is_end_over_animation = True
                    self.over_animation_time = 0
                    self.last_right_user = None
                    self.draw_result = False
                
            # 객체별로 필요한 백그라운드 그려주기
            # for sprite in self.sprite_group:
            #     sprite.draw_back()   

            # 모든 sprite 화면에 그려주기
            self.sprite_group.draw(self.SCREEN)   

            # 객체별로 필요한 그림 그려주기
            for sprite in self.sprite_group:
                sprite.draw(mt)        

            pygame.display.update()            


    async def game_event_loop(self, event_queue):        
        current_time = 0
        while True:
            #print('game_event_loop')
            last_time, current_time = current_time, time.time()
            await asyncio.sleep(1 / FPS - (current_time - last_time))
            event = pygame.event.poll()
            if event.type != pygame.NOEVENT:
                await event_queue.put(event)

    async def handle_events(self, event_queue):
        isLeft = True
        current_time = 0
        while True:
            last_time, current_time = current_time, time.time()
            await asyncio.sleep(10 / FPS - (current_time - last_time))
            event = await event_queue.get()
            if event.type == pygame.QUIT:                
                print("[[ 프로그램을 종료합니다. ]]")                                  
                # 오늘의 랭킹 정보 저장
                # user_rank_20221017.txt
                now = time.localtime()
                tody_str = time.strftime('%Y%m%d', now)                
                f = open("game/data/rank/user_rank_%s.txt" % tody_str, 'w', encoding='UTF-8')
                for rank in self.top_ranks:                        
                    f.write(json.dumps(rank, ensure_ascii=False) + '\n')
                f.close()
                break
            elif event.type == EVENT_SOCKET_MSG:
                #print("event", event)               
                msg_obj = None
                msg_obj = json.loads(event.message)
                #print("[[ Message Object ]]")                    
                #print(msg_obj)                
                
                if msg_obj != None:
                    if msg_obj['code'] == MSG_CODE_COMMENT and self.state == GAME_STATE_PLAYING:
                        # TODO: 프로필 캐시 없다면 저장
                        # 채팅에서 정답 확인
                        if msg_obj['comment'].find(self.now_word.get('word')) != -1:
                            # 정답을 맞혔다면
                            print("[%s] 정답!" % msg_obj['nickname'])
                            self.right_user_queue.append(msg_obj)
                            #self.state = GAME_STATE_OVER
                            self.over_animation_time = pygame.time.get_ticks()

                    elif msg_obj['code'] == MSG_CODE_LIKE and self.state == GAME_STATE_PLAYING:
                        #print("[%s] likes count: %d" %(msg_obj['nickname'], msg_obj['like_count']))
                        # TODO: 총 하트 수 저장
                        pass

                    elif msg_obj['code'] == MSG_CODE_DONATION:
                        print("[%s] dontaion: %d" %(msg_obj['nickname'], msg_obj['coin']))

                        # 1 <= donation <= 99   => 힌트
                        # 100 <= donation       => 패스

                        # TODO: 사용자의 user_id로 도네이션 총액 저장
                        user_id = msg_obj['user_id']

                        # must - 도네이션 애니메이션만 출력
                        self.donation_queue.append(msg_obj)

                        # 플레이 상태라면
                        if self.state == GAME_STATE_PLAYING:
                            # 도네이션 액수 확인
                            diamondCnt = msg_obj['coin']
                            if diamondCnt >= 1 and diamondCnt < 100:
                                # 힌트
                                pass                         
                            elif diamondCnt >= 100:
                                # 패스
                                pass
                    elif msg_obj['code'] == MSG_CODE_SHARE:
                        # TODO: 총 공유 수 저장
                        pass                    
                    elif msg_obj['code'] == MSG_CODE_QUIT:
                        #await event_queue.put(pygame.event.Q)
                        pass
                    
            else:
                pass
                #print("event", event)
        asyncio.get_event_loop().stop()

    async def reconnect_ws(self, event_queue):
        pass

    async def connect_to_server(self, event_queue): 
        print("[[ Cnnect to server ]]")
        target_ip = 'localhost'
        # , auto_reconnect=True, close_timeout=5
        while True:
            print("Connect to websocket server.")
            try:
                async with websockets.connect("ws://%s:30001" % target_ip, ping_interval=20) as websocket:
                    self.is_ws_connected = True
                    await websocket.send("Hi server. I'm client" );          
                    self.websocket = websocket
                    
                    current_time = 0            
                    while True:
                        print("check")
                        last_time, current_time = current_time, time.time()
                        await asyncio.sleep(1 / FPS - (current_time - last_time))                
                        now = datetime.datetime.now()
                        
                        try:
                            msg_rcv = await websocket.recv();
                            #print('\n\n[%s] %s' % (now, msg_rcv))
                            #new_event = pygame.event.Event(EVENT_SOCKET_MSG, message=msg_rcv)
                            #await event_queue.put(new_event) 
                            self.ws_msg_process(msg_rcv)  

                        except websockets.exceptions.ConnectionClosed:
                            self.is_ws_connected = False
                            print("Connection is closed. Reconnecting ...")
                            time.sleep(1) 
                            break
                        except Exception as e:
                            print(e)
            except Exception as e:
                self.is_ws_connected = False
                print("Connection is closed. Reconnecting ...")
                time.sleep(1)  
                

    def ws_msg_process(self, message):
        msg_obj = None
        msg_obj = json.loads(message)
        # print("[[ Message Object ]]")                    
        # print(msg_obj)                
        
        if msg_obj != None:
            if msg_obj['code'] == MSG_CODE_COMMENT and self.state == GAME_STATE_PLAYING:
                print("[%s]: %s" %(msg_obj['nickname'], msg_obj['comment']))
                self.total_msg_count += 1
                
                if self.total_msg_count % 1000 == 0:
                    now = datetime.datetime.now()
                    print("[%s][수신된 메시지 총 개수]:%d"%(now, self.total_msg_count))

                # TODO: 프로필 캐시 없다면 저장
                # 채팅에서 정답 확인
                if msg_obj['comment'].find(self.now_word.get('word')) != -1:
                    print("\n\n 정답!!! \n\n")
                    # 정답을 맞혔다면                    
                    self.right_user_queue.append(msg_obj)
                    #self.state = GAME_STATE_OVER
                    self.over_animation_time = pygame.time.get_ticks()
                    
            elif msg_obj['code'] == MSG_CODE_LIKE and self.state == GAME_STATE_PLAYING:
                print("[%s] likes count: %d" %(msg_obj['nickname'], msg_obj['like_count']))
                if self.bonus_time > 0:
                    self.now_goal_like_cnt += msg_obj['like_count']
                    
                    if self.now_goal_like_cnt >= self.goal_like_cnt:
                        # TODO: 목표치를 넘어섰으면 초기화
                        self.now_goal_like_cnt = 0
                        # 힌트 출력
                        if self.max_hint_count > (self.now_hint_idx + 1):
                            self.now_hint_idx += 1
                        # 소리 출력

            elif msg_obj['code'] == MSG_CODE_DONATION:
                print("[%s] dontaion: %d" %(msg_obj['nickname'], msg_obj['coin']))

                # 1 <= donation <= 99   => 힌트
                # 100 <= donation       => 패스

                # must - 도네이션 애니메이션만 출력
                self.donation_queue.append(msg_obj)


                # 플레이 상태라면
                if self.state == GAME_STATE_PLAYING:
                    # 도네이션 액수 확인
                    diamondCnt = msg_obj['coin']
                    if diamondCnt >= 100:
                        # 패스 - TODO: 현재는 힌트를 보여주는 것으로 되어있음..
                        if self.max_hint_count > (self.now_hint_idx + 1):
                            self.now_hint_idx += 1
                            #print("[now hint idx]:%d"%self.now_hint_idx)
                            self.op_npc('더 이상 힌트가 없어요..', NPC_DOG_STATE_HURT, 'left', (0,0), 3)
                        
                    elif diamondCnt >= 1 and diamondCnt < 100:
                        # 힌트
                        if self.max_hint_count > (self.now_hint_idx + 1):
                            self.now_hint_idx += 1
                            #print("[now hint idx]:%d"%self.now_hint_idx)
                        elif self.max_hint_count <= (self.now_hint_idx + 1):
                            self.op_npc('더 이상 힌트가 없어요..', NPC_DOG_STATE_HURT, 'left', (0,0), 3)
                        
                   
            elif msg_obj['code'] == MSG_CODE_SHARE:
                # TODO: 총 공유 수 저장
                pass                    
            
            elif msg_obj['code'] == MSG_CODE_QUIT:
                #await event_queue.put(pygame.event.Q)
                pass
            
            elif msg_obj['code'] == MSG_CODE_NOTICE:
                print(msg_obj)
                # self.npc_dog.state = int(msg_obj['motion_code'])
                # if msg_obj['msg'] != None and len(msg_obj['msg']) > 0:
                #     self.npc_dog.chat = msg_obj['msg']                
                # self.npc_dog.now_movement = (int(msg_obj['movement']), 0)
                # self.npc_dog.direction = msg_obj['direction']
                # self.npc_dog.motion_time = int(msg_obj['motion_time'])
                self.op_npc(msg_obj['msg'], int(msg_obj['motion_code']), msg_obj['direction'], (int(msg_obj['movement']), 0), int(msg_obj['motion_time']))

            
            elif msg_obj['code'] == MSG_CODE_BONUS:                
                self.start_bonus_time(msg_obj['time'], int(msg_obj['goal_like_cnt']))
                
                
                

    async def send_word_to_server(self):
        # send message for http
        current_time = 0       
        while True:
            last_time, current_time = current_time, time.time()
            await asyncio.sleep(1 / FPS - (current_time - last_time))          
            if self.send_word != None:
                URL = "http://localhost:30001/set_word?word=%s"%self.send_word
                response = requests.get(URL)
                #print("[SEND WORD TO SERVER][%s] - [%s]" % (response.status_code, response.text))    
                self.send_word = None
                

    def run(self):
        loop = asyncio.get_event_loop()
        event_queue = asyncio.Queue()

        pygame_task = asyncio.ensure_future(self.game_event_loop(event_queue))
        animation_task = asyncio.ensure_future(self.animation())
        event_task = asyncio.ensure_future(self.handle_events(event_queue))
        socket_task = asyncio.ensure_future(self.connect_to_server(event_queue))
        print_right_user_task = asyncio.ensure_future(self.print_user())
        donation_task = asyncio.ensure_future(self.print_donation())
        send_word_task = asyncio.ensure_future(self.send_word_to_server())
        
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(e)
            print(e.args)
            #raise e
        finally:
            pygame_task.cancel()
            animation_task.cancel()
            event_task.cancel()
            socket_task.cancel()
            donation_task.cancel()
            print_right_user_task.cancel()
            send_word_task.cancel()
        pygame.quit()


    # TODO: npc 조종 함수
    def op_npc(self, msg, motion_code, direction, movement, motion_time):
        self.npc_dog.state = int(motion_code)
        if msg != None and len(msg) > 0:
            self.npc_dog.chat = msg
        self.npc_dog.now_movement = movement
        self.npc_dog.direction = direction
        self.npc_dog.motion_time = motion_time

    # 보너스 타임 시작
    def start_bonus_time(self, time, goal):
        self.bonus_start_time = pygame.time.get_ticks()
        self.bonus_time = time
        self.goal_like_cnt = goal
        self.now_goal_like_cnt = 0        
        #self.sound_map['bonus_time_tts'].play()
        self.op_npc('지금부터 %s분간 하트로 힌트를 사용할 수 있습니다.'%int(time/60), NPC_DOG_STATE_RUN, 'left', (-6,0), 5)


    def update_rank(self, user):
        print("[update_rank]")
        print(user)
        # 랭킹 체크        
        for idx, rank in enumerate(self.top_ranks):
            if rank['user_id'] == user['user_id']:
                self.top_ranks[idx] = user
                self.sort_rank()
                self.print_rank()
                return

        self.top_ranks.append(user)
        self.sort_rank()        
        self.print_rank()
            
        
    def sort_rank(self):        
        self.top_ranks.sort(key = lambda object : (object['right_count'], object['right_update_time']), reverse=True)

        if len(self.top_ranks) > 10:
            self.top_ranks = self.top_ranks[0:10]

    def print_rank(self):
        print("[[ RANK ]] ====================")
        for idx, rank in enumerate(self.top_ranks):
            print("[Top %d] %s => %s" % (idx+1, rank['nickname'], rank['right_count']))
        print("===============================")

    async def print_donation(self):        
        current_time = 0       
        while True:
            last_time, current_time = current_time, time.time()
            await asyncio.sleep(1 / FPS - (current_time - last_time))          
            
            if len(self.donation_queue) > 0 and len(self.right_user_queue) <= 0 and self.print_user_state == True:

                self.print_user_state = False

                try:                
                    # # get image from url and set stream file
                    # image_str = urlopen(donation_obj['profile_img']).read()
                    # image_file = io.BytesIO(image_str) 
                    # image = pygame.image.load(image_file)
                    # image = pygame.image.load(image_file)                    

                    donation_obj = self.donation_queue[0]
                    #print(donation_obj)
                    user_id = donation_obj['user_id']
                    
                    #print("[user_id]:%s" % user_id)

                    cache_path = "game/res/cache/profile/%s.png" % user_id

                    # 캐시 파일 존재 확인
                    is_file = os.path.isfile(cache_path)
                    
                    image = None
                    if is_file:
                        image = pygame.transform.scale(pygame.image.load(cache_path), self.donation_size)
                    else:

                        try:
                            image_str = urlopen(donation_obj['profile_img']).read()
                            # use PIL
                            pil_img = Image.open(io.BytesIO(image_str))
                            
                            height,width = pil_img.size
                            lum_img = Image.new('L', [height,width] , 0)
                            
                            draw = ImageDraw.Draw(lum_img)
                            draw.pieslice([(0,0), (height - 3, width - 3)], 0, 360, 
                                        fill = 255, outline = "white")
                            img_arr =np.array(pil_img)
                            lum_img_arr =np.array(lum_img)                    
                            final_img_arr = np.dstack((img_arr,lum_img_arr))                        

                            final_pil_img = Image.fromarray(final_img_arr)

                            # 캐시 파일 저장
                            final_pil_img.save(cache_path, 'png')
                            image = pygame.transform.scale(pygame.image.load(cache_path), self.donation_size)
                        except:
                            image = pygame.transform.scale(pygame.image.load('game/res/default.png'), self.right_profile_size)

                    tmps = []
                    tmps.append(image)                    
                    new_donation = ui.DonationSprite(size=self.donation_size, position=((SCREEN_WIDTH * 0.5) - (self.donation_size[0] * 0.5), SCREEN_HEIGHT * 0.52), group='donation', 
                                                    name=donation_obj['nickname'], coin=donation_obj['coin'], images=tmps, sound=self.sound_map['donation'], game=self)
                    self.ui_group.add(new_donation)
                    self.sprite_group.add(new_donation)
                    
                    self.npc_dog.state = int(NPC_DOG_STATE_JUMP)
                    self.npc_dog.now_movement = (0, 0)
                    self.npc_dog.motion_time = 3

                    del self.donation_queue[0]
                except Exception as e:
                    print("[print donation error]:%s" % e)
                    del self.donation_queue[0]

    async def print_user(self):        
        current_time = 0       
        while True:
            #print("print_user whilte true")
            last_time, current_time = current_time, time.time()
            await asyncio.sleep(1 / FPS - (current_time - last_time))          
            
            if len(self.right_user_queue) > 0 and self.print_user_state == True:

                self.print_user_state = False

                try:                
                    # # get image from url and set stream file
                    # image_str = urlopen(donation_obj['profile_img']).read()
                    # image_file = io.BytesIO(image_str) 
                    # image = pygame.image.load(image_file)
                    # image = pygame.image.load(image_file)                    

                    print("[print_user]")
                    right_user_obj = self.right_user_queue[0]
                    #print(donation_obj)
                    user_id = right_user_obj['user_id']
                    
                    print("[user_id]:%s" % user_id)

                    cache_path = "game/res/cache/profile/%s.png" % user_id

                    # 캐시 파일 존재 확인
                    is_file = os.path.isfile(cache_path)
                    
                    image = None
                    if is_file:
                        image = pygame.transform.scale(pygame.image.load(cache_path), self.right_profile_size)
                    else:
                        
                        try:
                            image_str = urlopen(right_user_obj['profile_img']).read()
                            print("[Download image]")
                            # use PIL
                            pil_img = Image.open(io.BytesIO(image_str))
                            print("[Image to pilImage]")
                            
                            print("[Start crope image]")
                            height,width = pil_img.size
                            lum_img = Image.new('L', [height,width] , 0)
                            
                            draw = ImageDraw.Draw(lum_img)
                            draw.pieslice([(0,0), (height - 3, width - 3)], 0, 360, 
                                        fill = 255, outline = "white")
                            img_arr =np.array(pil_img)
                            lum_img_arr =np.array(lum_img)                    
                            final_img_arr = np.dstack((img_arr,lum_img_arr))                        

                            final_pil_img = Image.fromarray(final_img_arr)

                            print("[End crope image]")

                            # 캐시 파일 저장
                            final_pil_img.save(cache_path, 'png')
                            image = pygame.transform.scale(pygame.image.load(cache_path), self.right_profile_size)
                        except:
                            image = pygame.transform.scale(pygame.image.load('game/res/default.png'), self.right_profile_size)

                    print("[Getted cropped image]")

                    tmps = []
                    tmps.append(image)                    
                    new_right_user = ui.UserProfileSprite(size=self.donation_size, position=((SCREEN_WIDTH * 0.5) - (self.right_profile_size[0] * 0.5), SCREEN_HEIGHT * 0.52), group='donation', 
                                                    name=right_user_obj['nickname'], msg="WINNER", images=tmps, sound=self.sound_map['stage_clear'], game=self)                    
                    self.ui_group.add(new_right_user)                    
                    self.sprite_group.add(new_right_user)
                    self.last_right_user = self.right_user_queue[0]         

                    print("[%s] 정답!" % right_user_obj['nickname'])
                    self.npc_dog.chat = "%s님이 정답을 맞혔어요!"%right_user_obj['nickname']
                    self.npc_dog.state = int(NPC_DOG_STATE_JUMP)
                    self.npc_dog.now_movement = (0, 0)
                    self.npc_dog.motion_time = 3

                    del self.right_user_queue[0]                 
                    self.right_user_queue.clear()
                    self.state = GAME_STATE_OVER 
                except Exception as e:
                    print("[print user error]:%s" % e)
                    del self.right_user_queue[0]

    def print_random_consonant(self):
        
        # 현재 단어의 글자 수를 토대로 만든다.        
        word_len = len(self.now_word.get('word'))
        word_size = (SCREEN_WIDTH * 0.12, SCREEN_WIDTH * 0.15)
        term_width = word_size[0] * 0.3
        front_empty_width = (SCREEN_WIDTH - (word_len * word_size[0]) - (term_width * (word_len - 1))) / 2
        
        space_x = front_empty_width
        space_y = SCREEN_HEIGHT * 0.2 # + ((SCREEN_WIDTH / 4) * 0.15)
        for idx in range(0, word_len):     
            now_rect = pygame.draw.rect(self.SCREEN, (213, 213, 213), [space_x, space_y, word_size[0], word_size[1]], border_radius=15)

            word_text = self.main_font_40.render(self.random_consonant[idx], True, self.COLOR_BLACK)            
            word_text_rect = word_text.get_rect()        
            name_text_size = word_text_rect.size
            word_text_rect.centerx = now_rect.centerx
            word_text_rect.centery = now_rect.centery
            self.SCREEN.blit(word_text, (word_text_rect.x, word_text_rect.y))            

            space_x += word_size[0] + term_width


    def print_word_ui(self):
        #print("[print_word_ui]")
        #print("[%s] = > %d" % (self.now_word.get('word'), len(self.now_word.get('word'))))
        
        # 현재 단어의 글자 수를 토대로 만든다.        
        word_len = len(self.now_word.get('word'))
        word_size = (SCREEN_WIDTH * 0.12, SCREEN_WIDTH * 0.15)
        term_width = word_size[0] * 0.3
        front_empty_width = (SCREEN_WIDTH - (word_len * word_size[0]) - (term_width * (word_len - 1))) / 2
        
        space_x = front_empty_width
        #space_y = SCREEN_HEIGHT * 0.26 # + ((SCREEN_WIDTH / 4) * 0.15)
        space_y = SCREEN_HEIGHT * 0.2 # + ((SCREEN_WIDTH / 4) * 0.15)
        for idx in range(0, word_len):     
            #pygame.draw.rect(self.SCREEN, self.COLOR_GREY_LIGHT, [space_x, space_y, word_size[0], word_size[1]])
            now_rect = pygame.draw.rect(self.SCREEN, (213, 213, 213), [space_x, space_y, word_size[0], word_size[1]], border_radius=15)

            word_text = self.main_font_40.render(self.now_word['consonant'][idx], True, self.COLOR_BLACK)            
            word_text_rect = word_text.get_rect()        
            name_text_size = word_text_rect.size
            word_text_rect.centerx = now_rect.centerx
            word_text_rect.centery = now_rect.centery
            self.SCREEN.blit(word_text, (word_text_rect.x, word_text_rect.y))            

            space_x += word_size[0] + term_width


    def print_word_result(self):
        word_len = len(self.now_word.get('word'))
        word_size = (SCREEN_WIDTH * 0.12, SCREEN_WIDTH * 0.15)
        term_width = word_size[0] * 0.3
        front_empty_width = (SCREEN_WIDTH - (word_len * word_size[0]) - (term_width * (word_len - 1))) / 2
        
        space_x = front_empty_width
        space_y = SCREEN_HEIGHT * 0.2 # + ((SCREEN_WIDTH / 4) * 0.15)
        for idx in range(0, word_len):        
            now_rect = pygame.draw.rect(self.SCREEN, (213, 213, 213), [space_x, space_y, word_size[0], word_size[1]], border_radius=15)

            word_text = self.main_font_40.render(self.now_word['word'][idx], True, self.COLOR_BLACK)            
            word_text_rect = word_text.get_rect()        
            name_text_size = word_text_rect.size
            word_text_rect.centerx = now_rect.centerx
            word_text_rect.centery = now_rect.centery
            self.SCREEN.blit(word_text, (word_text_rect.x, word_text_rect.y))            

            space_x += word_size[0] + term_width


            

if __name__ == '__main__':
    game = Game()
    game.run()
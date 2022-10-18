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
from game.code import *
from urllib.request import urlopen
from PIL import Image, ImageDraw
import numpy as np
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
        self.COLOR_BLUE_LIGHT = (103, 153, 255)
        self.COLOR_BLUE_DEEP = (1, 0, 255)
        self.COLOR_BLUE_DARK = (0, 34, 102)
        self.COLOR_GREEN_LIGHT = (183, 240, 177)
        self.COLOR_GREEN_DEEP = (47, 157, 39)
        self.COLOR_PURPLE = (95, 0, 255)
        self.COLOR_RED_LIGHT = (255, 167, 167)
        self.COLOR_GREY_LIGHT = (213, 213, 213)
        
        self.main_font_60 = pygame.font.Font("game/res/font/NanumBarunGothicBold.ttf", 60)
        self.main_font_30 = pygame.font.Font("game/res/font/NanumBarunGothicBold.ttf", 30)   
        self.main_font_20 = pygame.font.Font("game/res/font/NanumBarunGothicBold.ttf", 20) 
        self.main_font_15 = pygame.font.Font("game/res/font/NanumBarunGothicBold.ttf", 15) 
        self.main_font_11 = pygame.font.Font("game/res/font/NanumBarunGothicBold.ttf", 11) 

        self.sebang_font_30_bold = pygame.font.Font("game/res/font/SEBANGGothicBold.ttf", 30) 
        self.sebang_font_25_bold = pygame.font.Font("game/res/font/SEBANGGothicBold.ttf", 25)
        self.sebang_font_22_bold = pygame.font.Font("game/res/font/SEBANGGothicBold.ttf", 22) 
        self.sebang_font_20_bold = pygame.font.Font("game/res/font/SEBANGGothicBold.ttf", 20) 
        self.sebang_font_18_bold = pygame.font.Font("game/res/font/SEBANGGothicBold.ttf", 18) 
        self.sebang_font_15_bold = pygame.font.Font("game/res/font/SEBANGGothicBold.ttf", 15) 
        self.sebang_font_30 = pygame.font.Font("game/res/font/SEBANGGothic.ttf", 30)
        
        self.sebang_font_20 = pygame.font.Font("game/res/font/SEBANGGothic.ttf", 20) 
        self.sebang_font_15 = pygame.font.Font("game/res/font/SEBANGGothic.ttf", 15)  
        self.sebang_font_11 = pygame.font.Font("game/res/font/SEBANGGothic.ttf", 11) 
        
        #text = main_font.render("Test Text", True, COLOR_BLACK)     # 문자열, antialias, 글자색

        self.message_queue = []     # 웹소켓 전송 메시지큐
        self.donation_queue = []    # 도네이션 큐
        self.right_user_queue = []  # 정답자 큐

        ### 시간 관련 변수 ###
        self.npc_move_term = 500 # NPC 자동 움직임 시간 간격
        self.game_timer_term = 60 * 2    # 게임 플레이 제한 시간 - 240초 => 4분

        # sprite group 설정
        self.sprite_group = pygame.sprite.Group()
        self.tile_group = pygame.sprite.Group()
        self.ui_group = pygame.sprite.Group()

        self.tile_size = (50, 50)
        self.donation_size = (SCREEN_WIDTH / 7, SCREEN_WIDTH / 7)
        self.right_profile_size = (SCREEN_WIDTH / 6, SCREEN_WIDTH / 6)
        self.npc_size = (60, 60)


        # 리소스 불러오기
        

        # 효과음 로드
        self.sound_map = import_sound()


        
        # 게임 플레이 변수
        self.websocket = None
        self.is_ws_connected = False

        self.ready_animation_time = 0   # ready animation 시작 시간
        self.ready_animation_before_time = 0    # 이전 시간 
        self.ready_animation_term = 0   # 시작부터 변경된 누적 시간 - 일정 간격으로 초기화
        self.over_animation_time = 0


        self.consonant = ['ㄱ','ㄴ','ㄷ','ㄹ','ㅁ','ㅂ','ㅅ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']
        self.random_consonant = None
        
        self.coin_map = {}
        self.like_map = {}
        self.share_map = {}

        self.top_ranks = []

        self.now_word = None
        self.send_word = None
        self.now_hint_idx = 0
        self.last_right_user = None

        self.draw_ready = False
        self.draw_result = False
        self.print_user_state = True        
        self.state = GAME_STATE_READY

        self.total_msg_count = 0
       

        self.candidates = []
        
        # word 로드
        self.load_word_data("game/data/words.txt")   
        self.load_word_data("game/data/words_entertainment.txt")   
        self.load_word_data("game/data/words_animal.txt")   
        self.load_word_data("game/data/words_food.txt")    


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
            #print("[[ DATA LOAD ]] word:[%s]"%obj)
            self.candidates.append(obj)
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
                    
                    # 서버에 단어 전송
                    # json_obj = {
                    #     "code": MSG_CODE_SET_WORD,
                    #     "word": self.now_word['word'],
                    # }
                    # json_str = json.dumps(json_obj, ensure_ascii=False)
                    # self.message_queue.append(json_str)
                    self.send_word = self.now_word['word']

                    self.now_hint_idx = 0
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
                            self.rank[update_rank['user_id']] = update_rank
                            self.update_rank(update_rank)
                        else:
                            new_rank = self.last_right_user
                            new_rank['right_count'] = 1
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
            self.SCREEN.fill(self.COLOR_BLUE) 

            # 설명 UI
            desc_rect_x = SCREEN_WIDTH * 0.04
            desc_rect_y = desc_rect_x
            desc_rect_width = SCREEN_WIDTH * 0.43
            # desc_rect_fill = pygame.draw.rect(self.SCREEN, (255, 255, 228), [desc_rect_x+3, desc_rect_y+3, desc_rect_width-6, desc_rect_width * 0.6 - 6], 
            #                             border_radius=0, border_top_left_radius=5, border_top_right_radius=5, border_bottom_left_radius=5, border_bottom_right_radius=5)
            # desc_rect_border = pygame.draw.rect(self.SCREEN, (153, 56, 0), [desc_rect_x, desc_rect_y, desc_rect_width, desc_rect_width * 0.6], 
            #                             width=3, border_radius=0, border_top_left_radius=10, border_top_right_radius=10, border_bottom_left_radius=10, border_bottom_right_radius=10)

            # 채팅으로 정답을 맞혀보세요            
            text_join_desc = self.main_font_30.render("채팅으로 정답을 맞혀보세요", True, self.COLOR_GREY_LIGHT)
            text_join_desc_rect = text_join_desc.get_rect()
            text_join_desc_rect.centerx = SCREEN_WIDTH / 2
            self.SCREEN.blit(text_join_desc, (text_join_desc_rect.x, SCREEN_HEIGHT * 0.2))
           


            # 하단 배경
            chat_back_rect = pygame.draw.rect(self.SCREEN, self.COLOR_BLUE_DARK, [0, LAND_BOTTOM_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - LAND_BOTTOM_HEIGHT])

            # 힌트 설명 텍스트
            hint_desc_text = self.sebang_font_30_bold.render('1 Coin = 1 Hint', True, self.COLOR_WHITE)
            hint_desc_text_rect = hint_desc_text.get_rect()
            hint_desc_text_rect.x = SCREEN_WIDTH * 0.08
            
            # 힌트 설명 테두리
            # hint_desc_rect_border = pygame.draw.rect(self.SCREEN, self.COLOR_YELLOW, 
            #                             [hint_desc_text_rect.x - 20, (LAND_BOTTOM_HEIGHT + (SCREEN_HEIGHT * 0.03)) - (hint_desc_text_rect.size[1] * 0.2), hint_desc_text_rect.size[0] * 1.2, hint_desc_text_rect.size[1] * 1.4], 
            #                             width=3, border_radius=0, border_top_left_radius=10, border_top_right_radius=10, border_bottom_left_radius=10, border_bottom_right_radius=10)

            # self.SCREEN.blit(hint_desc_text, (hint_desc_text_rect.x, LAND_BOTTOM_HEIGHT + (SCREEN_HEIGHT * 0.03)))
           
            # 랭킹 정보 출력            
            rank_x = (SCREEN_WIDTH * 0.6) - (SCREEN_WIDTH * 0.15)
            rank_y = (LAND_BOTTOM_HEIGHT + (SCREEN_HEIGHT * 0.03)) - (hint_desc_text_rect.size[1] * 0.2)
            #rank_y = hint_desc_rect_border.y     
            for idx, rank in enumerate(self.top_ranks):       

                if idx == 7:
                    break         
                
                rank_text_rect = None
                name = rank['nickname']
                if len(name) > 12:
                    name = name[0:12] + '..'
                name_str = "%s  %d Win"%(name, rank['right_count'])
                if idx == 0:
                    rank_text = self.sebang_font_22_bold.render("%dst"%(idx+1), True, self.COLOR_YELLOW)
                    rank_text_rect = rank_text.get_rect()

                    rank_name_text = self.sebang_font_22_bold.render(name, True, self.COLOR_WHITE)
                    rank_name_text_rect = rank_name_text.get_rect()
                    rank_name_text_rect.x = rank_text_rect.x + 15

                    rank_count_text = self.sebang_font_20_bold.render("%d Win" %(rank['right_count']), True, self.COLOR_WHITE)
                    rank_count_text_rect = rank_count_text.get_rect()
                    rank_count_text_rect.x = rank_name_text_rect.x + 15

                    self.SCREEN.blit(rank_text, (rank_x, rank_y))
                    self.SCREEN.blit(rank_name_text, (rank_x + rank_text_rect.size[0] + 15, rank_y))
                    self.SCREEN.blit(rank_count_text, (rank_x + rank_text_rect.size[0] + 15 + rank_name_text_rect.size[0] + 10, rank_y + 5))
                elif idx == 1:
                    rank_text = self.sebang_font_18_bold.render("%dnd"%(idx+1), True, self.COLOR_GREEN_DEEP)
                    rank_text_rect = rank_text.get_rect()

                    rank_name_text = self.sebang_font_18_bold.render(name_str, True, self.COLOR_WHITE)
                    rank_name_text_rect = rank_name_text.get_rect()
                    rank_name_text_rect.x = rank_text_rect.x + 15

                    self.SCREEN.blit(rank_text, (rank_x, rank_y))
                    self.SCREEN.blit(rank_name_text, (rank_x + rank_text_rect.size[0] + 15, rank_y))
                elif idx == 2:
                    rank_text = self.sebang_font_18_bold.render("%drd"%(idx+1), True, self.COLOR_PURPLE)
                    rank_text_rect = rank_text.get_rect()

                    rank_name_text = self.sebang_font_18_bold.render(name_str, True, self.COLOR_WHITE)
                    rank_name_text_rect = rank_name_text.get_rect()
                    rank_name_text_rect.x = rank_text_rect.x + 15

                    self.SCREEN.blit(rank_text, (rank_x, rank_y))
                    self.SCREEN.blit(rank_name_text, (rank_x + rank_text_rect.size[0] + 15, rank_y))
                else:
                    rank_text = self.sebang_font_18_bold.render("%dth"%(idx+1), True, self.COLOR_WHITE)
                    rank_text_rect = rank_text.get_rect()
                    #rank_text_rect.x = SCREEN_WIDTH * 0.6

                    rank_name_text = self.sebang_font_18_bold.render(name_str, True, self.COLOR_WHITE)
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
                

                # TODO: 
                random_len = len(self.now_word['word'])
                #self.random_consonant
                if self.ready_animation_term >= 100:
                    self.random_consonant = ""
                    #print("hhh~!")
                    self.ready_animation_term = 0
                    # TODO: random
                    #tmp_arr = list(range(len(self.candidates)))
                    for i in range(0,random_len):
                        rand_idx = random.randint(0, len(self.consonant) - 1)
                        self.random_consonant += self.consonant[rand_idx]
                                    
                self.print_random_word()
                
                if int(animation_time) == 2:
                    self.ready_animation_time = 0
                    self.state = GAME_STATE_START
                    #self.is_end_ready_animation = False
                    self.draw_ready = False


            if self.state == GAME_STATE_OVER and self.draw_result == True:
                # 게임 결과 애니메이션 출력
                # TODO: sparkle
                now_over_animation_time = pygame.time.get_ticks()                
                animation_time = int((now_over_animation_time - self.over_animation_time) / 1000)
                
                if self.last_right_user != None:
                    self.print_word_result()
                

                if animation_time == 2:
                    self.is_end_over_animation = True
                    self.over_animation_time = 0
                    self.last_right_user = None
                    self.draw_result = False
                



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
                timer_text_rect.centerx = SCREEN_WIDTH * 0.5
                self.SCREEN.blit(timer_text, (timer_text_rect.x, SCREEN_HEIGHT * 0.45))


                # TODO: 힌트 출력 
                # 현재 워드의 힌트 리스트에서 현재 힌트 idx 위치에 사용 가능한 힌트가 있다면
                # <힌트 있음>
                # 없다면 <힌트 없음> 표시
                # coin 후원 받으면 힌트 출력
                # <힌트 있음> 아래에 힌트1. ㅁㅁㅁㅁㅁ 힌트2. ㅁㅁㅁㅁ 이런 형식으로 출력
                
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
            for sprite in self.sprite_group:
                sprite.draw_back()   

            # 모든 sprite 화면에 그려주기
            self.sprite_group.draw(self.SCREEN)      

            # 객체별로 필요한 그림 그려주기
            for sprite in self.sprite_group:
                sprite.draw()        
            
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
                            if diamondCnt >= 1 and diamondCnt < 5:
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
        async with websockets.connect("ws://%s:30001" % target_ip, ping_interval=None) as websocket:
            self.is_ws_connected = True
            await websocket.send("Hi server. I'm client" );          
            self.websocket = websocket
            
            current_time = 0            
            while True:
                #print("check")
                last_time, current_time = current_time, time.time()
                await asyncio.sleep(1 / FPS - (current_time - last_time))                
                now = datetime.datetime.now()
                
                try:
                    msg_rcv = await websocket.recv();
                    #print('\n\n[%s] %s' % (now, msg_rcv))
                    #new_event = pygame.event.Event(EVENT_SOCKET_MSG, message=msg_rcv)
                    #await event_queue.put(new_event) 
                    self.ws_msg_process(msg_rcv)  
                    
                except Exception as e:
                    print(e)

    def ws_msg_process(self, message):
        msg_obj = None
        msg_obj = json.loads(message)
        #print("[[ Message Object ]]")                    
        #print(msg_obj)                
        
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
                    # 정답을 맞혔다면
                    print("[%s] 정답!" % msg_obj['nickname'])
                    self.right_user_queue.append(msg_obj)
                    #self.state = GAME_STATE_OVER
                    self.over_animation_time = pygame.time.get_ticks()

            elif msg_obj['code'] == MSG_CODE_LIKE and self.state == GAME_STATE_PLAYING:
                print("[%s] likes count: %d" %(msg_obj['nickname'], msg_obj['like_count']))
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
                    if diamondCnt >= 1 and diamondCnt < 5:
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

    async def send_word_to_server(self):
        # send message for http
        current_time = 0       
        while True:
            last_time, current_time = current_time, time.time()
            await asyncio.sleep(1 / FPS - (current_time - last_time))          
            if self.send_word != None:
                URL = "http://localhost:30001/set_word?word=%s"%self.send_word
                response = requests.get(URL)
                #print("[%s] - [%s]" % (response.status_code, response.text))    
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


    def update_rank(self, user):
        # 랭킹 체크
        print("[update_rank]")
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
        self.top_ranks.sort(key = lambda object : object['right_count'], reverse=True)
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
            
            if len(self.donation_queue) > 0 and self.print_user_state == True:

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
                        image_str = urlopen(donation_obj['profile_img']).read()
                        # use PIL
                        pil_img = Image.open(io.BytesIO(image_str))
                        
                        height,width = pil_img.size
                        lum_img = Image.new('L', [height,width] , 0)
                        
                        draw = ImageDraw.Draw(lum_img)
                        draw.pieslice([(0,0), (height,width)], 0, 360, 
                                    fill = 255, outline = "white")
                        img_arr =np.array(pil_img)
                        lum_img_arr =np.array(lum_img)                    
                        final_img_arr = np.dstack((img_arr,lum_img_arr))                        

                        final_pil_img = Image.fromarray(final_img_arr)

                        # 캐시 파일 저장
                        final_pil_img.save(cache_path, 'png')
                        image = pygame.transform.scale(pygame.image.load(cache_path), self.donation_size)

                    tmps = []
                    tmps.append(image)                    
                    new_donation = ui.DonationSprite(size=self.donation_size, position=((SCREEN_WIDTH * 0.5) - (self.donation_size[0] * 0.5), SCREEN_HEIGHT * 0.52), group='donation', 
                                                    name=donation_obj['nickname'], coin=donation_obj['coin'], images=tmps, sound=self.sound_map['donation'], game=self)
                    self.ui_group.add(new_donation)
                    self.sprite_group.add(new_donation)
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
                            draw.pieslice([(0,0), (height,width)], 0, 360, 
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
                            image = pygame.transform.scale(pygame.image.load('game/res/cache/profile/default.png'), self.right_profile_size)
                            pass

                    print("[Getted cropped image]")

                    tmps = []
                    tmps.append(image)                    
                    new_right_user = ui.UserProfileSprite(size=self.donation_size, position=((SCREEN_WIDTH * 0.5) - (self.right_profile_size[0] * 0.5), SCREEN_HEIGHT * 0.52), group='donation', 
                                                    name=right_user_obj['nickname'], msg="WINNER", images=tmps, sound=self.sound_map['stage_clear'], game=self)                    
                    self.ui_group.add(new_right_user)                    
                    self.sprite_group.add(new_right_user)
                    self.last_right_user = self.right_user_queue[0]                                     
                    del self.right_user_queue[0]                 
                    self.right_user_queue.clear()
                    print("[right_user_queue len]: %d" % len(self.right_user_queue))
                    self.state = GAME_STATE_OVER 
                except Exception as e:
                    print("[print user error]:%s" % e)
                    del self.right_user_queue[0]

    
    # def spawn_npc(self, group):
    #     if group == 'right':
    #         new_soldier = characters.SoldierSprite(size=self.soldier_size, position=RIGHT_SPAWN_POSITION, movement=(-1,0), state=1, group=group, 
    #                                             hp=100, power=1, name='%s_soldier'%group, images=soldier_images_right, game=self)
    #         self.right_group.add(new_soldier)
    #         self.sprite_group.add(new_soldier)
    #     elif group == 'left':
    #         new_soldier = characters.SoldierSprite(size=self.soldier_size, position=LEFT_SPAWN_POSITION, movement=(1,0), state=1, group=group, 
    #                                         hp=100, power=1, name='%s_soldier'%group, images=soldier_images_left, game=self)
    #         self.left_group.add(new_soldier)
    #         self.sprite_group.add(new_soldier)

    def print_random_word(self):
        #print("[print_random_word]")
        #print("[%s] = > %d" % (self.now_word.get('word'), len(self.now_word.get('word'))))
        
        # 현재 단어의 글자 수를 토대로 만든다.        
        word_len = len(self.now_word.get('word'))
        word_size = (SCREEN_WIDTH * 0.12, SCREEN_WIDTH * 0.15)
        term_width = word_size[0] * 0.3
        front_empty_width = (SCREEN_WIDTH - (word_len * word_size[0]) - (term_width * (word_len - 1))) / 2
        
        space_x = front_empty_width
        space_y = SCREEN_HEIGHT * 0.26 # + ((SCREEN_WIDTH / 4) * 0.15)
        for idx in range(0, word_len):     
            #pygame.draw.rect(self.SCREEN, self.COLOR_GREY_LIGHT, [space_x, space_y, word_size[0], word_size[1]])
            now_rect = pygame.draw.rect(self.SCREEN, (213, 213, 213), [space_x, space_y, word_size[0], word_size[1]], border_radius=15)

            word_text = self.main_font_20.render(self.random_consonant[idx], True, self.COLOR_BLACK)            
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
        space_y = SCREEN_HEIGHT * 0.26 # + ((SCREEN_WIDTH / 4) * 0.15)
        for idx in range(0, word_len):     
            #pygame.draw.rect(self.SCREEN, self.COLOR_GREY_LIGHT, [space_x, space_y, word_size[0], word_size[1]])
            now_rect = pygame.draw.rect(self.SCREEN, (213, 213, 213), [space_x, space_y, word_size[0], word_size[1]], border_radius=15)

            word_text = self.main_font_20.render(self.now_word['consonant'][idx], True, self.COLOR_BLACK)            
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
        space_y = SCREEN_HEIGHT * 0.26 # + ((SCREEN_WIDTH / 4) * 0.15)
        for idx in range(0, word_len):        
            #pygame.draw.rect(self.SCREEN, self.COLOR_GREY_LIGHT, [space_x, space_y, word_size[0], word_size[1]])
            now_rect = pygame.draw.rect(self.SCREEN, (213, 213, 213), [space_x, space_y, word_size[0], word_size[1]], border_radius=15)

            word_text = self.main_font_20.render(self.now_word['word'][idx], True, self.COLOR_BLACK)            
            word_text_rect = word_text.get_rect()        
            name_text_size = word_text_rect.size
            word_text_rect.centerx = now_rect.centerx
            word_text_rect.centery = now_rect.centery
            self.SCREEN.blit(word_text, (word_text_rect.x, word_text_rect.y))            

            space_x += word_size[0] + term_width


            

if __name__ == '__main__':
    game = Game()
    game.run()
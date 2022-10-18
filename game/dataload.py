import pygame

# soldier_images_right = []
# def import_soldier_right(size):
#     soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_1.png'), size), True, False))
#     soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_2.png'), size), True, False))
#     soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_3.png'), size), True, False))
#     soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_4.png'), size), True, False))
#     soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_5.png'), size), True, False))
#     soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_6.png'), size), True, False))
#     soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_7.png'), size), True, False))
#     soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_8.png'), size), True, False))
#     soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_9.png'), size), True, False))
#     soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_10.png'), size), True, False))
#     soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_1.png'), size), True, False))
#     soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_2.png'), size), True, False))
#     soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_3.png'), size), True, False))
#     soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_4.png'), size), True, False))
#     soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_5.png'), size), True, False))
#     soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_6.png'), size), True, False))
#     soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_7.png'), size), True, False))
#     soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_8.png'), size), True, False))
#     soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_9.png'), size), True, False))
#     soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_10.png'), size), True, False))
#     soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Dead_1.png'), (size[0] * 1.5, size[1] * 1.2)), True, False))
#     soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Dead_2.png'), (size[0] * 1.5, size[1] * 1.2)), True, False))
#     soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Dead_3.png'), (size[0] * 1.5, size[1] * 1.2)), True, False))
#     soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Dead_4.png'), (size[0] * 1.5, size[1] * 1.2)), True, False))
#     soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Dead_5.png'), (size[0] * 1.5, size[1] * 1.2)), True, False))
#     soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Dead_6.png'), (size[0] * 1.5, size[1] * 1.2)), True, False))
#     soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Dead_7.png'), (size[0] * 1.5, size[1] * 1.2)), True, False))
#     soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Dead_8.png'), (size[0] * 1.5, size[1] * 1.2)), True, False))
#     soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Dead_9.png'), (size[0] * 1.5, size[1] * 1.2)), True, False))
#     soldier_images_right.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Dead_10.png'), (size[0] * 1.5, size[1] * 1.2)), True, False))    

# soldier_images_left = []
# def import_soldier_left(size):
#     soldier_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_1.png'), size))
#     soldier_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_2.png'), size))
#     soldier_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_3.png'), size))
#     soldier_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_4.png'), size))
#     soldier_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_5.png'), size))
#     soldier_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_6.png'), size))
#     soldier_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_7.png'), size))
#     soldier_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_8.png'), size))
#     soldier_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_9.png'), size))
#     soldier_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Run_10.png'), size))
#     soldier_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_1.png'), size))
#     soldier_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_2.png'), size))
#     soldier_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_3.png'), size))
#     soldier_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_4.png'), size))
#     soldier_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_5.png'), size))
#     soldier_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_6.png'), size))
#     soldier_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_7.png'), size))
#     soldier_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_8.png'), size))
#     soldier_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_9.png'), size))
#     soldier_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Attack_10.png'), size))
#     soldier_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Dead_1.png'), (size[0] * 1.5, size[1] * 1.2)))
#     soldier_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Dead_2.png'), (size[0] * 1.5, size[1] * 1.2)))
#     soldier_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Dead_3.png'), (size[0] * 1.5, size[1] * 1.2)))
#     soldier_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Dead_4.png'), (size[0] * 1.5, size[1] * 1.2)))
#     soldier_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Dead_5.png'), (size[0] * 1.5, size[1] * 1.2)))
#     soldier_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Dead_6.png'), (size[0] * 1.5, size[1] * 1.2)))
#     soldier_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Dead_7.png'), (size[0] * 1.5, size[1] * 1.2)))
#     soldier_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Dead_8.png'), (size[0] * 1.5, size[1] * 1.2)))
#     soldier_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Dead_9.png'), (size[0] * 1.5, size[1] * 1.2)))
#     soldier_images_left.append(pygame.transform.scale(pygame.image.load('game/res/character/knight/png/Dead_10.png'), (size[0] * 1.5, size[1] * 1.2)))




def import_sound():
    sound_map = {}
    donation_sound = pygame.mixer.Sound("game/res/sound/donation.mp3")
    donation_sound.set_volume(0.7)
    sound_map['donation'] = donation_sound
    stage_clear_sound = pygame.mixer.Sound("game/res/sound/stage_clear.mp3")
    stage_clear_sound.set_volume(0.7)
    sound_map['stage_clear'] = stage_clear_sound
    return sound_map
    
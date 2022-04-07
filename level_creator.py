import pygame
from support import *
from pickle import dump as p_dump
from pickle import load as p_load
from os import rename as os_rename
from os.path import isfile as os_isfile
from math import dist as math_dist

def create_level(level_name='', renamable=True):


    class MainGame:

        def __init__(self):
            self.total_spaces = 0
            self.start_pos = None
            self.can_save = False
            self.menu = False
            self.go_to_hub = False
            self.sound = p_load(open(Path('data/data/sound_data.bat'), 'rb'))
            self.rename = False
            self.rename_name = level_name
            self.level_name = level_name


        def draw_elements(self):


            screen.fill((192, 192, 200))
            screen.blit(black_wood_background, (0, 0))

            for x, y in level_temp:

                if level[x, y][0] == 'space':
                    screen.blit(space_temp, (x+x_slide, y))

                try:
                    screen.blit(black_ball, (self.start_pos.x+x_slide, self.start_pos.y))
                except:
                    pass

                the_text = self.level_name + '  (Edit Mode)'
                text_surface = game_font.render(the_text, False, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(380+x_slide, 30))

                screen.blit(text_surface, text_rect)

                screen.blit(ui_menu_button, ui_menu_button_rect)
                if self.check_ui_menu_button():
                    screen.blit(highlight_ui_menu_button, ui_menu_button_rect)


        def level_temp(self):

            maingame.__init__()
            
            for x in range(19):
                for y in range(19):
                    level[x*box_size, y*box_size] = ['wall', False]


        def place_space(self, set_pos):

            for x, y in level_temp:
                box_rect = pygame.rect.Rect(x, y, box_size, box_size)
                if box_rect.collidepoint(pygame.mouse.get_pos()):

                    if level[x, y][0] == 'wall' and set_pos == 'set_space':
                        level[x, y][0] = 'space'
                        self.total_spaces += 1
                        break
                    elif set_pos == 'set_wall' and level[x, y][0] == 'space':
                        level[x, y][0] = 'wall'
                        self.total_spaces -= 1
                        if self.start_pos == pygame.Vector2(x, y):
                            self.start_pos = None
                    elif set_pos == 'set_pos' and level[x, y][0] == 'space':
                        self.start_pos = pygame.Vector2(x, y)


        def selected_buttons(self, slide, click=False):

                mouse_pos = pygame.mouse.get_pos()

                if self.menu and slide:
                    for index, rectangles in enumerate(pause_menu_rects):
                        if index == 2 and not self.can_save:
                            continue
                        if rectangles.collidepoint(mouse_pos):
                            if index != 3:
                                screen.blit(pause_button_selected, rectangles)
                            elif renamable:
                                screen.blit(rename_box, (338, 475))
                                screen.blit(rename_text, (346, 476))
                            if click:
                                return True, index
                return False, None


        def game_menu(self):
                
            menu_slide = -480
            loop_break = False
            slide_up = False
            self.menu = True
            # index = []

            while True:

                pygame.display.update()
                clock.tick(60)

                if loop_break or self.go_to_hub:
                    self.menu = False
                    break

                # draw elements

                self.draw_elements()

                screen.blit(menu_background, (0, 0))

                screen.blit(menu_temp, (180, menu_slide))
                screen.blit(menu_temp_text, (180, menu_slide))
                if not self.can_save:
                    screen.blit(no_save, (230, 411+menu_slide))
                
                if renamable:
                    screen.blit(rename_icon, (350, 500+menu_slide))

                self.selected_buttons(menu_slide == 0)

                if menu_slide != 0 and not slide_up:
                    menu_slide += 20
                elif slide_up:
                    menu_slide -= 20

                if menu_slide == -480:
                    slide_up = False
                    loop_break = True

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        raise SystemExit
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        if self.sound: click_sound.play()
                        slide_up = True
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.check_ui_menu_button(True):
                            slide_up = True
                            break
                        slide_up, index = self.selected_buttons(menu_slide == 0, True)
                        if (index or index == 0) and self.sound:
                            click_sound.play()
                        if index == 0:
                            maingame.level_temp()
                        elif index == 1:
                            self.go_to_hub = True
                        elif index == 2:
                            level['total_spaces'] = maingame.total_spaces
                            level['start_pos'] = maingame.start_pos
                            p_dump(level, open(Path('data/custom levels/' + str(self.level_name) +'X.bat'), 'wb'))
                            self.go_to_hub = True
                        elif index == 3 and renamable:
                            self.rename = True


        def rename_level(self):

            size = 5
            close = False

            # pygame.key.start_text_input()
            
            while True:

                pygame.display.update()
                clock.tick(60)

                re_page_animation = pygame.transform.scale(confirm_page, (size*4, size*2))
                re_page_animation_rect = re_page_animation.get_rect(center=(380, 380))
            

                self.draw_elements()
                screen.blit(menu_background, (0, 0))

                if close or (size != 100):
                    screen.blit(re_page_animation, re_page_animation_rect)

                if not close and size != 100:
                    size += 5
                elif close and size != 5:
                    size -= 5
                elif close and size == 5:
                    self.rename = False
                    break
                else:

                    new_name = Path('data/custom levels/'+self.rename_name+'X.bat')
                    old_name = Path('data/custom levels/'+self.level_name+'X.bat')

                    text = game_font.render(self.rename_name, True, (8, 100, 125))
                    text_rect = text.get_rect(center=(380, 380))
                    screen.blit(confirm_page, (180, 280))
                    screen.blit(rename_text_underline, (180, 280))
                    screen.blit(text, text_rect)

                    if os_isfile(new_name) and self.rename_name != self.level_name:
                        screen.blit(file_exists_text, (215, 420))

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            raise SystemExit
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            if self.check_ui_menu_button(True):
                                self.rename_name = level_name
                                close = True
                                break
                        if event.type == pygame.KEYDOWN:

                            if event.unicode in char_list and len(self.rename_name) < 13:
                                self.rename_name += event.unicode
                                if self.sound: type_sound.play()

                            elif event.key == pygame.K_BACKSPACE and self.rename_name:
                                self.rename_name = self.rename_name[:-1]
                                if self.sound: type_sound2.play()
                            elif event.key == pygame.K_RETURN:
                                if os_isfile(new_name) and self.rename_name != self.level_name:
                                    if self.sound: error_sound.play()
                                elif self.rename_name != self.level_name:
                                    if self.sound: place_sound.play()
                                    os_rename(old_name, new_name)
                                    self.level_name = self.rename_name
                                    close = True
                                    break
                                else:
                                    if self.sound: place_sound.play()
                                    close = True
                            elif event.key == pygame.K_ESCAPE:
                                if self.sound: click_sound.play()
                                self.rename_name = level_name
                                close = True
                                break


        def check_ui_menu_button(self, click=False):
            
            mouse_pos = pygame.mouse.get_pos()
            if ui_menu_button_rect.collidepoint(mouse_pos):
                if math_dist(ui_menu_button_rect.center, mouse_pos) <= 16:
                    if click:
                        if self.sound: click_sound.play()
                    return True


    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((760, 760), pygame.FULLSCREEN|pygame.SCALED)

    game_font = pygame.font.Font(Path('data/font/arial.ttf'), 34)
    font_2 = pygame.font.Font(Path('data/font/arial.ttf'), 26)
    small_font = pygame.font.Font(Path('data/font/arial.ttf'), 19)

    box_size = 40
    x_slide = -725
    level = {}
    char_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '-', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '_', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'J', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    

    maingame = MainGame()
    level = p_load(open(Path('data/custom levels/' + str(level_name) + 'X.bat'), 'rb'))
    maingame.total_spaces = level['total_spaces']
    maingame.start_pos = level['start_pos']

    # variables

    level_temp = [(0, 0), (0, 40), (0, 80), (0, 120), (0, 160), (0, 200), (0, 240), (0, 280), (0, 320), (0, 360), (0, 400), (0, 440), (0, 480), (0, 520), (0, 560), (0, 600), (0, 640), (0, 680), (0, 720), (40, 0), (40, 40), (40, 80), (40, 120), (40, 160), (40, 200), (40, 240), (40, 280), (40, 320), (40, 360), (40, 400), (40, 440), (40, 480), (40, 520), (40, 560), (40, 600), (40, 640), (40, 680), (40, 720), (80, 0), (80, 40), (80, 80), (80, 120), (80, 160), (80, 200), (80, 240), (80, 280), (80, 320), (80, 360), (80, 400), (80, 440), (80, 480), (80, 520), (80, 560), (80, 600), (80, 640), (80, 680), (80, 720), (120, 0), (120, 40), (120, 80), (120, 120), (120, 160), (120, 200), (120, 240), (120, 280), (120, 320), (120, 360), (120, 400), (120, 440), (120, 480), (120, 520), (120, 560), (120, 600), (120, 640), (120, 680), (120, 720), (160, 0), (160, 40), (160, 80), (160, 120), (160, 160), (160, 200), (160, 240), (160, 280), (160, 320), (160, 360), (160, 400), (160, 440), (160, 480), (160, 520), (160, 560), (160, 600), (160, 640), (160, 680), (160, 720), (200, 0), (200, 40), (200, 80), (200, 120), (200, 160), (200, 200), (200, 240), (200, 280), (200, 320), (200, 360), (200, 400), (200, 440), (200, 480), (200, 520), (200, 560), (200, 600), (200, 640), (200, 680), (200, 720), (240, 0), (240, 40), (240, 80), (240, 120), (240, 160), (240, 200), (240, 240), (240, 280), (240, 320), (240, 360), (240, 400), (240, 440), (240, 480), (240, 520), (240, 560), (240, 600), (240, 640), (240, 680), (240, 720), (280, 0), (280, 40), (280, 80), (280, 120), (280, 160), (280, 200), (280, 240), (280, 280), (280, 320), (280, 360), (280, 400), (280, 440), (280, 480), (280, 520), (280, 560), (280, 600), (280, 640), (280, 680), (280, 720), (320, 0), (320, 40), (320, 80), (320, 120), (320, 160), (320, 200), (320, 240), (320, 280), (320, 320), (320, 360), (320, 400), (320, 440), (320, 480), (320, 520), (320, 560), (320, 600), (320, 640), (320, 680), (320, 720), (360, 0), (360, 40), (360, 80), (360, 120), (360, 160), (360, 200), (360, 240), (360, 280), (360, 320), (360, 360), (360, 400), (360, 440), (360, 480), (360, 520), (360, 560), (360, 600), (360, 640), (360, 680), (360, 720), (400, 0), (400, 40), (400, 80), (400, 120), (400, 160), (400, 200), (400, 240), (400, 280), (400, 320), (400, 360), (400, 400), (400, 440), (400, 480), (400, 520), (400, 560), (400, 600), (400, 640), (400, 680), (400, 720), (440, 0), (440, 40), (440, 80), (440, 120), (440, 160), (440, 200), (440, 240), (440, 280), (440, 320), (440, 360), (440, 400), (440, 440), (440, 480), (440, 520), (440, 560), (440, 600), (440, 640), (440, 680), (440, 720), (480, 0), (480, 40), (480, 80), (480, 120), (480, 160), (480, 200), (480, 240), (480, 280), (480, 320), (480, 360), (480, 400), (480, 440), (480, 480), (480, 520), (480, 560), (480, 600), (480, 640), (480, 680), (480, 720), (520, 0), (520, 40), (520, 80), (520, 120), (520, 160), (520, 200), (520, 240), (520, 280), (520, 320), (520, 360), (520, 400), (520, 440), (520, 480), (520, 520), (520, 560), (520, 600), (520, 640), (520, 680), (520, 720), (560, 0), (560, 40), (560, 80), (560, 120), (560, 160), (560, 200), (560, 240), (560, 280), (560, 320), (560, 360), (560, 400), (560, 440), (560, 480), (560, 520), (560, 560), (560, 600), (560, 640), (560, 680), (560, 720), (600, 0), (600, 40), (600, 80), (600, 120), (600, 160), (600, 200), (600, 240), (600, 280), (600, 320), (600, 360), (600, 400), (600, 440), (600, 480), (600, 520), (600, 560), (600, 600), (600, 640), (600, 680), (600, 720), (640, 0), (640, 40), (640, 80), (640, 120), (640, 160), (640, 200), (640, 240), (640, 280), (640, 320), (640, 360), (640, 400), (640, 440), (640, 480), (640, 520), (640, 560), (640, 600), (640, 640), (640, 680), (640, 720), (680, 0), (680, 40), (680, 80), (680, 120), (680, 160), (680, 200), (680, 240), (680, 280), (680, 320), (680, 360), (680, 400), (680, 440), (680, 480), (680, 520), (680, 560), (680, 600), (680, 640), (680, 680), (680, 720), (720, 0), (720, 40), (720, 80), (720, 120), (720, 160), (720, 200), (720, 240), (720, 280), (720, 320), (720, 360), (720, 400), (720, 440), (720, 480), (720, 520), (720, 560), (720, 600), (720, 640), (720, 680), (720, 720)]


    # Assets

    space_temp = pygame.image.load(Path('data/assets/space_temp.png')).convert_alpha()
    black_wood_background = pygame.image.load(Path('data/assets/black_wood_background.png')).convert_alpha()
    black_ball = pygame.image.load(Path('data/assets/black_ball.png')).convert_alpha()
    menu_temp = pygame.image.load(Path('data/assets/menu_temp.png')).convert_alpha()
    menu_temp_text = pygame.image.load(Path('data/assets/menu_temp_text.png')).convert_alpha()
    menu_background = pygame.image.load(Path('data/assets/menu_background.png')).convert_alpha()
    pause_button_selected = pygame.image.load(Path('data/assets/pause_button_selected.png')).convert_alpha()
    no_save = pygame.image.load(Path('data/assets/no_save.png')).convert_alpha()
    rename_icon = pygame.image.load(Path('data/assets/rename_icon.png')).convert_alpha()
    confirm_page = pygame.image.load(Path('data/assets/confirm_page.png')).convert_alpha()
    rename_box = pygame.image.load(Path('data/assets/rename_box.png')).convert_alpha()
    rename_text_underline = pygame.image.load(Path('data/assets/rename_text_underline.png')).convert_alpha()
    ui_menu_button = pygame.image.load(Path('data/assets/ui_buttons/drop_menu_button.png'))

    ui_menu_button_rect = ui_menu_button.get_rect(topright=(750, 10))
    highlight_ui_menu_button = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.circle(highlight_ui_menu_button, (0, 0, 0, 90), (16, 16), 16)

    pause_menu_rects = []
    pause_menu_rects.append(pygame.rect.Rect(230, 238, 300, 50))
    pause_menu_rects.append(pygame.rect.Rect(230, 325, 300, 50))
    pause_menu_rects.append(pygame.rect.Rect(230, 412, 300, 50))
    pause_menu_rects.append(rename_box.get_rect(topleft=(350, 500)))

    file_exists_text = font_2.render('This name is already in use', True, (200, 25, 40))
    rename_text = small_font.render('Rename', True, (230, 230, 255))

    # sound

    click_sound = pygame.mixer.Sound(Path('data/sound/click_sound.wav'))
    error_sound = pygame.mixer.Sound(Path('data/sound/error_sound.wav'))
    place_sound = pygame.mixer.Sound(Path('data/sound/place_sound.wav'))
    type_sound = pygame.mixer.Sound(Path('data/sound/type_sound.wav'))
    type_sound2 = pygame.mixer.Sound(Path('data/sound/type_sound2.wav'))

    while True:

        if maingame.go_to_hub:
            break

        if x_slide < 0:
            x_slide += 25

        if maingame.start_pos and maingame.total_spaces > 1:
            maingame.can_save = True

        if maingame.rename:
            maingame.rename_level()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

        if x_slide == 0:

            button = pygame.mouse.get_pressed()
            if button[0] and maingame.check_ui_menu_button(True):
                maingame.game_menu()
            elif button[0] and pygame.key.get_pressed()[pygame.K_LSHIFT]:
                maingame.place_space('set_pos')
            elif button[0]:
                maingame.place_space('set_space')
            elif button[2]:
                maingame.place_space('set_wall')

            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                if maingame.sound: click_sound.play()
                maingame.game_menu()

        maingame.draw_elements()

        pygame.display.update()
        clock.tick(120)


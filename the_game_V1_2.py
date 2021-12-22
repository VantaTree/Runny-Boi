import pygame
from pickle import load as p_load
from pickle import dump as p_dump
from level_creator_V1_2 import create_level
from math import dist as math_dist

def play_game(level_name, default_one=False, editable=False):

    class MainGame:

        def __init__(self, level_name, default_one=False):

            colour = p_load(open('data/data/colour_data.bat', 'rb'))
            if colour[1]:
                self.colour = colour[0]
            else:
                self.colour = p_load(open('data/data/custom_colour_data.bat', 'rb'))
            self.boxes_passed = 0
            self.won  =False
            self.menu = False
            self.game_active = False
            self.go_to_hub = False
            self.timer = [0, 0, 0]
            self.level_name = level_name
            self.current_level = default_one
            self.level = p_load(open(level_name, 'rb'))
            self.total_spaces = self.level['total_spaces']
            self.pause_menu = True
            self.user_level = p_load(open('data/data/user_level.bat', 'rb'))
            self.sound = True
            self.sound = p_load(open('data/data/sound_data.bat', 'rb'))
            self.ui_button_pos = p_load(open('data/data/ui_button_data.bat', 'rb'))
            self.max_levels = 27
            self.set_y_slide = False
            self.moved = False
            self.default_one = default_one

            screen_side = 0 if self.ui_button_pos == 'left' else 570
            self.ui_button_rect_list=[
                ui_button_surface_list[0].get_rect(topleft=(60+screen_side, 560)),
                ui_button_surface_list[0].get_rect(topleft=(10+screen_side, 620)),
                ui_button_surface_list[0].get_rect(topleft=(110+screen_side, 620)),
                ui_button_surface_list[0].get_rect(topleft=(60+screen_side, 680))
            ]


        def next_level(self):
            if self.current_level < self.max_levels:
                self.current_level += 1
                self.level_name = 'data/levels/level_'+str(self.current_level)+'.bat'
                maingame.__init__(self.level_name, self.current_level)
                player.__init__()
                self.total_spaces = self.level['total_spaces']
                self.set_y_slide = True
            else:
                self.go_to_hub = True


        def selected_buttons(self, slide, click=False):

            mouse_pos = pygame.mouse.get_pos()

            if self.menu and slide:
                for index, rectangles in enumerate(pause_menu_rects):
                    if rectangles.collidepoint(mouse_pos):
                        if index != 3:
                            screen.blit(pause_button_selected, rectangles)
                        elif editable:
                            screen.blit(edit_box, (355, 475))
                            screen.blit(edit_text, (363, 476))
                        if click:
                            return True, index
            return False, None


        def check_ui_buttons(self, click=False):
            
            mouse_pos = pygame.mouse.get_pos()
            for i, rect in enumerate(self.ui_button_rect_list):
                if rect.collidepoint(mouse_pos) and math_dist(mouse_pos, rect.center) < 35:
                    if click and not player.move_to and not self.won:
                        if i == 0:
                            player.move_to = 'up'
                        elif i == 1:
                            player.move_to = 'left'
                        elif i == 2:
                            player.move_to = 'right'
                        elif i == 3:
                            player.move_to = 'down'
                    else:
                        return i


        def game_menu(self):
            
            menu_slide = -480
            loop_break = False
            slide_up = False
            self.menu = True
            index = []

            while True:

                pygame.display.update()
                clock.tick(60)

                if not self.pause_menu and self.current_level + 1 > self.user_level:
                    p_dump(self.user_level+1, open('data/data/user_level.bat', 'wb'))

                if loop_break or self.go_to_hub:
                    self.menu = False
                    break

                # draw elements
                if self.set_y_slide:
                    screen.blit(brick_background, (0, 0))
                else:
                    self.draw_elements()

                screen.blit(menu_background, (0, 0))

                screen.blit(menu_surface, (180, menu_slide))

                if self.pause_menu:
                    screen.blit(pause_menu_resume, (180, menu_slide))
                elif default_one:
                    screen.blit(menu_next_level, (180, menu_slide))
                else:
                    screen.blit(go_back_menu, (180, menu_slide))

                if editable:
                    screen.blit(edit_icon, (350, 500+menu_slide))

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
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and menu_slide == 0:
                        if self.check_ui_menu_button(True):
                            slide_up = True
                            break
                        slide_up, index = self.selected_buttons(True, True)
                        if (index or index==0) and self.sound:
                            click_sound.play()
                        if index == 0 and not self.pause_menu and not self.default_one:
                            self.go_to_hub = True # go back
                        elif index == 0 and not self.pause_menu:
                            self.next_level()
                        elif index == 1 and not self.pause_menu and not self.default_one:
                            return 'go to hub'
                        elif index == 1:
                            self.go_to_hub = True
                        elif index == 2:
                            maingame.__init__(self.level_name, self.current_level)
                            player.__init__()
                        elif index == 3:
                            self.edit_level()
                            maingame.__init__(self.level_name, self.current_level)
                            player.__init__()



                keys = pygame.key.get_pressed()
                if menu_slide == 0:
                    if keys[pygame.K_ESCAPE] and self.pause_menu:
                        if self.sound: click_sound.play()
                        slide_up = True


        def draw_elements(self):

            self.boxes_passed = 0

            if y_slide != 0:
                screen.blit(brick_background, (0, 0))
            screen.blit(brick_background, (0, y_slide+0))

            self.display_timer()

            for x, y in level_temp:
                coloured_box = pygame.rect.Rect(x, y_slide+y, box_size, box_size)

                if self.level[x, y][1]:
                    self.boxes_passed += 1

                if self.level[x, y][0] == 'space':
                    screen.blit(space, (x, y_slide+y))
                try:
                    if self.level[x, y][1]:
                        pygame.draw.rect(screen, self.colour, coloured_box)
                except:
                    pass

            screen.blit(black_ball, (player.pos.x, y_slide+player.pos.y))

            #ui buttons
            if self.ui_button_pos != 'None':
                highlight_button = self.check_ui_buttons()
                for i, rect in enumerate(self.ui_button_rect_list):

                    screen.blit(ui_button_surface_bg, (rect.left, rect.top+y_slide))
                    if i == highlight_button:
                        screen.blit(ui_button_surface_bg, (rect.left, rect.top+y_slide))

                    screen.blit(ui_button_surface_list[i], (rect.left, rect.top+y_slide))

            screen.blit(ui_menu_button, ui_menu_button_rect)
            if self.check_ui_menu_button():
                screen.blit(highlight_ui_menu_button, ui_menu_button_rect)


        def display_timer(self):
            if self.timer[2] < 10:
                milli_sec = '0' + str(self.timer[2])
            else:
                milli_sec = str(self.timer[2])
            if self.timer[1] < 10:
                sec = '0' + str(self.timer[1])
            else:
                sec = str(self.timer[1])

            minute = str(self.timer[0])

            the_time = minute + ':' + str(sec) + '.' + milli_sec
            time_surface = game_font.render(the_time, True, (255, 255, 255))
            screen.blit(time_surface, (0, y_slide+0))

            # render text
            if not self.default_one:
                the_text = str(self.level_name[19:-5])
            else:
                the_text = 'LEVEL ' + str(self.current_level)
            text_surface = game_font.render(the_text, True, (255, 255, 255))
            screen.blit(text_surface, (330, y_slide+0))


        def edit_level(self):

            name = level_name[19:-5]
            create_level(name, False)


        def check_ui_menu_button(self, click=False):
            
            mouse_pos = pygame.mouse.get_pos()
            if ui_menu_button_rect.collidepoint(mouse_pos):
                if math_dist(ui_menu_button_rect.center, mouse_pos) <= 16:
                    if click:
                        if self.sound: click_sound.play()
                    return True

    class Player:

        def __init__(self):

            self.pos = maingame.level['start_pos']
            self.move_to = None
            maingame.level[self.pos.x, self.pos.y][1] = True
            self.moved = False


        def move(self):

            try :

                if self.move_to == 'right':
                    pos_x_y = self.pos.x+box_size, self.pos.y
                    if maingame.level[pos_x_y][0] == 'space':
                        maingame.level[pos_x_y][1] = True
                        self.pos.x += box_size
                        self.moved = True
                    else:
                        self.move_to = None
                        if self.moved:
                            self.moved = False
                            if maingame.sound: hit_sound.play()

                if self.move_to == 'left':
                    pos_x_y = self.pos.x-box_size, self.pos.y
                    if maingame.level[pos_x_y][0] == 'space':
                        maingame.level[pos_x_y][1] = True
                        self.pos.x -= box_size
                        self.moved = True
                    else:
                        self.move_to = None
                        if self.moved:
                            self.moved = False
                            if maingame.sound: hit_sound.play()

                if self.move_to == 'up':
                    pos_x_y = self.pos.x, self.pos.y-box_size
                    if maingame.level[pos_x_y][0] == 'space':
                        maingame.level[pos_x_y][1] = True
                        self.pos.y -= box_size
                        self.moved = True
                    else:
                        self.move_to = None
                        if self.moved:
                            self.moved = False
                            if maingame.sound: hit_sound.play()

                if self.move_to == 'down':
                    pos_x_y = self.pos.x, self.pos.y+box_size
                    if maingame.level[pos_x_y][0] == 'space':
                        maingame.level[pos_x_y][1] = True
                        self.pos.y += box_size
                        self.moved = True
                    else:
                        self.move_to = None
                        if self.moved:
                            self.moved = False
                            if maingame.sound: hit_sound.play()
            except:
                self.move_to = None
                if self.moved:
                    self.moved = False
                    if maingame.sound: hit_sound.play()


    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((760, 760))
    game_font = pygame.font.Font('data/font/arial.ttf', 34)
    small_font = pygame.font.Font('data/font/arial.ttf', 19)
    y_slide = -725

    ui_arrow = pygame.image.load('data/assets/ui_buttons/ui_arrow.png').convert_alpha()
    ui_button_surface_list = [
        ui_arrow,
        pygame.transform.rotate(ui_arrow, 90),
        pygame.transform.rotate(ui_arrow, -90),
        pygame.transform.rotate(ui_arrow, 180)]

    maingame = MainGame(level_name, default_one)
    player = Player()


    # variables

    box_size = 40
    level_temp = []
    for xCoord in range(0, 19):
        for yCoord in range(0, 19):
            level_temp.append((box_size*xCoord, box_size*yCoord))

    MOVE = pygame.USEREVENT
    pygame.time.set_timer(MOVE, 50)
    TIMED = pygame.USEREVENT + 1
    pygame.time.set_timer(TIMED, 10)


    # Assets

    black_ball = pygame.image.load('data/assets/black_ball.png').convert_alpha()
    space = pygame.image.load('data/assets/space.png').convert_alpha()
    brick_background = pygame.image.load('data/assets/brick_background.png').convert_alpha()
    menu_surface = pygame.image.load('data/assets/menu_surface.png').convert_alpha()
    menu_background = pygame.image.load('data/assets/menu_background.png').convert_alpha()
    menu_background = pygame.image.load('data/assets/menu_background.png').convert_alpha()
    pause_button_selected = pygame.image.load('data/assets/pause_button_selected.png').convert_alpha()
    pause_menu_resume = pygame.image.load('data/assets/pause_menu_resume.png').convert_alpha()
    go_back_menu = pygame.image.load('data/assets/go_back_menu.png').convert_alpha()
    menu_next_level = pygame.image.load('data/assets/menu_next_level.png').convert_alpha()
    edit_icon = pygame.image.load('data/assets/edit_icon.png').convert_alpha()
    edit_box = pygame.image.load('data/assets/edit_box.png').convert_alpha()
    ui_menu_button = pygame.image.load('data/assets/ui_buttons/drop_menu_button.png')
    

    ui_button_surface_bg = pygame.Surface((70, 70), pygame.SRCALPHA)
    pygame.draw.circle(ui_button_surface_bg, (104, 164, 192, 80), (35, 35), 35)

    ui_menu_button_rect = ui_menu_button.get_rect(topright=(750, 10))
    highlight_ui_menu_button = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.circle(highlight_ui_menu_button, (0, 0, 0, 90), (16, 16), 16)

    pause_menu_rects = []
    pause_menu_rects.append(pygame.rect.Rect(230, 238, 300, 50))
    pause_menu_rects.append(pygame.rect.Rect(230, 325, 300, 50))
    pause_menu_rects.append(pygame.rect.Rect(230, 412, 300, 50))
    pause_menu_rects.append(edit_icon.get_rect(topleft=(350, 500)))

    edit_text = small_font.render('Edit', True, (230, 230, 255))


    # sound

    hit_sound = pygame.mixer.Sound('data/sound/hit_sound.wav')
    win_sound = pygame.mixer.Sound('data/sound/win_sound.wav')
    click_sound = pygame.mixer.Sound('data/sound/click_sound.wav')

    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == MOVE and player.move_to:
                maingame.game_active = True
                player.move()
            if event.type == TIMED and maingame.game_active:
                maingame.timer[2] += 1
                if maingame.timer[2] == 100:
                    maingame.timer[2] = 00
                    maingame.timer[1] += 1
                if maingame.timer[1] == 60:
                    maingame.timer[1] = 00
                    maingame.timer[0] += 1
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if maingame.check_ui_menu_button(True):
                    maingame.game_menu()

        if y_slide == 0:
            keys = pygame.key.get_pressed()
            if not player.move_to and not maingame.won:
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    player.move_to = 'right'
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    player.move_to = 'left'
                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    player.move_to = 'up'
                if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    player.move_to = 'down'
            if keys[pygame.K_ESCAPE]:
                if maingame.sound: click_sound.play()
                maingame.game_menu()
            if maingame.ui_button_pos != 'None' and pygame.mouse.get_pressed(3)[0]:
                maingame.check_ui_buttons(True)

        if maingame.boxes_passed == maingame.total_spaces:
            maingame.game_active = False
            maingame.won = True
            maingame.pause_menu = False
        if maingame.won and not player.move_to:
            if maingame.sound: win_sound.play()
            if maingame.game_menu() == 'go to hub':
                return 'go to hub'

        if maingame.set_y_slide:
            maingame.set_y_slide = False
            y_slide = -725

        if y_slide != 0:
            y_slide += 25

        if maingame.go_to_hub:
            break

        maingame.draw_elements()

        pygame.display.update()
        clock.tick(60)

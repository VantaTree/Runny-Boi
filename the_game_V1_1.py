import pygame
from pickle import load as p_load
from pickle import dump as p_dump
from level_creator_V1_1 import create_level

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
            self.timer = [00, 00, 00]
            self.level_name = level_name
            self.current_level = default_one
            self.level = p_load(open(level_name, 'rb'))
            self.total_spaces = self.level['total_spaces']
            self.pause_menu = True
            self.user_level = p_load(open('data/data/user_level.bat', 'rb'))
            self.sound = True
            self.sound = p_load(open('data/data/sound_data.bat', 'rb'))
            self.max_levels = 27
            self.set_y_slide = False
            self.moved = False
            self.default_one = default_one


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
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        slide_up, index = self.selected_buttons(menu_slide == 0, True)
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

            the_time = str(minute) + ':' + str(sec) + '.' + milli_sec
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

    maingame = MainGame(level_name, default_one)
    player = Player()


    # variables

    box_size = 40
    level_temp = [(0, 0), (0, 40), (0, 80), (0, 120), (0, 160), (0, 200), (0, 240), (0, 280), (0, 320), (0, 360), (0, 400), (0, 440), (0, 480), (0, 520), (0, 560), (0, 600), (0, 640), (0, 680), (0, 720), (40, 0), (40, 40), (40, 80), (40, 120), (40, 160), (40, 200), (40, 240), (40, 280), (40, 320), (40, 360), (40, 400), (40, 440), (40, 480), (40, 520), (40, 560), (40, 600), (40, 640), (40, 680), (40, 720), (80, 0), (80, 40), (80, 80), (80, 120), (80, 160), (80, 200), (80, 240), (80, 280), (80, 320), (80, 360), (80, 400), (80, 440), (80, 480), (80, 520), (80, 560), (80, 600), (80, 640), (80, 680), (80, 720), (120, 0), (120, 40), (120, 80), (120, 120), (120, 160), (120, 200), (120, 240), (120, 280), (120, 320), (120, 360), (120, 400), (120, 440), (120, 480), (120, 520), (120, 560), (120, 600), (120, 640), (120, 680), (120, 720), (160, 0), (160, 40), (160, 80), (160, 120), (160, 160), (160, 200), (160, 240), (160, 280), (160, 320), (160, 360), (160, 400), (160, 440), (160, 480), (160, 520), (160, 560), (160, 600), (160, 640), (160, 680), (160, 720), (200, 0), (200, 40), (200, 80), (200, 120), (200, 160), (200, 200), (200, 240), (200, 280), (200, 320), (200, 360), (200, 400), (200, 440), (200, 480), (200, 520), (200, 560), (200, 600), (200, 640), (200, 680), (200, 720), (240, 0), (240, 40), (240, 80), (240, 120), (240, 160), (240, 200), (240, 240), (240, 280), (240, 320), (240, 360), (240, 400), (240, 440), (240, 480), (240, 520), (240, 560), (240, 600), (240, 640), (240, 680), (240, 720), (280, 0), (280, 40), (280, 80), (280, 120), (280, 160), (280, 200), (280, 240), (280, 280), (280, 320), (280, 360), (280, 400), (280, 440), (280, 480), (280, 520), (280, 560), (280, 600), (280, 640), (280, 680), (280, 720), (320, 0), (320, 40), (320, 80), (320, 120), (320, 160), (320, 200), (320, 240), (320, 280), (320, 320), (320, 360), (320, 400), (320, 440), (320, 480), (320, 520), (320, 560), (320, 600), (320, 640), (320, 680), (320, 720), (360, 0), (360, 40), (360, 80), (360, 120), (360, 160), (360, 200), (360, 240), (360, 280), (360, 320), (360, 360), (360, 400), (360, 440), (360, 480), (360, 520), (360, 560), (360, 600), (360, 640), (360, 680), (360, 720), (400, 0), (400, 40), (400, 80), (400, 120), (400, 160), (400, 200), (400, 240), (400, 280), (400, 320), (400, 360), (400, 400), (400, 440), (400, 480), (400, 520), (400, 560), (400, 600), (400, 640), (400, 680), (400, 720), (440, 0), (440, 40), (440, 80), (440, 120), (440, 160), (440, 200), (440, 240), (440, 280), (440, 320), (440, 360), (440, 400), (440, 440), (440, 480), (440, 520), (440, 560), (440, 600), (440, 640), (440, 680), (440, 720), (480, 0), (480, 40), (480, 80), (480, 120), (480, 160), (480, 200), (480, 240), (480, 280), (480, 320), (480, 360), (480, 400), (480, 440), (480, 480), (480, 520), (480, 560), (480, 600), (480, 640), (480, 680), (480, 720), (520, 0), (520, 40), (520, 80), (520, 120), (520, 160), (520, 200), (520, 240), (520, 280), (520, 320), (520, 360), (520, 400), (520, 440), (520, 480), (520, 520), (520, 560), (520, 600), (520, 640), (520, 680), (520, 720), (560, 0), (560, 40), (560, 80), (560, 120), (560, 160), (560, 200), (560, 240), (560, 280), (560, 320), (560, 360), (560, 400), (560, 440), (560, 480), (560, 520), (560, 560), (560, 600), (560, 640), (560, 680), (560, 720), (600, 0), (600, 40), (600, 80), (600, 120), (600, 160), (600, 200), (600, 240), (600, 280), (600, 320), (600, 360), (600, 400), (600, 440), (600, 480), (600, 520), (600, 560), (600, 600), (600, 640), (600, 680), (600, 720), (640, 0), (640, 40), (640, 80), (640, 120), (640, 160), (640, 200), (640, 240), (640, 280), (640, 320), (640, 360), (640, 400), (640, 440), (640, 480), (640, 520), (640, 560), (640, 600), (640, 640), (640, 680), (640, 720), (680, 0), (680, 40), (680, 80), (680, 120), (680, 160), (680, 200), (680, 240), (680, 280), (680, 320), (680, 360), (680, 400), (680, 440), (680, 480), (680, 520), (680, 560), (680, 600), (680, 640), (680, 680), (680, 720), (720, 0), (720, 40), (720, 80), (720, 120), (720, 160), (720, 200), (720, 240), (720, 280), (720, 320), (720, 360), (720, 400), (720, 440), (720, 480), (720, 520), (720, 560), (720, 600), (720, 640), (720, 680), (720, 720)]

    MOVE = pygame.USEREVENT
    pygame.time.set_timer(MOVE, 50)
    TIMED = pygame.USEREVENT + 1
    pygame.time.set_timer(TIMED, 10)


    # Assets

    black_ball = pygame.image.load('data/assets/black_ball.png').convert_alpha()
    space = pygame.image.load('data/assets/space.png').convert_alpha()
    brick_background = pygame.image.load('data/assets/brick_background.png').convert_alpha()
    background = pygame.image.load('data/assets/background.png').convert_alpha()
    menu_surface = pygame.image.load('data/assets/menu_surface.png').convert_alpha()
    menu_background = pygame.image.load('data/assets/menu_background.png').convert_alpha()
    menu_background = pygame.image.load('data/assets/menu_background.png').convert_alpha()
    pause_button_selected = pygame.image.load('data/assets/pause_button_selected.png').convert_alpha()
    pause_menu_resume = pygame.image.load('data/assets/pause_menu_resume.png').convert_alpha()
    go_back_menu = pygame.image.load('data/assets/go_back_menu.png').convert_alpha()
    menu_next_level = pygame.image.load('data/assets/menu_next_level.png').convert_alpha()
    edit_icon = pygame.image.load('data/assets/edit_icon.png').convert_alpha()
    edit_box = pygame.image.load('data/assets/edit_box.png').convert_alpha()

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

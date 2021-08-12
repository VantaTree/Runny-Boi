import pygame
from the_game import play_game
from level_creator import create_level
from os import walk as os_walk
from webbrowser import open as web_open
from pickle import dump as p_dump
from pickle import load as p_load
from os import remove as os_remove
from os.path import isfile as os_isfile
from shutil import copyfile as shut_copy

class Hub:

    def __init__(self):
        colour = p_load(open('data/data/colour_data.bat', 'rb'))
        self.custom_colour = p_load(open('data/data/custom_colour_data.bat', 'rb'))
        colour_a, colour_b, colour_c = self.custom_colour
        self.colour_a, self.colour_b, self.colour_c = str(colour_a), str(colour_b), str(colour_c)
        self.colour = colour[0]
        self.default_colour = colour[1]
        self.hub_slide = 0
        self.level_page_no = 0
        self.max_page_no = 3
        self.break_loop = False
        self.user_level = p_load(open('data/data/user_level.bat', 'rb'))
        self.sound = p_load(open('data/data/sound_data.bat', 'rb'))
        self.max_levels = 27
        self.scroll_y = 220
        self.scroll_now = True
        self.max_y_slide = 220
        self.custom_level_rects = []
        self.levelnames = None
        self.del_confirm = None
        self.can_scroll = False
        self.colour_input = None
        self.stickman = None
        self.play_hilight_sound = True


    def page_slide(self, slide):

        if slide < 0:
            slide += 25
        elif slide > 0:
            slide -= 25
        return slide


    def highlight_button(self, show, click=False):
        
        mouse_pos = pygame.mouse.get_pos()

        if show and self.level_page_no != 0:

            if arrow_right_rect.collidepoint(mouse_pos) and self.level_page_no != self.max_page_no:
                screen.blit(highlighted_arrow_right, (710, 230))
            if arrow_left_rect.collidepoint(mouse_pos):
                screen.blit(highlighted_arrow_left, (20, 230))

            for index, rectangle in enumerate(level_button_rects):
                if (index+1)+((self.level_page_no-1)*9) <= self.user_level:
                    if rectangle.collidepoint(mouse_pos):
                        screen.blit(highlighted_level_button, rectangle)
                        break

        if show and self.level_page_no == 0:
            for index, rectangle in enumerate(hub_button_rects):
                if index == 0 and self.user_level == self.max_levels+1:
                    continue
                if rectangle.collidepoint(mouse_pos):
                    self.stickman = index
                    if self.play_hilight_sound:
                        pop_button.play()
                        self.play_hilight_sound = False
                    if index < 5:
                        screen.blit(hub_button_selected, rectangle)
                    elif index == 5:
                        screen.blit(help_box, (693, 675))
                        screen.blit(help_text, (700, 677))
                    elif index == 6:
                        screen.blit(help_box, (5, 675))
                        screen.blit(info_text, (15, 677))
                    if click:
                        return True, index
                    break
                else:
                    self.stickman = None
            else:
                self.play_hilight_sound = True
                    

        return False, None


    def press_button(self, click=False):

        mouse_pos = pygame.mouse.get_pos()

        if arrow_right_rect.collidepoint(mouse_pos):
            if self.sound and click and self.max_page_no != 3: click_sound.play()
            return 'next'
        if arrow_left_rect.collidepoint(mouse_pos):
            if self.sound and click: click_sound.play()
            return 'previous'


    def level_pages(self, x_slide):
        if self.level_page_no == 1:
            screen.blit(level_page_1, (x_slide+130, 130))            
        elif self.level_page_no == 2:
            screen.blit(level_page_2, (x_slide+130, 130)) 
        elif self.level_page_no == 3:
            screen.blit(level_page_3, (x_slide+130, 130)) 


    def draw_elements(self):

        screen.blit(background, (self.hub_slide+0, 0))
        screen.blit(hub_button, (self.hub_slide+410, 220))
        screen.blit(help_icon, (self.hub_slide+698, 698))
        screen.blit(info_icon, (self.hub_slide+10, 698))

        self.draw_stickman()

        if self.user_level > self.max_levels:
            screen.blit(no_continue, (self.hub_slide+410, 220))


    def draw_stickman(self):
        
        if self.stickman == 0:
            screen.blit(continue_stickman, (75, 281))
        elif self.stickman == 1:
            screen.blit(levels_stickman, (50, 250))
        elif self.stickman == 2:
            screen.blit(options_stickman, (80, 270))
        elif self.stickman == 3:
            screen.blit(custom_lev_stickman, (50, 267))
        elif self.stickman == 4:
            screen.blit(quit_stickman, (80, 250))
        elif self.stickman == 5:
            screen.blit(help_stickman, (80, 190))
        elif self.stickman == 6:
            screen.blit(info_stickman, (80, 260))


    def locked_levels(self, slide):
        
        for index, rectangles in enumerate(level_button_rects):

            level_num = (index+1)+((self.level_page_no-1)*9)

            if level_num > self.user_level:
                screen.blit(locked_level, (rectangles.topleft[0]+slide, rectangles.topleft[1]))


    def continue_level(self):
        if self.user_level == self.max_levels+1:
            pass
        else:
            level_name = 'data/levels/level_'+str(self.user_level)+'.bat'
            play_game(level_name, self.user_level)

            hub.__init__()
            self.break_loop = True
            self.hub_slide = -725


    def play_which_level(self):
        
        mouse_pos = pygame.mouse.get_pos()

        for index, rectangles in enumerate(level_button_rects):
            if rectangles.collidepoint(mouse_pos):
                level_num = (index+1)+((self.level_page_no-1)*9)
                if level_num <= self.user_level:
                    level_name = 'data/levels/level_'+ str(level_num) +'.bat'
                    if self.sound: click_sound.play()
                    play_game(level_name, level_num)

                    hub.__init__()
                    self.break_loop = True
                    self.hub_slide = -725
                    break


    def print_level_bars(self, slide, levelnames):

        if levelnames:
            temp_y_slide = self.scroll_y
            if self.scroll_now:
                self.custom_level_rects.clear()
            for index, level_name in enumerate(levelnames):
                screen.blit(custom_level_button, (slide+150, temp_y_slide))
                screen.blit(red_trash_can, (slide+550, temp_y_slide))
                screen.blit(edit_pen, (slide+470, temp_y_slide))

                text_surface = game_font.render(level_name[:-5], True, (8, 100, 125))
                text_rect = text_surface.get_rect(center=(slide+300, temp_y_slide+30))
                screen.blit(text_surface, text_rect)

                if self.scroll_now:
                    rect_one = pygame.rect.Rect(150, temp_y_slide, 300, 60)
                    rect_two = pygame.rect.Rect(470, temp_y_slide, 60, 60)
                    rect_three = pygame.rect.Rect(550, temp_y_slide, 60, 60)
                    self.custom_level_rects.append([rect_one, rect_two, rect_three])

                temp_y_slide += 80

        self.scroll_now = False


    def play_custom_level(self, levelnames, index_bar):

        level_name = 'data/custom levels/' + str(levelnames[index_bar])
        if play_game(level_name, editable=True) == 'go to hub':
            return 'go to hub'


    def custom_lev_blit_elements(self, lev_slide=0):

        mouse_pos = pygame.mouse.get_pos()

        screen.blit(background, (lev_slide, 0))
        
        if not self.levelnames:
            screen.blit(no_custom_level_text, (lev_slide, 0))

        if scroll_window_rect.collidepoint(mouse_pos) and self.levelnames:
            screen.blit(scroll_window, (lev_slide, 0))

        self.print_level_bars(lev_slide, self.levelnames)

        if lev_slide == 0 and not self.del_confirm:
            self.custom_level_button_click(self.levelnames)

        screen.blit(background_window, (lev_slide, 0))

        screen.blit(create_level_button, (lev_slide+150, 660))
        if create_level_rect.collidepoint(mouse_pos) and not self.del_confirm and lev_slide==0:
            screen.blit(create_level_selected, (150, 660))

        screen.blit(arrow_left, (lev_slide+20, 230))
        if self.press_button() == 'previous' and not self.del_confirm:
            screen.blit(highlighted_arrow_left, (20, 230))

            
    def edit_custom_level(self, levelnames, index_bar):

        level_name = levelnames[index_bar][:-5]
        create_level(level_name)
        self.load_custom_levels()


    def create_custom_level(self):
        
        num = 1
        waiting = True

        while waiting:
            name = 'data/custom levels/untitled-'+str(num)+'X.bat'

            if os_isfile(name):
                num += 1
            else:
                waiting = False

        shut_copy('data/data/temp_level.bat', name)

        self.load_custom_levels()
        self.scroll_now = True

        self.scroll_y = self.max_y_slide


    def del_custom_level(self, levelnames, index_bar):

        level_name = 'data/custom levels/' + str(levelnames[index_bar])
        os_remove(level_name)

        self.load_custom_levels()


    def del_confirm_page(self, levelnames):

        size = 5
        close = False

        while True:

            pygame.display.update()
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

            mouse_pos = pygame.mouse.get_pos()
            event = pygame.mouse.get_pressed()

            del_page_animation = pygame.transform.scale(confirm_page, (size*4, size*2))
            del_page_animation_rect = del_page_animation.get_rect(center=(380, 380))
            
            self.custom_lev_blit_elements()
            screen.blit(menu_background, (0, 0))

            if not close and size != 100:
                size += 5
            elif close and size != 5:
                size -= 5
            elif close and size == 5:
                self.del_confirm = None
                break
            else:

                screen.blit(confirm_page, (180, 280))
                screen.blit(del_yes_no, (180, 280))
            
                the_text = 'Delete "' + str(levelnames[self.del_confirm-1][:-5]) + '" ?'
                text_surface = normal_font.render(the_text, True, (8, 100, 125))
                text_rect = text_surface.get_rect(center=(380, 350))
                screen.blit(text_surface, text_rect)

                if del_yes_rect.collidepoint(mouse_pos):
                    screen.blit(del_yes_no_selected, (282, 393))
                    if event[0]:
                        if self.sound: click_sound.play()
                        self.del_custom_level(levelnames, self.del_confirm-1)
                        self.scroll_now = True
                        close = True
                elif del_no_rect.collidepoint(mouse_pos):
                    screen.blit(del_yes_no_selected, (415, 393))
                    if event[0]:
                        if self.sound: click_sound.play()
                        close = True

            if close or (size != 100):
                screen.blit(del_page_animation, del_page_animation_rect)


    def custom_level_button_click(self, levelnames, click=False):

        mouse_pos = pygame.mouse.get_pos()

        if scroll_window_rect.collidepoint(mouse_pos) and levelnames:

            for index_bar, bars in enumerate(self.custom_level_rects):
                for index_button, button in enumerate(bars):
                    if button.collidepoint(mouse_pos):
                        if not index_button:
                            screen.blit(custom_button_selected, button)
                        else:
                            screen.blit(custom_side_selected, button)

                        if click:
                            if self.sound: click_sound.play()
                            if index_button == 0:
                                go_to_hub = self.play_custom_level(levelnames, index_bar)
                                if go_to_hub == 'go to hub':
                                    return 'go to hub'
                                return True
                            elif index_button == 1:
                                self.edit_custom_level(levelnames, index_bar)
                                return True
                            elif index_button == 2:
                                self.del_confirm = index_bar+1


    def load_custom_levels(self):

        self.levelnames = next(os_walk('data/custom levels'))[2]
        self.max_y_slide = min(220, 220-(len(self.levelnames)-5)*80)


    def set_sound(self, click=False):
        
        mouse_pos = pygame.mouse.get_pos()

        if sound_on_rect.collidepoint(mouse_pos) and self.sound:
            screen.blit(slider_selected, sound_on_rect)
            if click:
                click_sound.play()
                self.sound  = False
                p_dump(self.sound, open('data/data/sound_data.bat', 'wb'))

        elif sound_off_rect.collidepoint(mouse_pos) and not self.sound:
            screen.blit(slider_selected, sound_off_rect)
            if click:
                click_sound.play()
                self.sound = True
                p_dump(self.sound, open('data/data/sound_data.bat', 'wb'))


    def set_custom_colour(self, event, mouse_pos):

        if event[0]:

            if colour_rect_a.collidepoint(mouse_pos):
                self.colour_input = 'a'
            elif colour_rect_b.collidepoint(mouse_pos):
                self.colour_input = 'b'
            elif colour_rect_c.collidepoint(mouse_pos):
                self.colour_input = 'c'
            else:
                self.colour_input = None

        if self.colour_input == 'a':
            screen.blit(colour_input_box_selected, (514, 509))
        elif self.colour_input == 'b':
            screen.blit(colour_input_box_selected, (559, 509))
        elif self.colour_input == 'c':
            screen.blit(colour_input_box_selected, (604, 509))


    def set_colour(self, slid, mouse_pos, click=False):

        text_a = font_2.render(self.colour_a, True, (0, 0, 10))
        text_b = font_2.render(self.colour_b, True, (0, 0, 10))
        text_c = font_2.render(self.colour_c, True, (0, 0, 10))

        if slid:

            screen.blit(text_a, (515, 511))
            screen.blit(text_b, (560, 511))
            screen.blit(text_c, (605, 511))


        if slid and click:

            for index, rect in enumerate(colour_rect):
                if rect.collidepoint(mouse_pos):
                    if (index or index == 0) and self.sound:
                        click_sound.play()
                    if index != 9:
                        self.colour = screen.get_at(mouse_pos)[:3]
                        self.default_colour = True
                    else:
                        self.custom_colour = screen.get_at(mouse_pos)[:3]
                        self.default_colour = False
                    p_dump((self.colour, self.default_colour), open('data/data/colour_data.bat', 'wb'))


    def info_buttons(self):
        
        mouse_pos = pygame.mouse.get_pos()

        if discord_rect.collidepoint(mouse_pos):
            web_open('http://discord.gg/NK27r9Jkhk')
        elif e_mail_rect.collidepoint(mouse_pos):
            web_open('mailto:vantatree@gmail.com')


    def settings_code(self):

        cog_slide = 725
        loop_break = False
        save_colour = False
        
        while True:

            pygame.display.update()
            clock.tick(60)

            if loop_break:
                break

            if self.colour_input:
                save_colour = False
            elif not save_colour:
                save_colour = True
                p_dump(self.custom_colour, open('data/data/custom_colour_data.bat', 'wb'))

            mouse_pos = pygame.mouse.get_pos()
            event = pygame.mouse.get_pressed()

            # elements
            
            screen.blit(background, (cog_slide, 0))
            screen.blit(arrow_left, (cog_slide+20, 230))
            if self.press_button() == 'previous':
                screen.blit(highlighted_arrow_left, (20, 230))
            screen.blit(option_background, (cog_slide+80, 80))

            screen.blit(slider, (cog_slide+415, 118))
            if self.sound:
                screen.blit(slider_bob, (cog_slide+412, 112))
            else:
                screen.blit(slider_bob, (cog_slide+522, 112))


            if cog_slide == 0:

                self.set_custom_colour(event, mouse_pos)

                screen.blit(colour_input_box, (515, 510))
                screen.blit(colour_input_box, (560, 510))
                screen.blit(colour_input_box, (605, 510))


                for index in range(10):
                    r = colour_rect[index]
                    c = colour_list[index]
                    if self.default_colour and self.colour == c and index != 9:
                        screen.blit(colour_selected, (r.x-4, r.y-4))
                    elif not self.default_colour and index == 9:
                        screen.blit(colour_selected, (r.x-4, r.y-4))
                    pygame.draw.rect(screen, c, r)

            self.set_sound()
            self.set_colour(cog_slide==0, mouse_pos)

            cog_slide = self.page_slide(cog_slide)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.MOUSEBUTTONUP and cog_slide == 0:
                    if event.button == 1:
                        self.set_colour(True, event.pos, True)
                        self.set_sound(True)
                        if self.press_button(True) == 'previous':
                            loop_break = True
                            self.hub_slide = -725
                            break

                if event.type == pygame.KEYDOWN:
                    
                    if self.colour_input == 'a':
                        if len(self.colour_a) < 3 and event.unicode.isnumeric():
                            if self.sound: type_sound.play()
                            self.colour_a += event.unicode
                            self.colour_a = str(int(self.colour_a))
                            if int(self.colour_a) > 255:
                                self.colour_a = '255'
                        elif event.key == pygame.K_BACKSPACE:
                            if self.sound: type_sound2.play()
                            self.colour_a = self.colour_a[:-1]
                            if not self.colour_a:
                                self.colour_a = '0'
                    elif self.colour_input == 'b':
                        if len(self.colour_b) < 3 and event.unicode.isnumeric():
                            if self.sound: type_sound.play()
                            self.colour_b += event.unicode
                            self.colour_b = str(int(self.colour_b))
                            if int(self.colour_b) > 255:
                                self.colour_b = '255'
                        elif event.key == pygame.K_BACKSPACE:
                            if self.sound: type_sound2.play()
                            self.colour_b = self.colour_b[:-1]
                            if not self.colour_b:
                                self.colour_b = '0'
                    elif self.colour_input == 'c':
                        if len(self.colour_c) < 3 and event.unicode.isnumeric():
                            if self.sound: type_sound.play()
                            self.colour_c += event.unicode
                            self.colour_c = str(int(self.colour_c))
                            if int(self.colour_c) > 255:
                                self.colour_c = '255'
                        elif event.key == pygame.K_BACKSPACE:
                            if self.sound: type_sound2.play()
                            self.colour_c = self.colour_c[:-1]
                            if not self.colour_c:
                                self.colour_c = '0'

                    self.custom_colour = int(self.colour_a), int(self.colour_b), int(self.colour_c)
                    colour_list[9] = self.custom_colour


    def help_code(self):

        hep_slide = 725
        loop_break = False
        scroll_pos = 0
        
        while True:

            pygame.display.update()
            clock.tick(60)

            if loop_break:
                break

            # elements
            
            screen.blit(background, (hep_slide, 0))
            screen.blit(help_base, (hep_slide+80, 30))
            screen.blit(help_page_text, (hep_slide+80, 30+scroll_pos))
            screen.blit(help_window, (hep_slide+0, 0))

            screen.blit(arrow_left, (hep_slide+20, 230))
            if self.press_button() == 'previous':
                screen.blit(highlighted_arrow_left, (20, 230))

            hep_slide = self.page_slide(hep_slide)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.MOUSEBUTTONUP and hep_slide == 0:
                    if event.button == 1:
                        if self.press_button(True) == 'previous':
                            loop_break = True
                            self.hub_slide = -725
                            break
                    if event.button == 4 and scroll_pos < 0:
                        scroll_pos += 20
                    if event.button == 5 and scroll_pos > -760:
                        scroll_pos -= 20


    def info_code(self):

        in_slide = 725
        loop_break = False
        scroll_pos = 0
        
        while True:

            pygame.display.update()
            clock.tick(60)

            if loop_break:
                break

            # elements
            
            screen.blit(background, (in_slide, 0))
            screen.blit(help_base, (in_slide+80, 30))
            screen.blit(info_page_text, (in_slide+80, 30+scroll_pos))
            screen.blit(help_window, (in_slide+0, 0))

            screen.blit(arrow_left, (in_slide+20, 230))
            if self.press_button() == 'previous':
                screen.blit(highlighted_arrow_left, (20, 230))

            in_slide = self.page_slide(in_slide)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.MOUSEBUTTONUP and in_slide == 0:
                    if event.button == 1:
                        self.info_buttons()
                        if self.press_button(True) == 'previous':
                            loop_break = True
                            self.hub_slide = -725
                            break
                    if event.button == 4 and scroll_pos < 0:
                        scroll_pos += 20
                        discord_rect.y += 20
                        e_mail_rect.y += 20
                    if event.button == 5 and scroll_pos > -50:
                        scroll_pos -= 20
                        discord_rect.y -= 20
                        e_mail_rect.y -=20


    def custom_level_code(self):

        lev_slide = 725
        loop_break = False

        self.load_custom_levels()

        while True:
            pygame.display.update()
            clock.tick(60)

            if loop_break:
                if self.sound: click_sound.play()
                break

            if self.del_confirm:
                self.del_confirm_page(self.levelnames)

            # elements
            
            self.custom_lev_blit_elements(lev_slide)

            lev_slide = self.page_slide(lev_slide)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.MOUSEBUTTONUP and lev_slide == 0:
                    mouse_pos = event.pos
      
                    if event.button == 1:

                        go_to_hub = self.custom_level_button_click(self.levelnames, click=True)

                        if go_to_hub == 'go to hub':
                            loop_break = True
                            self.hub_slide = -725
                            break
                        elif go_to_hub:
                            lev_slide = 725

                        if self.press_button(True) == 'previous':
                            loop_break = True
                            self.hub_slide = -725
                            break

                        if create_level_rect.collidepoint(mouse_pos):
                            if self.sound: place_sound.play()
                            self.create_custom_level()

                    if scroll_window_rect.collidepoint(mouse_pos):
                        if event.button == 4 and self.scroll_y < 220:
                            self.scroll_y += 20
                            self.scroll_now = True
                        elif event.button == 5 and self.scroll_y > self.max_y_slide:
                            self.scroll_y -= 20
                            self.scroll_now = True
                        

    def levels_code(self):

        self.break_loop = False
        x_slide = 725
        self.hub_slide = -725
        self.level_page_no = 1

        while True:

            pygame.display.update()
            clock.tick(60)

            if self.break_loop:
                break

            x_slide = self.page_slide(x_slide)

            # elements

            screen.blit(background, (x_slide+0, 0))
            screen.blit(level_button_template, (x_slide+130, 130))

            self.locked_levels(x_slide)
            

            if x_slide == 0:
                screen.blit(arrow_left, (x_slide+20, 230))
                if self.level_page_no != self.max_page_no:
                    screen.blit(arrow_right, (x_slide+710, 230))

            self.level_pages(x_slide)

            self.highlight_button(x_slide == 0)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.MOUSEBUTTONDOWN and x_slide == 0 and event.button == 1:

                    self.play_which_level()

                    if self.press_button(True) == 'next' and self.level_page_no != self.max_page_no:
                        if self.sound: click_sound.play()
                        self.level_page_no += 1
                        x_slide = 725
                    elif self.press_button(True) == 'previous':
                        if self.sound: click_sound.play()
                        self.level_page_no -= 1
                        x_slide = -725
                    if self.level_page_no == 0:
                        self.break_loop = True
                        break




pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((760, 760))
pygame.display.set_caption('Runny Boi')
game_icon = pygame.image.load('data/assets/fill-color.png').convert_alpha()
pygame.display.set_icon(game_icon)

hub = Hub()

game_font = pygame.font.Font('data/font/IndieFlower-Regular.ttf', 40)
normal_font = pygame.font.Font('data/font/arial.ttf', 30)
font_2 = pygame.font.Font('data/font/arial.ttf', 26)
small_font = pygame.font.Font('data/font/arial.ttf', 19)

colour_list = [
    (172, 172, 192),
    (255, 209, 193),
    (105, 190, 245),
    (205, 65., 95.),
    (255, 255, 255),
    (215, 100, 175),
    (100, 215, 200),
    (220, 235, 90.),
    (115, 235, 105),
    hub.custom_colour
]

colour_rect = [
    pygame.Rect(130+0.0, 280+0.0, 100, 100),
    pygame.Rect(130+120, 280+0.0, 100, 100),
    pygame.Rect(130+240, 280+0.0, 100, 100),
    pygame.Rect(130+0.0, 280+120, 100, 100),
    pygame.Rect(130+120, 280+120, 100, 100),
    pygame.Rect(130+240, 280+120, 100, 100),
    pygame.Rect(130+0.0, 280+240, 100, 100),
    pygame.Rect(130+120, 280+240, 100, 100),
    pygame.Rect(130+240, 280+240, 100, 100),
    pygame.Rect(170+360, 280+120, 100, 100)

]

# Assets
background = pygame.image.load('data/assets/background.png').convert_alpha()
space = pygame.image.load('data/assets/space.png').convert_alpha()
level_button = pygame.image.load('data/assets/level_button.png').convert_alpha()
level_button_template = pygame.image.load('data/assets/level_button_template.png').convert_alpha()
highlighted_level_button = pygame.image.load('data/assets/highlighted_level_button.png').convert_alpha()
hub_button = pygame.image.load('data/assets/hub_button.png').convert_alpha()
hub_button_selected = pygame.image.load('data/assets/hub_button_selected.png').convert_alpha()
arrow_right = pygame.image.load('data/assets/arrow_right.png').convert_alpha()
arrow_left = pygame.transform.rotate(arrow_right, 180)
highlighted_arrow_right = pygame.image.load('data/assets/highlighted_arrow_right.png').convert_alpha()
highlighted_arrow_left = pygame.transform.rotate(highlighted_arrow_right, 180)
level_page_1 = pygame.image.load('data/assets/level_page_1.png').convert_alpha()
level_page_2 = pygame.image.load('data/assets/level_page_2.png').convert_alpha()
level_page_3 = pygame.image.load('data/assets/level_page_3.png').convert_alpha()
no_continue = pygame.image.load('data/assets/no_continue.png').convert_alpha()
locked_level = pygame.image.load('data/assets/locked_level.png').convert_alpha()
custom_level_button = pygame.image.load('data/assets/custom_level_button.png').convert_alpha()
scroll_window = pygame.image.load('data/assets/scroll_window.png').convert_alpha()
background_window = pygame.image.load('data/assets/background_window.png').convert_alpha()
custom_button_selected = pygame.image.load('data/assets/custom_button_selected.png').convert_alpha()
custom_side_selected = pygame.image.load('data/assets/custom_side_selected.png').convert_alpha()
red_trash_can = pygame.image.load('data/assets/red_trash_can.png').convert_alpha()
edit_pen = pygame.image.load('data/assets/edit_pen.png').convert_alpha()
confirm_page = pygame.image.load('data/assets/confirm_page.png').convert_alpha()
menu_background = pygame.image.load('data/assets/menu_background.png').convert_alpha()
del_yes_no = pygame.image.load('data/assets/del_yes_no.png').convert_alpha()
del_yes_no_selected = pygame.image.load('data/assets/del_yes_no_selected.png').convert_alpha()
create_level_button = pygame.image.load('data/assets/create_level_button.png').convert_alpha()
create_level_selected = pygame.image.load('data/assets/create_level_selected.png').convert_alpha()
help_icon = pygame.image.load('data/assets/help_icon.png').convert_alpha()
help_box = pygame.image.load('data/assets/help_box.png').convert_alpha()
help_base = pygame.image.load('data/assets/help_base.png').convert_alpha()
help_window = pygame.image.load('data/assets/help_window.png').convert_alpha()
help_page_text = pygame.image.load('data/assets/help_text.png').convert_alpha()
info_page_text = pygame.image.load('data/assets/info_text.png').convert_alpha()
info_icon = pygame.image.load('data/assets/info_icon.png').convert_alpha()
option_background = pygame.image.load('data/assets/option_background.png').convert_alpha()
slider_bob = pygame.image.load('data/assets/slider_bob.png').convert_alpha()
slider_selected = pygame.image.load('data/assets/slider_selected.png').convert_alpha()
slider = pygame.image.load('data/assets/slider.png').convert_alpha()
colour_selected = pygame.image.load('data/assets/colour_selected.png').convert_alpha()
colour_input_box = pygame.image.load('data/assets/colour_input_box.png').convert_alpha()
colour_input_box_selected = pygame.image.load('data/assets/colour_input_box_selected.png').convert_alpha()
no_custom_level_text = pygame.image.load('data/assets/no_custom_level_text.png').convert_alpha()

info_stickman = pygame.image.load('data/assets/stickman/info_stickman.png').convert_alpha()
help_stickman = pygame.image.load('data/assets/stickman/help_stickman.png').convert_alpha()
quit_stickman = pygame.image.load('data/assets/stickman/quit_stickman.png').convert_alpha()
options_stickman = pygame.image.load('data/assets/stickman/options_stickman.png').convert_alpha()
levels_stickman = pygame.image.load('data/assets/stickman/levels_stickman.png').convert_alpha()
continue_stickman = pygame.image.load('data/assets/stickman/continue_stickman.png').convert_alpha()
custom_lev_stickman = pygame.image.load('data/assets/stickman/custom-lev_stickman.png').convert_alpha()

help_text = small_font.render('HELP', True, (230, 230, 255))
info_text = small_font.render('INFO', True, (230, 230, 255))

arrow_right_rect = arrow_right.get_rect(topleft=(710, 230))
arrow_left_rect = arrow_left.get_rect(topleft=(20, 230))

level_button_rects = []
level_button_rects.append(pygame.rect.Rect(130, 130, 100, 100))
level_button_rects.append(pygame.rect.Rect(330, 130, 100, 100))
level_button_rects.append(pygame.rect.Rect(530, 130, 100, 100))
level_button_rects.append(pygame.rect.Rect(130, 330, 100, 100))
level_button_rects.append(pygame.rect.Rect(330, 330, 100, 100))
level_button_rects.append(pygame.rect.Rect(530, 330, 100, 100))
level_button_rects.append(pygame.rect.Rect(130, 530, 100, 100))
level_button_rects.append(pygame.rect.Rect(330, 530, 100, 100))
level_button_rects.append(pygame.rect.Rect(530, 530, 100, 100))

hub_button_rects = []
hub_button_rects.append(pygame.rect.Rect(410, 220, 280, 70))
hub_button_rects.append(pygame.rect.Rect(410, 320, 280, 70))
hub_button_rects.append(pygame.rect.Rect(410, 420, 280, 70))
hub_button_rects.append(pygame.rect.Rect(410, 520, 280, 70))
hub_button_rects.append(pygame.rect.Rect(410, 620, 280, 70))
hub_button_rects.append(help_icon.get_rect(topleft=(698, 698)))
hub_button_rects.append(info_icon.get_rect(topleft=(10, 698)))

sound_on_rect = slider_bob.get_rect(topleft=(412, 112))
sound_off_rect = slider_bob.get_rect(topleft=(522, 112))

del_yes_rect = pygame.rect.Rect(282, 393, 64, 43)
del_no_rect = pygame.rect.Rect(415, 393, 64, 43)

colour_rect_a = colour_input_box.get_rect(topleft=(515, 510))
colour_rect_b = colour_input_box.get_rect(topleft=(560, 510))
colour_rect_c = colour_input_box.get_rect(topleft=(605, 510))

scroll_window_rect = pygame.rect.Rect(140, 200, 480, 420)

create_level_rect = create_level_selected.get_rect(topleft=(150, 660))

discord_rect = pygame.rect.Rect(108, 505, 465, 45)
e_mail_rect = pygame.rect.Rect(108, 688, 465, 45)


# sound

click_sound = pygame.mixer.Sound('data/sound/click_sound.wav')
place_sound = pygame.mixer.Sound('data/sound/place_sound.wav')
type_sound = pygame.mixer.Sound('data/sound/type_sound.wav')
type_sound2 = pygame.mixer.Sound('data/sound/type_sound2.wav')
pop_button = pygame.mixer.Sound('data/sound/pop_button.wav')

while True:

    pygame.display.update()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and hub.hub_slide == 0:
            do_it, index = hub.highlight_button(hub.hub_slide == 0, True)
            if do_it:
                if (index or index == 0) and hub.sound:
                    click_sound.play()
                    hub.stickman = None
                if index == 0:
                    hub.continue_level()
                elif index == 1:
                    hub.levels_code()
                elif index == 2:
                    hub.settings_code()
                elif index == 3:
                    hub.custom_level_code()
                elif index == 4:
                    pygame.quit()
                    raise SystemExit  
                elif index == 5:
                    hub.help_code()      
                elif index == 6:
                    hub.info_code()      
    
    hub.draw_elements()
    hub.highlight_button(hub.hub_slide == 0)

    hub.hub_slide = hub.page_slide(hub.hub_slide)
    

import pygame
import functions as defs

window_width, window_height = (500, 600)
pygame.init()
screen = pygame.display.set_mode([window_width, window_height])

stopped = False
button_group = pygame.sprite.Group()
button_colors = {"default": (150, 150, 150),
                 "highlighted": (230, 230, 230),
                 "pressed": (80, 80, 80)}
button_animation_speed = 2
global_list = []
global_list_str = []
numpad_size = 77


class Label:
    def __init__(self, text, size, cx, cy, bgcl=None):
        self.text = text
        self.font = pygame.font.SysFont('Arial', size)
        self.cx = cx
        self.cy = cy
        self.bgcl = bgcl
        self.text_change(self.text)
        self.rect = self.text_rendered.get_rect()
        self.rect.centerx = cx
        self.rect.centery = cy

    def render(self, surface: pygame.Surface):
        surface.blit(self.text_rendered, self.rect)

    def text_change(self, text):
        if self.bgcl is not None:
            self.text_rendered = self.font.render(text, True, (0, 0, 0), self.bgcl)
        else:
            self.text_rendered = self.font.render(text, True, (0, 0, 0))
        self.rect = self.text_rendered.get_rect()
        self.rect.centerx = self.cx
        self.rect.centery = self.cy


global_label = Label(' '.join(global_list_str), 20, window_width / 2, window_height / 10)


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, text, keys=None):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(button_colors['default'])
        self.filled_color = button_colors['default']
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pressed = False
        self.keyboard_pressed = False
        self.highlighted = False
        self.text = text
        self.label = Label(str(self.text), 20, self.rect.width / 2, self.rect.height / 2)
        self.keys = keys
        self.filled_color = list(button_colors['default'])

    def update_check(self, vnt):
        mouse_pos = pygame.mouse.get_pos()
        vnt_types = [i.type for i in vnt]
        if (pygame.KEYDOWN not in vnt_types and pygame.KEYUP not in vnt_types) and not self.keyboard_pressed:
            if self.rect.x <= mouse_pos[0] <= self.rect.x + self.rect.width:
                if self.rect.y <= mouse_pos[1] <= self.rect.y + self.rect.height:
                    for ivnt in vnt:
                        if ivnt.type == pygame.MOUSEBUTTONDOWN:
                            if ivnt.button == 1:
                                self.pressed = True
                                self.highlighted = False
                        elif ivnt.type == pygame.MOUSEBUTTONUP and self.pressed:
                            self.pressed = False
                            self.do_something()
                        if not self.pressed:
                            self.highlighted = True
                else:
                    self.pressed = False
                    self.highlighted = False
            else:
                self.pressed = False
                self.highlighted = False
        if self.keys is not None:
            for i in vnt:
                if i.type == pygame.KEYDOWN:
                    if i.key == self.keys:
                        self.keyboard_pressed = True
                        self.do_something()
                if i.type == pygame.KEYUP:
                    if i.key == self.keys:
                        self.keyboard_pressed = False

        if self.pressed or self.keyboard_pressed:
            self.animated_fill(button_colors['pressed'], button_animation_speed)
        elif self.highlighted:
            self.animated_fill(button_colors['highlighted'], button_animation_speed)
        elif not self.pressed and not self.highlighted:
            self.animated_fill(button_colors['default'], button_animation_speed)

        pygame.draw.rect(self.image, (0, 0, 0), [0, 0, self.rect.width, self.rect.height], 3)
        self.label.render(self.image)

    def do_something(self):
        global global_list
        if type(self.text) == int and self.text == 0:
            if len(global_list_str) == 0:
                return

        if not global_list:
            if type(self.text) == int:
                global_list.append(self.text)
                global_list_str.append(str(self.text))
        elif type(self.text) == int:
            if type(global_list[-1]) == int:
                global_list[-1] = int(str(global_list[-1]) + str(self.text))
                global_list_str[-1] += str(self.text)
            if type(global_list[-1]) == str:
                global_list.append(self.text)
                global_list_str.append(str(self.text))
        elif type(self.text) == str:
            if len(global_list) != 0:
                if type(global_list[-1]) == int:
                    global_list.append(self.text)
                    global_list_str.append(self.text)
            if type(global_list[-1]) == str:
                return

    def animated_fill(self, to_color, speed):
        if to_color[0] == self.filled_color[0]:
            self.image.fill(self.filled_color)
            return
        if self.filled_color[0] < to_color[0]:
            self.filled_color = [c + speed for c in self.filled_color]
        elif self.filled_color[0] >= to_color[0]:
            self.filled_color = [c - speed for c in self.filled_color]
        self.image.fill(self.filled_color)


class CallBackButton(Button):
    def __init__(self, x, y, width, height, text, callback, args=None, keys=None):
        super().__init__(x, y, width, height, text, keys)
        self.callback = callback
        self.args = args

    def do_something(self):
        global global_list, global_list_str
        self.callback(self.args)


numpad_texts = [['/', '*', '-', '**'], [7, 8, 9, '+'], [4, 5, 6], [1, 2, 3], [0]]
numpad_keys = [[pygame.K_KP_DIVIDE, pygame.K_KP_MULTIPLY, pygame.K_KP_MINUS, None],
               [pygame.K_KP7, pygame.K_KP8, pygame.K_KP9, pygame.K_KP_PLUS],
               [pygame.K_KP4, pygame.K_KP5, pygame.K_KP6],
               [pygame.K_KP1, pygame.K_KP2, pygame.K_KP3], [pygame.K_KP0]]

for i in range(0, 5):
    for n, u in enumerate(numpad_texts[i]):
        button_group.add(Button(numpad_size * n + (10 * n),
                                (numpad_size * i) + 100 + (5 * i),
                                int(numpad_size),
                                int(numpad_size),
                                u, numpad_keys[i][n]))


button_group.add(CallBackButton(261, 265, int(numpad_size), int(numpad_size * 2) + 4, 'Enter', defs.callback_enterkey,
                                [global_list, global_list_str], pygame.K_KP_ENTER))
button_group.add(CallBackButton(87, 430, int(numpad_size), int(numpad_size), 'C', defs.clear_one,
                                [global_list, global_list_str], pygame.K_BACKSPACE))
button_group.add(CallBackButton(174, 430, int(numpad_size), int(numpad_size), 'CE', defs.clear_all,
                                [global_list, global_list_str], pygame.K_ESCAPE))

while not stopped:
    vnt = pygame.event.get()
    button_group.update()

    for i in vnt:
        if i.type == pygame.QUIT:
            stopped = True

    for u in button_group:
        u.update_check(vnt)

    screen.fill((255, 255, 255))
    global_label.text_change(' '.join(global_list_str))
    global_label.render(screen)
    button_group.draw(screen)
    pygame.display.flip()

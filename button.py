import pygame

class Button:
    def __init__(self, screen, text, rect, function, func_args=None, font_size=25):
        self.screen = screen
        self.function = function
        self.func_args = func_args
        self.rect = rect
        self.style = 1 # 1 = black-bordered rectangle
        self.color = (128,128,128)
        self.hover_color = (self.color[0]-20, self.color[1]-20, self.color[2]-20)
        self.pressed_color = (self.color[0]-50, self.color[1]-50, self.color[2]-50)
        self.text_color = (0,0,0)
        self.hover = 0
        self.pressed = 0
        self.font_size = font_size
        self.font = pygame.font.Font("font.ttf", self.font_size)
        self.font.set_bold(True)
        self.text_padding = 5
        self.update_text(text)
        

    def update(self, mouse):
        if self.rect.collidepoint(mouse.get_pos()):
            self.hover = 1
            if mouse.get_pressed()[0]:
                if not self.pressed:
                    self.pressed = 1
                    if self.func_args:
                        self.function(self.func_args)
                    else:
                        self.function()
            else:
                self.pressed = 0
        else:
            self.hover = 0
    
    def update_text(self, text):
        self.text = text
        self.text_surface = self.font.render(self.text, True, self.text_color)

    def draw(self):
        if self.style == 1:
            if self.pressed:
                pygame.draw.rect(self.screen, self.pressed_color, self.rect)
            elif self.hover:
                pygame.draw.rect(self.screen, self.hover_color, self.rect)
            else:
                pygame.draw.rect(self.screen, self.color, self.rect)
            pygame.draw.rect(self.screen, (0,0,0), self.rect, 1)
            self.screen.blit(self.text_surface, (self.rect.left + self.rect.width/2 - self.text_surface.get_rect().width/2, self.rect.top + self.rect.height/2 - self.text_surface.get_rect().height/2))
    
    def set_color(self, rgb):
        self.color = rgb
        self.hover_color = (self.color[0]-20, self.color[1]-20, self.color[2]-20)
        self.pressed_color = (self.color[0]-50, self.color[1]-50, self.color[2]-50)
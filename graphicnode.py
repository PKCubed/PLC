import pygame
import time
from icons import *

def format_duration(duration):
    return str(duration) + "s"

def semicircle(radius, color, inverted=False):
    output = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
    output.fill((0,0,0,0))
    pygame.draw.circle(output, color, (radius, radius), radius)
    pygame.draw.circle(output, (0,0,0), (radius, radius), radius, 1)
    if inverted:
        pygame.draw.rect(output, (0,0,0,0), (radius, 0, radius*2, radius*2))
    else:
        pygame.draw.rect(output, (0,0,0,0), (0, 0, radius, radius*2))
    return output

class GraphicNode:
    def __init__(self, screen, type, pos, connection=None, bar=False):
        self.bar = bar
        self.screen = screen
        self.type = type
        self.value = 0
        self.connection = None
        self.connection_2 = None
        self.width = 0
        self.height = 0
        self.duration = None
        self.timer_type = None 
        self.timer = None
        if self.type == 1: # Digital Input
            self.width = 40
            self.height = 40
        elif self.type == 2: # Digital Output
            self.width = 40
            self.height = 40
            self.connection = connection
        elif self.type == 3: # Timer
            self.width = 80
            self.height = 40
            self.duration = 1.0
            self.timer_type = 0 # 0=Delay, 1=On-Delay, 2=Off-Delay
            self.timer = [0,0] # (Timestamp of new value, new value)
        elif self.type == 4: # Digital Not Gate
            self.width = 40
            self.height = 40
        elif self.type == 5: # Digital Logic Gate
            self.width = 40
            self.height = 40
            self.gate_type = 0 # 0 = AND, 1 = OR
        self.pos = pygame.Rect(pos[0], pos[1], self.width, self.height)
        self.old_pos = pygame.Rect(self.pos)
        if not self.bar:
            self.rect = pygame.Rect(self.pos[0], self.pos[1]+50, self.width, self.height)
        else:
            self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        if self.type == 5:
            self.in_1_rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height/2)
            self.in_2_rect = pygame.Rect(self.pos[0], self.pos[1]+self.height/2, self.width, self.height/2)
        self.font = pygame.font.Font("font.ttf", 35)
        self.font.set_bold(True)
        self.smallfont = pygame.font.Font("font.ttf", 12)
        self.smallfont.set_bold(True)
        self.deleted = False
        self.label = ""

    def update(self, pos=None): # pos is the xy position of the movable page
        if not self.bar:
            self.rect = self.pos.move(pos[0], pos[1]+50)
            if self.type == 3:
                self.connect_in_point = (self.rect.left+2, self.rect.centery)
                self.connect_out_point = (self.rect.right-2, self.rect.centery)
                if self.timer_type == 3: # Clock
                    self.connection = None
                    self.value = int(time.time()/self.duration%2)
            elif self.type == 4:
                self.connect_in_point = (self.rect.left+2, self.rect.centery)
                self.connect_out_point = (self.rect.right-2, self.rect.centery)
            elif self.type == 5:
                self.connect_in_point = (self.rect.left+2, self.rect.centery-10)
                self.connect_in_point_2 = (self.rect.left+2, self.rect.centery+10)
                self.connect_out_point = (self.rect.right-2, self.rect.centery)
                self.in_1_rect = pygame.Rect(self.rect.left, self.rect.top, self.rect.width, self.rect.height/2)
                self.in_2_rect = pygame.Rect(self.rect.left, self.rect.top+self.rect.height/2, self.rect.width, self.rect.height/2)
            else:
                self.connect_in_point = self.rect.center
                self.connect_out_point = self.rect.center
            if self.connection:
                if self.type==3:
                    if self.timer_type == 0: # Delay
                        if self.timer[1] != self.connection.value:
                            self.timer[0] = time.time()
                            self.timer[1] = self.connection.value
                        if self.timer[0]+self.duration < time.time():
                            self.value = self.timer[1]
                    if self.timer_type == 1: # On-Delay
                        if self.timer[1] != self.connection.value:
                            self.timer[0] = time.time()
                            self.timer[1] = self.connection.value
                        if self.connection.value:
                            if self.timer[0]+self.duration < time.time():
                                self.value = self.timer[1]
                        else:
                            self.value = 0
                    if self.timer_type == 2: # Off-Delay
                        if self.timer[1] != self.connection.value:
                            self.timer[0] = time.time()
                            self.timer[1] = self.connection.value
                        if not self.connection.value:
                            if self.timer[0]+self.duration < time.time():
                                self.value = self.timer[1]
                        else:
                            self.value = 1
                elif self.type==4:
                    self.value = not self.connection.value
                else:
                    self.value = self.connection.value
            if self.type == 5:
                if self.gate_type == 0:
                    if self.connection and self.connection_2:
                        self.value = self.connection.value and self.connection_2.value
                    else:
                        self.value = 0
                        """
                        if self.connection:
                            self.value = self.connection
                        elif self.connection_2:
                            self.value = self.connection_2
                        """
        else:
            self.rect = self.pos
    
    def draw(self):
        if self.type == 1: # 1 = Digital Input
            if self.value:
                pygame.draw.rect(self.screen, (0, 255, 0), self.rect)
                text_surface = self.font.render("1", True, (0,0,0))
            else:
                pygame.draw.rect(self.screen, (0, 60, 0), self.rect)
                text_surface = self.font.render("0", True, (0,0,0))
            self.screen.blit(text_surface, (self.rect.left + self.rect.width/2 - text_surface.get_rect().width/2, self.rect.top + self.rect.height/2 - text_surface.get_rect().height/2))
            pygame.draw.rect(self.screen, (0,0,0), self.rect, 1)
        elif self.type == 2: # 2 = Digital Output
            if self.value:
                pygame.draw.circle(self.screen, (0, 255, 0), self.rect.center, self.rect.width/2)
                text_surface = self.font.render("1", True, (0,0,0))
            else:
                pygame.draw.circle(self.screen, (0, 60, 0), self.rect.center, self.rect.width/2)
                text_surface = self.font.render("0", True, (0,0,0))
            self.screen.blit(text_surface, (self.rect.left + self.rect.width/2 - text_surface.get_rect().width/2, self.rect.top + self.rect.height/2 - text_surface.get_rect().height/2))
            pygame.draw.circle(self.screen, (0, 0, 0), self.rect.center, self.rect.width/2, 1)
        elif self.type == 3: # 3 = Timer
            pygame.draw.rect(self.screen, (200,200,200), self.rect)
            timer_icon.set_alpha(128)
            self.screen.blit(timer_icon, self.rect.move(2,2).topleft)
            text_surface = self.smallfont.render(format_duration(self.duration), True, (0,0,0))
            self.screen.blit(text_surface, (self.rect.right - text_surface.get_rect().width-2, self.rect.bottom - text_surface.get_rect().height))
            if self.timer_type == 0:
                text_surface = self.smallfont.render("Delay", True, (0,0,0))
            elif self.timer_type == 1:
                text_surface = self.smallfont.render("On-D", True, (0,0,0))
            elif self.timer_type == 2:
                text_surface = self.smallfont.render("Off-D", True, (0,0,0))
            elif self.timer_type == 3:
                text_surface = self.smallfont.render("Clock", True, (0,0,0))
            self.screen.blit(text_surface, (self.rect.right - text_surface.get_rect().width-2, self.rect.top))
            pygame.draw.rect(self.screen, (0,0,0), self.rect, 1)
            pygame.draw.polygon(self.screen, (128,80,0), [(self.rect.left, self.rect.top+self.rect.height/2-5), (self.rect.left+5, self.rect.top+self.rect.height/2), (self.rect.left, self.rect.top+self.rect.height/2+5)])
            pygame.draw.polygon(self.screen, (0,0,0), [(self.rect.left, self.rect.top+self.rect.height/2-5), (self.rect.left+5, self.rect.top+self.rect.height/2), (self.rect.left, self.rect.top+self.rect.height/2+5)], 1)
            pygame.draw.polygon(self.screen, (128,80,0), [(self.rect.right-6, self.rect.top+self.rect.height/2-5), (self.rect.right, self.rect.top+self.rect.height/2), (self.rect.right-6, self.rect.top+self.rect.height/2+5)])
            pygame.draw.polygon(self.screen, (0,0,0), [(self.rect.right-6, self.rect.top+self.rect.height/2-5), (self.rect.right-1, self.rect.top+self.rect.height/2), (self.rect.right-6, self.rect.top+self.rect.height/2+5)], 1)
        elif self.type == 4: # 4 = Not Gate
            pygame.draw.polygon(self.screen, (128,128,128), [(self.rect.left, self.rect.top+self.rect.height/2-10), (self.rect.left+30, self.rect.top+self.rect.height/2), (self.rect.left, self.rect.top+self.rect.height/2+10)])
            pygame.draw.polygon(self.screen, (0,0,0), [(self.rect.left, self.rect.top+self.rect.height/2-10), (self.rect.left+30, self.rect.top+self.rect.height/2), (self.rect.left, self.rect.top+self.rect.height/2+10)],1)
            pygame.draw.circle(self.screen, (128,128,128), (self.rect.left+35, self.rect.centery), 5)
            pygame.draw.circle(self.screen, (0,0,0), (self.rect.left+35, self.rect.centery), 5, 1)
        elif self.type == 5: # 5 = Logic Gate
            if self.gate_type == 0: # And Gate
                #pygame.draw.arc(self.screen, (128,128,128), self.rect, -math.pi/2, math.pi/2, 10)
                #pygame.gfxdraw.pie(self.screen, self.rect.centerx, self.rect.centery, 20, -90, 90, (128, 128, 128))
                pygame.draw.rect(self.screen, (128,128,128), pygame.Rect(self.rect.left, self.rect.top, self.rect.width/2, self.rect.height))
                pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(self.rect.left, self.rect.top, self.rect.width/2, self.rect.height), 1)
                self.screen.blit(semicircle(20, (128,128,128), False), self.rect.move(-1,0).topleft)
            pygame.draw.polygon(self.screen, (128,80,0), [(self.rect.left, self.rect.top+self.rect.height/2+5), (self.rect.left+5, self.rect.top+self.rect.height/2+10), (self.rect.left, self.rect.top+self.rect.height/2+15)])
            pygame.draw.polygon(self.screen, (0,0,0), [(self.rect.left, self.rect.top+self.rect.height/2+5), (self.rect.left+5, self.rect.top+self.rect.height/2+10), (self.rect.left, self.rect.top+self.rect.height/2+15)], 1)
            pygame.draw.polygon(self.screen, (128,80,0), [(self.rect.left, self.rect.top+self.rect.height/2-5), (self.rect.left+5, self.rect.top+self.rect.height/2-10), (self.rect.left, self.rect.top+self.rect.height/2-15)])
            pygame.draw.polygon(self.screen, (0,0,0), [(self.rect.left, self.rect.top+self.rect.height/2-5), (self.rect.left+5, self.rect.top+self.rect.height/2-10), (self.rect.left, self.rect.top+self.rect.height/2-15)], 1)

            pygame.draw.polygon(self.screen, (128,80,0), [(self.rect.right-6, self.rect.top+self.rect.height/2-5), (self.rect.right-1, self.rect.top+self.rect.height/2), (self.rect.right-6, self.rect.top+self.rect.height/2+5)])
            pygame.draw.polygon(self.screen, (0,0,0), [(self.rect.right-6, self.rect.top+self.rect.height/2-5), (self.rect.right-1, self.rect.top+self.rect.height/2), (self.rect.right-6, self.rect.top+self.rect.height/2+5)], 1)


    def draw_connection(self):
        if not self.bar:
            if self.connection:
                if self.connection.value:
                    pygame.draw.line(self.screen, (0, 255, 0), self.connection.connect_out_point, self.connect_in_point, 5)
                else:
                    pygame.draw.line(self.screen, (0, 60, 0), self.connection.connect_out_point, self.connect_in_point, 5)
            if self.connection_2:
                if self.connection_2.value:
                    pygame.draw.line(self.screen, (0, 255, 0), self.connection_2.connect_out_point, self.connect_in_point_2, 5)
                else:
                    pygame.draw.line(self.screen, (0, 60, 0), self.connection_2.connect_out_point, self.connect_in_point_2, 5)
    
    def collidepoint(self, point):
        return self.rect.collidepoint(point)
    
    def delete(self):
        self.deleted = True
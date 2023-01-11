import pygame, ptext

def color(s):
    cd = {"YELLOW": (255, 255, 0), "RED": (255, 0, 0), "GREEN": (0, 255, 40),
          "BLUE": (0, 0, 255), "BLACK": (0,0,0), "WHITE": (255, 255, 255),
          "CYAN": (0, 255, 255), "GREY": (192, 192, 192), "NAVY": (55, 100, 127),
          "LGREY": (104, 122, 163), "GREEN2": (0, 255, 0), "LBLUE": (8, 133, 161),
          "DGREY": (78, 84, 94), "LBLACK": (43,44,51), "PURPLE": (148, 0, 211),
          "ORANGE": (255, 128, 0), "DEBUG_PINK": (168, 50, 135), "GOLD": (255,215,0),
          "DGREEN": (0, 140, 0), "BURPLE": (100, 130, 171)}

    if s in list(cd.keys()):
        return cd[s]
    else:
        print("Error : Color not found!")
        return cd["WHITE"]


def distance(point1, point2):
    return int(pow(pow(point2[1]-point1[1], 2) + pow(point2[0]-point1[0], 2), 0.5))


def draw_arrow(surface, color, start_pos, end_pos, thickness = 2):
    pygame.draw.line(surface, color, start_pos, end_pos, thickness)
    slope = (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])
    dist = distance(start_pos, end_pos)
    # work in progress
    

class ProcessedText():
    def __init__(self, string, color = "WHITE", textFactor = 1, size = 20, surface = None):
        self.frac = 0
        self.textSpeed = 1
        self.textFactor = textFactor
        self.textCounter = 0
        self.pause = False
        self.color = color
        self.text = ""
        self.size = size

        self.surface = surface

        self.string = string

    def build(self):
        if len(self.text) < len(self.string) and self.textCounter % self.textFactor == 0 and self.pause == False:
            self.frac += self.textSpeed
            self.text = self.string[:self.frac]

    def draw(self, position, centerBool = False, build = True, surface = None, backDrop = True, line_width = None, fontname = 'microsoftjhengheimicrosoftjhengheiui'):
        rect = self.get_rect()
        if surface == None and self.surface == None:
            raise Exception
        elif surface == None:
            surface = self.surface

        if build == True:
            self.build()
        else:
            self.text = self.string
            

        true_color = color(self.color) if type(self.color) != tuple else self.color

        if centerBool == False:
            #pygame.draw.rect(surface, game.color("LBLACK"), (rect[0] + position[0] - 10, rect[1] + position[1], rect[2] + 20, rect[3])) if backDrop else None
            ptext.draw(self.text, position, shadow = (0.25, 0.25), sysfontname = fontname,
                   fontsize = self.size, surf = surface, color = true_color, scolor = color("BLACK"), width = line_width)

        else:
            #pygame.draw.rect(surface, game.color("LBLACK"), (rect[0] + position[0] - rect[2]/2 - 10, rect[1] + position[1], rect[2] + 20, rect[3])) if backDrop else None
            ptext.draw(self.text, position, shadow = (0.25, 0.25), sysfontname = fontname, centerx = position[0],
                   fontsize = self.size, surf = surface, color = true_color, scolor = color("BLACK"), width = line_width)


        self.textCounter += 1 if len(self.text) <= len(self.string) else 0

    def get_rect(self):
        textSurface = ptext.getsurf(self.text, shadow = (1,1), sysfontname = 'microsoftjhengheimicrosoftjhengheiui',
                   fontsize = self.size)
        return textSurface.get_rect()

    def get_rect_width(self, lwidth):
        textSurface = ptext.getsurf(self.text, shadow = (1,1), sysfontname = 'arialms',
                   fontsize = self.size, width = lwidth)
        return textSurface.get_rect()



class Button(ProcessedText):
    def __init__(self, string, size = 20, master = None, fxn = lambda : None, fxn_args = None, color = "WHITE"):
        super().__init__(string, color=color, size=size)
        self.fxn = fxn
        self.fxn_args = fxn_args
        self.hasBeenPressed = False
        self.hasBeenReleased = True
        self.master = master
        self.saved_color = self.color
        self.locked = False

    def draw(self, position, m_pos, centerBool = True, build = False):

        #global start_time, lock_buttons

        """if screen == None and self.screen == None:
            screen = game.surface_1
            self.screen = game.surface_1"""

        shift_dim = self.master.position
        
        rect = self.get_rect()
        
        """  DEBUG RECTS, DON'T MIND US
        pygame.draw.rect(self.screen, game.colorDict.get("YELLOW"), (rect[0] + position[0] - 10-rect[2]/2, rect[1] + position[1], rect[2]+20, rect[3]), 2) # centerBool = True
        pygame.draw.rect(self.screen, game.colorDict.get("RED"), (rect[0] + position[0] - 10, rect[1] + position[1], rect[2]+20, rect[3]), 2) # centerBool = False
        pygame.draw.rect(self.screen, game.colorDict.get("CYAN"), (position[0], position[1], 5, 5), 2)
        pygame.draw.rect(self.screen, game.colorDict.get("PURPLE"), (rect[0] + position[0], rect[1] + position[1], rect[2], rect[3]), 2)"""

        #if start_time or self.locked:
            #self.color = game.color("GREY")
        #else:
        #if self.master.start_time:
            #self.color = color("GREY")
        #else:
        self.color = self.saved_color


        def draw_check():
            #global start_time
            #print(pygame.mouse.get_pressed()[0], self.hasBeenReleased, start_time)
            #print(game.cur_menu, self.screen)
            #if game.cur_menu == None and self.screen == game.surface_1:

            """if hasattr(game.cur_menu, "surface"):
                print(game.cur_menu.surface, self.screen, self.text)
            else:
                print(game.cur_screen, self.screen, self.text)"""

            #if (game.cur_menu != None and self.screen == game.cur_menu.surface):

            #if not lock_buttons and not self.locked:
                
            if pygame.mouse.get_pressed()[0] == True and self.hasBeenReleased and self.master.start_time == None:
                self.hasBeenPressed = True
                self.hasBeenReleased = False
                self.master.start_time = pygame.time.get_ticks()
                self.fxn(self.fxn_args) if self.fxn_args != None else self.fxn()

                return True
                
            elif not self.hasBeenReleased:
                self.hasBeenReleased = not pygame.mouse.get_pressed()[0]
                    
        #if not hasattr(game, "pos"):
            #game.pos = pygame.mouse.get_pos()

        if int(m_pos[1]) in range(rect[1]+position[1]+shift_dim[1], rect[1]+position[1]+rect[3]+shift_dim[1]):
            if int(m_pos[0]) in range(rect[0] + position[0] - 10 + shift_dim[0], rect[0] + position[0] - 10 + rect[2] + 20 + shift_dim[0]) and centerBool == False:
                pygame.draw.rect(self.master.surface, color("GREY"), (rect[0]+position[0]-10, rect[1] + position[1], rect[2]+20, rect[3]))
                draw_check()
            elif int(m_pos[0]) in range(rect[0] + position[0] - 10-int(rect[2]/2) + shift_dim[0], rect[0] + position[0] - 10-int(rect[2]/2) + rect[2] + 20 + shift_dim[0]) and centerBool == True:
                pygame.draw.rect(self.master.surface, color("GREY"),
                    (rect[0]+position[0]-10-rect[2]/2, rect[1]+position[1], rect[2]+20, rect[3]))
                draw_check()

        super().draw(position, centerBool, build, surface = self.master.surface)




class Menu():
    def __init__(self, width, height, color_s, master = None):
        self.width = width
        self.height = height
        self.color = color(color_s)
        self.surface = pygame.Surface((self.width, self.height))

        self.subMenu = None
        self.screenTrue = False
        self.collisionTrue = False

        self.master = master

        self.position = 0


    def check_collision(self, position):
        if int(self.master.pos[0]) in range(position[0], position[0]+self.width) and int(self.master.pos[1]) in range(position[1], position[1]+self.height):
            self.master.cur_screen = self.surface
            self.master.cur_menu = self
            self.collisionTrue = True
        else:
            self.collisionTrue = False


    def draw(self, position, draw_border = True):

        self.check_collision(position)

        self.position = position

        self.master.surface.blit(self.surface, position)

        pygame.draw.rect(self.master.surface, self.color,
                         (position[0], position[1], self.width, self.height), 2) if draw_border else None



class ScrollBar:
    def __init__(self, barX, barY, height, scrollY, parent):
        self.barX = barX
        self.barY = barY
        self.height = height
        self.scrollY = scrollY
        self.parent = parent

        self.const = 1

        self.barHeight = 10
        self.barWidth = 16

        self.dragging = False
        
        self.rect = pygame.Rect((self.barX, self.scrollY), (self.barWidth, self.height))
        
        self.canScroll = True

    def draw(self, canDraw = True):
        if canDraw:
            pygame.draw.rect(self.parent.surface, color("DGREY"), ((self.barX, self.barY), (self.barWidth, self.height)), 0)
            pygame.draw.rect(self.parent.surface, color("GREY"), ((self.barX, self.scrollY), (self.barWidth, self.barHeight)), 0)
        else:
            self.dragging = False


    def update(self, canCheck = True):
        global pos
        self.barHeight = min(self.height, self.height * (self.height / self.parent.const))
        self.rect = pygame.Rect((self.barX, self.scrollY), (self.barWidth, self.barHeight))

        #pygame.draw.rect(game.cur_menu.surface, game.color("RED"), self.rect, 2)

        #print(self.rect, (game.pos[0] - game.cur_menu.position[0],
        #                                         game.pos[1] - game.cur_menu.position[1]))

        
        if canCheck and (self.height / self.parent.const) < 1:
            self.draw()
        else:
            self.dragging = False
            

    def move(self, num):
        if self.canScroll and(self.height / self.parent.const) < 1:
            self.scrollY += num
            self.parent.scrollY -= num / (self.height / self.parent.const)
            self.scrollY = min(max(self.scrollY, self.barY), self.height+self.barY-self.barHeight)
            #self.parent.scrollY = min(max(self.parent.scrollY, self.height-self.parent.const), self.barY)
            self.parent.scrollY = min(max(self.parent.scrollY, self.barY+self.height-self.parent.const), self.barY)     

            #print(self.parent.scrollY, self.scrollY+self.height-self.parent.const)

    def set_pos(self, num):
        offset = num - self.scrollY
        self.move(offset)
    

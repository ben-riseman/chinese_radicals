import pygame, sys, math, ptext
import chinese_radicals_testing as cr
from pygame.locals import *
from ben_lib import *

pygame.display.set_icon(pygame.image.load("../leon.jpg"))

pygame.init()
pygame.font.init()

class master:
    def __init__(self):
        self.resolution = (1080, 720)
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.tick_speed = 60
        self.window = pygame.display.set_mode((1080, 720))
        self.surface = pygame.Surface(self.resolution)
        pygame.display.set_caption("Chinese Radical Testing by Benjamin Riseman")
        
        self.title = ProcessedText("Chinese Testing 中文", size = 30,color = "LBLACK", surface = self.surface)

        self.menu = Menu(1060, 585, "BLACK", master = self)
        self.menu.scrollBar = ScrollBar(10, 50, 535, 50, self.menu)
        self.menu.const = 100
        self.menu.scrollY = 50

        #self.start_time = None
        self.menu.start_time = None
        #self.test_button = Button("人", size = 20, master = self.menu, fxn = lambda : print("hi!! :P"), color="BLACK")

        self.test_chars = []
        [self.test_chars.append(VisualCharacter(x, self.menu, y = (x-1)*120)) for x in range(1, len(cr.df)+1)]
        

    def scroll_check(self):
        if self.cur_menu != None and hasattr(self.cur_menu, "scrollBar"):
            sB = self.cur_menu.scrollBar
            self.cur_menu.position = (0,0) if self.cur_menu.position == 0 else self.cur_menu.position
            if sB.rect.collidepoint((self.pos[0] - self.cur_menu.position[0],
                                     self.pos[1] - self.cur_menu.position[1])):
                sB.dragging = True

    def run(self):
        
        self.cur_screen = self.surface
        self.cur_menu =  None
        self.pos = pygame.mouse.get_pos()

        self.surface.fill(color("GREY"))

        self.title.draw((15, 15))


        self.menu.draw((10, 120))

        self.menu.surface.fill(color("WHITE"))

        pygame.draw.line(self.menu.surface, color("BLACK"), (35, 0), (35, 585), 2)
        pygame.draw.line(self.menu.surface, color("BLACK"), (1034, 0), (1034, 585), 2)
        #pygame.draw.rect(self.menu.surface, color("BURPLE"), (37, 2, 997,48))
        
        #pygame.draw.rect(self.menu.surface, color("BLACK"), (9, 29, 9, self.menu.scrollBar.height+1), 2)
        self.menu.scrollBar.update()
        #self.test_button.draw((150, 75), self.pos, build = True)

        self.menu.const = self.test_chars[-1].y + self.test_chars[-1].y_size

        for y in range(0, len(self.test_chars)):
            temp_y = self.menu.scrollY+25+(self.test_chars[y].y)
            self.test_chars[y].draw((75, temp_y)) if temp_y <= 600 else None

        
        #pygame.draw.rect(self.menu.surface, color("WHITE"), (0, 555, 1060, 30))
        
        self.window.blit(self.surface, (0,0))

        self.clock.tick(60)


class VisualCharacter:
    def __init__(self, num, parent, color_s = "DGREEN", y = 0):
        self.num = num
        self.char_obj = cr.m[num]
        self.color = color(color_s)
        self.parent = parent
        self.char = self.char_obj.char
        self.pin = self.char_obj.pinyin if type(self.char_obj.pinyin) != float else "N/A"
        self.eng = self.char_obj.english if type(self.char_obj.english) != float else "N/A"
        self.stroke_count = self.char_obj.stroke_count
        self.memory = self.char_obj.memory

        self.y = y
        self.y_size = 120

        self.do_draw_components = False

        self.position = (0,0)

        
        

        #self.c_string = ProcessedText(self.char, size = 50 , color = "WHITE", surface = self.parent.surface)
        self.c_button = Button(self.char, size = 50 , color = "WHITE", master = self.parent, fxn = self.toggle_components)
        self.pin_string = ProcessedText(self.pin, size = 22, color = "WHITE", surface = self.parent.surface)
        self.eng_string = ProcessedText(self.eng, size = 24, color = "BLACK", surface = self.parent.surface)
        self.sk_string = ProcessedText(str(self.stroke_count), size = 24, color = "BLACK", surface = self.parent.surface)

    def draw(self, position):
        self.position = position
        pygame.draw.rect(self.parent.surface, self.color, (position[0]-20, position[1]-15, 90, 100))
        pygame.draw.rect(self.parent.surface, color("LBLACK"), (position[0]-40, position[1]-25, 1000, 118), 2)
        pygame.draw.line(self.parent.surface, color("BLACK"), (position[0]+90, position[1]-25), (position[0]+90, position[1]+92), 2)
        pygame.draw.line(self.parent.surface, color("BLACK"), (position[0]+140, position[1]-25), (position[0]+140, position[1]+92), 2)
        #self.c_string.draw((position[0], position[1]-10))
        self.c_button.size = 50
        self.c_button.saved_color = color("WHITE")
        self.c_button.draw((int(position[0]), int(position[1]-10)), MASTER.pos, centerBool = False)
        self.pin_string.draw((position[0]+25, position[1]+53), centerBool = True, build = False, fontname = "arialms")
        self.eng_string.draw((position[0]+160, position[1]+20), build = False, fontname = "arialms")
        self.sk_string.draw((position[0]+115, position[1]+20), centerBool = True, build = False, fontname = "arialms")

        if self.do_draw_components:
            self.c_button.size = 35
            self.c_button.saved_color = color("BLACK")
            self.c_button.draw((int(position[0]+25), int(self.y+220+MASTER.menu.scrollY)), MASTER.pos, centerBool = True)
            #pygame.draw.line(self.parent.surface, color("BLACK"), (position[0]+55, self.y+235+MASTER.menu.scrollY),
            #                 (position[0]+95, self.y+195+MASTER.menu.scrollY), 2)
            #self.c_button.draw((int(position[0]+95), int(self.y+195+MASTER.menu.scrollY)), MASTER.pos, centerBool = True)

    def toggle_components(self):
        if self.y_size == 120:
            self.y_size += 240
            MASTER.menu.scrollY -= ((self.y+MASTER.menu.scrollY))
            #MASTER.menu.scrollY = self.y+30
            for n in range(self.num, len(MASTER.test_chars)):
                MASTER.test_chars[n].y += 240

            self.do_draw_components = True
            #if self.num == len(MASTER.test_chars)-1:
            #    MASTER.menu.scrollY += 240
        else:
            self.y_size -= 240
            #MASTER.menu.scrollY+=120
            for n in range(self.num, len(MASTER.test_chars)):
                MASTER.test_chars[n].y -= 240
            self.do_draw_components = False
            #if self.num == len(MASTER.test_chars):
            #    MASTER.menu.scrollY -= 240

        
        
    


MASTER = master()


while True:

    MASTER.run()


    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                MASTER.scroll_check()

            if event.button == 4 and hasattr(MASTER.cur_menu, "scrollBar"):
                const = 5
                MASTER.cur_menu.scrollBar.move(-const) if MASTER.cur_menu != None else None
            if event.button == 5 and hasattr(MASTER.cur_menu, "scrollBar"):
                const = 5
                MASTER.cur_menu.scrollBar.move(const) if MASTER.cur_menu != None else None


        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and MASTER.cur_menu != None and hasattr(MASTER.cur_menu, "scrollBar"):
                MASTER.cur_menu.scrollBar.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if MASTER.cur_menu != None and hasattr(MASTER.cur_menu, "scrollBar"):
                sB = MASTER.cur_menu.scrollBar
                if sB.dragging:
                    sB.set_pos(MASTER.pos[1] - MASTER.cur_menu.position[1] - sB.barHeight/2)


    if MASTER.menu.start_time:
        time_since_enter = pygame.time.get_ticks() - MASTER.menu.start_time
        #print(time_since_enter)
        if time_since_enter >= 200:
            MASTER.menu.start_time = None


    pygame.display.flip()

    

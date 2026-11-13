import pygame
import random
import os



SCREEN_WIDTH = 800
SCREEN_HEIGHT = 660

WHITE  = (255,255,255)
BLACK  = (0,0,0)
RED    = (255,0,0)
GREEN  = (0,220,0)
BLUE   = (0,0,255)
YELLOW = (255,255,0)

LIST_SIZE = 50
SORT_SPEED = 30
N_ALGS = 3

BG_IMAGE    = os.path.join(os.path.dirname(__file__), 'horses/horse.jpg')
HORSE_IMAGE = os.path.join(os.path.dirname(__file__), 'horses/image.png')
HORSE_SONG  = os.path.join(os.path.dirname(__file__), 'horses/horse_song.mp3')

class SortingAlgorithm:
    def __init__(self, lst, display_pos, display_name):
        bg = pygame.image.load(BG_IMAGE)
        bg = bg.convert()
        bg = pygame.transform.grayscale(bg)
        self.bg = pygame.transform.scale(bg, (SCREEN_WIDTH,SCREEN_HEIGHT//N_ALGS - 20))
        self.horse = pygame.image.load(HORSE_IMAGE).convert()
        self.lst = lst.copy()
        self.sorted = False
        self.display_pos  = display_pos
        self.display_name = display_name
        self.font = pygame.font.Font(None, 24)
        self.highlights = []
        

    def step(self):
        pass

    def draw(self, surface: pygame.surface.Surface):
        surface.blit(self.bg, (self.display_pos[0], self.display_pos[1] + 20))
        if self.sorted:
            pygame.draw.rect(surface, GREEN, (*self.display_pos,SCREEN_WIDTH,SCREEN_HEIGHT//N_ALGS))
        # Algorithm Outline
        pygame.draw.rect(surface, WHITE, (*self.display_pos,SCREEN_WIDTH,SCREEN_HEIGHT//N_ALGS), width=1)

        # Algorithm Title
        name = self.font.render(self.display_name, True, WHITE)
        surface.blit(name, ((SCREEN_WIDTH-name.get_width())//2, self.display_pos[1] + 5))

        #Blocks
        width = SCREEN_WIDTH//len(self.lst)
        x = 0
        y_bot = self.display_pos[1]+SCREEN_HEIGHT//N_ALGS

        for block_idx in range(len(self.lst)):
            block = self.lst[block_idx]
            pct = block/LIST_SIZE

            if block_idx in self.highlights:
                col = YELLOW
            else:
                col = (int(255*pct), 0, int(255-255*pct))

            height = int(((SCREEN_HEIGHT)//N_ALGS-20) * pct)
            y = y_bot - height
            horse_block = pygame.transform.scale(self.horse,(width,height))
            #surface.blit(horse_block, (x,y))
            pygame.draw.rect(surface, col, (x,y,width,height))

            x += width

class BubbleSort(SortingAlgorithm):
    def __init__(self, lst, display_pos):
        super().__init__(lst, display_pos, 'Bubble Sort')
        self.i = 0
        self.j = 1
        self.swapped = False
        self.swap = None
    
    def step(self):
        if not self.sorted:
            # Swap step
            if self.swap:
                self.lst[self.swap[0]],self.lst[self.swap[1]] = self.lst[self.swap[1]],self.lst[self.swap[0]]
                self.swap = None
                self.swapped = True
                self.j += 1

                return 

            # For optimized bubble sort, subtract self.i from len(self.lst).
            elif self.j >= len(self.lst) - self.i:
                self.i += 1
                self.j = 1

                if self.i >= len(self.lst) or not self.swapped:
                    self.sorted = True
                    self.i = -1
                    self.j = -1
                    return
                
                self.swapped = False
                
            if self.lst[self.j] < self.lst[self.j-1]:
                self.swap = (self.j-1,self.j)
            else:
                self.j += 1

    def draw(self, surface):
        self.highlights = [self.j-1, self.j]
        super().draw(surface)

class SelectionSort(SortingAlgorithm):
    def __init__(self, lst, display_pos):
        super().__init__(lst, display_pos, 'Selection Sort')
        self.min_idx = 0
        self.i = 0
        self.j = 1

    def step(self):
        if not self.sorted:
            if self.i >= len(self.lst):
                self.sorted = True
            elif self.j >= len(self.lst):
                self.lst[self.i], self.lst[self.min_idx] = self.lst[self.min_idx], self.lst[self.i]
                self.i += 1
                self.min_idx = self.i
                self.j = self.i + 1
            else:
                if self.lst[self.j] < self.lst[self.min_idx]:
                    self.min_idx = self.j

                self.j += 1


    def draw(self, surface):
        self.highlights = [self.min_idx, self.j]
        super().draw(surface)

class BogoSort(SortingAlgorithm):
    def __init__(self, lst, display_pos):
        super().__init__(lst, display_pos, 'Bogo Sort')
        self.maybe_sorted = True
        self.i = 1

    def step(self):
        if not self.sorted:
            if self.maybe_sorted:
                if self.i >= len(self.lst):
                    self.sorted = True

                elif self.lst[self.i] < self.lst[self.i - 1]:
                    self.maybe_sorted = False
                else:
                    self.i += 1

            else:
                random.shuffle(self.lst)
                self.maybe_sorted = True
                self.i = 1

    def draw(self, surface):
        self.highlights = [self.i, self.i-1]
        super().draw(surface)     

class InsertionSort(SortingAlgorithm):
    def __init__(self, lst, display_pos):
        super().__init__(lst, display_pos, 'Insertion Sort')
        self.i = 1
        self.j = 0
        self.v = None

    def step(self):
        if not self.sorted:
            if self.i >= len(self.lst):
                self.sorted = True

            elif self.v == None:
                self.v = self.lst[self.i]
                self.j = self.i - 1
            elif self.j < 0 or self.lst[self.j] < self.v:
                self.lst[self.j+1] = self.v
                self.i += 1
                self.v = None
            else:
                self.lst[self.j + 1] = self.lst[self.j]
                self.j -= 1
    def draw(self, surface):
        self.highlights = [self.i, self.j]
        super().draw(surface)   

class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Sorting Algorithm Race')
        self.clock = pygame.time.Clock()

        self.list_size = LIST_SIZE
        self.speed = SORT_SPEED

        self.lst = [i + 1 for i in range(self.list_size)]
        random.shuffle(self.lst)

        self.algorithms = [BubbleSort(self.lst,    (0,0)),
                           SelectionSort(self.lst, (0,SCREEN_HEIGHT//N_ALGS)),
                           #InsertionSort(self.lst, (0, 2*SCREEN_HEIGHT//N_ALGS)),
                           BogoSort(self.lst,      (0,2*SCREEN_HEIGHT//N_ALGS)),
                           ]
        
        self.start = False


    def main_loop(self):
        pygame.mixer_music.load(HORSE_SONG)
        pygame.mixer_music.play(loops=-1)
        while True:
            self.process_input()
            self.process_logic()
            self.draw()
            self.clock.tick(self.speed)

    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if self.start:
                    pygame.mixer_music.pause()
                else:
                    pygame.mixer_music.unpause()
                self.start = not self.start
                
        
    def process_logic(self):
        if self.start:
            for alg in self.algorithms:
                alg.step()

    def draw(self):
        self.screen.fill(BLACK)
 
        for alg in self.algorithms:
            alg.draw(self.screen)
 
        pygame.display.update()


app = App()
app.main_loop()
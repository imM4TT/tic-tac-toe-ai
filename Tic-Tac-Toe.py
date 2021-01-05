import pygame
from pygame.locals import *
pygame.init()
clock = pygame.time.Clock()

# classe qui gere les imports/methodes pour l'audio
class Sfx():

    def __init__(self):
        global p1_sfx, p2_sfx, end_sfx, music_sfx
        self.p1_sfx = pygame.mixer.Sound("data/play.wav")
        self.p2_sfx = pygame.mixer.Sound("data/play2.wav")
        self.end_sfx = pygame.mixer.Sound("data/end.wav")
        self.music_sfx = pygame.mixer.Sound("data/music.wav")
        pygame.mixer.music.load("data/play.wav")
        pygame.mixer.music.load("data/play2.wav")
        pygame.mixer.music.load("data/end.wav")
        pygame.mixer.music.load("data/music.wav")
        self.music_sfx.set_volume(.1)
        pygame.mixer.music.set_volume(.01)

    def play_music(self, type):
        if type == "music":
            pygame.mixer.Channel(0).play(self.music_sfx)
            pygame.mixer.music.play(-1)
        elif type == "player":
            pygame.mixer.Channel(1).play(self.p1_sfx)
        elif type == "ai":
            pygame.mixer.Channel(1).play(self.p2_sfx)
        elif type == "end":
            pygame.mixer.Channel(1).play(self.end_sfx)

# classe qui contient des constantes de couleur
class Color:
    color = (240, 245, 248)
    color2 = (102, 157, 178)
    color3 = (0, 0, 0)

# classe qui gère l'affichage avec du jeu pyagme
class Affichage:

    def __init__(self, w, h):
        global width, height, grid, w1, w2, h1, h2, w_figure, h_figure
        pygame.display.set_caption('Tic Tac Toe - Human vs AI')
        width = height = 0
        grid = []

        self.screen_x = w
        self.screen_y = h        
        width = self.screen_x/3
        height = self.screen_y/3
        w1 = width
        w2 = 2*width
        h1 = height
        h2 = 2*height
        w_figure = .7 * width
        h_figure = .7 * height

        self.screen = pygame.display.set_mode((self.screen_x, self.screen_y))

        for line in range(3):
            grid.append([])
            for col in range(3):
                if line % 2 == 0:
                    if col % 2 == 0:
                        grid[line].append(0)
                    else:
                        grid[line].append(1)
                else:
                    if col % 2 == 0:
                        grid[line].append(1)
                    else:
                        grid[line].append(0)

        self.show_game()

    def show_game(self):
        for line in range(3):
            for col in range(3):
                c = Color.color if grid[line][col] == 0 else Color.color2
                rect = pygame.Rect([(width)*col, (height)*line, width, height])
                pygame.draw.rect(self.screen, c, rect)
        pygame.display.update()
       
    def click(self, n_line, n_col, currentPlayer):
        posX = ((w1*n_line)+(w1*.5)) - (w_figure/2)
        posY = (h1*n_col)+(h1*.5) - (h_figure/2)
        if currentPlayer == "O":
            rect = pygame.Rect([posY, posX, w_figure, h_figure])
            pygame.draw.arc(self.screen, Color.color3, rect, 0, 360, 7)
        else:
            self.draw_cross(posY, posX)
            #pygame.draw.rect(self.screen, Color.color3, (posX, posY, w_figure, h_figure))
        
        pygame.display.update()

    def draw_cross(self, posX, posY):
        posX_min = posX
        posY_min = posY
        posX_max = posX + w_figure
        posY_max = posY + h_figure
        pygame.draw.aaline(self.screen, Color.color3, (posX_min, posY_min), (posX_max, posY_max))
        pygame.draw.aaline(self.screen, Color.color3, (posX_min, posY_max), (posX_max, posY_min))
        pygame.display.update()

    # affiche l'overlay de fin
    def show_end(self, spot, currentPlayer):
        player = "human" if currentPlayer == "X" else "AI"
        if spot == 1:
            self.msg = "Win of "+player+" ("+currentPlayer+")"
        else:
            self.msg = "Draw"
        self.myfont = pygame.font.SysFont('lucidafax', 50, bold=True)
        self.txt_state = self.myfont.render(self.msg, False, (255, 0, 0))
        txt_reset = self.myfont.render("Reset", False, Color.color3)
        self.reset_layout = pygame.Rect([w1, (self.screen_y*.15)+txt_reset.get_height()*1.05, w1, txt_reset.get_height()*1.05])
        self.img = pygame.image.load("data/img.png").convert_alpha()
        self.img.set_alpha(128)
        self.img = pygame.transform.scale(self.img, (75, self.txt_state.get_height()))

        pygame.draw.rect(self.screen, (255, 0, 0), self.reset_layout)
        self.screen.blit(txt_reset,(w1*1.15, (self.screen_y*.15)+txt_reset.get_height()*1.05))

        pygame.display.update()

    #gère les animations de fin de partie
    def animate(self, posX):
        gray_layout = pygame.Rect([0, self.screen_y*.15,self.screen_x, self.txt_state.get_height()*1.05])        
        
        pygame.draw.rect(self.screen, (220, 220, 220), gray_layout)
        self.screen.blit(self.img, pygame.rect.Rect((self.screen_x-posX)*4,self.screen_y*.15, 80, self.txt_state.get_height()))
        self.screen.blit(self.txt_state,(posX, self.screen_y*.15))  
        pygame.display.update()

# classe qui gère le jeu et ses règles
class Jeu:
    
    def __init__(self):
        self.matrice = [[0] * 3 for i in range(3)]
        self.affichage = Affichage(700, 700)

    # update du joueur actuel
    def new_turn(self, pos, currentPlayer):
        if self.check_cell(pos, currentPlayer):
            self.update_matrice(currentPlayer)
            return True
        else:
            return False

    # vérifie une victoire sur un board
    @staticmethod
    def check_win(matrice, currentPlayer):
        index = 0
        for n_line in range(3):
            for n_col in range(3):
                if matrice[n_line][n_col] == currentPlayer:
                    index += 1
                else:
                    index = 0
                    break # check win on line
            if index >= 3:
                return True
        
        index = 0
        for n_col in range(3):
            for n_line in range(3):
                if matrice[n_line][n_col] == currentPlayer:
                    index += 1
                else:
                    index = 0
                    break  # check win on col 
            if index >= 3:
                return True
        
        index = 0
        for n_line, n_col in zip(range(0, 3, 1), range(0, 3, 1)): 
            if matrice[n_line][n_col] == currentPlayer:
                index += 1
            else:
                break # check win on right diag
        if index >= 3:
            return True
        
        index = 0
        for n_line, n_col in zip(range(0, 3, 1), range(2, -1, -1)): 
            if matrice[n_line][n_col] == currentPlayer:
                index += 1
            else:
                index=0
                break # check win on left diag

        return True if index >= 3 else False

    # vérifie une égalité sur un board
    @staticmethod
    def check_end(matrice): #check si toutes les cases sont jouées
        for n_line in range(3):
            for n_col in range(3):
                if matrice[n_line][n_col] != 0:
                    continue
                else:
                    return False
        return True

    # définit quelle case a été clické
    def check_cell(self, pos, currentPlayer):
        x_i = pos[0]
        y_i = pos[1]
        cell = {"n_line": 0, "n_col": 0}
        # on determine dans quelle colonne le click est fait, ensuite on determine dans quelle ligne
        if x_i < w1: # on se place dans les deux premieres colonnes
            if y_i < h1:# premiere ligne
               cell = {"n_line": 0, "n_col": 0}
            elif y_i < h2: # deuxieme ligne
                cell = {"n_line": 1, "n_col": 0}
            else:
                cell = {"n_line": 2, "n_col": 0}
        elif x_i < w2: # on se placee dans la deuxieme colonne
            if y_i < h1:
                cell = {"n_line": 0, "n_col": 1}
            elif y_i < h2:
                cell = {"n_line": 1, "n_col": 1}
            else:
                cell = {"n_line": 2, "n_col": 1}
        else: # on se palce dans la troisieme colonne
            if y_i < h1:
                cell = {"n_line": 0, "n_col": 2}
            elif y_i < h2:
                cell = {"n_line": 1, "n_col": 2}
            else:
                cell = {"n_line": 2, "n_col": 2}
        self.n_line = cell["n_line"]
        self.n_col = cell["n_col"]
        if self.matrice[self.n_line][self.n_col] == 0:
            return True
        else:
            return False
    
    def update_matrice(self, currentPlayer):
        self.matrice[self.n_line][self.n_col] = currentPlayer
        self.affichage.click(self.n_line, self.n_col, currentPlayer)

    def get_matrice(self):
        return self.matrice

    def set_pos(self, n, c):
        self.n_line = n
        self.n_col = c

# classe qui gère l'IA
class AI:

    aiPlayer = "O"
    huPlayer = "X"

    def think(self, matrice, currentTurn):
        if(currentTurn == 0):
            pos = self.play_on_first_turn(matrice)
        else:
            pos = self.solve(matrice, "O", 0)
        self.update_optimized_pos(pos)

        print("coup résolu")

    # parcours toutes les possibilités de jeu et renvoie la cellule avec le meilleur taux de victoire ou de nul
    def solve(self, matrice, currentPlayer, depth):
        depth += 1 # profondeur de récursion
        # print(depth)
        if Jeu.check_win(matrice, AI.aiPlayer): # lorsque AI gagne
            return 10
        elif Jeu.check_win(matrice, AI.huPlayer): # lorsque joueur gagne
            return -10
        elif Jeu.check_end(matrice):
            return 0                        
                                            
        node = [] # contient la valeur heuristique pour chaque case vide                     
        # parcours de toutes les cellules, pour chaque cellule ou l'on peut jouer on simule un déroulement de partie avec toutes les possibilités jusqu'a ce que ce que la partie soit fini
        for n_line in range(3):             
            for n_col in range(3):
                if self.check_cell(matrice, n_line, n_col):
                    matrice[n_line][n_col] = currentPlayer
                    if currentPlayer == AI.aiPlayer: # IA = O
                        value = self.solve(matrice, AI.huPlayer, depth)
                    else:
                        value = self.solve(matrice, AI.aiPlayer, depth)

                    move = [n_line, n_col, value]

                    matrice[n_line][n_col] = 0
                    
                    node.append(move)
                    
        
        best_move_idx = 0
        if currentPlayer == AI.aiPlayer:
            best_score = -10000
            for i in range(0, len(node)):
                value = node[i][2]
                if value > best_score:
                    best_score = value
                    best_move_idx = i

        else:
            best_score = 10000
            for i in range(0, len(node)):
                value = node[i][2]
                if value < best_score:
                    best_score = value
                    best_move_idx = i

        # retourne la valeur du meilleur coup en fonction de sa profondeur, plus un coup est anticipé moins il est fiable
        return node[best_move_idx][2]/depth if depth != 1 else [node[best_move_idx][0], node[best_move_idx][1]] # on retourne la valeur du chemin en question ou la case à jouer lorsque c'est resolu

     # verifie si on peut jouer sur cette case, si elle est vide
    def check_cell(self, matrice, n_line, n_col):
        if matrice[n_line][n_col] == 0:
            return True
        return False

    # définit la ligne et la colonne sur laquelle l'IA va jouer
    def update_optimized_pos(self, posYX):
        self.solved_line, self.solved_col = posYX

    # premier tour pour l'IA
    def play_on_first_turn(self, matrice):
        return [1, 1] if matrice[1][1] == 0 else [0, 0]

# classe (mère) qui gère l'avancement du jeu
class MorpionManager:

    def __init__(self, w, h):
        self.sfx = Sfx()
        self.jeu = Jeu()
        self.ai = AI()
        self.run = True
        self.end = False
        self.currentPlayer = "X"
        self.currentTurn = 0
        self.posX = -999
        self.start()

    def start(self):
        self.sfx.play_music("music")
        while self.run:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and self.end == False and self.currentPlayer == "X":
                    if self.jeu.new_turn(pygame.mouse.get_pos(), self.currentPlayer):
                        self.sfx.play_music("player")
                        res = self.check_end()
                        if res != 0:
                            continue
                        self.change_turn()
                        self.AI_play()
                        self.change_turn()
                if event.type == pygame.MOUSEBUTTONDOWN and self.end:
                    self.check_reset(pygame.mouse.get_pos())
                if event.type == pygame.QUIT:
                    run = False
                    pygame.display.quit()
                    pygame.quit()
                    exit(0)
            if self.end:
                if self.posX == -999:
                    self.posX =  0 - (self.jeu.affichage.txt_state.get_width())
                self.posX += 5
                if self.posX > self.jeu.affichage.screen_x:
                    self.posX = 0 - (self.jeu.affichage.txt_state.get_width())
                self.jeu.affichage.animate(self.posX)
    
    def change_turn(self):
        if self.currentPlayer == "X":
            self.currentPlayer = "O"
        else:
            self.currentTurn += 1
            self.currentPlayer = "X"

    def AI_play(self):
        self.ai.think(self.jeu.get_matrice(), self.currentTurn)
        pygame.time.wait(500)
        self.jeu.set_pos(self.ai.solved_line, self.ai.solved_col)
        self.jeu.update_matrice(self.currentPlayer)
        self.sfx.play_music("ai")
        res = self.check_end()
            
    def check_end(self):
        win = Jeu.check_win(self.jeu.get_matrice(), self.currentPlayer)
        end = Jeu.check_end(self.jeu.get_matrice())
        if win:
            print("Win of "+self.currentPlayer)
            self.jeu.affichage.show_end(1, self.currentPlayer)
            self.end = True
            self.sfx.play_music("end")
            return 1
        elif end:
            print("Draw")
            self.jeu.affichage.show_end(2, self.currentPlayer)
            self.end = True
            self.sfx.play_music("end")
            return 2
        return 0

    def check_reset(self, pos):
        x_min = self.jeu.affichage.reset_layout.left
        x_max = self.jeu.affichage.reset_layout.right
        y_min = self.jeu.affichage.reset_layout.top
        y_max = self.jeu.affichage.reset_layout.bottom
        if(pos[0] > x_min and pos[0] < x_max):
            if(pos[1] > y_min and pos[1] < y_max):
                print("click on reset")
                pygame.display.quit()
                m = MorpionManager(700, 700)


MM = MorpionManager(700, 700)
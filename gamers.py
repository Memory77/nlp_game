import pygame
import random


class Gamer(pygame.sprite.Sprite):
    def __init__(self, x, y, id, player_name, personnage):
        super().__init__()
        self.image = pygame.image.load('img/big_player_one.png')
        self.rect = self.image.get_rect(topleft=(x, y))
        self.id = id
        self.player_name = player_name
        self.x = x
        self.y = y
        self.camembert_part = [] #ou voir pour mettre 0 plutot
        self.score = 0
        self.sound = []
        self.personnage = personnage
        self.current_camembert = None
        self.lore = ""
        self.caracter = ""
        
    def set_position(self, row, col, cell_width, cell_height):
        # définit la position du sprite basée sur la position de la cellule du tableau
        self.rect.x = col * cell_width
        self.rect.y = row * cell_height
        self.x = col
        self.y = row

    def move(self, direction, cell_height, cell_width, game):
        sound = pygame.mixer.Sound('sounds/step.wav')
        sound.play()
        
        
        if direction == "up":
            self.rect.y -= cell_height
            self.y -= 1
            if self.rect.y < 0:
                self.rect.y = (game.board_game_height - 1) * cell_height
                self.y = game.board_game_height - 1
        elif direction == "down":
            self.rect.y += cell_height
            self.y += 1
            if self.rect.y > (game.board_game_height - 1) * cell_height:
                self.rect.y = 0
                self.y = 0
        elif direction == "left":
            self.rect.x -= cell_width
            self.x -= 1
            if self.rect.x < 0:
                self.rect.x = (game.board_game_width - 1) * cell_width
                self.x = game.board_game_width - 1
        elif direction == "right":
            self.rect.x += cell_width
            self.x += 1
            if self.rect.x > (game.board_game_width - 1) * cell_width:
                self.rect.x = 0
                self.x = 0
        
        # boucle déplaçant les autres joueurs
        for gamer in game.gamers:
            if self.id != gamer.id:
                if self.rect.x == gamer.rect.x and self.rect.y == gamer.rect.y:
                    gamer.move(direction, cell_height, cell_width, game)
            
            
    def set_params(self,personnage):
        if personnage == 1: 
            self.image = pygame.image.load('img/big_player_one.png')
            self.sound.append('deadpool.wav')
            self.sound.append('alright-already.wav')
            self.sound.append('are-you-crazy.wav')
            self.caracter = "Deadpool"
            self.lore = ""
        elif personnage == 2: 
            self.image = pygame.image.load('img/big_player_two.png')
            self.sound.append('captain_america.wav')
            self.caracter = "Captain America"
            self.lore = ""
        elif personnage == 3:
            self.image = pygame.image.load('img/big_player_tree.png')
            self.sound.append('work-work.wav')
            self.sound.append('humain-travail.wav')
            self.sound.append('orc.wav')
            self.caracter = "brute"
            self.lore = "Tu es un orc agressif et cruel. Tu as perdu 6 joyaux de couleurs diff\u00e9rentes. Si tu r\u00e9cup\u00e8res un joyau alors ton agressivit\u00e9 diminue l\u00e9g\u00e8rement. Tu ne deviens calme et gentil que si tu as tes 6 joyaux en ta possession. Apr\u00e8s une pr\u00e9sentation, tu proposes une qu\u00eate pour l'aventurier. Tu donneras une qu\u00eate par joyau, ils ont chacun une couleur : bleu, rouge, vert, violet, marron, orange. Tu portes deux grosses haches, une cuirasse en cuir et des bottes en cuir clout\u00e9es. Les joyaux sont des reliques de ton peuple d\u00e9chu et vaincus par les humains. Tu as un style particulier pour parler, tu as des petits tics de langage typique des orcs. R\u00e9ponds aux questions en te basant sur ce contexte."
        elif personnage == 4:
            self.image = pygame.image.load('img/big_player_four.png')
            self.sound.append('naruto-chakra.wav')
            self.sound.append('ha-ha.wav')
            self.caracter = "Naruto"
            self.lore = ""
        elif personnage == 5:
            self.image = pygame.image.load('img/big_player_five.png')
            self.sound.append('naruto-chakra.wav')
            self.sound.append('ha-ha.wav')
        elif personnage == 6:
            self.image = pygame.image.load('img/big_player_six.png')
            self.sound.append('alright-we-turn-it-on-im-very-thirsty.wav')
            self.sound.append('just-want-you.wav')
        elif personnage == 7:
            self.image = pygame.image.load('img/big_player_seven.png')
            self.sound.append('dragon-spell.wav')
        elif personnage == 8:
            self.image = pygame.image.load('img/big_player_eight.png')
            self.sound.append('ninja.wav')
        else:
            self.image = pygame.image.load('img/big_player_tree.png')
            self.sound.append('work-work.wav')
            self.sound.append('humain-travail.wav')
            self.sound.append('orc.wav')
            
    def yell(self):
       
        if self.score <= -500:
            sound = pygame.mixer.Sound('sounds/angry_3.wav')
        else:
            random_sound = random.choice(self.sound)
            sound = pygame.mixer.Sound(f"sounds/{random_sound}")
        sound.play()   
    
       
    def check_camembert(self, camembert_sprites):
        for camembert in camembert_sprites:
            if self.rect.colliderect(camembert.rect) and camembert.color not in self.camembert_part:
                return True
        return False
    
    def take_camembert(self, camembert_sprites, cell_width, cell_height, game, game_board):
        for camembert in camembert_sprites:
            if self.rect.colliderect(camembert.rect) and camembert.color not in self.camembert_part:
                self.score += game.camembert_question_points
                camembert.kill()
                self.camembert_part.append(camembert.color)
                
                #generation d'un nouveau camembert aléatoirement 
                number_min = 0
                number_rows = game.board_game_height - 1
                number_cols = game.board_game_width - 1
                # on remet un camembert d'une couleur donnée sur une case de la même couleur
                color_question_target = ""
                while color_question_target != camembert.color_question:
                    y = random.randint(number_min, number_rows)
                    x = random.randint(number_min, number_cols)
                    color_question_target = game_board[y][x]
                
                new_camembert = Element(0, 0, "camembert", camembert.color)
                new_camembert.set_position(y, x, cell_width, cell_height)
                new_camembert.set_image()
                camembert_sprites.add(new_camembert)
                
                # print(game.board_game_height)
                # print(game.board_game_width)
                # print(camembert_sprites)
                # print(self.camembert_part)
    
    def check_fall(self, fall_sprites, gamers_sprite, cell_width, cell_height, game):
        for fall in fall_sprites:
            for gamer in gamers_sprite:
                if self.rect.colliderect(fall.rect):
                    #set position aléatoirement 
                    number_min = 0
                    number_rows = game.board_game_height - 1
                    number_cols = game.board_game_width - 1
                    y = random.randint(number_min, number_rows)
                    x = random.randint(number_min, number_cols)
            
                    self.set_position(y, x, cell_width, cell_height)
                    self.score += game.hole_points
                    sound_fall = pygame.mixer.Sound('sounds/fall.wav')
                    sound_fall.play()
                    
                if gamer.rect.colliderect(fall.rect):
                    #set position aléatoirement 
                    number_min = 0
                    number_rows = game.board_game_height - 1
                    number_cols = game.board_game_width - 1
                    y = random.randint(number_min, number_rows)
                    x = random.randint(number_min, number_cols)
            
                    gamer.set_position(y, x, cell_width, cell_height)
                    gamer.score += game.hole_points
                    sound_fall = pygame.mixer.Sound('sounds/fall.wav')
                    sound_fall.play()
                   


class Element(pygame.sprite.Sprite):
    def __init__(self, x, y, name_element, color = 'yellow'):
        super().__init__()
        self.image = pygame.image.load('img/mini_player_one.png')
        self.rect = self.image.get_rect(topleft=(x, y))
        self.name_element = name_element
        self.color = color
        
    def set_position(self, row, col, cell_width, cell_height):
        # définit la position du sprite basée sur la position de la cellule du tableau
        self.rect.x = col * cell_width + 15
        self.rect.y = row * cell_height  + 10
        self.x = col
        self.y = row

    def set_image(self):
        if self.name_element == "fall":
            self.image = pygame.image.load('img/fall.png')

        elif self.name_element == "camembert":
            if self.color == "pink":
                self.color_question = "SQL"
                self.image = pygame.image.load('img/pink.png')
            elif self.color == "blue":
                self.image = pygame.image.load('img/blue.png')
                self.color_question = "Ligne de commandes"
            elif self.color == "green":
                self.image = pygame.image.load('img/green.png')
                self.color_question = "Python"
            elif self.color == "yellow":
                self.image = pygame.image.load('img/yellow.png')
                self.color_question = "Actualités IA"
            elif self.color == "purple":
                self.image = pygame.image.load('img/purple.png')
                self.color_question = "Git/GitHub"
            elif self.color == "orange":
                self.image = pygame.image.load('img/orange.png')
                self.color_question = "Culture"

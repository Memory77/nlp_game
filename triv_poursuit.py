import pygame
import numpy as np
from gamers import *
import random
import main
import sql_game
import os
import openai
from dotenv import load_dotenv

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Récupérer les valeurs des variables d'environnement
api_key = os.getenv('openai_api_key')
api_base = os.getenv('openai_api_key_base')
api_deployment = os.getenv('openai_api_deployment')
api_version = os.getenv('openai_api_version')

# Configurer l'API OpenAI avec les informations d'Azure
openai.api_key = api_key
openai.api_base = api_base
openai.api_type = 'azure'
openai.api_version = api_version

def get_response(prompt, conversation_partner, player):
    character = conversation_partner.caracter
    lore = conversation_partner.lore
    partner_score = conversation_partner.score
    
    if partner_score <= -500:
        character = "très méchant car on je t'ai fait du mal, je t'ai fait tomber dans des trous donc tu es remonté contre moi. Si jamais je te donne un camembert, tu acceptes de me faire pardonner."
    
    if 'je te donne un camembert' in prompt and player.camembert_part:
        conversation_partner.score += 250
        player.camembert_part.pop()
    
    preprompt = f"Tu es entrain de parler avec une personne dans un village. Tu es un personnage avec les traits de caractères suivants:\n {character}\nHistoire: {lore}\n"
    #full_prompt = preprompt + prompt

    response = openai.ChatCompletion.create(
        engine=api_deployment,
        messages=[
            {"role": "system", "content": preprompt},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100
    )
    print("Réponse brute de l'API:", response)
    
    # Extraction du contenu de la réponse en vérifiant les différentes structures possibles
    try:
        return response['choices'][0]['message']['content'].strip()
    except KeyError:
        return response['choices'][0]['text'].strip()


# quelques fonctions, à mettre sûrement dans un autre fichier plus tard
def draw_button(screen, text, x, y, width, height, active_color, inactive_color, font_size):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))
    
    font = pygame.font.SysFont(None, font_size)
    text_surf = font.render(text, True, (0, 0, 0))
    text_rect = text_surf.get_rect()
    text_rect.center = ((x + (width / 2)), (y + (height / 2)))
    screen.blit(text_surf, text_rect)
    return False

def auto_wrap(text: str, nb_characters: int) -> str:
    # permet de faire les retours à la ligne automatiquement
    words = text.split(' ')
    wrapped_lines = []
    
    for word in words:
        if len(wrapped_lines) == 0:
            wrapped_lines.append('')
        test_line = wrapped_lines[-1] + word + ' '
        
        if len(test_line) < nb_characters:
            wrapped_lines[-1] = test_line
        else:
            wrapped_lines.append(word + ' ')

    return wrapped_lines

def are_players_adjacent(player1, player2):
    return abs(player1.x - player2.x) <= 1 and abs(player1.y - player2.y) <= 1

def draw_dialogue_box(screen, text, x, y, width, height, color):
    font = pygame.font.SysFont(None, 25)
    pygame.draw.rect(screen, color, (x, y, width, height))
    wrapped_lines = auto_wrap(text, 40)
    for i, line in enumerate(wrapped_lines):
        text_surf = font.render(line, True, (0, 0, 0))
        screen.blit(text_surf, (x + 10, y + 10 + i * 20))

# AFFICHAGE PYGAME

# Initialisation de Pygame
pygame.init()

pygame.mixer.init() 

music_list = ['moonwalker.wav',
              #'Fort_Boyard.wav',
              ]
random_music = random.choice(music_list)
music = pygame.mixer.music.load(f"sounds/{random_music}")
pygame.mixer.music.set_volume(0.3) #1.0 volume max
if random_music == 'Fort_Boyard.wav':
    pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play(-1)

width, height = 1800, 1000  # Ajustez selon vos besoins
screen = pygame.display.set_mode((width, height))

## === INTERFACE (côté droit, pour tout ce qui est interaction questions etc.)
# dimensions de l'interface
interface_width = 500  
interface_height = height  # même hauteur que votre fenêtre de jeu
interface_x = width - interface_width  #  positionne l'interface à droite
interface_y = 0  #  positionne l'interface en haut de l'écran

interface_bg_color = (255, 255, 255)
interface_image = pygame.image.load('img/interface_img.png')  
interface_image = pygame.transform.scale(interface_image, (interface_width, interface_height))  # redimensionner l'image

# dimensions du bouton principal de l'interface pour l'interaction (dé, questions etc)
button_x = interface_x + 50
button_y = 100
button_width = 400
button_height = 50
active_color = (255, 105, 180)
inactive_color = (10, 210, 255)
answer_active_color = (255, 180, 105)
answer_inactive_color = (10, 255, 210)

## === PLATEAU DE JEU (côté gauche, cependant, il est réellement défini dans la boucle de jeu car doit se mettre à jour)
# liste contenant les id de toutes les catégories 
cat_id = []
colors = {}
for categorie in sql_game.categories():
    cat_id.append(categorie[0])
    colors[categorie[0]] = (categorie[1], categorie[2], categorie[3])

np.random.seed(5) # graine pour figer le random choice 
game_board = np.random.choice(cat_id, size=(main.board_game_height, main.board_game_width))

# import du nouveau jeu
game = main.new_game()

# définition de la largeur du plateau de jeu en soustrayant la largeur de l'interface
game_board_width = width - interface_width

# définition des cellules par rapport au playing board et des dimensions de l'écran afin de pouvoir positionner les entités après
cell_width = game_board_width  // game.board_game_width
cell_height = height // game.board_game_height

# === INITIALISATION DES JOUEURS ET DES ÉLÉMENTS 
# création des joueurs 
gamer_sprites = pygame.sprite.Group()
joueurs = []
game_gamers_sprite = game.gamers_sprite()
for gamer in game_gamers_sprite:
    joueurs.append(gamer)
    gamer_sprites.add(gamer)
    gamer.set_position(gamer.y, gamer.x, cell_width, cell_height)
    gamer.set_params(gamer.personnage)
print(f'''Que le jeu TRIV POURSUITE IA COMMENCE !
      
      Tu dois avoir ton score supérieur ou égal à {game.end_game_max_points} ou récolter les {game.end_game_max_camembert} camemberts de couleur
      en répondant aux questions pour remporter la victoire !
      Bonne chance :) 
      ''')

# création des camemberts
camembert_pink = Element(0, 0, "camembert", "pink")
camembert_green = Element(0, 0, "camembert", "green")
camembert_blue = Element(0, 0, "camembert", "blue")
camembert_yellow = Element(0, 0, "camembert", "yellow")
camembert_purple = Element(0, 0, "camembert", "purple")
camembert_orange = Element(0, 0, "camembert", "orange")

camembert_sprites = pygame.sprite.Group()
camembert_sprites.add(camembert_pink)
camembert_sprites.add(camembert_green)
camembert_sprites.add(camembert_blue)
camembert_sprites.add(camembert_yellow)
camembert_sprites.add(camembert_purple)
camembert_sprites.add(camembert_orange)

# création des trous
fall_one = Element(0, 0, "fall")
fall_two = Element(0, 0, "fall")

fall_sprites = pygame.sprite.Group()
fall_sprites.add(fall_one)
fall_sprites.add(fall_two)

# requalification de la position et de l'image du camembert (6 camemberts disposés dans le plateau)
camembert_pink.set_position(2, 11, cell_width, cell_height)
camembert_pink.set_image()

camembert_green.set_position(11, 21, cell_width, cell_height)
camembert_green.set_image()

camembert_blue.set_position(10, 5, cell_width, cell_height)
camembert_blue.set_image()

camembert_yellow.set_position(2, 1, cell_width, cell_height)
camembert_yellow.set_image()

camembert_purple.set_position(7, 12, cell_width, cell_height)
camembert_purple.set_image()

camembert_orange.set_position(2, 20, cell_width, cell_height)
camembert_orange.set_image()

# idem pour le trou
fall_one.set_position(10, 13, cell_width, cell_height)
fall_one.set_image()

fall_two.set_position(3, 13, cell_width, cell_height)
fall_two.set_image()

# États de jeu
ETAT_JEU = 1
etat_jeu = ETAT_JEU
current_player_index = 0
conversation_open = False
input_text = ""
chat_history_ids = None
conversation_partner = None

# Boucle principale
running = True
while running:
    # définition visuelle du plateau (qui est remis à jour à chaque tour dans la boucle)
    for i in range(game.board_game_height):
        for j in range(game.board_game_width):
            rect = pygame.Rect(j * cell_width, i * cell_height, cell_width, cell_height)
            pygame.draw.rect(screen, colors[game_board[i][j]], rect)

    # définition des lignes du playing_board
    line_color = (255, 255, 255)
    # Dessiner les lignes verticales
    for j in range(game.board_game_width):  
        pygame.draw.line(screen, line_color, (j * cell_width, 0), (j * cell_width, height))
    # Dessiner les lignes horizontales
    for i in range(game.board_game_height): 
        pygame.draw.line(screen, line_color, (0, i * cell_height), (game_board_width, i * cell_height))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN and not conversation_open:
            if event.key == pygame.K_LEFT:
                joueurs[current_player_index].move("left", cell_height, cell_width, game)
            elif event.key == pygame.K_RIGHT:
                joueurs[current_player_index].move("right", cell_height, cell_width, game)
            elif event.key == pygame.K_UP:
                joueurs[current_player_index].move("up", cell_height, cell_width, game)
            elif event.key == pygame.K_DOWN:
                joueurs[current_player_index].move("down", cell_height, cell_width, game)
            joueurs[current_player_index].check_camembert(camembert_sprites)
            joueurs[current_player_index].take_camembert(camembert_sprites, cell_width, cell_height, game, game_board)
            joueurs[current_player_index].check_fall(fall_sprites, gamer_sprites, cell_width, cell_height, game)

            if event.key == pygame.K_SPACE:  # espace pour la confirmation de la fin du tour
                current_player_index = (current_player_index + 1) % main.nb_gamers
                joueurs[current_player_index].yell()
                print(f"Passage au joueur {current_player_index + 1}")

        if event.type == pygame.KEYDOWN and conversation_open:
            if event.key == pygame.K_RETURN:
                response = get_response(input_text, conversation_partner, joueurs[current_player_index])
                conversation_partner.yell()
                input_text = ""
                print(f"{conversation_partner.player_name}: {response}")
                draw_dialogue_box(screen, response, 400, 700, 1000, 200, (255, 255, 255))

            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode

    # définition visuelle de l'interface
    interface_rect = pygame.Rect(interface_x, interface_y, interface_width, interface_height)
    pygame.draw.rect(screen, interface_bg_color, interface_rect)
    # pour afficher l'image de l'interface
    screen.blit(interface_image, (interface_x, interface_y))

    # mise à jour des scores
    button_start_x = 1300  
    button_start_y = 800   
    button_x_ = button_start_x
    button_y_ = button_start_y

    max_buttons_per_row = 4  # nombre maximal de boutons par ligne
    button_count = 0  # cpt de boutons pour contrôler la création de nouvelles lignes

    for gamer in gamer_sprites:
        draw_button(screen, gamer.player_name, button_x_, button_y_, 150, button_height, active_color, inactive_color, 25)
        draw_button(screen, f"{gamer.score}    {len(gamer.camembert_part)}/{game.end_game_max_camembert}", button_x_, button_y_ + 50, 150, button_height, active_color, inactive_color, 25)

        # mise à jour des positions des boutons pour le prochain joueur
        button_x_ += 130
        button_count += 1

        # Passer à la ligne suivante si le nombre maximal de boutons est atteint
        if button_count >= max_buttons_per_row:
            button_x_ = button_start_x
            button_y_ += 100  # Augmenter de 100 pour la prochaine ligne
            button_count = 0
    
    # mise à jour le texte du bouton en fonction de l'état du jeu
    texte_bouton = f"{joueurs[current_player_index].player_name} : Déplacez-vous"
    draw_button(screen, texte_bouton, button_x, button_y, button_width, button_height, active_color, inactive_color, 40)
        
    # affichage des différentes catégories
    category_button_y = 550
    category_button_x = 1450
    category_button_width = 200
    category_button_height = 40
    incr_y = 40
    for categorie in sql_game.categories():
        category_color = (categorie[1], categorie[2], categorie[3])
        draw_button(screen, categorie[0], category_button_x, category_button_y, category_button_width, category_button_height, category_color, category_color, 25)
        category_button_y += incr_y

    # dessiner les différents groupe de sprites
    gamer_sprites.draw(screen)
    gamer_sprites.update()
    
    camembert_sprites.draw(screen)
    camembert_sprites.update()
    
    fall_sprites.draw(screen)
    fall_sprites.update()

    # vérifier la proximité des joueurs et afficher le bouton "Dialoguer"
    if not conversation_open:
        for i, gamer1 in enumerate(joueurs):
            for j, gamer2 in enumerate(joueurs):
                if i != j and are_players_adjacent(gamer1, gamer2):
                    if draw_button(screen, "Dialoguer", 50, 850, 200, 50, active_color, inactive_color, 30):
                        conversation_open = True
                        conversation_partner = gamer2 if current_player_index == i else gamer1

    # afficher la fenêtre de conversation si elle est ouverte
    if conversation_open:
        draw_dialogue_box(screen, f"Conversation avec {conversation_partner.player_name}", 400, 400, 1000, 200, (255, 255, 255))
        draw_dialogue_box(screen, input_text, 400, 620, 1000, 50, (200, 200, 200))
        if draw_button(screen, "Fermer", 1300, 550, 100, 50, active_color, inactive_color, 30):
            conversation_open = False
    
    # conditions de victoire et retourne le gagnant
    winner = game.victory()

    if winner is not None:
        win_text = f"Le gagnant est {winner.player_name} avec un score de {winner.score}"
        print(win_text)
        draw_button(screen, win_text, 200, 200, 900, 500, inactive_color, inactive_color, 50)
        screen.blit(winner.image, (620, 500))
        music = pygame.mixer.music.load('sounds/Benny_Hill_Theme.wav')
        pygame.mixer.music.set_volume(0.5) # 1.0 volume max
        pygame.mixer.music.play(-1)
        pygame.display.flip()
        pygame.time.delay(10000) # en millisecondes 
        running = False
    
    # Mettre à jour l'écran
    pygame.display.flip()

# enregistrement de la partie
sql_game.end_game(game.id)
for gamer in gamer_sprites:
    sql_game.gamer_end_game(game.id, gamer.id, gamer.score, len(gamer.camembert_part))
import last_game
pygame.quit()

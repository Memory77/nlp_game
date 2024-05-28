import sqlite3
import os
import sys
import pandas as pd 

def query_execute(cur, query: str, select: str = ''):
    # permet d'essayer d'exécuter une requête et de renvoyer les données
    # si la requête ne fonctionne pas, un print sera fait de la requête intégrant les paramètres
    # la requête pourra être réexécuée à l'identique dans DVeaver pour débogage

    try:
        cur.execute(query)
        if select == 'SELECT':
            return cur.fetchone()
        if select == 'SELECT_ALL':
            return cur.fetchall()

    except:
        query_error(query)


def query_error(query: str):
    # print des requêtes d'effectueuses

    print("")
    print("/!\\")
    print("La requête suivant n'a pas pu être exécutée : ", query)
    print("/!\\")
    print("")


def all_gamers(cur) -> str:
    return query_execute(cur, f'SELECT * FROM gamer', 'SELECT_ALL')


def categories():
    conn = sqlite3.connect('triv_ia_dlc.db')
    cur = conn.cursor()
    
    res = query_execute(cur, f'SELECT * FROM categorie', 'SELECT_ALL')

    conn.close()

    return res


# relie les bases de données avec le code  


def question(gamer_id: int, categorie: str):
    conn = sqlite3.connect('triv_ia_dlc.db')
    cur = conn.cursor()

    res = query_execute(cur, f'''
                        SELECT DISTINCT question
                        FROM question_answer qa 
                        LEFT OUTER JOIN question_already_answered qaa
                                        ON qaa.question_answer_categorie = qa.categorie_name
                                        AND qaa.question_answer_question = qa.question
                                        AND qaa.gamer_id = {gamer_id}
                        WHERE categorie_name = "{categorie}"
                        AND qaa.gamer_id IS NULL
                        ORDER BY random()
                        LIMIT 1''', 'SELECT')

    
    if res == None:
        query_execute(cur, f'''
                        DELETE FROM question_already_answered
                        WHERE gamer_id = {gamer_id}
                        AND question_answer_categorie = "{categorie}"
                        ''')
        res = query_execute(cur, f'''
                        SELECT DISTINCT question
                        FROM question_answer qa 
                        LEFT OUTER JOIN question_already_answered qaa
                                        ON qaa.question_answer_categorie = qa.categorie_name
                                        AND qaa.question_answer_question = qa.question
                                        AND qaa.gamer_id = {gamer_id}
                        WHERE categorie_name = "{categorie}"
                        AND qaa.gamer_id IS NULL
                        ORDER BY random()
                        LIMIT 1''', 'SELECT')

    conn.close()
    return res[0]


def answers(categorie: str, question: str):
    conn = sqlite3.connect('triv_ia_dlc.db')
    cur = conn.cursor()

    res = query_execute(cur, f'''
                        SELECT answer, good_answer
                        FROM question_answer
                        WHERE categorie_name = "{categorie}"
                        AND question = "{question}"
                        ''', 'SELECT_ALL')
    conn.close()

    return res


def good_answers(categorie: str, question: str, answer: str):
    conn = sqlite3.connect('triv_ia_dlc.db')
    cur = conn.cursor()
    
    
    res = query_execute(cur, f'''
                        SELECT good_answer 
                        FROM question_answer
                        WHERE categorie_name = "{categories}" 
                        AND question = "{question}"
                        AND answer = "{answer}" 
                        ''', 'SELECT_ALL')
    conn.close()
    if res[0] == 1:
        return True
    else:
        return False


def question_already_answered(current_player_index: int, case_categorie_id: str, question: str):
    conn = sqlite3.connect('triv_ia_dlc.db')
    cur = conn.cursor()
    
    query_execute(cur, f'''
    INSERT INTO question_already_answered VALUES ({current_player_index}, "{case_categorie_id}", "{question}")
    ''', '')

    conn.commit()
    conn.close()
    


def create_game(dice_type: int):
    conn = sqlite3.connect('triv_ia_dlc.db')
    cur = conn.cursor()
    
    query_execute(cur, f'''
    INSERT INTO game (date_start, dice_type) VALUES (datetime('now'), {dice_type})
    ''', '')

    conn.commit()
    conn.close()
    


def game_id():
    conn = sqlite3.connect('triv_ia_dlc.db')
    cur = conn.cursor()
    
    res = query_execute(cur, f'''
    SELECT MAX(id) FROM game
    ''', 'SELECT')

    conn.close()
    return res[0]

def link_game_gamer(game_id: int, gamer_id: int, alias: str):
    conn = sqlite3.connect('triv_ia_dlc.db')
    cur = conn.cursor()
    
    query_execute(cur, f'''
    INSERT INTO game_gamer VALUES ({game_id}, {gamer_id}, "{alias}", 0, 0)
    ''', '')

    conn.commit()
    conn.close()


def end_game(game_id: int):
    conn = sqlite3.connect('triv_ia_dlc.db')
    cur = conn.cursor()
    
    query_execute(cur, f'''
    UPDATE game SET date_end = datetime('now') WHERE id = {game_id}
    ''', '')
    print(f'''
    UPDATE game SET date_end = datetime('now') WHERE id = {game_id}
    ''')

    conn.commit()
    conn.close()


def gamer_end_game(game_id: int, gamer_id: int, score: int, camembert: int):
    conn = sqlite3.connect('triv_ia_dlc.db')
    cur = conn.cursor()
    
    query_execute(cur, f'''
                  UPDATE  game_gamer
                  SET score = {score},
                  camembert = {camembert}
                  WHERE game_id = {game_id}
                  AND gamer_id = {gamer_id}
    ''', '')

    conn.commit()
    conn.close()







##################################################
##################################################
##################################################


def gamer_choice_added(game_id: int, gamers_id: list, personnages):
    conn = sqlite3.connect('triv_ia_dlc.db')
    cur = conn.cursor()
    os.system('clear')

    gamers = {}

    for gamer in all_gamers(cur):
        if gamer[0] not in gamers_id:
            print(gamer)
            gamers[gamer[0]] = gamer[1]

    id = input("Choisir un joueur à partir de son 'id' : ")
    try:
        id = int(id)
    except:
        print("/!\ FATAL ERROR /!\ 001 : sql_game.py > choix ID joueur")
        sys.exit()
    
    print('Quel personnage veux-tu prendre ?')
    for i in range(1, len(personnages)):
        print(i, ":", personnages[i])
    personnage = int(input('\n > '))

    try:
        personnage = int(personnage)
    except:
        print("/!\ FATAL ERROR /!\ 002 : sql_game.py > choix personnage")
        sys.exit()

    conn.close()

    try:
        link_game_gamer(game_id, id, gamers[id])
    except:
        print("/!\ FATAL ERROR /!\ 003 : sql_game.py > mauvais choix d'ID gamer. L'ID choisi n'est certainement pas dans la BDD")
        sys.exit()

    return id, gamers[id], personnages[personnage], personnage


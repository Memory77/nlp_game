import sqlite3
import os
import sys

conn = sqlite3.connect('triv_ia_dlc.db')
cur = conn.cursor()

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


def all_gamers() -> str:
    res = query_execute(cur, f'SELECT * FROM gamer', 'SELECT_ALL')
    return res


def new_gamer(alias: str):
    query_execute(cur, f"INSERT INTO gamer (alias) VALUES ('{alias}')")


def delete_gamer(id: int):
    query_execute(cur, f"DELETE FROM gamer WHERE id = {id}")


###################################################################################
###################################################################################
###################################################################################


os.system('clear')

print('Liste des joueurs')

if all_gamers() == None:
    print("Il n'y a pas de joueur d'inscrit.")
else:
    for gamer in all_gamers():
        print(gamer)

action = input("Quelle action voulez-vous faire ? (id du joueur à supprimer ou 0 pour créer un joueur) ")
try:
    action = int(action)
except:
    sys.exit()

if action == 0:
    alias = input("Quel est le pseudo du joueur ? ")
    new_gamer(alias)
else:
    delete_gamer(action)


conn.commit()
conn.close()
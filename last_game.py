'''
Permet d'afficher les résultats de la dernière partie
'''

import sqlite3
import os

conn = sqlite3.connect('triv_ia_dlc.db')
cur = conn.cursor()

cur.execute(f'''
SELECT STRFTIME('%d/%m/%Y', date_start), (STRFTIME('%s', date_end) - STRFTIME('%s', date_start)) / 60, dice_type, alias, score, camembert
FROM game g
JOIN game_gamer gg ON gg.game_id = g.id  
WHERE id IN (SELECT MAX(id) FROM game)
ORDER BY camembert, score DESC''')
res = cur.fetchall()

conn.close()

gamers = ''
for gamer in res:
    date = gamer[0]
    duration = gamer[1]
    dice_type = gamer[2]
    gamers += f"{gamer[3]} >>> score : {gamer[4]} >>> nombre de camemberts : {gamer[5]}\n"

os.system('clear')
print('''
 _______ _______ _______ _______    _______ _     _ _______ ______  
(_______|_______|_______|_______)  (_______|_)   (_|_______|_____ \ 
 _   ___ _______ _  _  _ _____      _     _ _     _ _____   _____) )
| | (_  |  ___  | ||_|| |  ___)    | |   | | |   | |  ___) |  __  / 
| |___) | |   | | |   | | |_____   | |___| |\ \ / /| |_____| |  \ \ 
 \_____/|_|   |_|_|   |_|_______)   \_____/  \___/ |_______)_|   |_|                                                        
''')
print(f'Partie du {date} (durée {duration} min)')
print('''
    ___    ___     ___     ___    _   _  __  __ 
   | _ \  / _ \   |   \   |_ _|  | | | ||  \/  |
   |  _/ | (_) |  | |) |   | |   | |_| || |\/| |
  _|_|_   \___/   |___/   |___|   \___/ |_|__|_|
_| """ |_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|
"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'
''')
print(gamers)

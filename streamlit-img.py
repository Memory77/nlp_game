import os
from dotenv import load_dotenv
import openai
import requests
import streamlit as st
import json

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Récupérer les variables d'environnement
openai_api_key = os.getenv('openai_api_key')
openai_api_key_base = os.getenv('openai_api_key_base')
openai_api_deployment = os.getenv('openai_api_deployment')
openai_api_version = os.getenv('openai_api_version')

# Configurer l'API OpenAI avec les variables chargées
openai.api_key = openai_api_key

# Lire le pré-prompt à partir du fichier JSON
with open('preprompt.json', 'r', encoding='utf-8') as file:
    preprompt = json.load(file)

# Lire la quête principale à partir du fichier JSON
with open('main_quest.json', 'r', encoding='utf-8') as file:
    mainquest = json.load(file)

# Lire les lieux à partir du fichier JSON
with open('lieux.json', 'r', encoding='utf-8') as file:
    lieux = json.load(file)

# Convertir les lieux en une chaîne de texte à inclure dans le pré-prompt
lieux_text = "\n\nVoici les lieux que tu connais :\n"
for lieu in lieux["lieux"]:
    lieux_text += f"\n{lieu['nom']} :\n - Description : {lieu['description']}\n - Position : {lieu['position']}\n - Distance : {lieu['distance']}"
    if "scenes_de_vie" in lieu:
        lieux_text += f"\n - Scènes de vie : {lieu['scenes_de_vie']}"
    if "quetes" in lieu:
        lieux_text += f"\n - Quêtes : {lieu['quetes']}"

# Ajouter les lieux au pré-prompt initial
# preprompt["content"] += lieux_text

# Initialiser l'historique de la conversation avec un pré-prompt détaillé
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = [
        {"role": "system", "content": preprompt["content"]},
        {"role": "system", "content": json.dumps(mainquest)}
    ]

# Initialiser l'état de l'image
if 'current_image' not in st.session_state:
    st.session_state.current_image = "visuels/7e4878aa-323e-442b-af46-ab64fcefd83d.webp"

# Fonction pour appeler l'API Azure OpenAI avec un pré-prompt
def azure_openai_request(conversation_history):
    url = f"{openai_api_key_base}/openai/deployments/{openai_api_deployment}/chat/completions?api-version={openai_api_version}"
    headers = {
        "Content-Type": "application/json",
        "api-key": openai.api_key
    }
    data = {
        "messages": conversation_history,
        "max_tokens": 500,  # Limiter les tokens pour des réponses courtes
        "stop": ["\n"]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error: {response.status_code}, {response.text}")
        return None

# Fonction pour ajouter un message utilisateur à la conversation
def add_user_message(message):
    st.session_state.conversation_history.append({"role": "user", "content": message})

# Fonction pour ajouter une réponse du modèle à la conversation
def add_model_response(response):
    st.session_state.conversation_history.append({"role": "assistant", "content": response})

# Fonction pour sélectionner l'image en fonction de l'entrée utilisateur ou de la réponse du modèle
def update_image(location):
    location = location.lower()
    if "carte du monde" in location:
        st.session_state.current_image = 'visuels/7e4878aa-323e-442b-af46-ab64fcefd83d.webp'
    elif "allons aux montagnes de tharok" in location:
        st.session_state.current_image = "visuels/Montagnes de Tharok/eaeb6dc8-45bd-4792-b829-17f5b1b321a5.webp"
    elif "allons à la forêt d'eldoria" in location:
        st.session_state.current_image = "visuels/Forêt d'Eldoria/5653eb0e-0354-4142-8c4a-8ebbd506c3ea.webp"
    elif "allons au village de ravenwood" in location:
        st.session_state.current_image = "visuels/Village de Ravenwood/50e99546-587a-42b6-bb66-554a88bf66d5.webp"
    elif "allons à la cité de lumina" in location:
        st.session_state.current_image = "visuels/Cité de Lumina/831b6611-74e9-47c5-9536-4fde6db436dc.webp"
    elif "allons à la forteresse de kael'thor" in location:
        st.session_state.current_image = "visuels/Forteresse de Kael'thor/ae826e83-f836-4e13-b602-98207581d251.webp"
    elif "allons au désert de vereth" in location:
        st.session_state.current_image = "visuels/Désert de Vereth/2703cce7-cad3-4102-b5f6-8dfb869f6d03.webp"
    elif "allons au bourg de drakenshire" in location:
        st.session_state.current_image = "visuels/Bourg de Drakenshire/0f0ded15-dc4d-4008-91dd-a73988602a1c.webp"
    elif "entrons dans les cavernes de nymor" in location:
        st.session_state.current_image = "visuels/Cavernes de Nymor/878a9aa7-755b-4b75-bbd1-f47cac39e002.webp"
    elif "je vois le ver géant du désert" in location:
        st.session_state.current_image = "visuels/Bestiaire/a49b6b9a-1dbe-447f-b5b3-51e808a17160.webp"
    elif "bonjour eldric" in location:
        st.session_state.current_image = "visuels/pnj/eldric.webp"
    elif "bonjour borik" in location:
        st.session_state.current_image = "visuels/pnj/borik.webp"
    elif "bonjour gareth" in location:
        st.session_state.current_image = "visuels/pnj/gareth.webp"
    elif "bonjour mira" in location:
        st.session_state.current_image = "visuels/pnj/mira2.webp"
    elif "bonjour lena" in location:
        st.session_state.current_image = "visuels/pnj/lena1.webp"
def update_image_sidebar(location):
    location = location.lower()
    if "carte du monde" in location:
        st.session_state.current_image = 'visuels/7e4878aa-323e-442b-af46-ab64fcefd83d.webp'
    elif "montagnes de tharok" in location:
        st.session_state.current_image = "visuels/Montagnes de Tharok/eaeb6dc8-45bd-4792-b829-17f5b1b321a5.webp"
    elif "forêt d'eldoria" in location:
        st.session_state.current_image = "visuels/Forêt d'Eldoria/5653eb0e-0354-4142-8c4a-8ebbd506c3ea.webp"
    elif "village de ravenwood" in location:
        st.session_state.current_image = "visuels/Village de Ravenwood/50e99546-587a-42b6-bb66-554a88bf66d5.webp"
    elif "cité de lumina" in location:
        st.session_state.current_image = "visuels/Cité de Lumina/831b6611-74e9-47c5-9536-4fde6db436dc.webp"
    elif "forteresse de kael'thor" in location:
        st.session_state.current_image = "visuels/Forteresse de Kael'thor/ae826e83-f836-4e13-b602-98207581d251.webp"
    elif "désert de vereth" in location:
        st.session_state.current_image = "visuels/Désert de Vereth/2703cce7-cad3-4102-b5f6-8dfb869f6d03.webp"
    elif "bourg de drakenshire" in location:
        st.session_state.current_image = "visuels/Bourg de Drakenshire/0f0ded15-dc4d-4008-91dd-a73988602a1c.webp"
    elif "cavernes de nymor" in location:
        st.session_state.current_image = "visuels/Cavernes de Nymor/878a9aa7-755b-4b75-bbd1-f47cac39e002.webp"


# Interface utilisateur Streamlit
st.title("Elara, le Mage Puissant")
st.write("Vous parlez maintenant à Elara, un puissant mage dans un monde de fantasy héroïque.")

# Ajouter une barre latérale avec des boutons pour chaque lieu
st.sidebar.title("Lieux")
locations = [
    "Carte du Monde", "Montagnes de Tharok", "Forêt d'Eldoria", "Village de Ravenwood", 
    "Cité de Lumina", "Forteresse de Kael'thor", "Désert de Vereth", 
    "Bourg de Drakenshire", "Cavernes de Nymor"
]
for location in locations:
    if st.sidebar.button(location):
        update_image_sidebar(location)
        st.experimental_rerun()

# Afficher l'image actuelle
col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    st.image(st.session_state.current_image, use_column_width=True)
# Afficher l'historique de la conversation (en filtrant les messages de rôle 'system')
for message in st.session_state.conversation_history:
    if message['role'] != 'system':
        role = "Vous" if message["role"] == "user" else "Elara"
        st.write(f"**{role}:** {message['content']}")

# Utiliser un formulaire pour gérer l'entrée utilisateur
with st.form(key='user_input_form', clear_on_submit=True):
    user_input = st.text_input("Vous: ", key="user_input")
    submit_button = st.form_submit_button(label='Envoyer')

if submit_button and user_input:
    add_user_message(user_input)
    update_image(user_input)  # Mettre à jour l'image en fonction de l'entrée utilisateur
    response = azure_openai_request(st.session_state.conversation_history)
    if response:
        model_reply = response['choices'][0]['message']['content'].strip()
        add_model_response(model_reply)
        update_image(model_reply)  # Mettre à jour l'image en fonction de la réponse du modèle
    st.rerun()

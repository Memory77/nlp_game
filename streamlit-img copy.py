import os
import openai
import requests
import streamlit as st
import json

# Configurer l'API OpenAI pour utiliser le serveur local LM Studio
openai.api_key = "lm-studio"
openai.api_base = "http://localhost:1234/v1"

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

# Fonction pour appeler le serveur local OpenAI (LM Studio)
def lm_studio_request(conversation_history):
    response = openai.ChatCompletion.create(
        model="model-identifier",  # Remplace "model-identifier" par le nom du modèle sur ton serveur local
        messages=conversation_history,
        max_tokens=500,  # Limiter les tokens pour des réponses courtes
        temperature=0.7
    )
    return response

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
    # (ajouter les autres conditions pour les lieux...)

def update_image_sidebar(location):
    location = location.lower()
    if "carte du monde" in location:
        st.session_state.current_image = 'visuels/7e4878aa-323e-442b-af46-ab64fcefd83d.webp'
    elif "montagnes de tharok" in location:
        st.session_state.current_image = "visuels/Montagnes de Tharok/eaeb6dc8-45bd-4792-b829-17f5b1b321a5.webp"
    # (ajouter les autres conditions pour les lieux...)

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
    response = lm_studio_request(st.session_state.conversation_history)
    if response:
        model_reply = response.choices[0].message['content'].strip()
        add_model_response(model_reply)
        update_image(model_reply)  # Mettre à jour l'image en fonction de la réponse du modèle
    st.experimental_rerun()

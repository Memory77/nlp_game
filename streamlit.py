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

# Lire la quete principaleà partir du fichier JSON
with open('main_quest.json', 'r', encoding='utf-8') as file:
    mainquest = json.load(file)





# Initialiser l'historique de la conversation avec un pré-prompt détaillé
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = [preprompt]

# Ajouter la quête principale à l'historique de la conversation
st.session_state.conversation_history.append({"role": "system", "content": json.dumps(mainquest)})

# Fonction pour appeler l'API Azure OpenAI avec un pré-prompt
def azure_openai_request(conversation_history):
    url = f"{openai_api_key_base}/openai/deployments/{openai_api_deployment}/chat/completions?api-version={openai_api_version}"
    headers = {
        "Content-Type": "application/json",
        "api-key": openai_api_key
    }
    data = {
        "messages": conversation_history,
        "max_tokens": 500
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


# Interface utilisateur Streamlit
st.title("Elara, le Mage Puissant")
st.write("Vous parlez maintenant à Elara, un puissant mage dans un monde de fantasy héroïque.")

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
    response = azure_openai_request(st.session_state.conversation_history)
    if response:
        model_reply = response['choices'][0]['message']['content'].strip()
        add_model_response(model_reply)
    st.rerun()

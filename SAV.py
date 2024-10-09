import os
import openai
import streamlit as st
import json

openai.api_key = "lm-studio"
openai.api_base = "http://localhost:1234/v1"

# Lire le pré-prompt à partir du fichier JSON
with open('preprompt_SAV.json', 'r', encoding='utf-8') as file:
    preprompt = json.load(file)

with open('id_client.json', 'r', encoding='utf-8') as file:
    client = json.load(file)

# Initialiser l'historique de la conversation
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = [
        {"role": "system", "content": preprompt["content"]},
        {"role": "system", "content": json.dumps(client)}

    ]

# Fonction pour appeler le serveur local OpenAI (LM Studio)
def lm_studio_request(conversation_history):
    response = openai.ChatCompletion.create(
        model="model-identifier",  # Remplace "model-identifier" par le nom du modèle sur ton serveur local
        messages=conversation_history,
        max_tokens=250,  
        temperature=0.4
    )
    return response

# Fonction pour ajouter un message utilisateur à la conversation
def add_user_message(message):
    st.session_state.conversation_history.append({"role": "user", "content": message})

# Fonction pour ajouter une réponse du modèle à la conversation
def add_model_response(response):
    st.session_state.conversation_history.append({"role": "assistant", "content": response})

# Interface utilisateur Streamlit
st.title("ROBOT SAV")
st.write("Vous parlez maintenant au SAV.")

# Afficher l'historique de la conversation
for message in st.session_state.conversation_history:
    if message['role'] == 'user':
        st.write(f"**🟢 Vous**: {message['content']}")
    elif message['role'] == 'assistant':
        st.write(f"**🤖 ROBOT SAV**: {message['content']}")

# Utiliser un formulaire pour gérer l'entrée utilisateur
with st.form(key='user_input_form', clear_on_submit=True):
    user_input = st.text_input("Vous: ", key="user_input")
    submit_button = st.form_submit_button(label='Envoyer')

# Lorsque l'utilisateur envoie un message
if submit_button and user_input:
    add_user_message(user_input)
    response = lm_studio_request(st.session_state.conversation_history)
    if response:
        model_reply = response.choices[0].message['content'].strip()
        add_model_response(model_reply)
    st.experimental_rerun()

# Afficher la nouvelle réponse après traitement (facultatif)
if 'model_reply' in st.session_state:
    st.write(f"**ROBOT SAV**: {st.session_state.model_reply}")

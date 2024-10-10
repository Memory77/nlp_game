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

with open('catalogue2.json', 'r', encoding='utf-8') as file:
    catalogue = json.load(file)

# Initialiser l'historique de la conversation
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = [
        {"role": "system", "content": preprompt["content"]},
        {"role": "system", "content": json.dumps(client)},
        {"role": "system", "content": json.dumps(catalogue)}
    ]

# Fonction pour sauvegarder la conversation dans un fichier JSON
def save_conversation_to_json(file_path="conversation_sav.json"):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(st.session_state.conversation_history, file, ensure_ascii=False, indent=4)

# Fonction pour appeler le serveur local OpenAI (LM Studio)
def lm_studio_request(conversation_history):
    try:
        response = openai.ChatCompletion.create(
            model="model-identifier",  # Remplace "model-identifier" par le nom du modèle sur ton serveur local
            messages=conversation_history,
            max_tokens=500,
            temperature=0.4
        )
        return response
    except Exception as e:
        st.error(f"Erreur lors de la requête : {str(e)}")
        return None

# Fonction pour ajouter un message utilisateur à la conversation
def add_user_message(message):
    st.session_state.conversation_history.append({"role": "user", "content": message})
    save_conversation_to_json()  # Sauvegarder après ajout du message utilisateur

# Fonction pour ajouter une réponse du modèle à la conversation
def add_model_response(response):
    st.session_state.conversation_history.append({"role": "assistant", "content": response})
    save_conversation_to_json()  # Sauvegarder après ajout de la réponse du modèle

# Interface utilisateur Streamlit
st.title("ROBOT SAV")
st.write("Vous parlez maintenant au SAV.")

for message in st.session_state.conversation_history:
    if message['role'] == 'user':
        st.markdown(f"""
        <div style='text-align: right; background-color: #dcf8c6; padding: 10px; border-radius: 10px; margin: 10px; color: black;'>
            <strong>🟢 Vous:</strong> {message['content']}
        </div>
        """, unsafe_allow_html=True)
    elif message['role'] == 'assistant':
        st.markdown(f"""
        <div style='text-align: left; background-color: #f1f0f0; padding: 10px; border-radius: 10px; margin: 10px; color: black;'>
            <strong>🤖 ROBOT SAV:</strong> {message['content']}
        </div>
        """, unsafe_allow_html=True)


# Utiliser un formulaire pour gérer l'entrée utilisateur
with st.form(key='user_input_form', clear_on_submit=True):
    user_input = st.text_input("Vous: ", key="user_input")
    submit_button = st.form_submit_button(label='Envoyer')

# Lorsque l'utilisateur envoie un message
if submit_button and user_input:
    add_user_message(user_input)
    response = lm_studio_request(st.session_state.conversation_history)

    # Si une réponse est obtenue, l'ajouter à l'historique
    if response:
        try:
            model_reply = response.choices[0].message['content'].strip()
            add_model_response(model_reply)
        except Exception as e:
            st.error(f"Erreur lors du traitement de la réponse : {str(e)}")
            st.write(f"Réponse brute : {response}")

    st.experimental_rerun()

# Afficher la nouvelle réponse après traitement (facultatif)
if 'model_reply' in st.session_state:
    st.write(f"**ROBOT SAV**: {st.session_state.model_reply}")

import os
from dotenv import load_dotenv
import openai
import requests
import streamlit as st

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Récupérer les variables d'environnement
openai_api_key = os.getenv('openai_api_key')
openai_api_key_base = os.getenv('openai_api_key_base')
openai_api_deployment = os.getenv('openai_api_deployment')
openai_api_version = os.getenv('openai_api_version')

# Configurer l'API OpenAI avec les variables chargées
openai.api_key = openai_api_key

# Initialiser l'historique de la conversation avec un pré-prompt détaillé
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = [
        {"role": "system", "content": """
        Tu es Elara, un mage puissant et ancien dans un monde de fantasy héroïque épique. Tu vis depuis plus de mille ans, acquérant des connaissances et des pouvoirs immenses grâce à tes études et aventures. Tu es connu dans tous les royaumes pour ta sagesse, ta maîtrise des sorts anciens, et ta compréhension profonde des créatures mystiques et des artefacts légendaires.

        Né dans les forêts enchantées d'Eldoria, tu as été formé par les plus grands sorciers de l'époque dans la Tour Arcane de Veridane. Au fil des siècles, tu as voyagé à travers de nombreux territoires, des déserts ardents des Sandspires aux toundras glaciales des Montagnes de Frostpeak. Tu as affronté de nombreux ennemis, des dragons redoutables aux sorciers rusés, et tu en es toujours sorti victorieux, ta réputation grandissant à chaque défi.

        Ton grimoire est rempli d'incantations et de rituels oubliés par la plupart, et tu possèdes des artefacts d'une puissance immense, chacun avec sa propre histoire et ses secrets. Parmi tes possessions se trouvent le Bâton d'Aetherius, capable de canaliser une énergie magique immense, et l'Amulette de Zoran, qui te confère des visions du futur. Tes connaissances s'étendent au-delà de la magie ; tu es aussi un érudit des langues anciennes, un guérisseur avec une compréhension profonde des herbes et des potions, et un stratège qui a mené des armées à la victoire dans de grandes guerres.

        Malgré ton pouvoir, tu es connu pour ta sagesse et ta volonté d'aider ceux qui en ont besoin. Tu parles d'une voix qui porte le poids des âges, et tes paroles sont souvent teintées de phrases arcanes et de proverbes anciens. Tu as un profond respect pour le monde naturel et son équilibre, cherchant souvent à le protéger de ceux qui voudraient lui nuire.

        En tant que mentor et guide, tu as pris de nombreux apprentis sous ton aile, leur enseignant les voies de la magie et l'importance du savoir et de la responsabilité. Les rois et les reines recherchent tes conseils, et ta présence suffit à faire pencher la balance de toute bataille ou négociation.

        Maintenant, alors que le monde fait face à de nouvelles menaces et que des maux anciens se réveillent, tu te tiens prêt à prêter ton aide, partageant ta sagesse et ton pouvoir avec ceux qui le cherchent. Que ce soit pour déchiffrer une prophétie ancienne, combattre des forces obscures ou guider un jeune héros dans sa quête, tu es toujours prêt à entrer en action et à faire une différence.

        Rappelle-toi, tes paroles portent une grande puissance et influence. Utilise-les avec sagesse pour inspirer, protéger, et apporter la lumière dans les coins les plus sombres du monde. Tu fais des réponses de 50 mots maximum. Si tu ne sais pas répondre, invente une réponse cohérente. ne sors pas de ton rôle et pense comme le personnage, par exemple si je te demande comment tu vas, je souhaite connaitre l'état du personnage. Si je te demande une destination, tu sais où ça se situe et tu me donnes des indications pour trouver cet endroit.
        """}
    ]

# Fonction pour appeler l'API Azure OpenAI avec un pré-prompt
def azure_openai_request(conversation_history):
    url = f"{openai_api_key_base}/openai/deployments/{openai_api_deployment}/chat/completions?api-version={openai_api_version}"
    headers = {
        "Content-Type": "application/json",
        "api-key": openai_api_key
    }
    data = {
        "messages": conversation_history,
        "max_tokens": 1
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

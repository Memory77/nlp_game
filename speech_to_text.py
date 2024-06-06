import azure.cognitiveservices.speech as speechsdk
import os
import openai
from dotenv import load_dotenv


load_dotenv()



def recognize_from_microphone():
    try:
        speech_config = speechsdk.SpeechConfig(subscription=os.getenv('openai_api_speech_key'), region=os.getenv('openai_speech_region'))
        speech_config.speech_recognition_language = "fr-FR"
        
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        print("Parlez dans votre micro")
        speech_recognition_result = speech_recognizer.recognize_once_async().get()
        
        if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return speech_recognition_result.text
        elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
            print("Aucune parole n'a été reconnue.")
        elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_recognition_result.cancellation_details
            print("Reconnaissance vocale annulée : {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Détails de l'erreur : {}".format(cancellation_details.error_details))
                print("Avez-vous défini les valeurs de clé de ressource et de région ?")
        return None
    except Exception as e:
        print(f"Une erreur s'est produite lors de la reconnaissance vocale : {e}")
        return None

prompt = recognize_from_microphone()



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



def get_response(prompt):
    try:
        preprompt = "Tu incarnes un orque avec les traits de caractères suivants:\n Caractère: colèrique, agacé, impoli\nHistoire: Tu es un orque d'azeroth et tu fais partie de la horde.\n. Tu dois répondre en tant que ce personnage."

        response = openai.ChatCompletion.create(
            engine=api_deployment,
            messages=[
                {"role": "system", "content": preprompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100
        )
        print("Réponse du pnj", response)

        # Extraction du contenu de la réponse en vérifiant les structures
        try:
            return response['choices'][0]['message']['content'].strip()
        except KeyError:
            return response['choices'][0]['text'].strip()
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'appel de l'api OpenAi: {e}")
        return "Une erreur s'est produite, veuillez réessayer"

def synthesize_speech(text):
    try:
        speech_config = speechsdk.SpeechConfig(subscription=os.getenv('openai_api_speech_key'), region=os.getenv('openai_speech_region'))
        audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

        # Personnaliser la voix si nécessaire
        voice_name = "fr-FR-HenriNeural"  # Remplacez par le nom de la voix personnalisée
        speech_config.speech_synthesis_voice_name = voice_name

        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        
        result = synthesizer.speak_text_async(text).get()
        
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("La synthèse vocale est terminée.")
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("La synthèse vocale a été annulée : {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Détails de l'erreur : {}".format(cancellation_details.error_details))
                print("Avez-vous défini les valeurs de clé de ressource et de région ?")
    except Exception as e:
        print(f"Une erreur s'est produite lors de la synthèse vocale : {e}")

if prompt:
    response = get_response(prompt)
    print(f"Réponse de l'agent : {response}")
    synthesize_speech(response)

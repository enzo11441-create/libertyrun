import streamlit as st
from google import genai
from google.genai import types

# 1. Configuration de la page web
st.set_page_config(page_title="Liberty Run Assistant", page_icon="🏃‍♂️")
st.title("🏃‍♂️ Liberty Run Assistant")
st.caption("Ton expert en sapes de running de performance")

# 2. Initialisation de la clé API et du client Gemini
# Remplace par ta vraie clé API ou configure-la dans tes variables d'environnement
if "GEMINI_API_KEY" not in st.session_state:
    st.session_state.GEMINI_API_KEY = "TON_API_KEY_ICI" 

client = genai.Client(api_key=st.session_state.GEMINI_API_KEY)

# Le prompt système que nous avons construit ensemble
SYSTEM_INSTRUCTION = """
Tu es "Liberty Run Assistant", l'expert ultime en textile et sapes de running de performance...
[METS ICI TOUT LE CONTENU DE TON PROMPT SYSTÈME]
"""

# 3. Gestion de l'historique de discussion (pour que l'IA se souvienne du contexte)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Sdk frérot ! Je suis l'assistant IA Liberty Run. Si t'as besoin d'aide sur de la tech running ou si tu veux capter des liens d'articles, je suis là pour t'aiguiller direct. Tu cherches quoi aujourd'hui ?"}
    ]

# Affichage des anciens messages à l'écran
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Zone de saisie pour l'utilisateur
if user_prompt := st.chat_input("Pose ta question ici..."):
    # On affiche le message de l'utilisateur
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # On prépare la requête pour Gemini en lui envoyant tout l'historique
    formatted_contents = []
    for msg in st.session_state.messages:
        role = "user" if msg["role"] == "user" else "model"
        # On évite d'envoyer le tout premier message d'accueil forcé à l'API
        if msg["content"] != st.session_state.messages[0]["content"]:
            formatted_contents.append(types.Content(
                role=role,
                parts=[types.Part.from_text(text=msg["content"])]
            ))

    # Appel à l'API Gemini
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=formatted_contents,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=0.7,
                )
            )
            assistant_response = response.text
            message_placeholder.markdown(assistant_response)
            # On sauvegarde la réponse dans l'historique
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        except Exception as e:
            st.error(f"Erreur API : {e}")

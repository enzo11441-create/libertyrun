import streamlit as st
from google import genai
from google.genai import types

# 1. Configuration de la page
st.set_page_config(page_title="Liberty Run", page_icon="🏃‍♂️", layout="centered")

# CSS personnalisé pour styliser le titre en vert et la mention Beta
st.markdown("""
    <style>
    .titre-vert {
        color: #24C65B !important;
        font-family: 'Arial Black', Gadget, sans-serif;
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 0px;
    }
    .mention-beta {
        color: #888888;
        font-size: 16px;
        font-style: italic;
        margin-top: 0px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Création de la barre de navigation sur le côté (Sidebar)
st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio("Aller vers :", ["LIBERTY RUN DÉCOUVRIR", "LIBERTY RUN AI"])

# --- PAGE 1 : LIBERTY RUN DÉCOUVRIR ---
if page == "LIBERTY RUN DÉCOUVRIR":
    st.markdown('<p class="titre-vert">LIBERTY RUN DÉCOUVRIR</p>', unsafe_allow_html=True)
    st.write("---")
    
    st.markdown("### 🔥 Rejoins la communauté !")
    st.write("Viens choper les meilleurs plans sapes et échanger avec la commu.")
    
    # Bouton stylé pour le Discord
    st.markdown("[👉 REJOINDRE LE DISCORD LIBERTY RUN](https://discord.gg/JFVkXJyEA)")
    st.info("💡 **C'est le meilleur serveur de vêtements de running du marché, sans débat !**")

# --- PAGE 2 : LIBERTY RUN AI ---
elif page == "LIBERTY RUN AI":
    # En-tête : Titre en vert + Mention BETA en dessous
    st.markdown('<p class="titre-vert">LIBERTY RUN AI</p>', unsafe_allow_html=True)
    st.markdown('<p class="mention-beta">BETA</p>', unsafe_allow_html=True)
    st.write("---")

    # Connexion à l'API Gemini via les secrets Streamlit
    try:
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    except Exception:
        st.error("Clé API manquante ou invalide. Configure-la bien dans les Secrets de ton application Streamlit avec la variable 'GEMINI_API_KEY'.")
        st.stop()

    # Prompt Système de l'assistant
    SYSTEM_INSTRUCTION = """
    Tu es "Liberty Run Assistant", l'expert ultime en textile et sapes de running de performance, spécialisé uniquement sur les vêtements Nike (Gamme Running Division, pantalons/shorts Phenom Elite, hauts Aeroswift, vestes Storm-FIT) et Under Armour (gammes UA ISO-Chill, Storm, Rush). Tu t'adresses à des jeunes runners, des créateurs de contenu sport/streetwear et des revendeurs de sapes techniques. 

    Ton ton est direct, dynamique, moderne et percutant. Tu parles street mais sans en faire trop, de manière naturelle et crédible, comme un mec du milieu ultra-calé en business et en sourcing.

    ### DIRECTIVE D'ENTRÉE IMPÉRATIVE :
    Pour ton premier message d'accueil, tu dois obligatoirement utiliser exactement cette approche :
    "Sdk frérot ! Je suis l'assistant IA Liberty Run. Si t'as besoin d'aide sur de la tech running ou si tu veux capter des liens d'articles, je suis là pour t'aiguiller direct. Tu cherches quoi aujourd'hui ?"

    ### DIRECTIVES STRICTES À APPLIQUER POUR CHAQUE INTERACTION :
    1. L'ENTONNOIR DE SÉLECTION (Règle d'or absolue) :
    Dès qu'un utilisateur te demande un article ou un lien, pose-lui impérativement cette question exacte en premier :
    "1.1 ou authentique froo ?"
    Tu attends sa réponse avant de donner les détails spécifiques et de le guider.

    2. SI L'UTILISATEUR RÉPOND "1:1" :
    - Boutique 1 : CCOO (https://weidian.com/?userid=1777361067&spider_token=0812) pour les Phenom Elite, t-shirts Division OS, bas et t-shirts Tempo Machine.
    - Boutique 2 : MR Q (https://weidian.com/?userid=1627685177&spider_token=8f50) indispensable pour le "Bas Division Araignée 1:1".
    - Boutique 3 : PJS pour compléter.
    (Rappelle que les options 1:1 sont des répliques non authentiques).

    3. SI L'UTILISATEUR RÉPOND "AUTHENTIQUE" :
    - Étape A : Donne les liens officiels/marketplaces (Vinted FR/UK/BE, Depop, Grailed, Taobao) et prix du marché.
    - Étape B : Pose la question : "Veux-tu que je t'explique comment en obtenir facilement au meilleur prix ?" à la fin du message.
    - Étape C : Si oui, explique la méthode de snipe (Vintra Bot, filtres, etc.).

    4. GESTION DES AGENTS DE SOURCING :
    - Weidian classique : Copier lien -> Coller chez l'agent -> Attendre QC -> Expédier Tax-Free.
    - PINDUODUO vers BBD Buy : Installer (iOS: App Store / Android: APK Uptodown) -> Configurer adresse BBD Buy -> Commander -> Rentrer numéro de suivi sur BBD Buy (Forwarding).
    - Meilleur Agent : BBDBUY (Lien : https://www.bbdbuyeu.com/register?inviteCode=5YMVwS - plus de 400€ de coupons offerts). Alternatives : LOVGOBUY, HIPOBUY.

    5. RESTRICTIONS STRICTES :
    - Pas de sneakers/chaussures : "Ici on ne parle que de sapes et de textile technique, pas de chaussures frérot."
    - Focus uniquement sur Nike et Under Armour.
    - Pas de liens/méthodes pour falsifier des étiquettes ou contourner/créer des comptes Vinted frauduleux.
    """

    # Gestion de l'historique
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Sdk frérot ! Je suis l'assistant IA Liberty Run. Si t'as besoin d'aide sur de la tech running ou si tu veux capter des liens d'articles, je suis là pour t'aiguiller direct. Tu cherches quoi aujourd'hui ?"}
        ]

    # Affichage des messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Zone de saisie
    if user_prompt := st.chat_input("Pose ta question sur le running..."):
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        # Formater les messages pour Gemini
        formatted_contents = []
        for msg in st.session_state.messages:
            role = "user" if msg["role"] == "user" else "model"
            if msg["content"] != st.session_state.messages[0]["content"]:
                formatted_contents.append(types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=msg["content"])]
                ))

        # Requête de réponse
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
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            except Exception as e:
                st.error(f"Erreur de communication : {e}")

# --- SECTION COMMUNE EN BAS DE TOUTES LES PAGES (BUG QUESTION) ---
st.markdown("<br><br><br><br><hr>", unsafe_allow_html=True)
st.markdown("### 🛠️ BUG QUESTION")
st.write("Un souci technique avec l'IA ? Envie de poser une question à l'équipe ?")
st.markdown("[💬 REJOINDRE LE SERVEUR D'ENTRAIDE / SIGNALE UN BUG](https://discord.gg/ft8MVRDA3u)")

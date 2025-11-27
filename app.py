import streamlit as st
import os
from utils.ocr_utils import process_cin, process_passport
from utils.chatbot_ai import ChatbotAI
from utils.ml_models import SavingsRecommender, CreditPredictor
import plotly.express as px
import pandas as pd
from PIL import Image

import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# Configuration de la page
st.set_page_config(
    page_title="UIR Neobank",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
def load_css():
    try:
        with open("static/css/style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except:
        st.markdown("""
        <style>
        .main-header {
            text-align: center;
            padding: 1rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        </style>
        """, unsafe_allow_html=True)

load_css()

# Initialisation session state
if 'user_authenticated' not in st.session_state:
    st.session_state.user_authenticated = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'ocr_data' not in st.session_state:
    st.session_state.ocr_data = None

def show_login():
    st.sidebar.title("🔐 Connexion")
    
    # Pour la démo, on utilise une connexion simple
    username = st.sidebar.text_input("Nom d'utilisateur")
    password = st.sidebar.text_input("Mot de passe", type="password")
    
    if st.sidebar.button("Se connecter", use_container_width=True):
        if username and password:
            st.session_state.user_authenticated = True
            st.session_state.user_data = {
                'nom': username,
                'solde': 15450,
                'epargne': 8200
            }
            st.rerun()
        else:
            st.sidebar.error("Veuillez entrer vos identifiants")

def show_inscription():
    st.header("👤 Inscription - Vérification d'identité")
    
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Informations personnelles")
            nom = st.text_input("Nom")
            prenom = st.text_input("Prénom")
            email = st.text_input("Email")
            telephone = st.text_input("Téléphone")
        
        with col2:
            st.subheader("Vérification d'identité")
            doc_type = st.radio("Type de document", 
                              ["Carte Nationale (CIN)", "Passeport"])
            
            uploaded_file = st.file_uploader(
                "Uploader votre document", 
                type=['jpg', 'png', 'jpeg'],
                help="Photo claire de votre document d'identité"
            )
            
            if uploaded_file is not None:
                # Aperçu de l'image
                st.image(uploaded_file, caption="Document uploadé", width=300)
                
                if st.button("🔍 Vérifier le document", use_container_width=True):
                    with st.spinner("Analyse OCR en cours..."):
                        if "Carte Nationale" in doc_type:
                            result = process_cin(uploaded_file)
                        else:
                            result = process_passport(uploaded_file)
                        
                        if result['success']:
                            st.session_state.ocr_data = result['data']
                            st.success("✅ Document vérifié avec succès!")
                            
                            # Afficher les données extraites
                            with st.expander("Données extraites"):
                                st.json(result['data'])
                        else:
                            st.error("❌ Erreur lors de la vérification")
    
    # Bouton d'inscription final
    if st.session_state.ocr_data and nom and prenom:
        if st.button("🎉 Finaliser l'inscription", type="primary", use_container_width=True):
            st.session_state.user_authenticated = True
            st.session_state.user_data = {
                'nom': nom,
                'prenom': prenom,
                'email': email,
                'telephone': telephone,
                'solde': 15450,
                'epargne': 8200
            }
            st.success("Inscription réussie! Redirection...")
            st.rerun()

def show_dashboard():
    st.header("📊 Tableau de Bord UIR Neobank")
    
    # Cartes de solde
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Solde Principal", 
            f"{st.session_state.user_data.get('solde', 0):,} MAD",
            delta="+1,200 MAD"
        )
    
    with col2:
        st.metric(
            "Compte Épargne", 
            f"{st.session_state.user_data.get('epargne', 0):,} MAD",
            delta="+245 MAD"
        )
    
    with col3:
        st.metric("Crédit Disponible", "50,000 MAD")
    
    with col4:
        st.metric("Dépenses du mois", "3,600 MAD", delta="-12%")
    
    # Graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Répartition des dépenses")
        data_depenses = pd.DataFrame({
            'Catégorie': ['Alimentation', 'Transport', 'Loisirs', 'Factures', 'Shopping'],
            'Montant': [1200, 800, 500, 1100, 800]
        })
        fig_depenses = px.pie(data_depenses, values='Montant', names='Catégorie')
        st.plotly_chart(fig_depenses, use_container_width=True)
    
    with col2:
        st.subheader("💰 Recommandations d'épargne")
        recommender = SavingsRecommender()
        recommendation = recommender.get_recommendation(st.session_state.user_data)
        
        st.info(f"💡 **Recommandation :** {recommendation}")
        
        # Simulation d'investissement
        st.metric("Rendement projeté (1 an)", "+1,250 MAD", delta="+3.2%")
        
        if st.button("➕ Ouvrir un compte épargne"):
            st.success("Compte épargne ouvert avec succès!")

def show_chatbot():
    st.header("🤖 Assistant Virtuel UIR Neobank")
    
    # Initialisation du chatbot
    chatbot = ChatbotAI()
    
    # Zone de chat
    chat_container = st.container()
    
    with chat_container:
        # Afficher l'historique des messages
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Input utilisateur
    if prompt := st.chat_input("Posez votre question sur vos comptes, virements, crédits..."):
        # Ajouter le message utilisateur à l'historique
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # Afficher le message utilisateur
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Réponse du chatbot
            with st.chat_message("assistant"):
                with st.spinner("Réflexion..."):
                    response = chatbot.get_response(prompt, st.session_state.user_data)
                    st.markdown(response)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})

def show_virements():
    st.header("💸 Virements Bancaires")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Nouveau virement")
        compte_destinataire = st.text_input("Compte destinataire")
        montant = st.number_input("Montant (MAD)", min_value=10, max_value=100000)
        motif = st.text_input("Motif du virement")
        
        if st.button("💳 Effectuer le virement", type="primary"):
            if compte_destinataire and montant:
                st.success(f"Virement de {montant} MAD effectué avec succès!")
            else:
                st.error("Veuillez remplir tous les champs")
    
    with col2:
        st.subheader("Derniers virements")
        virements = [
            {"date": "2024-01-15", "destinataire": "Mohamed A.", "montant": -1500},
            {"date": "2024-01-10", "destinataire": "SARL Tech", "montant": -3200},
            {"date": "2024-01-05", "destinataire": "Dépôt", "montant": 5000},
        ]
        
        for virement in virements:
            montant_color = "green" if virement["montant"] > 0 else "red"
            st.write(f"**{virement['date']}** - {virement['destinataire']} - "
                    f":{montant_color}[{virement['montant']} MAD]")

def main():
    # Header principal
    st.markdown("""
    <div class='main-header'>
        <h1>🏦 UIR Neobank</h1>
        <p>Votre banque digitale innovante par l'Université Internationale de Rabat</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    if not st.session_state.user_authenticated:
        show_login()
        show_inscription()
    else:
        # Sidebar pour utilisateur connecté
        with st.sidebar:
            st.title(f"👋 Bienvenue, {st.session_state.user_data.get('nom', 'Client')}")
            st.divider()
            
            menu = st.radio(
                "Navigation",
                ["📊 Tableau de Bord", "💸 Virements", "💰 Épargne", "🤖 Assistant", "⚙️ Paramètres"]
            )
            
            if st.button("🚪 Déconnexion", use_container_width=True):
                st.session_state.user_authenticated = False
                st.session_state.user_data = {}
                st.session_state.chat_history = []
                st.rerun()
        
        # Contenu principal selon le menu
        if menu == "📊 Tableau de Bord":
            show_dashboard()
        elif menu == "💸 Virements":
            show_virements()
        elif menu == "🤖 Assistant":
            show_chatbot()
        elif menu == "💰 Épargne":
            st.header("💰 Gestion de l'Épargne")
            show_dashboard()  # Réutiliser pour la démo
        else:
            st.header("⚙️ Paramètres du Compte")
            st.write("Fonctionnalité en développement...")

if __name__ == "__main__":
    main()
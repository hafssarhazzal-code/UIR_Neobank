import streamlit as st
import random
from datetime import datetime

class ChatbotAI:
    def __init__(self):
        self.context = "UIR Neobank - Banque digitale marocaine"
        
    def get_response(self, user_input, user_data=None):
        user_input = user_input.lower()
        
        # Réponses contextuelles
        responses = {
            'solde': [
                "Votre solde actuel est de 15,450 MAD.",
                "Vous avez 15,450 MAD sur votre compte principal.",
                "Solde disponible : 15,450 MAD."
            ],
            'virement': [
                "Pour effectuer un virement, rendez-vous dans l'onglet 'Virements'.",
                "Je vous redirige vers la section virements...",
                "Vous pouvez faire des virements depuis le tableau de bord."
            ],
            'crédit': [
                "Vous êtes éligible à un crédit jusqu'à 50,000 MAD.",
                "Notre offre crédit : jusqu'à 50,000 MAD à 5% d'intérêt.",
                "Demande de crédit possible via l'application."
            ],
            'épargne': [
                "Nous recommandons notre compte épargne à 3% d'intérêt annuel.",
                "Épargnez avec notre compte à 3% d'intérêt.",
                "Votre épargne rapporte 3% par an actuellement."
            ],
            'carte': [
                "Votre carte Visa est active jusqu'au 12/2025.",
                "Carte bancaire : statut actif, plafond 8,000 MAD.",
                "Votre carte fonctionne normalement."
            ],
            'salut': [
                "Bonjour ! Comment puis-je vous aider aujourd'hui ?",
                "Salut ! Je suis là pour vous aider.",
                "Bonjour, que souhaitez-vous savoir ?"
            ],
            'merci': [
                "Je vous en prie ! N'hésitez pas si vous avez d'autres questions.",
                "Avec plaisir ! 👍",
                "De rien, bonne journée !"
            ]
        }
        
        # Recherche par mot-clé
        for keyword, response_list in responses.items():
            if keyword in user_input:
                return random.choice(response_list)
        
        # Réponse par défaut
        default_responses = [
            "Je suis là pour vous aider avec vos questions bancaires.",
            "Pouvez-vous reformuler votre question ?",
            "Je peux vous aider avec : soldes, virements, crédits, épargne...",
            "Consultez notre FAQ ou contactez le service client au 0522-123456."
        ]
        
        return random.choice(default_responses)
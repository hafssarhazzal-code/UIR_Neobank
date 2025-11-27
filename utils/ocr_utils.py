import cv2
import pytesseract
from PIL import Image
import numpy as np
import streamlit as st
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def process_cin(uploaded_file):
    """Traite l'OCR pour la Carte Nationale Marocaine"""
    try:
        # Convertir l'image uploadée
        image = Image.open(uploaded_file)
        img_array = np.array(image)
        
        # Pré-traitement de l'image
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        
        # Améliorer le contraste
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        
        # Seuillage adaptatif
        thresh = cv2.adaptiveThreshold(enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                     cv2.THRESH_BINARY, 11, 2)
        
        # OCR avec Tesseract
        custom_config = r'--oem 3 --psm 6 -l fra+ara'
        text = pytesseract.image_to_string(thresh, config=custom_config)
        
        # Extraction des informations
        data = extract_cin_data(text)
        
        return {
            'success': True,
            'data': data,
            'raw_text': text
        }
        
    except Exception as e:
        st.error(f"Erreur OCR: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

def extract_cin_data(text):
    """Extrait les données de la CIN marocaine"""
    data = {
        'nom': 'Non trouvé',
        'prenom': 'Non trouvé',
        'cin_number': 'Non trouvé',
        'date_naissance': 'Non trouvé',
        'lieu_naissance': 'Non trouvé'
    }
    
    # Expressions régulières pour la CIN marocaine
    patterns = {
        'nom': r'Nom[\s:]*([A-Za-zÀ-ÿ\s]+)',
        'prenom': r'(?:Prénom|Prenom)[\s:]*([A-Za-zÀ-ÿ\s]+)',
        'cin_number': r'([A-Z]{1,2}\d{5,6})',
        'date_naissance': r'(\d{2}[\/\-]\d{2}[\/\-]\d{4})'
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data[key] = match.group(1).strip()
    
    return data

def process_passport(uploaded_file):
    """Traite l'OCR pour le passeport"""
    try:
        image = Image.open(uploaded_file)
        img_array = np.array(image)
        
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        custom_config = r'--oem 3 --psm 6 -l eng+fra'
        text = pytesseract.image_to_string(gray, config=custom_config)
        
        # Logique d'extraction pour passeport
        data = extract_passport_data(text)
        
        return {
            'success': True,
            'data': data,
            'raw_text': text
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def extract_passport_data(text):
    """Extrait les données du passeport"""
    data = {
        'nom': 'Non trouvé',
        'prenom': 'Non trouvé',
        'passeport_number': 'Non trouvé',
        'nationalite': 'Marocaine'
    }
    
    # Patterns pour passeport
    patterns = {
        'passeport_number': r'[A-Z]{1,2}\d{6,7}',
        'nom': r'Nom[\s:]*([A-Z\s]+)',
        'prenom': r'(?:Prénom|Prenom)[\s:]*([A-Z\s]+)'
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            data[key] = match.group(1).strip() if match.groups() else match.group(0)
    
    return data
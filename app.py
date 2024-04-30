import streamlit as st
import numpy as np
import pickle
import os

# Chargement du modèle
model_path = 'ridge_model.pkl'
if os.path.exists(model_path):
    with open(model_path, 'rb') as file:
        regressor = pickle.load(file)
else:
    st.error('Erreur : Modèle non trouvé. Veuillez vérifier le chemin du fichier du modèle.')

# Configuration de la page pour une largeur maximale et un titre
st.set_page_config(page_title="Prédiction Immobilière en Californie", layout="wide")

# Ajout d'un menu de navigation pour différentes sections de l'application
st.sidebar.title('Menu de Navigation')
page = st.sidebar.radio("Choisissez une page :", ["Accueil", "Prédiction", "Informations"])

# Chargement d'images
header_image = 'image.jpg'  # Assurez-vous que le chemin est correct
footer_image = 'image.jpeg'  # Assurez-vous que le chemin est correct

if page == "Accueil":
    st.image(header_image, use_column_width=True)
    st.title('Bienvenue sur l\'application de Prédiction Immobilière en Californie')
    st.markdown("""
        Cette application permet d'estimer la valeur médiane des maisons en Californie basée sur plusieurs caractéristiques.
        Naviguez vers l'onglet **Prédiction** pour estimer la valeur d'une maison.
        """)

elif page == "Prédiction":
    st.title('Estimation de la Valeur Médiane des Maisons')
    st.write("Veuillez entrer les détails de la maison pour estimer son prix :")
    
    # Définition des colonnes pour une mise en page en grille
    col1, col2 = st.columns(2)
    
    with col1:
        longitude = st.number_input('Longitude :', format='%f')
        latitude = st.number_input('Latitude :', format='%f')
        housing_median_age = st.number_input('Âge médian du logement :', format='%f')
        total_rooms = st.number_input('Total des pièces :', format='%f')
        total_bedrooms = st.number_input('Nombre total de chambres :', format='%f')
    
    with col2:
        population = st.number_input('Population :', format='%f')
        households = st.number_input('Ménages :', format='%f')
        median_income = st.number_input('Revenu médian :', format='%f')
        ocean_proximity = st.selectbox('Proximité de l’océan :', ['<1H OCEAN', 'INLAND', 'NEAR OCEAN', 'NEAR BAY', 'ISLAND'])
    
    if st.button('Prédire le prix'):
        ocean_proximity_values = {
            '<1H OCEAN': [1, 0, 0, 0, 0],
            'INLAND':    [0, 1, 0, 0, 0],
            'NEAR OCEAN':[0, 0, 1, 0, 0],
            'NEAR BAY':  [0, 0, 0, 1, 0],
            'ISLAND':    [0, 0, 0, 0, 1]
        }
        ocean_proximity_encoded = ocean_proximity_values[ocean_proximity]
        input_features = [longitude, latitude, housing_median_age, total_rooms, total_bedrooms, 
                          population, households, median_income] + ocean_proximity_encoded
        input_data = np.array([input_features])
        prediction = regressor.predict(input_data)
        st.success(f'La valeur médiane prédite de la maison est de ${prediction[0]:,.2f}.')

elif page == "Informations":
    st.title('À propos de cette application')
    st.markdown("""
        Cette application utilise un modèle de régression pour estimer la valeur médiane des maisons en Californie. 
        Elle est conçue pour aider les acheteurs, les vendeurs et les agents immobiliers à obtenir une estimation rapide basée sur des données historiques.
        Elle a été développée par EKEME PETER Blake.
        """)
    # Chemin vers l'image spécifique pour la section Informations
    info_image = 'specific_image.jpg'  # Remplacez par le chemin vers votre image spécifique
    # Affichage de l'image spécifique dans la section Informations
    st.image(info_image, use_column_width=True, caption='Photo du dévéloppeur BG.')

# Footer
st.image(footer_image, use_column_width=True)  # Affichage de l'image de pied de page

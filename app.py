import pandas as pd
import plotly.express as px
import streamlit as st

# Titre de l'application
st.title("Analyse des produits alimentaires")

# Charger les données
df = pd.read_csv('off_racourci.csv', sep=',')

# Liste des colonnes à conserver
columns_to_keep = [
    'product_name', 'product_code',  # Ajout des codes produits
    'origins', 'origins_tags', 'origins_fr', 'countries_fr', 'main_category_fr'
]

# Zone de saisie pour les codes produits (un ou plusieurs, séparés par des virgules ou des retours à la ligne)
codes_input = st.text_area("Entrez les codes des produits que vous recherchez (séparés par des virgules ou des lignes) :")

# Convertir l'entrée utilisateur en une liste de codes
if codes_input:
    codes = [code.strip() for code in codes_input.replace('\n', ',').split(',') if code.strip()]
    st.write(f"Vous avez recherché {len(codes)} code(s) : {', '.join(codes)}")

    # Filtrer les lignes où 'product_code' correspond aux codes recherchés
    df_filtered = df[df['product_code'].isin(codes)]
else:
    st.warning("Veuillez entrer au moins un code produit.")
    df_filtered = pd.DataFrame(columns=columns_to_keep)  # DataFrame vide si aucun code saisi

# Sélectionner les colonnes spécifiées
df_filtered = df_filtered[columns_to_keep]

# Fonction de modification de la colonne "origins_tags"
def modify_origins_tags(value):
    if isinstance(value, str):
        if "en:" in value:
            parts = value.split("en:")
            if len(parts) > 1:
                modified_part = parts[1][0].upper() + parts[1][1:] if len(parts[1]) > 0 else ''
                return parts[0] + " " + modified_part
        elif "fr:" in value:
            parts = value.split("fr:")
            if len(parts) > 1:
                modified_part = parts[1][0].upper() + parts[1][1:] if len(parts[1]) > 0 else ''
                return parts[0] + " " + modified_part
    return value

# Appliquer la fonction sur la colonne "origins_tags"
if not df_filtered.empty and 'origins_tags' in df_filtered.columns:
    df_filtered['origins_tags'] = df_filtered['origins_tags'].apply(modify_origins_tags)

# Extraire les origines uniques
if not df_filtered.empty and 'origins_tags' in df_filtered.columns:
    origins_tags_string = " ".join(df_filtered['origins_tags'].astype(str).tolist())
    origins_list = list(set(origins_tags_string.split()))
else:
    origins_list = []

# Convert origins_list to a DataFrame with a 'Pays' column
df_origins = pd.DataFrame({"Pays": origins_list}) 

# Create the choropleth map
if not df_origins.empty:
    fig = px.choropleth(
        df_origins,
        locations="Pays",
        locationmode="country names",
        color_discrete_sequence=["blue"], 
        title="Carte des pays uniques"
    )
    st.plotly_chart(fig)
else:
    st.warning("Aucune origine trouvée pour les codes produits saisis.")

# Afficher le DataFrame filtré
st.subheader("Résultats du filtrage des produits")
st.dataframe(df_filtered)

import pandas as pd
import plotly.express as px
import streamlit as st

# Titre de l'application
st.title("Analyse des produits alimentaires")

# Charger les données
df = pd.read_csv('off_racourci.csv', sep=',')

# Liste des colonnes à conserver
columns_to_keep = [
    'code','product_name', 'product_code',  # Ajout des codes produits
    'origins', 'origins_tags', 'origins_fr', 'countries_fr', 'main_category_fr'
]
# Zone de saisie pour l'utilisateur
search_term = st.text_input("Entrez les noms de produits que vous recherchez dans votre panier :").lower()


# Filtrer les lignes où 'origins' contient une information non vide
df_filtered = df[df['origins'].notnull()]

# Filtrer les lignes où 'product_name' contient le terme recherché (en ignorant la casse)
df_filtered = df_filtered[df_filtered['product_name'].str.contains(search_term, case=False, na=False)]

# Exclure les lignes dont le 'product_name' contient "es:Mondo" (en ignorant la casse)
df_filtered = df_filtered[~df_filtered['product_name'].str.contains('es:Mondo', case=False, na=False)]

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
fig = px.choropleth(
    df_origins,  # Use the DataFrame instead of the list
    locations="Pays",  # 'Pays' is now a column in the DataFrame
    locationmode="country names",
    color_discrete_sequence=["blue"], 
    title="Carte des pays uniques"
)
# Afficher la carte dans Streamlit
st.plotly_chart(fig)

st.subheader("Résultats du filtrage des produits")
st.dataframe(df_filtered)

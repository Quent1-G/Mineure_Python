import pandas as pd
import plotly.express as px
import streamlit as st

# Spécifiez le chemin absolu vers votre fichier CSV
file_path = '/content/drive/MyDrive/fr.openfoodfacts.org.products.csv'

# Lire le fichier CSV
df = pd.read_csv(file_path, nrows=150000, low_memory=False, sep='\t')

# Liste des colonnes à conserver
columns_to_keep = [
    'product_name', 'origins', 'origins_tags', 'origins_fr', 'countries_fr', 'main_category_fr'
]

# Demander à l'utilisateur d'entrer un terme de recherche
search_term = st.text_input("Entrez un terme à rechercher dans les noms de produits : ").lower()

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
df_filtered['origins_tags'] = df_filtered['origins_tags'].apply(modify_origins_tags)

# Créer une liste des origines
origins_tags_string = " ".join(df_filtered['origins_tags'].astype(str).tolist())
origins_list = []
current_origin = ""
for char in origins_tags_string:
    if char == '\n' or char == ' ':
        if current_origin:
            origins_list.append(current_origin)
            current_origin = ""
    else:
        current_origin += char
if current_origin:
    origins_list.append(current_origin)

origins_list = list(set(origins_list))

# Convertir origins_list en DataFrame
df_origins = pd.DataFrame({"Pays": origins_list})

# Créer la carte choroplèthe
fig = px.choropleth(
    df_origins,
    locations="Pays",
    locationmode="country names",
    color_discrete_sequence=["blue"],
    title="Carte des pays uniques"
)

st.plotly_chart(fig)

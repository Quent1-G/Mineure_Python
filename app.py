import pandas as pd
import plotly.express as px
import streamlit as st

# Titre de l'application
st.title("Analyse des produits alimentaires")

df = pd.read_csv('off_racourci.csv',sep=',')
# Liste des colonnes à conserver, incluant le nom et le numéro du produit
columns_to_keep = [
    'code', 'product_name',  # Ajout du nom et du numéro du produit
    'origins', 'origins_tags', 'origins_fr', 'countries_fr', 'main_category_fr'
]
# Zone de saisie pour le code produit (entrée sous forme de texte)
search_code = st.text_input("Entrez le code du produit que vous recherchez :")

# Filtrer les lignes où 'code' correspond au code entré (en tant que chaîne)
# Filtrer les lignes où 'code' correspond au code entré (en tant que chaîne)
# Filtrer les lignes où 'code' correspond au code entré (en tant que chaîne)
if search_code:
    # Convertir la colonne 'code' en chaîne de caractères avant de comparer
    df['code_str'] = df['code'].astype(str)  # Crée une colonne temporaire avec le code en texte
    df_filtered = df[df['code_str'] == search_code]  # Comparaison avec l'entrée utilisateur
else:
    df_filtered = pd.DataFrame()  # Si aucun code n'est saisi, il n'y a pas de résultat

# Appliquer le filtre "origins" uniquement sur df_filtered
if not df_filtered.empty:
    df_filtered = df_filtered[df_filtered['origins'].notnull()]



# Exclure les lignes dont le 'product_name' contient "es:Mondo" (en ignorant la casse)
df_filtered = df_filtered[~df_filtered['product_name'].str.contains('es:Mondo', case=False, na=False)]

# Sélectionner les colonnes spécifiées
df_filtered = df_filtered[columns_to_keep]

# Fonction de modification de la colonne "origins_tags"
def modify_origins_tags(value):
    if isinstance(value, str):
        # Vérifie si "en:" est dans la chaîne
        if "en:" in value:
            parts = value.split("en:")
            if len(parts) > 1:
                # Modifie la lettre suivant "en:"
                modified_part = parts[1][0].upper() + parts[1][1:] if len(parts[1]) > 0 else ''
                return parts[0] + " " + modified_part
        # Vérifie si "fr:" est dans la chaîne
        elif "fr:" in value:
            parts = value.split("fr:")
            if len(parts) > 1:
                # Modifie la lettre suivant "fr:"
                modified_part = parts[1][0].upper() + parts[1][1:] if len(parts[1]) > 0 else ''
                return parts[0] + " " + modified_part
    return value

# Appliquer la fonction sur la colonne "origins_tags"
df_filtered['origins_tags'] = df_filtered['origins_tags'].apply(modify_origins_tags)

# This line was missing, leading to the error.
# Assuming you want to process the 'origins_tags' column of the DataFrame,
# replace 'df_filtered' and 'origins_tags' with your actual DataFrame and column name.
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
if current_origin:  # Ajoute le dernier élément si la chaîne ne se termine pas par un espace ou une nouvelle ligne
    origins_list.append(current_origin)


origins_list = list(set(origins_list))

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

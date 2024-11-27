import pandas as pd
import plotly.express as px
import streamlit as st

# Titre de l'application
st.title("Analyse des produits alimentaires")

df = pd.read_csv('off_racourci.csv', sep=',')
# Liste des colonnes à conserver, incluant le nom et le numéro du produit
columns_to_keep = [
    'code', 'product_name',  # Ajout du nom et du numéro du produit
    'origins', 'origins_tags', 'origins_fr', 'countries_fr', 'main_category_fr'
]

# Zone de saisie pour le code produit (entrée sous forme de texte)
search_code = st.text_input("Entrez le code du produit que vous recherchez :")

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
    if 'product_name' in df_filtered.columns:  # Vérifier si la colonne 'product_name' existe
        df_filtered = df_filtered[~df_filtered['product_name'].str.contains('es:Mondo', case=False, na=False)]

    # Sélectionner les colonnes spécifiées
    df_filtered = df_filtered[columns_to_keep]

# Afficher les résultats du filtrage des produits
if not df_filtered.empty:
    st.subheader("Résultats du filtrage des produits")
    st.dataframe(df_filtered)
else:
    st.write("Aucun produit trouvé pour ce code.")

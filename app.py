import streamlit as st
import pandas as pd
from sklearn.datasets import load_wine

values, target = load_wine(return_X_y=True)
target_names = load_wine().target_names
feature_names = load_wine().feature_names

st.title('Grosse colab KFC Burger King')

df = pd.DataFrame(values, columns=feature_names)

df
plot = df["alcohol"]
st.write("le graph avec alcohol:")
st.line_chart(plot)

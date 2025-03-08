import streamlit as st
import pandas as pd

st.write("""
         # Unsere Solaranlage
         """)

df = pd.read_excel("Kostal4.2.xlsx")
# df.set_axis(["Datum", "Uhrzeit", "Leistung", "Ertrag"], axis=1, inplace=True)
st.bar_chart(df)

import streamlit as st
import pandas as pd

st.write("""
         # Unsere Solaranlagen
         
         ## Die alte Anlage
         
         """)

df = pd.read_excel("Kostal4.2.xlsx")

# delete all rows where the value of the column "Daily" is 0
df = df[df.Daily != 0]

st.line_chart(df, x="Date", y=["Daily"], y_label="Daily production in kWh")

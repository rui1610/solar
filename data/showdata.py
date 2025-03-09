import streamlit as st
import pandas as pd

st.write("""
         # Unsere Solaranlagen
         
         """)

df_sol1 = pd.read_excel("Kostal4.2.xlsx")
df_sol2 = pd.read_excel("SUNNY_TRIPOWER_6.0_SE.xlsx")


# delete all rows where the value of the column "Daily" is 0
df_sol1 = df_sol1[df_sol1.Daily != 0]
# Remove all columns from df_sol1 except "Date" and "Daily"
df_sol1 = df_sol1[["Datum", "Daily"]]
# Multiply all values in the column "Daily" by 1000
df_sol1["Daily"] = df_sol1["Daily"] * 1000
# Add a column "Anlage" with the value "Sol 1" to all rows of df_sol1
df_sol1["Anlage"] = "Solaranlage alt"
# Change the date so that the time is always 00:00:00
df_sol1["Datum"] = df_sol1["Datum"].dt.floor("d")

# Remove all columns from df_sol2 except "Datum" and "Daily"
df_sol2 = df_sol2[["Datum", "Daily"]]
# Add a column "Anlage" with the value "Sol 2" to all rows of df_sol2
df_sol2["Anlage"] = "Solaranlage neu"
# Change the date so that it's always one day earlier
df_sol2["Datum"] = df_sol2["Datum"] - pd.DateOffset(days=1)


# Merge the two dataframes df_sol1 and df_sol2 so that the data is displayed in one chart
df_sol = pd.concat([df_sol1, df_sol2])
# Create a new df with the column "Daily" for each day, and the values for column "Solaranlage alt" and "Solaranlage neu"
df_sol = df_sol.pivot_table(
    index="Datum", columns="Anlage", values="Daily", aggfunc="sum"
)


# Sort the data by the column "Datum" in descending order
df_sol = df_sol.sort_values("Datum", ascending=False)
st.write("## Tägliche Produktion in Wh")
# Display the data in a chart
st.line_chart(df_sol)

# Accumulate the daily values to get the total production for each month
df_sol = df_sol.resample("M").sum()
st.write("## Monatliche Produktion in Wh")
# Display the data in a chart
st.bar_chart(df_sol)

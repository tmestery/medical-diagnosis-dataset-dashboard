import streamlit as st
import matplotlib.pyplot as plt
import data_aggregation
import pandas as pd

st.title('Medical Diagnosis Dashboard')

# Get ages and scores
ages = data_aggregation.getAges()
scores = data_aggregation.getScores("data/completion_scores.csv")

st.write(f"Number of ages: {len(ages)}")
st.write(f"Number of scores: {len(scores)}")

# Make sure they are the same length
min_len = min(len(ages), len(scores))
ages = ages[:min_len]
scores = scores[:min_len]

# Combine into a DataFrame for clear organization
df = pd.DataFrame({
    "Age": ages,
    "Severity": scores
})

# Sort by Age for ordered x-axis
df = df.sort_values(by="Age").reset_index(drop=True)

st.write("Here are the ages with their respective severity scores:")
st.dataframe(df)  # shows the table in Streamlit

# Create scatter plot
plt.figure(figsize=(10, 4))
plt.scatter(df["Age"], df["Severity"], color='dodgerblue', s=20)
plt.ylim(0, 100)
plt.yticks(range(0, 101, 10))
plt.xlim(0, 100)  # optional: force x-axis 0-100
plt.xlabel("Age", fontsize=12)
plt.ylabel("Severity Score", fontsize=12)
plt.title("Patient Ages vs. Severity Scores", fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()

st.pyplot(plt)
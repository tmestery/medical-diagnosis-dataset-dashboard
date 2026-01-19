import streamlit as st
import matplotlib.pyplot as plt
import data_aggregation

st.title('Medical Diagnosis Dashboard')

# Run data aggregation script
ages = data_aggregation.getAges()

# Create dot plot
plt.figure(figsize=(10, 3))
plt.plot(ages, [1]*len(ages), 'o', color='dodgerblue', markersize=3)
plt.yticks([])  # hide y-axis
plt.xlabel("Age", fontsize=12)
plt.title("Dot Plot of Patient Ages", fontsize=14)
plt.grid(axis='x', linestyle='--', alpha=0.5)
plt.tight_layout()

# Display in Streamlit
st.pyplot(plt)
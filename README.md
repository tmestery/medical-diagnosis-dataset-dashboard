# Medical Diagnosis Dashboard
A Dashboard that shares insights into Medical Diagnosis data. It utilizes pyspark for data aggregation and streamlit for dashboard UI. Visualized the correlation between patient age and symptom severity using a fine-tuned local LLaMA3 model for severity scoring.

## Setup
Virtual Enviorment with Pyspark:
- ```cd ~/Desktop/testingPyspark```
- ```/opt/homebrew/bin/python3 -m venv venv```
- ```source venv/bin/activate```
- ```pip install -r requirements.txt```

Start ollama3:
-```ollama run llama3```

## Run the Program
- ```streamlit run src/app.py```

If that fails it's likely due to streamlit install location, try:
- ```./venv/bin/streamlit run src/app.py```

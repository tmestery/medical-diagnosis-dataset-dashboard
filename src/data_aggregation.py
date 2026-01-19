from datasets import load_dataset
from pyspark.sql import SparkSession
import pandas as pd
import re
import subprocess
import ollama

# Load dataset
ds = load_dataset("BI55/MedText", split="train")
spark = SparkSession.builder.getOrCreate()
df = spark.createDataFrame(ds.to_pandas())

OLLAMA_CLI = "/opt/homebrew/bin/ollama"  # adjust if needed
MODEL_NAME = "llama3.1"  # your local model


def getAges():
    ages = []
    rows = df.collect()
    for row in rows:
        text = row["Prompt"]
        numbers = re.findall(r'\b\d+\b', text)
        if numbers:
            ages.append(numbers[0])
    return ages


def checkAnalysis():
    completions = []
    rows = df.collect()
    for row in rows:
        completion_text = row["Completion"]
        if completion_text:
            completions.append(completion_text)
    return completions

def ollama_predict(prompt, model_name=MODEL_NAME):
    """Call Olama CLI in interactive mode and return output."""
    try:
        result = subprocess.run(
            [OLLAMA_CLI, "run", model_name],
            input=prompt + "\n",
            capture_output=True,
            text=True,
            timeout=60,  # avoid hanging indefinitely
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print("Error running Ollama:", e)
        print("stdout:", e.stdout)
        print("stderr:", e.stderr)
        return None
    except subprocess.TimeoutExpired:
        print("Ollama timed out for prompt.")
        return None

def ollamaScoreAnalysis():
    completions = checkAnalysis()
    scores = []
    csv_file = "completion_scores.csv"

    for i, completion in enumerate(completions):
        safe_completion = completion.replace("\n", " ").replace("\r", " ")
        prompt = f"Score this medical case from 1 (mild) to 100 (severe). Return **only the number**:\n\n{safe_completion}"

        try:
            response = ollama.chat(
                model="llama3",          # ← or MODEL_NAME if you prefer
                messages=[
                    {"role": "user", "content": prompt}
                ],
                options={"temperature": 0.0}   # help get just the number
            )
            text = response['message']['content'].strip()
            score = int(text)
        except Exception as e:
            print(f"Error scoring completion {i+1}: {e}")
            score = None

        scores.append(score)

        # Save progressively (good practice)
        pd.DataFrame({"Completion": completions[:i+1], "Score": scores}).to_csv(csv_file, index=False)
        print(f"Processed {i+1}/{len(completions)} - Current score: {score}")

    print(f"Saved final scores to {csv_file}")


def getScores(csv_file="completion_scores.csv"):
    """
    Read the CSV of completions and scores and return a list of numeric scores.
    Expects CSV with columns: 'Completion', 'Score'
    """
    try:
        df = pd.read_csv(csv_file)
        # Ensure Score column is numeric
        scores = pd.to_numeric(df['Score'], errors='coerce')
        # Fill any None/NaN with 0 or some default value
        scores = scores.fillna(0).tolist()
        return scores
    except FileNotFoundError:
        print(f"{csv_file} not found. Make sure you ran ollamaScoreAnalysis() first.")
        return []
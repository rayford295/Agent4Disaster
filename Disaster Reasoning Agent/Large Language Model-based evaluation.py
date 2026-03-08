# ============================================
# 0 Install Dependencies
# ============================================

!pip install -q openai pandas openpyxl tqdm

# ============================================
# 1 Import Libraries
# ============================================

import os
import json
import time
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from openai import OpenAI


# ============================================
# 2 Configuration
# ============================================

MODEL_NAME = "gpt-5.2-2025-12-11"

BASE_DIR = Path(r"C:\Users\yyang295\Desktop\Agent4")
OUTPUT_DIR = BASE_DIR / "LLM_JUDGE_RESULTS"
OUTPUT_DIR.mkdir(exist_ok=True)

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


# ============================================
# 3 LLM Evaluation Prompt
# ============================================

SYSTEM_PROMPT = """
You are an expert disaster assessment evaluator.

Evaluate the reasoning quality of disaster interpretation text.

Score from 1-5 for:
1. factual_consistency
2. causal_plausibility
3. completeness
4. actionability

Scoring rubric:
1 = very poor
2 = poor
3 = acceptable
4 = good
5 = excellent

Return ONLY JSON:
{
 "factual_consistency": int,
 "causal_plausibility": int,
 "completeness": int,
 "actionability": int,
 "overall_mean": float
}
"""


# ============================================
# 4 LLM Judge Function
# ============================================

def judge_reasoning(reasoning_text):

    prompt = f"""
Evaluate this disaster reasoning text:

{reasoning_text}
"""

    try:
        # Updated to the standard OpenAI Python SDK syntax
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            response_format={"type": "json_object"} # Ensures valid JSON output
        )

        text = response.choices[0].message.content.strip()

        result = json.loads(text)

        return result

    except Exception as e:

        print("LLM ERROR:", e)

        return {
            "factual_consistency": None,
            "causal_plausibility": None,
            "completeness": None,
            "actionability": None,
            "overall_mean": None
        }


# ============================================
# 5 Process a Single Excel File
# ============================================

def process_excel(file_path):

    print("\nProcessing:", file_path.name)

    df = pd.read_excel(file_path)

    if "Reasoning" not in df.columns:
        print("Skipping (no Reasoning column found)")
        return None

    scores = []

    for i, row in tqdm(df.iterrows(), total=len(df)):

        reasoning = str(row["Reasoning"])

        result = judge_reasoning(reasoning)

        scores.append(result)

        time.sleep(0.2)  # Prevent hitting API rate limits

    score_df = pd.DataFrame(scores)

    result_df = pd.concat([df, score_df], axis=1)

    out_file = OUTPUT_DIR / f"{file_path.stem}_judged.xlsx"

    result_df.to_excel(out_file, index=False)

    print("Saved:", out_file)

    summary = {
        "model": file_path.stem,
        "factual": score_df["factual_consistency"].mean(),
        "plausibility": score_df["causal_plausibility"].mean(),
        "completeness": score_df["completeness"].mean(),
        "actionability": score_df["actionability"].mean(),
        "overall": score_df["overall_mean"].mean()
    }

    return summary


# ============================================
# 6 Automatically Read All Excel Files
# ============================================

excel_files = list(BASE_DIR.glob("*.xlsx"))

print("Found Excel files:", len(excel_files))

for f in excel_files:
    print("-", f.name)


# ============================================
# 7 Batch Processing
# ============================================

all_results = []

for file in excel_files:

    result = process_excel(file)

    if result is not None:
        all_results.append(result)


# ============================================
# 8 Generate Statistical Summary for Paper
# ============================================

summary_df = pd.DataFrame(all_results)

summary_path = OUTPUT_DIR / "MODEL_COMPARISON_RESULTS.xlsx"

summary_df.to_excel(summary_path, index=False)

print("\nAll finished!")
print("Summary saved to:", summary_path)

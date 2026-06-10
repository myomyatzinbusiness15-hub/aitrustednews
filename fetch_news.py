import os
import json
import time
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-3.5-flash')

# Try to generate content, retry if quota is hit
for attempt in range(3):
    try:
        response = model.generate_content("Give me 3 short AI news headlines.")
        data = {"news": response.text}
        with open("news_data.json", "w") as f:
            json.dump(data, f)
        break # Success, exit loop
    except Exception as e:
        if "429" in str(e) or "Quota" in str(e):
            print(f"Quota hit, waiting 60 seconds... (Attempt {attempt+1})")
            time.sleep(60)
        else:
            raise e
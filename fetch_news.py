import os
import json
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Using the correct model name for your current access
model = genai.GenerativeModel('gemini-3.5-flash')

response = model.generate_content("Give me 3 short AI news headlines with a one-sentence summary for each.")

data = {"news": response.text}
with open("news_data.json", "w") as f:
    json.dump(data, f)
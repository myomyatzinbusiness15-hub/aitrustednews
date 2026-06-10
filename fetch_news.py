import json
import os
import google.generativeai as genai

# Use the secret key from GitHub
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = model = genai.GenerativeModel('gemini-pro')

# Ask the AI for news
response = model.generate_content("Give me 3 short AI news headlines with a one-sentence summary for each.")

# Save the output to a file that your website can read
data = {"news": response.text}
with open("news_data.json", "w") as f:
    json.dump(data, f)
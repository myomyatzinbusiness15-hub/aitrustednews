import json
import os
import google.generativeai as genai

# Setup API
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Use the current stable model
model = genai.GenerativeModel('gemini-1.5-flash')

# Generate content
response = model.generate_content("Give me 3 short AI news headlines with a one-sentence summary for each.")
    
# Save the output
data = {"news": response.text}
with open("news_data.json", "w") as f:
    json.dump(data, f)
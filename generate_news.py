import os
import json
import datetime
import google.generativeai as genai

# Setup the AI tool using your saved GitHub Secret key
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("Missing GEMINI_API_KEY inside GitHub settings.")

genai.configure(api_key=API_KEY)

# The 10 categories matching your website tabs exactly
CATEGORIES = ["AI", "War", "Economy", "Crypto", "Tech", "Science", "Climate", "Creator", "Cyber", "Sports"]

def build_daily_newspaper():
    # Using the fast, connected model
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    today_str = datetime.date.today().strftime("%B %d, %Y")
    current_time = datetime.datetime.utcnow().strftime("%H:%M UTC")
    
    print(f"Starting news generation for: {today_str}")
    all_articles = []

    for i, cat in enumerate(CATEGORIES):
        print(f"AI is searching and writing for category: {cat}")
        
        # Explicitly telling the AI to write long, detailed articles with real source links
        prompt = f"""
        Today's date is {today_str}.
        
        Task:
        1. Search the live internet for the most important breaking news event in the world right now regarding the topic '{cat}'.
        2. Write a highly detailed, comprehensive news article about it. 
        3. Make the article LONG and deep (minimum 250 words). Include backgrounds, facts, and explanations. Do not make it a short summary.
        4. Find the actual source URL link (like reuters.com, bloomberg.com, techcrunch.com) where you found this news.
        
        Return your answer ONLY as a clean, raw JSON object matching this structure exactly (do not wrap it in markdown code blocks):
        {{
          "id": "{cat.lower()}-{i}",
          "category": "{cat}",
          "title": "Write a powerful, professional news headline here",
          "date": "{datetime.date.today().strftime('%Y-%m-%d')}",
          "time": "{current_time}",
          "content": "Write your long, multi-paragraph, detailed news article here. Make it highly engaging and rich with information for the reader.",
          "source": "https://www.the-real-news-link-you-found.com"
        }}
        """

        try:
            # The 'google_search' tool forces Gemini to look up the live web before writing
            response = model.generate_content(prompt, tools=[{'google_search': {}}])
            text_reply = response.text.strip()
            
            # Clean up potential markdown formatting issues
            if text_reply.startswith("```"):
                text_reply = text_reply.split("```json")[-1].split("```")[0].strip()
            if text_reply.startswith("```"):
                text_reply = text_reply.split("```")[-1].split("```")[0].strip()
                
            article_json = json.loads(text_reply)
            all_articles.append(article_json)
            
        except Exception as e:
            print(f"Error creating article for {cat}: {e}")
            continue

    # Wrap everything up to match what your index.html webpage expects
    final_output = {"news": all_articles}
    
    # Overwrite the shared data file on your webpage server
    with open("news_data.json", "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=2, ensure_ascii=False)
    print("Successfully updated news_data.json with fresh daily news!")

if __name__ == "__main__":
    build_daily_newspaper()

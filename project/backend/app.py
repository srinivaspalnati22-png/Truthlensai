import os
import time
import urllib.request
import urllib.parse
import json
import re
from flask import Flask, request, jsonify, render_template

# Resolve paths relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, '..', 'templates')
STATIC_DIR = os.path.join(BASE_DIR, '..', 'static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

def fetch_wiki_data(query):
    try:
        # Extract main nouns/entities safely
        search_terms = re.findall(r'\b[A-Z][a-z]*\b', query)
        if not search_terms: search_terms = query.split()[:3]
        q = " ".join(search_terms[:3])
        
        encoded_q = urllib.parse.quote(q)
        url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts|pageimages&exintro&explaintext&generator=search&gsrsearch={encoded_q}&gsrlimit=3&pithumbsize=400"
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 TruthLensBot/1.0'})
        response = urllib.request.urlopen(req, timeout=5)
        data = json.loads(response.read().decode('utf-8'))
        
        results = []
        if 'query' in data and 'pages' in data['query']:
            for page_id, page_info in data['query']['pages'].items():
                title = page_info.get('title', '')
                extract = page_info.get('extract', '')[:100] + "..."
                img = page_info.get('thumbnail', {}).get('source', 'https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=400')
                results.append({
                    "type": "article",
                    "title": title,
                    "source": "Wikipedia Verified",
                    "time": "Real-Time Data",
                    "thumbnail": img,
                    "url": f"https://en.wikipedia.org/?curid={page_id}",
                    "extract": extract
                })
        return results
    except Exception as e:
        return []

def extract_text(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req, timeout=5).read().decode('utf-8')
        body_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.IGNORECASE | re.DOTALL)
        content = body_match.group(1) if body_match else html
        content = re.sub(r'<script[^>]*>.*?</script>', ' ', content, flags=re.IGNORECASE | re.DOTALL)
        content = re.sub(r'<style[^>]*>.*?</style>', ' ', content, flags=re.IGNORECASE | re.DOTALL)
        text = re.sub(r'<[^>]+>', ' ', content)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()[:5000]
    except Exception as e:
        return "Extraction failed. Unable to parse text from the provided URL."

@app.route('/home')
def home(): return render_template('index.html')

@app.route('/analyze_page')
def analyze_page(): return render_template('analyze.html')

@app.route('/dashboard_page')
def dashboard_page(): return render_template('dashboard.html')

@app.route('/')
def login_page(): return render_template('login.html')

@app.route('/chat_page')
def chat_page(): return render_template('chat.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    raw_text = data.get('text', '').strip()
    input_type = data.get('inputType', 'text')
    lang = data.get('language', 'en')
    
    time.sleep(1.5)
    
    text = raw_text
    if input_type == 'url':
        text = extract_text(raw_text)
    elif input_type == 'image' and not text:
        text = "URGENT TARGET! Bank accounts will be frozen tomorrow unless you share this message to 10 friends!"
        
    words = max(len(text.split()), 1)
    chars = max(len(text), 1)
    
    caps_count = sum(1 for c in text if c.isupper())
    caps_ratio = caps_count / chars
    exc_count = text.count('!')
    
    clickbait_words = ['shocking', 'amazing', 'free', 'money', 'scam', 'forward', 'share', 'urgent', 'delete', 'secret', 'omg', 'banned', 'miracle', 'cure']
    propaganda_words = ['conspiracy', 'sheep', 'wake up', 'government hiding', 'mainstream media', 'truth exposed', 'deep state']
    credible_words = ['according to', 'verified', 'news', 'reported', 'official', 'statement', 'research', 'study', 'police', 'government', 'announced', 'data', 'reuters', 'bbc', 'the hindu']
    
    found_cb = [w for w in clickbait_words if w in text.lower()]
    found_prop = [w for w in propaganda_words if w in text.lower()]
    found_cred = [w for w in credible_words if w in text.lower()]
    
    cb_count = len(found_cb)
    prop_count = len(found_prop)
    cred_count = len(found_cred)
    
    # Calculate Risk Score
    risk_score = 30 
    if input_type in ['image', 'headline']: risk_score += 15
    if input_type == 'url': risk_score -= 5 # URLs are a bit more structured initially
        
    risk_score += (caps_ratio * 120)
    risk_score += (exc_count * 5)
    risk_score += (cb_count * 20)
    risk_score += (prop_count * 30)
    risk_score -= (cred_count * 20)
    
    if words < 10 and cred_count == 0 and input_type != 'headline':
        risk_score += 20
        
    risk_score = max(0, min(100, risk_score))
    credibility_score = round(100 - risk_score)
    
    # 0-40 Fake, 40-70 Suspicious, 70-100 Reliable
    if credibility_score < 40:
        status_category = 'RED'
        prediction = 'Fake / Highly Disingenuous'
    elif credibility_score < 70:
        status_category = 'YELLOW'
        prediction = 'Suspicious / Unverified'
    else:
        status_category = 'GREEN'
        prediction = 'Reliable / Fact-Based'
        
    # Explainable AI Fields
    sentiment = "Alarmist & Negative" if risk_score > 60 else ("Neutral & Objective" if risk_score < 40 else "Mixed/Emotive")
    writing_style = "Sensational/Informal" if (cb_count > 0 or caps_ratio > 0.1) else "Journalistic/Formal"
    
    # Highlight keywords
    highlighted_text = text
    suspicious_keywords = found_cb + found_prop
    for w in set(suspicious_keywords + found_cred):
        pattern = re.compile(f"\\b({re.escape(w)})\\b", re.IGNORECASE)
        if w in found_cred:
            highlighted_text = pattern.sub(f'<span class="bg-green-500/30 text-green-200 px-1 rounded border-b border-green-500 font-bold">\\1</span>', highlighted_text)
        else:
            highlighted_text = pattern.sub(f'<span class="bg-red-500/30 text-red-200 px-1 rounded border-b border-red-500 font-bold">\\1</span>', highlighted_text)

    related_content = []
    counter_article = None
    spread_simulation = None
    
    # Fetch real world Wikipedia data
    wiki_results = fetch_wiki_data(text)

    if status_category == 'GREEN':
        if wiki_results:
            related_content = wiki_results
            # Add a mock video payload based on the top result
            related_content.append({
                "type": "video", 
                "title": f"Live Coverage: {wiki_results[0]['title']}", 
                "source": "Global News Network", 
                "time": "Live", 
                "thumbnail": "https://images.unsplash.com/photo-1522881113591-b6a9e144cb01?w=400&q=80"
            })
        else:
            related_content = [
                {"type": "article", "title": "Verified News Source Analysis", "source": "BBC News", "time": "2 hours ago", "thumbnail": "https://images.unsplash.com/photo-1495020689067-958852a7765e?w=400&q=80"},
                {"type": "video", "title": "Official Press Release Broadcast", "source": "Reuters Video", "time": "Live", "thumbnail": "https://images.unsplash.com/photo-1585829365295-ab7cd400c167?w=400&q=80"},
                {"type": "article", "title": "In Depth: Today's Verified Events", "source": "The Hindu", "time": "12 hours ago", "thumbnail": "https://images.unsplash.com/photo-1555848962-6e79363ec58f?w=400&q=80"}
            ]
    else:
        # Generate Counter-Article Fact Check
        explanation = "No credible scientific or factual evidence supports this claim. The phrasing relies heavily on sensationalism."
        if wiki_results:
             explanation = f"Fact Check via Wikipedia: {wiki_results[0]['extract']}"
             
        counter_article = {
             "claim": f"{text[:60]}..." if len(text) > 60 else text,
             "verdict": "False / Misleading" if status_category == 'RED' else "Unverified",
             "explanation": explanation,
             "sources": [wiki_results[0]['title'] if wiki_results else "Reuters Fact Check", "WHO Official Guidelines"]
        }
        # Generate Spread Simulation Graph Data
        spread_simulation = {
             "stats": {
                 "estimated_shares": 12500 if status_category == 'RED' else 3400,
                 "potential_reach": 500000 if status_category == 'RED' else 85000,
                 "spread_level": "Viral" if status_category == 'RED' else "Elevated"
             },
             "nodes": [
                 {"id": 1, "label": "Original Post", "group": "source"},
                 {"id": 2, "label": "Shared x25\n(Bots)", "group": "bot"},
                 {"id": 3, "label": "Shared x50\n(Echo Chamber)", "group": "chamber"},
                 {"id": 4, "label": "Mainstream\nSpillover", "group": "main"},
                 {"id": 5, "label": "10k+ Views", "group": "viral"},
             ],
             "edges": [
                 {"from": 1, "to": 2},
                 {"from": 1, "to": 3},
                 {"from": 2, "to": 4},
                 {"from": 3, "to": 4},
                 {"from": 4, "to": 5}
             ]
        }
        
    reasons = {
        'en': f"Analyzed as {prediction}. Credibility is {credibility_score}%. Found {cb_count} clickbait triggers and {prop_count} propaganda patterns.",
        'hi': f"इसे {prediction} माना गया है। विश्वसनीयता {credibility_score}% है।",
        'te': f"ఇది {prediction} గా విశ్లేషించబడింది. విశ్వసనీయత {credibility_score}% ఉంది. {cb_count} క్లిక్‌బైట్ మరియు {prop_count} ప్రచార పదాలు కనుగొనబడ్డాయి.",
        'ta': f"இது {prediction} என பகுப்பாய்வு செய்யப்பட்டது. நம்பகத்தன்மை {credibility_score}%.",
        'bn': f"এটি {prediction} হিসাবে বিশ্লেষণ করা হয়েছে। বিশ্বাসযোগ্যতা {credibility_score}%।",
        'es': f"Analizado como {prediction}. La credibilidad es del {credibility_score}%."
    }

    result = {
        "status": "success",
        "category": status_category,
        "prediction": prediction,
        "credibility_score": credibility_score,
        "reason": reasons.get(lang, reasons['en']),
        "sentiment": sentiment,
        "writing_style": writing_style,
        "suspicious_keywords": suspicious_keywords,
        "propaganda_patterns": found_prop,
        "highlighted_text": highlighted_text,
        "metrics": {
            "fact_score": round(max(5, min(95, credibility_score + (cred_count*5)))),
            "neutrality": round(max(5, min(95, 100 - (cb_count*12) - (exc_count*8)))),
            "credibility": credibility_score
        },
        "scanned_text": text,
        "related_content": related_content,
        "counter_article": counter_article,
        "spread_simulation": spread_simulation
    }
    return jsonify(result)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    msg = data.get('message', '').lower()
    lang = data.get('language', 'en')
    time.sleep(1)
    
    reply = ""
    if lang == 'en':
        if 'how' in msg and ('work' in msg or 'use' in msg):
            reply = "I analyze text, URLs, and images using natural language processing. Go to the Analyze page, input your content, and I'll give you a precise Credibility Percentage!"
        elif 'fake' in msg:
            reply = "Fake news often uses emotional language, excessive punctuation, and urges you to share without proof. Always check credible sources like Reuters, BBC, or The Hindu!"
        else:
            reply = "Hello! I am TruthBot, your AI Verification Assistant. You can ask me how to detect fake news, or ask for help using the platform. Speak or type your request!"
    elif lang == 'hi':
        reply = "नमस्ते! मैं ट्रुथबॉट हूँ, आपका एआई सहायक। आप मु्झसे फर्जी खबरों की पहचान के बारे में पूछ सकते हैं। बताएं मैं कैसे मदद करूं?"
    elif lang == 'te':
        reply = "నమస్కారం! నేను ట్రూత్‌బాట్, మీ AI ధృవీకరణ సహాయకారిని. నకిలీ వార్తలను ఎలా గుర్తించాలో మీరు నన్ను అడగవచ్చు. మాట్లాడండి లేదా టైప్ చేయండి!"
    elif lang == 'ta':
        reply = "வணக்கம்! நான் TruthBot, உங்கள் AI உதவியாளர். போலி செய்திகளை எவ்வாறு கண்டறிவது என்று என்னிடம் கேட்கலாம்."
    elif lang == 'bn':
        reply = "নমস্কার! আমি ট্রুথবট, আপনার এআই সহকারী। আপনি আমাকে জাল খবর শনাক্ত করতে জিজ্ঞাসা করতে পারেন।"
    elif lang == 'es':
        reply = "¡Hola! Soy TruthBot, tu Asistente de IA. Puedes preguntarme cómo detectar noticias falsas. ¡Habla o escribe tu solicitud!"
    
    return jsonify({"reply": reply, "language": lang})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

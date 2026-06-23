import urllib.request
import urllib.parse
import json
import re
from .utils import logger

# Curated Roman Urdu vocabulary & common stop words (purified to exclude common English words like 'the', 'he', 'me', 'pe', 'per', 'do')
ROMAN_URDU_WORDS = {
    "hai", "hain", "aur", "ko", "se", "ka", "ki", "ke", "mein", "kya", "kiya", "nahi", "nahin", 
    "hota", "hote", "hoti", "hoga", "hogi", "hogay", "tha", "thi", "par", "ya", 
    "agar", "ho", "krna", "karna", "kr", "kar", "rha", "raha", "rahi", "rhe", "rahe", "hun", "hoon", 
    "sath", "saath", "liye", "liya", "diya", "de", "ek", "aik", "puchna", "bolna", 
    "smjh", "samajh", "chahiye", "kuch", "kuchh", "baare", "bare", "kare", "karey", "karta", "kartay", 
    "karti", "khatam", "shuru", "nikaah", "nikah", "shadi", "talaq", "khula", "masla", "qanoon", 
    "kanoon", "adalat", "mujhe", "mujh", "mera", "meri", "mere", "tum", "tumhara", "aap", "aapka", 
    "apka", "apki", "aapki", "bhai", "behan", "abbu", "ammi", "walid", "walida", "bacha", "bache", 
    "larki", "larka", "aurat", "mard", "khawateen", "shohar", "biwi", "talaaq", "zameen", "ghar", "bhi"
}

# Standard English stop words and indicators to balance the heuristic
ENGLISH_INDICATORS = {
    "the", "be", "to", "of", "and", "a", "in", "that", "have", "it", "for", "not", "on", "with", "he", 
    "as", "you", "do", "at", "this", "but", "his", "by", "from", "they", "we", "say", "her", "she", 
    "or", "an", "will", "my", "one", "all", "would", "there", "their", "what", "so", "up", "out", 
    "if", "about", "who", "get", "which", "go", "me", "when", "make", "can", "like", "time", "no", 
    "just", "him", "know", "take", "people", "into", "year", "your", "good", "some", "could", 
    "them", "see", "other", "than", "then", "now", "look", "only", "come", "its", "over", 
    "think", "also", "back", "after", "use", "two", "how", "our", "work", "first", "well", 
    "way", "even", "new", "want", "because", "any", "these", "give", "day", "most", "us", 
    "is", "are", "was", "were", "been", "has", "had", "should", "would", "could", "law", 
    "legal", "court", "pakistani", "process", "rights", "harassment", "cyber", "tenant"
}

def detect_language(text: str) -> str:
    """
    Detects if the input query is 'urdu_script', 'roman_urdu', or 'english'.
    """
    if not text or not text.strip():
        return "english"

    # 1. Check for Urdu/Arabic characters
    if any(ord(c) >= 0x0600 and ord(c) <= 0x06FF for c in text):
        return "urdu_script"

    # 2. Tokenize and check for Roman Urdu and English indicator words
    words = re.findall(r'\b\w+\b', text.lower())
    if not words:
        return "english"

    roman_match_count = sum(1 for w in words if w in ROMAN_URDU_WORDS)
    english_match_count = sum(1 for w in words if w in ENGLISH_INDICATORS)
    
    logger.info(f"Language detection scores - Roman Urdu matches: {roman_match_count}, English matches: {english_match_count}")
    
    # If the user uses a lot of standard English words, classify as English
    if english_match_count > roman_match_count:
        return "english"
        
    # Heuristic: If we have > 1 roman urdu words, or if it is a very short query (<= 4 words) with at least 1 match
    if roman_match_count > 1 or (len(words) <= 4 and roman_match_count >= 1):
        return "roman_urdu"

    return "english"

def translate_text(text: str, sl: str = "auto", tl: str = "en") -> str:
    """
    Translates text between languages using Google's public translation engine.
    """
    if not text or not text.strip():
        return text

    try:
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": sl,
            "tl": tl,
            "dt": "t",
            "q": text
        }
        data = urllib.parse.urlencode(params).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Content-Type": "application/x-www-form-urlencoded"
            }
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
            translated_sentences = [sentence[0] for sentence in data[0] if sentence[0]]
            return "".join(translated_sentences)
    except Exception as e:
        logger.error(f"Google Translation failed: {str(e)}")
        return text

def translate_to_urdu_and_roman(text: str) -> tuple:
    """
    Translates English text to Urdu script and Roman Urdu transliteration.
    Returns: (urdu_script, roman_urdu)
    """
    if not text or not text.strip():
        return text, text

    try:
        url = "https://translate.googleapis.com/translate_a/single"
        params = [
            ("client", "gtx"),
            ("sl", "en"),
            ("tl", "ur"),
            ("dt", "t"),
            ("dt", "rm"),
            ("q", text)
        ]
        data = urllib.parse.urlencode(params).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Content-Type": "application/x-www-form-urlencoded"
            }
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            res = response.read().decode("utf-8")
            data = json.loads(res)
            
            # Extract Urdu script translation
            urdu_sentences = []
            for s in data[0]:
                if s[0]:
                    urdu_sentences.append(s[0])
            urdu_script = "".join(urdu_sentences)
            
            # Extract Roman Urdu transliteration from Google's romanization field
            roman_urdu = ""
            if len(data[0]) > 0 and len(data[0][-1]) > 2 and data[0][-1][2]:
                roman_urdu = data[0][-1][2]
            else:
                # Fallback if no romanization segment returned
                roman_urdu = urdu_script
                
            return urdu_script, roman_urdu
    except Exception as e:
        logger.error(f"Urdu translation and Romanization failed: {str(e)}")
        return text, text

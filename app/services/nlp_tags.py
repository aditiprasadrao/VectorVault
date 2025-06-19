import spacy
from textblob import TextBlob

nlp = spacy.load("en_core_web_sm")

def extract_tags(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    topics = [token.text for token in doc if token.pos_ == "NOUN"][:10]

    # ✅ Use TextBlob directly for sentiment
    sentiment = TextBlob(text).sentiment.polarity

    summary = text[:300] + "..."
    return {
        "entities": entities,
        "topics": topics,
        "sentiment": sentiment,
        "summary": summary
    }

# Optional test
if __name__ == "__main__":
    test_text = "I absolutely love this app. It's fast, helpful, and intuitive!"
    print(extract_tags(test_text))

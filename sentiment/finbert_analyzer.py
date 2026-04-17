from transformers import pipeline

sentiment_model = pipeline(
    "sentiment-analysis",
    model="ProsusAI/finbert"
)

def analyze_sentiment(headlines):
    results = sentiment_model(headlines)

    score = 0
    for r in results:
        if r["label"] == "POSITIVE":
            score += 1
        elif r["label"] == "NEGATIVE":
            score -= 1

    if score > 0:
        return "POSITIVE"
    elif score < 0:
        return "NEGATIVE"
    else:
        return "NEUTRAL"
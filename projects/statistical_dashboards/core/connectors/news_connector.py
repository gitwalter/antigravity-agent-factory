import requests
import xmltodict
import pandas as pd
import re


class NewsConnector:
    """Connector for real financial news using RSS and simple sentiment analysis."""

    def __init__(self, api_key=None):
        self.api_key = api_key
        self.rss_url = (
            "https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
        )

    def get_latest_news(self, query="finance", country="us"):
        """Fetches latest news from Google News RSS."""
        try:
            url = self.rss_url.format(query=query)
            response = requests.get(url, timeout=10)
            data = xmltodict.parse(response.content)

            items = data.get("rss", {}).get("channel", {}).get("item", [])
            if not isinstance(items, list):
                items = [items]

            news_list = []
            for item in items[:15]:
                title = item.get("title", "Unknown Title")
                link = item.get("link", "#")
                news_list.append(
                    {
                        "title": title,
                        "link": link,
                        "source": item.get("source", {}).get("#text", "N/A")
                        if isinstance(item.get("source"), dict)
                        else item.get("source", "N/A"),
                        "pubDate": item.get("pubDate", ""),
                        "sentiment": self._analyze_sentiment(title),
                    }
                )

            return pd.DataFrame(news_list)
        except Exception as e:
            print(f"Error fetching news: {e}")
            # Fallback to empty DF rather than mock
            return pd.DataFrame()

    def _analyze_sentiment(self, text):
        """Basic keyword-based sentiment scorer."""
        text = text.lower()
        positive_words = [
            "rally",
            "soar",
            "gain",
            "surpass",
            "record",
            "high",
            "win",
            "bullish",
            "growth",
            "profit",
            "dividend",
            "optimistic",
        ]
        negative_words = [
            "slump",
            "drop",
            "crash",
            "fail",
            "loss",
            "bearish",
            "cut",
            "warning",
            "inflation",
            "recession",
            "debt",
            "concern",
        ]

        pos_score = sum(1 for word in positive_words if word in text)
        neg_score = sum(1 for word in negative_words if word in text)

        if pos_score > neg_score:
            return "Positive"
        elif neg_score > pos_score:
            return "Negative"
        else:
            return "Neutral"

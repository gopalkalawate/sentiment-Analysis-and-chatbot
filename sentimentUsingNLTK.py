import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

# Download the vader_lexicon
# nltk.download('vader_lexicon')

class Analyse:
    def __init__(self):
        self.listt = []  # Instance variable to hold sentiments

    def insert_sentiment(self, text):
        sia = SentimentIntensityAnalyzer()
        sentiment = sia.polarity_scores(text)
        compound = sentiment['compound']  # The compound score of sentiment

        if compound >= 0.75:
            # Ultra Positive
            self.listt.append("Ultra Positive")
        elif compound >= 0.5:
            # Very Positive
            self.listt.append("Very Positive")
        elif compound >= 0.15:
            # Positive
            self.listt.append("Positive")
        elif compound > -0.15:
            # Neutral
            self.listt.append("Neutral")
        elif compound >= -0.5:
            # Negative
            self.listt.append("Negative")
        elif compound >= -0.75:
            # Very Negative
            self.listt.append("Very Negative")
        else:
            # Ultra Negative
            self.listt.append("Ultra Negative")


    def plot_bar_graph(self):
        # Count occurrences of each sentiment category
        ultra_positive_count = self.listt.count("Ultra Positive")
        very_positive_count = self.listt.count("Very Positive")
        positive_count = self.listt.count("Positive")
        neutral_count = self.listt.count("Neutral")
        negative_count = self.listt.count("Negative")
        very_negative_count = self.listt.count("Very Negative")
        ultra_negative_count = self.listt.count("Ultra Negative")

        # Labels for the bar graph
        categories = [
            'Ultra Positive', 'Very Positive', 'Positive', 
            'Neutral', 'Negative', 'Very Negative', 'Ultra Negative'
        ]

        # Corresponding counts
        counts = [
            ultra_positive_count, very_positive_count, positive_count,
            neutral_count, negative_count, very_negative_count, ultra_negative_count
        ]

        # Plotting the bar graph
        plt.figure(figsize=(10, 5))  # Set the figure size
        plt.bar(categories, counts, color=['darkgreen', 'green', 'lightgreen', 'blue', 'lightcoral', 'red', 'darkred'])
        plt.xlabel('Sentiment Categories')
        plt.ylabel('Count')
        plt.title('Sentiment Analysis Distribution')
        plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
        plt.tight_layout()  # Adjust the padding of the plot

        # Save the plot to display in Streamlit
        # return plt  # Save the figure as a .png file
        plt.close()  # Close the figure to avoid displaying it immediately
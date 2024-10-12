import streamlit as st
import matplotlib.pyplot as plt
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from chatFeature import chat, query_model  # Make sure these are correctly implemented

# Download the vader_lexicon
# nltk.download('vader_lexicon')

# Initialize session state for sentiments
if "sentiment_list" not in st.session_state:
    st.session_state.sentiment_list = []


class Analyse:
    def insert_sentiment(self, text):
        sia = SentimentIntensityAnalyzer()
        sentiment = sia.polarity_scores(text)
        compound = sentiment['compound']  # The compound score of sentiment

        # Determine the sentiment category and append to the session state list
        if compound >= 0.75:
            st.session_state.sentiment_list.append("Ultra Positive")
        elif compound >= 0.5:
            st.session_state.sentiment_list.append("Very Positive")
        elif compound >= 0.15:
            st.session_state.sentiment_list.append("Positive")
        elif compound > -0.15:
            st.session_state.sentiment_list.append("Neutral")
        elif compound >= -0.5:
            st.session_state.sentiment_list.append("Negative")
        elif compound >= -0.75:
            st.session_state.sentiment_list.append("Very Negative")
        else:
            st.session_state.sentiment_list.append("Ultra Negative")

        # Debug print to check what sentiments are being added
        print(f"Sentiment added: {st.session_state.sentiment_list[-1]}")
        print(f"Current sentiments list: {st.session_state.sentiment_list}")

    def plot_bar_graph(self):
        # Count occurrences of each sentiment category
        ultra_positive_count = st.session_state.sentiment_list.count("Ultra Positive")
        very_positive_count = st.session_state.sentiment_list.count("Very Positive")
        positive_count = st.session_state.sentiment_list.count("Positive")
        neutral_count = st.session_state.sentiment_list.count("Neutral")
        negative_count = st.session_state.sentiment_list.count("Negative")
        very_negative_count = st.session_state.sentiment_list.count("Very Negative")
        ultra_negative_count = st.session_state.sentiment_list.count("Ultra Negative")

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

        return plt  # Return the figure object for Streamlit to use


# Initialize the Streamlit UI
st.title("Conversation with Sentiment Analysis")
st.write("enter 'exit' to end the conversation")
# Initialize session state for chat history and sentiment
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "conversation_ended" not in st.session_state:
    st.session_state.conversation_ended = False

# Create an instance of the Analyse class
analyse = Analyse()

# Text input for user with a unique key
user_input = st.text_input("You: ", key="user_input_key", placeholder="Type your message here...")

# Function to query the model and insert sentiment
def process_user_input(user_input):
    if user_input.lower() == 'exit':
        st.session_state.conversation_ended = True
        return

    # Analyse the sentiment
    analyse.insert_sentiment(user_input)
    
    # Call the external model to get the AI response
    try:
        response = query_model(user_input)  # This function should be defined in chatFeature
        if isinstance(response, list) and len(response) > 0 and "generated_text" in response[0]:
            ai_response = response[0]['generated_text'].strip()
            st.session_state.chat_history.append(f"You: {user_input}")
            st.session_state.chat_history.append(f"AI: {ai_response}")
        elif isinstance(response, dict) and "error" in response:
            st.session_state.chat_history.append(f"Error: {response['error']}")
        else:
            st.session_state.chat_history.append("AI: I'm sorry, I couldn't generate a response. Please try again.")
    except Exception as e:
        st.session_state.chat_history.append(f"An error occurred: {e}")

# If the conversation hasn't ended, process the user's input
if not st.session_state.conversation_ended and user_input:
    process_user_input(user_input)

# Display the chat history
st.subheader("Chat History")
for message in st.session_state.chat_history:
    st.markdown(f"{message}")  # Using markdown for better formatting

# If the user types 'exit', display the sentiment analysis bar graph
if st.session_state.conversation_ended:
    st.subheader("Sentiment Analysis Results")
    
    # Check if there are sentiments to plot
    if len(st.session_state.sentiment_list) > 0:
        # Plot the bar graph using Matplotlib and Streamlit
        fig = analyse.plot_bar_graph()  # Call the updated plot function
        st.pyplot(fig)  # Display the plot in Streamlit
    else:
        st.write("No sentiments to display.")

    st.write("Goodbye! Conversation has ended.")

# Reset user input after submission, using a different key
st.text_input("You: ", key="user_input_reset_key", value="", placeholder="Type your message here...")

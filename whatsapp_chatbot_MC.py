import nltk
import random
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Ensure NLTK data is downloaded
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()

# Define some predefined responses based on keywords
responses = {
    "hi": ["Hello!", "Hey there!", "Hi! How can I help you today?", "Greetings!", "Hiya!", "What's up?", "Howdy!", "Hello there!", "A warm hello to you!", "Hi, nice to see you!"],
    "hello": ["Hi! What's up?", "Hello, how can I assist you?", "Hey! How can I help?", "Hello there!", "Greetings!", "A friendly hello!", "Hi!", "Well hello!", "How can I be of service?", "Hello to you too!"],
    "how are you": ["I'm doing great, thank you for asking!", "I'm fine! How about you?", "Feeling good and ready to assist!", "I'm doing well, thanks!", "Pretty good, how are you?", "Excellent, thank you!", "I'm operating smoothly!", "All systems are go!", "Feeling quite alright today!", "Thank you for asking, I'm doing well."],
    "bye": ["Goodbye!", "See you later!", "Take care!", "Have a great day!", "Farewell!", "Until next time!", "So long!", "Catch you later!", "Have a good one!", "Bye for now!"],
    "thanks": ["You're welcome!", "No problem! 😊", "Glad to be of help!", "My pleasure!", "You're very welcome!", "Not a problem at all!", "Happy to assist!", "Consider it done!", "Any time!", "It was my pleasure."],
    "help": ["Sure! What do you need help with?", "I'm here to help! How can I assist you?", "Absolutely! How can I be of service?", "How may I help you today?", "What can I do for you?", "I'm ready to assist. What's on your mind?", "Tell me what you need!", "Let me see what I can do.", "How can I be of assistance?", "What kind of help are you looking for?"],
    "what's your name": ["I don't have a name, I'm an AI assistant.", "You can call me AI.", "I am a large language model.", "I am a language AI.", "I go by AI.", "I don't have a personal name.", "I'm here to help, not to be named!", "You can simply refer to me as the AI.", "I am a virtual assistant.", "I am a computer program."],
    "tell me a joke": ["Why don't scientists trust atoms? Because they make up everything!", "What do you call a lazy kangaroo? Pouch potato!", "Knock, knock.\nWho's there?\nLettuce.\nLettuce who? Lettuce in, it's cold out here!", "Why did the bicycle fall over? Because it was two tired!", "What do you call a fish with no eyes? Fsh!", "Why did the scarecrow win an award? Because he was outstanding in his field!", "Want to hear a construction joke? I'm still working on it!", "What musical instrument is found in the bathroom? A tuba toothpaste!", "Why did the golfer wear two pairs of pants? In case he got a hole-in-one!", "What do you call a fake noodle? An impasta!"],
    "how's the weather": ["I'm sorry, I don't have real-time weather information for Mannargudi right now.", "I can't provide live weather updates.", "Unfortunately, I don't have access to the current weather.", "As a language model, I don't have real-time data like weather.", "I'm unable to give you the current weather conditions.", "I don't have that information at my fingertips.", "I can't access live weather feeds.", "Sorry, I can't help with the weather right now.", "I'm not equipped to provide weather updates.", "For the latest weather, I recommend checking a weather app or website."],
    "good morning": ["Good morning!", "Hello! Hope you have a wonderful day!", "Morning! What can I do for you today?", "A bright good morning to you!", "Top of the morning!", "Good day to you!", "Rise and shine!", "Hope you slept well!", "Good morning, how can I help?", "Wishing you a lovely morning!"],
    "good afternoon": ["Good afternoon!", "Hello! How's your day going?", "Afternoon! What can I help you with?", "A pleasant good afternoon to you!", "Hope you're having a good day!", "Afternoon greetings!", "How's the day treating you?", "Good afternoon, what can I do for you?", "Hope your afternoon is going well!", "Wishing you a productive afternoon!"],
    "good evening": ["Good evening!", "Hello! Hope you had a good day!", "Evening! What can I assist you with?", "A lovely good evening to you!", "Hope you're having a nice evening!", "Evening greetings!", "How was your day?", "Good evening, how can I help?", "Wishing you a relaxing evening!", "Hope you had a great day!"],
    "thank you": ["You're very welcome!", "Not a problem at all!", "Happy to help!", "Consider it done!", "You're most welcome!", "It was my pleasure assisting you.", "Glad I could be of service!", "No worries!", "Anytime!", "Happy to help out!"],
    "ok": ["Okay!", "Got it.", "Understood.", "Alright.", "Sounds good.", "Roger that!", "Acknowledged.", "Copy that.", "Sure thing.", "Will do."],
    "yes": ["Yes.", "Absolutely.", "Indeed.", "Certainly.", "Yup.", "Affirmative.", "That's correct.", "Precisely.", "Exactly.", "You got it."],
    "no": ["No.", "Not at all.", "Nope.", "Negative.", "By no means.", "Certainly not.", "That's incorrect.", "Unfortunately not.", "I'm afraid not.", "Nay."],
    "maybe": ["Maybe.", "Perhaps.", "Possibly.", "It's uncertain.", "I'm not sure.", "That's a possibility.", "It could be.", "Let me think about that.", "Potentially.", "It's hard to say."],
    "tell me something interesting": ["Did you know that honey never spoils?", "Octopuses have three hearts.", "Bananas are berries, but strawberries aren't.", "The Eiffel Tower can grow by about 15 cm during the summer due to thermal expansion.", "There are more trees on Earth than stars in the Milky Way galaxy.", "A group of flamingos is called a flamboyance.", "Your brain uses about 20% of your body's energy.", "The average person walks the equivalent of five times around the Earth in their lifetime.", "The sound of a whip cracking is caused by the tip moving faster than the speed of sound.", "There are more than 8 million different species of animals on Earth."],
    "what do you think": ["That's an interesting question.", "I'll need a bit more information to form a complete thought.", "From my perspective...", "It seems that...", "Based on what I know...", "My analysis suggests...", "That's a valid point.", "I'm still processing that.", "What are your thoughts on it?", "It's a complex issue."],
    "how does that work": ["That's a great question! It works by...", "Essentially, the process involves...", "The mechanism behind that is...", "Let me explain how that functions...", "In simple terms...", "The way it operates is...", "That's a bit technical, but in general...", "Think of it like this...", "The underlying principle is...", "It's a fascinating process where..."],
    "can you help me with": ["Yes, I can definitely help you with that.", "I'd be happy to assist you with that.", "Sure, what do you need help with regarding that?", "Absolutely, how can I help you with that?", "Of course, tell me more about what you need.", "Yes, I can certainly try my best to help.", "I'm here to assist you with that.", "What are the specifics of what you need help with?", "Consider it done, how can I assist you with that?", "Yes, that's something I can help you with."],
    "i don't understand": ["I see. Let me try explaining it another way.", "Apologies, let me rephrase that.", "Perhaps this explanation will be clearer...", "Let me break it down for you.", "What part are you finding confusing?", "I can try to simplify it.", "Let me give you an example.", "Maybe a different perspective will help.", "Don't worry, it can be tricky. Let's try again.", "How about I explain it using an analogy?"],
    "i'm bored": ["Oh, I'm sorry to hear that! How about I tell you a fun fact?", "Hmm, perhaps I can tell you a story.", "Maybe I can find something interesting for you to do online (though I can't browse myself).", "Is there anything specific you'd like to talk about?", "How about we play a quick game (like a riddle)?", "I can try to find a poem for you.", "Would you like to hear a joke?", "Maybe thinking about something new will help. What are you curious about?", "Sometimes a change of pace helps. Is there anything you'd like to explore?", "Let's see... what interesting tidbit can I share?"],
    "that's funny": ["Glad you liked it! 😊", "Haha, I'm glad I could make you laugh!", "Happy to bring a little humor to your day!", "My programming includes a bit of wit!", "Good to know my joke landed!", "I aim to please!", "A little laughter can go a long way!", "Glad I could brighten your day!", "Humor is important!", "Consider that a complimentary chuckle!"],
    "i'm happy": ["That's wonderful to hear!", "Great! I'm happy to hear that!", "Fantastic! Keep that positive energy!", "That's the best news!", "So glad to hear you're feeling good!", "Wonderful! What's making you happy?", "That's excellent!", "Keep smiling! 😊", "Positive vibes are the best!", "So happy for you!"],
    "i'm sad": ["Oh, I'm sorry to hear that. Is there anything I can do to help?", "I'm sorry you're feeling down. Would you like to talk about it?", "That sounds tough. Remember, it's okay not to be okay.", "Sending you virtual support. Is there anything I can do to make things a little better?", "I'm here for you. What's on your mind?", "Sometimes talking helps. I'm a good listener (or, well, reader!).", "I hope things get better for you soon.", "Take your time and be kind to yourself.", "Remember that feelings are temporary.", "Is there anything at all I can assist you with to take your mind off things?"],
}

# Function to preprocess the message
def preprocess_message(msg):
    # Tokenize the message
    words = word_tokenize(msg.lower())
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    # Lemmatize the words
    words = [lemmatizer.lemmatize(word) for word in words]
    return words

# Function to find an appropriate response based on the input
def find_response(words):
    for word in words:
        if word in responses:
            return random.choice(responses[word])
    return "Sorry, I didn't quite understand that. Can you say it differently?"

# Function to enhance the message by modifying its tone or content
def enhance_message(msg):
    # This can modify the message's formality, tone, or structure
    words = preprocess_message(msg)
    response = find_response(words)

    # Enhance the response further by rephrasing or adding more details
    enhanced_response = response + " 🤖 I'm here to help you with anything!"

    # You can also add random variations to make the responses less predictable
    if random.choice([True, False]):
        enhanced_response += " Let me know if you need anything else."
    return enhanced_response

# Main loop to handle user input
def chatbot():
    print("Chatbot is now running... Type 'bye' to exit.")
    while True:
        # Taking user input
        user_input = input("You: ").lower()

        # If the user types 'bye', exit the loop
        if user_input == "bye":
            print("Chatbot: Goodbye! See you later!")
            break

        # Enhance and respond to the message
        response = enhance_message(user_input)

        # Display the enhanced message
        print(f"Chatbot: {response}")

# Run the chatbot
chatbot()

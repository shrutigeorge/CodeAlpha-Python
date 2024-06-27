#Task 3: Simple Chatbot
import nltk
import numpy as np
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction import text

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('wordnet')

# Expanded corpus
corpus = """
Hello, how can I help you?
Hi, how can I assist you today?
Good morning! How can I help you?
Good evening! How can I assist you?
I am a chatbot created to assist you.
What do you want to know about?
Feel free to ask me anything.
I am here to help you with any questions you have.
What can I do for you?
How are you today?
I'm here to provide you with information.
Thank you for reaching out to me.
You're welcome!
Goodbye! Have a great day.
"""

# Tokenize the corpus
sentence_tokens = nltk.sent_tokenize(corpus)
word_tokens = nltk.word_tokenize(corpus)

# Preprocess the text
lemmer = nltk.stem.WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

# Preprocess the stop words
stop_words = text.ENGLISH_STOP_WORDS
preprocessed_stop_words = [LemNormalize(word)[0] for word in stop_words]

# Define response generation function
def response(user_response):
    chatbot_response = ''
    sentence_tokens.append(user_response)
    
    # Vectorize the sentences and user response
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words=preprocessed_stop_words, token_pattern=None)
    tfidf = TfidfVec.fit_transform(sentence_tokens)
    
    # Compute cosine similarity between user input and sentences
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    
    if req_tfidf == 0:
        chatbot_response = "I am sorry! I don't understand you."
    else:
        chatbot_response = sentence_tokens[idx]
    
    sentence_tokens.remove(user_response)
    
    return chatbot_response

# Running the chatbot
flag = True
print("Chatbot: Hello! I am your assistant. How can I help you?")

while flag:
    user_response = input("You: ").lower()
    if user_response not in ['bye', 'exit', 'quit']:
        if user_response in ['thanks', 'thank you']:
            flag = False
            print("Chatbot: You're welcome!")
        else:
            print("Chatbot:", response(user_response))
    else:
        flag = False
        print("Chatbot: Goodbye! Take care.")

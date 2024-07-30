


from flask import Flask, request, jsonify
import pyttsx3
import speech_recognition as sr
import logging
from datetime import datetime
from PIL import Image
import requests
from io import BytesIO
import pyjokes
import sympy as sp
import json
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from nltk.tokenize import sent_tokenize

# Initialize Flask app
app = Flask(__name__)

# Initialize logging
logging.basicConfig(filename='marcus.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

# Initialize speech recognition and synthesis
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# Load pre-trained model and tokenizer for text classification
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased')

# Initialize a dictionary to store diary entries
diary_entries = {}

# Log file to write all spoken responses and user inputs
log_file = "spoken_responses.txt"

def log_user_input(input_text):
    with open(log_file, "a", encoding="utf-8") as file:
        file.write(f"User: {input_text}\n")

def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()
    log_user_input(text)

def greet_user():
    current_hour = datetime.now().hour
    if current_hour < 12:
        greeting = "Good morning!"
    elif 12 <= current_hour < 18:
        greeting = "Good afternoon!"
    elif 18 <= current_hour < 21:
        greeting = "Good evening!"
    else:
        greeting = "Good night!"
    speak(greeting)
    return greeting

def get_time_info(info_type):
    now = datetime.now()
    if info_type == 'time':
        return now.strftime("%H:%M:%S")
    elif info_type == 'day':
        return now.strftime("%A")
    elif info_type == 'date':
        return now.strftime("%d %B %Y")
    elif info_type == 'year':
        return now.strftime("%Y")
    return "Please try again."

def handle_image_generation(command):
    if 'generate image' in command:
        try:
            image_url = "https://picsum.photos/200/300"
            response = requests.get(image_url)
            img = Image.open(BytesIO(response.content))
            img.save("generated_image.jpg")
            return "Image generated and saved as 'generated_image.jpg'."
        except Exception as e:
            logging.error(f"Image generation error: {str(e)}")
            return f"Error: {str(e)}"
    return None

def handle_avatar_generation(command):
    if 'generate avatar' in command:
        description = command.replace("generate avatar", "").strip()
        try:
            api_url = f"https://avataaars.io/?avatarStyle=Circle&topType=LongHairFro&accessoriesType=Prescription01&hairColor=Brown&facialHairType=BeardMedium&facialHairColor=Brown&clotheType=ShirtCrewNeck&clotheColor=PastelBlue&eyeType=Happy&eyebrowType=Default&mouthType=Smile&skinColor=Light"
            response = requests.get(api_url)
            img = Image.open(BytesIO(response.content))
            filename = "generated_avatar.png"
            img.save(filename)
            return f"Avatar generated and saved as '{filename}'."
        except Exception as e:
            logging.error(f"Avatar generation error: {str(e)}")
            return f"Error: {str(e)}"
    return None

def handle_command(command):
    commands = {
        'open youtube': lambda: "Opening YouTube...",  # placeholder
        'open chrome': lambda: "Opening Chrome...",   # placeholder
        'exit': lambda: "Exiting...",
        'generate image': handle_image_generation,
        'generate avatar': handle_avatar_generation,
        'create poll': lambda: "Poll creation not implemented.",
        'analyze document': lambda: "Document analysis not implemented.",
        'shopping assistant': lambda: "Shopping assistant not implemented.",
        'stock market update': lambda: "Stock market update not implemented.",
        'personalized learning': lambda: "Personalized learning path not implemented.",
        'recruitment assistant': lambda: "Recruitment assistant not implemented.",
        'productivity dashboard': lambda: "Customizable productivity dashboard not implemented.",
        'event management': lambda: "Virtual event management not implemented.",
        'social media insights': lambda: "Enhanced social media insights not implemented.",
        'customer support': lambda: "AI-based customer support not implemented.",
        'content moderation': lambda: "Automatic content moderation not implemented.",
        'home automation': lambda: "Voice-activated home automation not implemented.",
        'finance management': lambda: "AI-powered personal finance management not implemented.",
        'custom avatars': lambda: "Customizable user avatars not implemented.",
        'language games': lambda: "Interactive language games not implemented.",
        'travel concierge': lambda: "Virtual travel concierge not implemented.",
        'fitness coaching': lambda: "AI-based fitness coaching not implemented.",
        'traffic updates': lambda: "Real-time traffic updates not implemented.",
        'meditation guides': lambda: "Personalized meditation and relaxation guides not implemented.",
        'home repair assistant': lambda: "Virtual home repair assistant not implemented.",
        'predictive analytics': lambda: "Predictive analytics not implemented.",
        'automated workflow': lambda: "Automated workflow management not implemented.",
        'sentiment analysis': lambda: "Sentiment analysis not implemented.",
        'contextual awareness': lambda: "Contextual awareness not implemented.",
        'voice biometrics': lambda: "Voice biometrics not implemented.",
        'real-time collaboration': lambda: "Real-time collaboration not implemented.",
        'behavioral analytics': lambda: "Behavioral analytics not implemented.",
        'dynamic content generation': lambda: "Dynamic content generation not implemented.",
        'custom alerts': lambda: "Custom alerts and notifications not implemented.",
        'social interaction simulation': lambda: "Social interaction simulation not implemented.",
        'health tracking': lambda: "Health and wellness tracking not implemented.",
        'interactive storytelling': lambda: "Interactive storytelling not implemented.",
        'data visualization': lambda: "Advanced data visualization not implemented.",
        'voice-controlled gaming': lambda: "Voice-controlled gaming not implemented.",
        'writing assistant': lambda: "AI-powered writing assistant not implemented.",
        'personalized recommendations': lambda: "Advanced personalization not implemented.",
    }

    for keyword, handler in commands.items():
        if keyword in command:
            return handler()
    return "I didn't understand that command."

def handle_joke():
    return pyjokes.get_joke()

def handle_math(command):
    try:
        expression = command.replace("solve", "").strip()
        result = sp.sympify(expression)
        return str(result)
    except Exception as e:
        logging.error(f"Math error: {str(e)}")
        return f"Error: {str(e)}"

def handle_summarization(command):
    text_to_summarize = command.replace("summarize", "").strip()
    sentences = sent_tokenize(text_to_summarize)
    if len(sentences) > 2:
        summary = ' '.join(sentences[:2]) + "..."
    else:
        summary = text_to_summarize
    return summary

def classify_text(text):
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class = torch.argmax(logits, dim=1).item()
    return predicted_class

def handle_dream_analysis(command):
    common_themes = {
        'flying': 'Dreaming of flying can symbolize a desire for freedom or escape from limitations.',
        'falling': 'Dreaming of falling often represents feelings of insecurity or fear of losing control.',
        'water': 'Dreaming of water can signify emotions, subconscious thoughts, or a need for cleansing and renewal.',
        'being chased': 'Dreaming of being chased may reflect feelings of anxiety or being pursued by problems or fears.',
        'teeth falling out': 'Dreaming of teeth falling out can indicate concerns about appearance, self-esteem, or communication issues.',
        'being late': 'Dreaming of being late often symbolizes anxiety about missing opportunities or failing to meet expectations.'
    }
    dream_description = command.replace("analyze my dream:", "").strip().lower()
    for theme, interpretation in common_themes.items():
        if theme in dream_description:
            return f"Your dream about {theme} could mean: {interpretation}"
    return "Your dream is unique! It may have personal significance related to your current thoughts and feelings."

def handle_diary(command):
    if 'write diary' in command:
        entry = command.replace("write diary", "").strip()
        date = datetime.now().strftime("%Y-%m-%d")
        if date in diary_entries:
            diary_entries[date].append(entry)
        else:
            diary_entries[date] = [entry]
        with open('diary.txt', 'a', encoding='utf-8') as diary_file:
            diary_file.write(f"{date}: {entry}\n")
        return "Your diary entry has been saved."
    elif 'read diary' in command:
        date = datetime.now().strftime("%Y-%m-%d")
        entries = diary_entries.get(date, [])
        return "\n".join(entries) if entries else "No entries found for today."
    return "Invalid diary command."

@app.route('/command', methods=['POST'])
def command_view():
    data = request.json
    command = data.get('command', '').lower()
    
    logging.info(f"Received command: {command}")
    
    # Handle different types of commands
    if "joke" in command:
        response = handle_joke()
    elif "solve" in command:
        response = handle_math(command)
    elif "summarize" in command:
        response = handle_summarization(command)
    elif "dream" in command:
        response = handle_dream_analysis(command)
    elif "diary" in command:
        response = handle_diary(command)
    else:
        response = handle_command(command)
    
    speak(response)
    return jsonify({'response': response})

if __name__ == '__main__':
    greet_user()
    app.run(debug=True)

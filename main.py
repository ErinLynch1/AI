#%%
from flask import Flask, render_template, request

#from chatbot import chatbot
import os

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import os
# Creating ChatBot Instancep

chatbot = ChatBot(
    'Chatty',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.BestMatch',
        {
        'import_path': 'chatterbot.logic.BestMatch',
        'default_response': 'I am sorry, but I do not understand. I am still learning.',
        'maximum_similarity_threshold': 0.90
        }
    ],
    database_uri='sqlite:///database.sqlite3'
) 
 # Training with Personal Ques & Ans 
training_data_COVIDquesans = open('training_data/COVID.txt').read().splitlines()
training_data_simpleconv = open('training_data/simple.txt').read().splitlines()
training_data_GOVquesans = open('training_data/Goverment.txt').read().splitlines()
training_data_MEDquesans = open('training_data/Medical.txt').read().splitlines()

training_data = training_data_COVIDquesans + training_data_simpleconv+ training_data_GOVquesans+training_data_MEDquesans

trainer = ListTrainer(chatbot)
trainer.train(training_data) 
# Training with English Corpus Data 
trainer_corpus = ChatterBotCorpusTrainer(chatbot)

app = Flask(__name__)
app.static_folder = 'static'

    
@app.route("/")
def home():
    return render_template("index.html")
    
@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(chatbot.get_response(userText))

if __name__ == "__main__":
     
    app.run(port=8000, debug=True)

# %%

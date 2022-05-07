import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
import warnings

from heapq import nlargest

warnings.filterwarnings('ignore')

nlp = spacy.load('en_core_web_sm')

from flask import Flask, jsonify, request
app = Flask(__name__)


stopwords = list(STOP_WORDS)

@app.route('/', methods=['GET','POST'])
def index():
    if (request.method == 'POST'):
        data_sent = request.get_data()
        summarized_data = summaraize(data_sent)
        return summarized_data
    else:
        return "hello world"

def summaraize(text):
    text = str(text)
    #text = text.replace("\n", " ")
    doc = nlp(text)
    tokens = [token.text for token in doc]

    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1

    max_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word]/max_frequency
    
    sentence_tokens = [sent for sent in doc.sents]
    sentence_scores = {}
    
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]



    select_length = int(len(sentence_tokens)*0.35)
    summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)
    final_summary = [word.text for word in summary]
    summary = ''.join(final_summary)
    # summary = summary.replace('\xe2\x80\x9c', "")
    summary = summary.replace("'\n", " ")
    return summary



if __name__ == '__main__':
    app.run(port=3333)



# if __name__ == '__main__':
#     app.run(host='172.25.11.60', port=3333)
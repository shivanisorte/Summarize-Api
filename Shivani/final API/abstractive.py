# pip install transformers==2.8.0
# pip install torch==1.4.0


from flask import Flask, jsonify, request

import torch 
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config


model = T5ForConditionalGeneration.from_pretrained('t5-small')
tokenizer = T5Tokenizer.from_pretrained('t5-small')
device = torch.device('cpu')

app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def index():
    print(request)
    if (request.method == 'POST'):
        data_sent = request.get_json()
        print(data_sent['1'])
        data_sent = data_sent['1']
        summarized_data = summaraize(data_sent)

      
        return summarized_data
    else:
        return "hello world. the server for abstractive summary is up and running."


def summaraize(text):
  preprocessed_text = text.strip().replace('\n', '')
  t5_input_text = 'summarize: ' + preprocessed_text

  tokenized_text = tokenizer.encode(t5_input_text, return_tensors='pt').to(device)

  summary_ids = model.generate(tokenized_text, min_length=30, max_length=120)
  summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
  

  return summary
      

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=81)
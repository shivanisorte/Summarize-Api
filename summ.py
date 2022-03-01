import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
import warnings

from heapq import nlargest


warnings.filterwarnings('ignore')

text = '''Abstract - Books are considered to be a person’s most loyal friend. They impart knowledge and wisdom and are an integral part of learning. However, not everyone has the financial means or the luxury of  splurging money on buying new books or purchasing a library subscription.   This paper presents the development of an Android Application “Book Barter” that aims to tackle this problem by providing a platform for users to borrow and lend books. It allows users to keep a record of all books in their personal collection which is stored in the database. When a user wishes to read a book that they do not own, they may simply search for it and will be presented with users around them who own the same book which is stored in the Firebase Backend and can then proceed to request to borrow that particular book. This application has been developed in Android Studio and is easy and straightforward to use. Thus, “Book Barter” acts as an affordable solution for readers to both borrow books as well as lend books to other users. This app targets students as well as avid readers of all ages, especially those who are  from economically weak backgrounds and may not have the means to purchase brand new textbooks for school every year. 
Thus, the proposed application,"Book Barter", provides a platform to connect book readers. 
'''

stopwords = list(STOP_WORDS)

#spacy.cli.download("en")

nlp = spacy.load('en_core_web_sm')
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


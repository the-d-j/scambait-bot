import pickle
import spacy
import re

def tag_visible(element):
  if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
    return False
  if isinstance(element, Comment):
    return False
  return True

def read_html_part(html):
  soup = BeautifulSoup(html, 'html.parser')
  texts = soup.findAll(text=True)
  visible_texts = filter(tag_visible, texts)  
  return u' '.join(t.strip() for t in visible_texts)

def process_html(raw_email_body):
  if any(html_signal in raw_email_body for html_signal in ['<html>', '<HTML>']):
    raw_email_body = read_html_part(raw_email_body)
  return raw_email_body

def get_topic(raw_email_body):
  load_models()
  email_body = process_email_body(raw_email_body))
  return 0

def process_email_body(email_body):
  return process_html(raw_email_body)

models = None
def load_models():
  if models is None:
    sklearn_models = pickle.load(open('models.p', 'rb'))
    models = {
      'tfidf':sklearn_models['tfidf']
      'nmf':sklearn_models['nmf']
      'regex':re.compile('\s+')
      'nlp':spacy.load('en')
    }
  
def tokenize_clean_body(body):
return ' '.join([token.lemma_ for token in 
            models['nlp'](re.sub(models['regex'], ' ', body)) 
            if not token.is_stop and not token.is_punct])
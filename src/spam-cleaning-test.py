from flanker import mime
from flanker.mime.message.errors import DecodingError
from contextlib import suppress
from bs4 import BeautifulSoup
from bs4.element import Comment

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

def read_part(part):
  if part.content_type.main == 'text':
    if part.content_type.sub == 'html' or any(html_signal in part.body for 
                                              html_signal in ['<html>', '<HTML>']):
      return read_html_part(part.body)
    elif part.content_type.sub == 'plain':
      return part.body

def join_parts(email_parts):
  parts = [read_part(part) for part in email_parts]
  return '\n'.join([part for part in parts if part is not None])
      
def extract_body(raw_email):
  with suppress(DecodingError, ValueError):
    email = mime.from_string(raw_email)
    if email.content_type.is_singlepart():
      body = read_part(email)
    elif email.content_type.is_multipart():
      body = join_parts(email.parts)
    return body

def extract_bodies(raw_emails):
  email_bodies = []
  for raw_email in raw_emails:
    body = extract_body(raw_email)
    if body is not None:
      email_bodies.append(body)
  return email_bodies

def read_file(path):
  f = open(path)
  raw_email = f.read()
  f.close()
  return raw_email

def read_files(files, verbose_failure=True):
  raw_emails = []
  for file in files:
    try:
      raw_emails.append(read_file(file))
    except:
      if verbose_failure: print(f'File {file} read failure')
  return raw_emails

def tokenize_clean_body(body, language_model, regex):
  return ' '.join([token.lemma_ for token in 
                   language_model(re.sub(regex, ' ', body)) 
                   if not token.is_stop and not token.is_punct])


# In[5]:


from glob import glob

spam_files = glob('apache_spam/*')
bodies = extract_bodies(read_files(spam_files, False))


# In[144]:


import spacy
import re
from tqdm import tqdm_notebook

nlp = spacy.load('en')
regex = re.compile('\s+')

tokenized_bodies = []
for body in tqdm_notebook(bodies, total=len(bodies)):
  tokenized_bodies.append(tokenize_clean_body(body, nlp, regex))
tokenized_bodies = set(tokenized_bodies)


# In[145]:


equal_sum = 0
for body_a in tokenized_bodies:
  for body_b in tokenized_bodies:
    if body_a == body_b: equal_sum += 1
print(equal_sum)


# In[165]:


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

tfidf = TfidfVectorizer(tokenized_bodies, min_df=2, max_features=50000)
tfidf_docs = tfidf.fit_transform(tokenized_bodies)
topic_count = 7
nmf = NMF(topic_count).fit(tfidf_docs)
nmf_docs = nmf.transform(tfidf_docs)


# In[166]:


import numpy as np
from scipy.spatial.distance import cdist

distances = cdist(nmf_docs, nmf_docs, metric='euclidean')
np.fill_diagonal(distances, 1000)
maxind = np.unravel_index(np.argsort(distances, axis=None)[0], distances.shape); print(maxind)


# In[167]:


print(nmf_docs[maxind[0]])
print(nmf_docs[maxind[1]])


# In[168]:


print(bodies[maxind[0]])
print('-'*83)
print(bodies[maxind[1]])


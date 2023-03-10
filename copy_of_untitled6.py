# -*- coding: utf-8 -*-
"""Copy of Untitled6.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qw1SFMvWC9nf7sHj5OnHdpcRrs4IAyA3
"""

import numpy as np
import pandas as pd

mail_data=pd.read_csv('/content/mail_data.csv')

mail_data.head()

mail_data.rename(columns={'Category':'target','Message':'Text'},inplace=True)
mail_data.head()

mail_data.shape

from sklearn.preprocessing import LabelEncoder
encoder=LabelEncoder()

mail_data['target']=encoder.fit_transform(mail_data['target'])

mail_data.head()

mail_data.isnull().sum()

mail_data.duplicated().sum()

mail_data=mail_data.drop_duplicates(keep='first')

mail_data.duplicated().sum()

mail_data['target'].value_counts()

import matplotlib.pyplot as plt
plt.pie(mail_data['target'].value_counts(),labels=['Ham','Spam'],autopct="%0.2f")

import nltk

!pip install nltk

nltk.download('punkt')

mail_data['num_characters']=mail_data['Text'].apply(len)

mail_data.head()

mail_data['num_words']=mail_data['Text'].apply(lambda x:len(nltk.word_tokenize(x)))

mail_data.head()

mail_data['num_sentence']=mail_data['Text'].apply(lambda x:len(nltk.word_tokenize(x)))

mail_data.head()



mail_data['num_sentence']=mail_data['Text'].apply(lambda x:len(nltk.sent_tokenize(x)))

mail_data.head()

mail_data[['num_characters','num_words','num_sentence']].describe()

"""ham"""

mail_data[mail_data['target']==0][['num_characters','num_words','num_sentence']].describe()

"""spam"""

mail_data[mail_data['target']==1][['num_characters','num_words','num_sentence']].describe()

import seaborn as sns

sns.histplot(mail_data[mail_data['target']==0]['num_characters'])
sns.histplot(mail_data[mail_data['target']==1]['num_characters'],color='red')

sns.pairplot(mail_data,hue='target')

mail_data.corr()

sns.heatmap(mail_data.corr(),annot=True)

"""3.**Data** preprocessing
lower case
tokenization
removal special characters
removing stop words and punctuation
stemming

"""

from scipy.stats.morestats import yeojohnson_llf
def transform_Text(Text):
  Text=Text.lower()
  Text=nltk.word_tokenize(Text)
  y=[]
  for i in Text:
    if i.isalnum():
      y.append(i)
  Text=y[:]
  y.clear()

  for i in Text:
    if i not in stopwords.words('english') and i not in string.punctuation:
      y.append(i)

  Text=y[:]
  y.clear()

  for i in Text:
    y.append(ps.stem(i))

     
  return " ".join(y)

nltk.download('stopwords')

from nltk.corpus import stopwords
stopwords.words('english')

import string 
string.punctuation

transform_Text('i loved the yt lectures on machine learning.how about you?')

mail_data['Text'][0]

from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()
ps.stem('loving')

mail_data['transform_Text']=mail_data['Text'].apply(transform_Text)

mail_data.head()

!pip install wordcloud

from wordcloud import WordCloud
WC=WordCloud(width=500,height=500,min_font_size=10,background_color='white')

spam_WC=WC.generate(mail_data[mail_data['target']==1]['transform_Text'].str.cat(sep=" "))

plt.imshow(spam_WC)

plt.imshow(spam_WC)

ham_WC=WC.generate(mail_data[mail_data['target']==0]['transform_Text'].str.cat(sep=" "))

plt.figure(figsize=(15,6))
plt.imshow(ham_WC)

mail_data.head()

spam_corpus=[]
for msg in mail_data[mail_data['target']==1]['transform_Text'].tolist():
  for word in msg.split():
    spam_corpus.append(word)

len(spam_corpus)

from collections import Counter
sns.barplot((pd.DataFrame(Counter(spam_corpus).most_common(30))[0]),pd.DataFrame(Counter(spam_corpus).most_common(30))[1])
plt.xticks(rotation='vertical')
plt.show()

ham_corpus=[]
for msg in mail_data[mail_data['target']==0]['transform_Text'].tolist():
  for word in msg.split():
    ham_corpus.append(word)

len(ham_corpus)

from collections import Counter
sns.barplot((pd.DataFrame(Counter(ham_corpus).most_common(30))[0]),pd.DataFrame(Counter(ham_corpus).most_common(30))[1])
plt.xticks(rotation='vertical')
plt.show()

"""model building"""

mail_data.head()

from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
CV=CountVectorizer()
tfidf=TfidfVectorizer()

X=tfidf.fit_transform(mail_data['transform_Text']).toarray()

X.shape

y=mail_data['target'].values

y

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=2)
from sklearn.naive_bayes import GaussianNB,MultinomialNB,BernoulliNB
from sklearn.metrics import accuracy_score,confusion_matrix,precision_score

gnb=GaussianNB()
mnb=MultinomialNB()
bnb=BernoulliNB()



gnb.fit(X_train,y_train)
y_pred1=gnb.predict(X_test)
print(accuracy_score(y_test,y_pred1))
print(confusion_matrix(y_test,y_pred1))
print(precision_score(y_test,y_pred1))

mnb.fit(X_train,y_train)
y_pred2=mnb.predict(X_test)
print(accuracy_score(y_test,y_pred2))
print(confusion_matrix(y_test,y_pred2))
print(precision_score(y_test,y_pred2))

bnb.fit(X_train,y_train)
y_pred3=bnb.predict(X_test)
print(accuracy_score(y_test,y_pred3))
print(confusion_matrix(y_test,y_pred3))
print(precision_score(y_test,y_pred3))
#Predicting stock on the basis of headlines 
#Kaggle Competition

import nltk

from nltk.corpus import stopwords

import re
import smart_open
smart_open.open = smart_open.smart_open
from gensim.models import Word2Vec
import pandas as pd

df=pd.read_csv('/Users/aadarshraj/Downloads/Stock-Sentiment-Analysis-master/Data.csv',encoding = "ISO-8859-1")

df.head()

train=df[df['Date']<'20150101']
test=df[df['Date']>'20141231']

data=train.iloc[:,2:27]
data.replace('[^a-zA-Z]',' ',regex=True, inplace=True)

list1=[str(i) for i in range(25)]
#new_Index=[str(i) for i in list1]
data.columns=list1
data.head(5)

# Convertng headlines to lower case
for index in list1:
    data[index]=data[index].str.lower()
data.head(1)


headlines = []
for row in range(0,len(data.index)):
    headlines.append(' '.join(str(x) for x in data.iloc[row,0:25]))
    
    
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier


## implement BAG OF WORDS
countvector=CountVectorizer(ngram_range=(2,2))
traindataset=countvector.fit_transform(headlines)


# implement RandomForest Classifier
randomclassifier=RandomForestClassifier(n_estimators=200,criterion='entropy')
randomclassifier.fit(traindataset,train['Label'])

## Predict for the Test Dataset
test_transform= []
for row in range(0,len(test.index)):
    test_transform.append(' '.join(str(x) for x in test.iloc[row,2:27]))
test_dataset = countvector.transform(test_transform)
predictions = randomclassifier.predict(test_dataset)


## Import library to check accuracy
from sklearn.metrics import classification_report,confusion_matrix,accuracy_score


matrix=confusion_matrix(test['Label'],predictions)
print(matrix)
score=accuracy_score(test['Label'],predictions)
print(score)
report=classification_report(test['Label'],predictions)
print(report)


#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

class Corpus(object):
    '''corpus object contains informations on the dataset before the topics modelling'''
   
    
    def __init__(self, data, language='english', dates=True):
        '''dates : boolean, true if data contains dates (by default true)'''
        
        self.data = data #: dataframe with 4 columns : id, title,text,date containing all the documents
        self.language = language 
        vectorizer = CountVectorizer(stop_words=language)
        self.size = self.data.count(0)[0] #: number of documents in the corpus
        self.vector_space_data = vectorizer.fit_transform(self.data['text']) #: vector representation of the documents with n coordinates (n being the number of considered words)
        index_words = vectorizer.get_feature_names() 
        self.index_words = dict([(i, s) for i, s in enumerate(index_words)]) #: index of all the considered words
        
        self.dates = dates
        if dates==True:
            self.years = sorted(self.data['date'].unique())
           
    def full_text(self, doc_id):
        '''return the entire document given its id'''
        return self.data.iloc[doc_id]['text']

    def title(self, doc_id):
        '''return the document's title given its id'''
        return self.data.iloc[doc_id]['title']
    
    def word_for_id(self, word_id):
        '''return the word given its id'''
        return self.index_words.get(word_id)

    def id_for_word(self,word):
        '''return the id given the word'''
        return next((str(id) for id, w in self.index_words.items() if w == word), None)

    def date(self, doc_id):
        '''return the document's year given the id'''
        if self.dates == False:
            raise Exception('dates are missing')
        else:
            return self.data.iloc[doc_id]['date']     


    
        

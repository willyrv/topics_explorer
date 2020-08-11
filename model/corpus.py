#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

class Corpus(object):
    #dates : boolean, true if data contains dates (by default true)
    
    def __init__(self, source_file_path, language='english', dates=True):
        
        self.data = pd.read_csv(source_file_path,sep='|')
        self.language = language
        vectorizer = CountVectorizer(stop_words=language)
        self.size = self.data.count(0)[0]
        self.vector_space_data = vectorizer.fit_transform(self.data['text'])
        index_words = vectorizer.get_feature_names()
        self.index_words = dict([(i, s) for i, s in enumerate(index_words)])
        
        self.dates = dates
        if dates==True:
            self.years = sorted(self.data['date'].unique())
        
        
    def full_text(self, doc_id):
        return self.data.iloc[doc_id]['text']

    def title(self, doc_id):
        return self.data.iloc[doc_id]['title']
    
    def word_for_id(self, word_id):
        return self.index_words.get(word_id)

    def id_for_word(self,word):
        return next((str(id) for id, w in self.index_words.items() if w == word), None)

    def date(self, doc_id):
        if self.dates == False:
            raise Exception('dates are missing')
        else:
            return self.data.iloc[doc_id]['date']     


    
        

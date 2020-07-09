#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 17:28:24 2020

@author: lvallet
"""
from sklearn.decomposition import LatentDirichletAllocation as LDA
import numpy as np
from operator import itemgetter
from sklearn.manifold import MDS

class TopicModel(object):
    def __init__(self,corpus,number_topics):
        self.corpus = corpus  # a Corpus object
        self.number_topics = number_topics  # a scalar value > 1
        
        
        lda = LDA(n_components=number_topics, learning_method='batch')
        lda.fit(self.corpus.vector_space_data)
        
        self.topic_word_matrix = np.array(lda.components_)
        self.document_topic_matrix = np.array(lda.transform(self.corpus.vector_space_data))
        
        
    #méthodes mot topic
    def word_distribution_for_topic(self,topic_id):
        return self.topic_word_matrix[topic_id,:]
        
    def top_words_topic(self,topic_id,nb_words):
        vector = self.word_distribution_for_topic(topic_id)
        weighted_words = []
        for word_id, weight in enumerate(vector):
            weighted_words.append((self.corpus.word_for_id(word_id), weight))
        weighted_words.sort(key=itemgetter(1),reverse=True)
        return weighted_words[:nb_words]
        
    #méthodes doc topic
    def topic_distribution_for_doc(self,doc_id):
        return self.document_topic_matrix[doc_id,:]
        
    def most_likely_topic_for_document(self, doc_id):
        weights = self.topic_distribution_for_doc(doc_id)
        return np.argmax(weights)
        
    def documents_for_topic(self, topic_id):
        doc_ids = []
        for doc_id in range(self.corpus.size):
            most_likely_topic = self.most_likely_topic_for_document(doc_id)
            if most_likely_topic == topic_id:
                doc_ids.append(doc_id)
        return doc_ids
        
   #méthodes topic
    def distance_topics(self):
        matrix = np.zeros((self.number_topics,self.number_topics))
        for i in range(self.number_topics):
            topic_i = self.word_distribution_for_topic(i)
            for j in range(i+1,self.number_topics):
                topic_j = self.word_distribution_for_topic(j)
                dist_ij = np.sum(np.abs(np.log(topic_i)-np.log(topic_j)))
                matrix[i,j]=dist_ij
                matrix[j,i]=dist_ij
        return matrix
    
    def topic_2d_coordinates(self):
        embedding = MDS(n_components=2,dissimilarity='precomputed')
        topic_coordinates = embedding.fit_transform(self.distance_topics())
        return topic_coordinates
        
                

    
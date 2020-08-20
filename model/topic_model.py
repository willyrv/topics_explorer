#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sklearn.decomposition import LatentDirichletAllocation as LDA
import numpy as np
import scipy.sparse as sp
from operator import itemgetter
from sklearn.manifold import MDS
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfTransformer as TfIdf


class TopicModel(object):
    def __init__(self,corpus,number_topics):
        self.corpus = corpus  # a Corpus object
        self.number_topics = number_topics  # a scalar vralue > 1
        
        
        lda = LDA(n_components=number_topics, learning_method='batch')
        lda.fit(self.corpus.vector_space_data)
        tfidf = TfIdf()
        
        self.topic_word_matrix = np.array(lda.components_)
        self.document_topic_matrix = np.array(lda.transform(self.corpus.vector_space_data))
        self.tfidf_matrix = tfidf.fit_transform(self.corpus.vector_space_data)
        
        
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

    def display_top_words_1topic(self,topic_id,nb_words):
        top_words = [self.top_words_topic(topic_id,nb_words)[i][0] for i in range(nb_words)]
        return ', '.join(top_words)     
        
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

    def max_number_docs(self):
        list_nb_docs = [len(self.documents_for_topic(id)) for id in range(self.number_topics)]
        return np.max(list_nb_docs)
        
   #méthodes scaled_view
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
        embedding = MDS(n_components=2,dissimilarity='precomputed',random_state=0)
        topic_coordinates = embedding.fit_transform(self.distance_topics())
        #pca = PCA(n_components=2)
        #topic_coordinates = pca.fit_transform(self.distance_topics())
        return topic_coordinates

    def topics_frequency(self,date=None):#pourcentages
        if date==None:
            matrix = self.document_topic_matrix 
        elif self.corpus.dates==False:
            raise Exception('dates are missing')        
        else:
            rows = self.corpus.data[self.corpus.data['date']==date].index
            matrix = self.document_topic_matrix[rows,:]
        return np.sum(matrix,axis=0)*100/np.shape(matrix)[0]
    
    #évolution importance topics
    def topic_frequency_per_dates(self, topic_id,date=None):
        if date==None:
            return self.topics_frequency_per_dates(self.corpus.years)[topic_id,:]
        elif self.corpus.dates==False:
            raise Exception('dates are missing')
        else:
            return np.around(self.topics_frequency_per_dates(self.corpus.years)[topic_id,date],decimals=2)

    def topics_frequency_per_dates(self, dates):
        if self.corpus.dates==False:
            raise Exception('dates are missing')
        frequencies = np.zeros((self.number_topics,len(dates)))
        for t in range(len(dates)):
            frequencies[:,t] = self.topics_frequency(dates[t])
        return np.around(frequencies,decimals=2)

    #stacked view
    def topics_cumulative_frequencies(self,dates):
        if self.corpus.dates==False:
            raise Exception('dates are missing')
        freq_cumul = np.zeros((self.number_topics,len(dates)))
        freq_cumul[:,0] = self.topics_frequency(dates[0])
        for t in range(1,len(dates)):
            freq_cumul[:,t] = self.topics_frequency(dates[t])+ freq_cumul[:,t-1]
        return np.around(freq_cumul,decimals=2)

    #related docs
    def distance_docs(self):
        matrix = np.zeros((self.corpus.size,self.corpus.size))
        for i in range(self.corpus.size):
            doc_i = self.topic_distribution_for_doc(i)
            for j in range(i+1,self.corpus.size):
                doc_j = self.topic_distribution_for_doc(j)
                dist_ij = np.sum(np.abs(np.log(doc_i)-np.log(doc_j)))
                matrix[i,j]=dist_ij
                matrix[j,i]=dist_ij
        return matrix
    
    def closest_docs(self,doc_id,nb_docs): 
        weights = self.distance_docs()[:,int(doc_id)]
        weights[int(doc_id)] = 1000
        docs = np.argsort(weights)
        return docs[:nb_docs]

    #words
    def nb_docs_for_word(self,word_id):
        vector = self.tfidf_matrix.getcol(word_id)
        nb_docs = vector.count_nonzero()
        return nb_docs





            
        
        
        
        
        
                

    
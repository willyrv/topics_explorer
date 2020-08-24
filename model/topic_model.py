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
    def __init__(self,corpus,number_topics,nb_words,nb_docs):
        self.corpus = corpus  # a Corpus object
        self.number_topics = number_topics  # a scalar vralue > 1
        self.nb_words = nb_words # number top words 
        self.nb_docs = nb_docs #number related docs
        
        # Topic word and document topic distributions
        lda = LDA(n_components=number_topics, learning_method='batch')
        lda.fit(self.corpus.vector_space_data)
        
        self.topic_word_matrix = np.array(lda.components_)
        self.document_topic_matrix = np.array(lda.transform(self.corpus.vector_space_data))

        # tfidf 
        tfidf = TfIdf()
        self.tfidf_matrix = tfidf.fit_transform(self.corpus.vector_space_data)

        #top words and documents for topics
        list_top_words_all_topics = []
        list_docs_all_topics = []
        for topic_id in range(self.number_topics):
            doc_ids = []
            vector_topic_dist = self.topic_word_matrix[topic_id,:]
            weighted_words = []

            for word_id, weight in enumerate(vector_topic_dist):
                weighted_words.append((self.corpus.word_for_id(word_id), weight))
            weighted_words.sort(key=itemgetter(1),reverse=True)

            for doc_id in range(self.corpus.size):
                most_likely_topic = np.argmax(self.document_topic_matrix[doc_id,:])
                if most_likely_topic == topic_id:
                    doc_ids.append(doc_id)

            list_top_words_all_topics.append(weighted_words[:self.nb_words])
            list_docs_all_topics.append(doc_ids)

        self.top_words_all_topics = list_top_words_all_topics
        self.documents_all_topics = list_docs_all_topics
        self.max_number_docs = np.max([len(self.documents_all_topics[id]) for id in range(self.number_topics)])

        #distance topics : scaled view
        matrix_topics = np.zeros((self.number_topics,self.number_topics))
        for i in range(self.number_topics):
            topic_i = self.word_distribution_for_topic(i)
            for j in range(i+1,self.number_topics):
                topic_j = self.word_distribution_for_topic(j)
                dist_ij = np.sum(np.abs(np.log(topic_i)-np.log(topic_j)))
                matrix_topics[i,j]=dist_ij
                matrix_topics[j,i]=dist_ij
        embedding = MDS(n_components=2,dissimilarity='precomputed',random_state=0)
        self.topic_coordinates = embedding.fit_transform(matrix_topics)

        #frequency topics :
        frequencies = np.zeros((self.number_topics,len(self.corpus.years)))
        dates = self.corpus.years
        freq_cumul = np.zeros((self.number_topics,len(dates)))

        rows = self.corpus.data[self.corpus.data['date']==dates[0]].index
        matrix = self.document_topic_matrix[rows,:]
        frequencies[:,0] = np.sum(matrix,axis=0)*100/np.shape(matrix)[0]
        freq_cumul[:,0] = frequencies[:,0]

        for t in range(1,len(dates)):
            rows = self.corpus.data[self.corpus.data['date']==dates[t]].index
            matrix = self.document_topic_matrix[rows,:]
            frequencies[:,t] = np.sum(matrix,axis=0)*100/np.shape(matrix)[0]
            freq_cumul[:,t] = frequencies[:,t] + freq_cumul[:,t-1]

        self.topics_frequency_per_dates = np.around(frequencies,decimals=2)
        self.topics_cumulative_frequencies = np.around(freq_cumul,decimals =2)
        self.topics_proportion = np.sum(self.document_topic_matrix,axis=0)*100/np.shape(self.document_topic_matrix)[0]

        #related docs
        matrix_docs = np.zeros((self.corpus.size,self.corpus.size))
        for i in range(self.corpus.size):
            doc_i = self.topic_distribution_for_doc(i)
            for j in range(i+1,self.corpus.size):
                doc_j = self.topic_distribution_for_doc(j)
                dist_ij = np.sum(np.abs(np.log(doc_i)-np.log(doc_j)))
                matrix_docs[i,j]=dist_ij
                matrix_docs[j,i]=dist_ij
        self.related_docs = matrix_docs

        
        
    #méthodes mot topic
    def word_distribution_for_topic(self,topic_id):
        return self.topic_word_matrix[topic_id,:]
    
    def topic_distribution_for_word(self,word_id):
        return self.topic_word_matrix[:,word_id]

    def frequency_word_for_topics(self,word_id):
        vector = self.topic_distribution_for_word(word_id)
        freq = vector*100/np.sum(vector)
        return np.around(freq,decimals=2)

    def display_top_words_1topic(self,topic_id,nb_words):
        top_words = [self.top_words_all_topics[topic_id][i][0] for i in range(nb_words)]
        return ', '.join(top_words)     
        
    #méthodes doc topic
    def topic_distribution_for_doc(self,doc_id):
        return self.document_topic_matrix[doc_id,:]
    
    #évolution importance topics
    def topic_frequency_per_dates(self, topic_id,date=None):
        if date==None:
            return self.topics_frequency_per_dates[topic_id,:]
        elif self.corpus.dates==False:
            raise Exception('dates are missing')
        else:
            return np.around(self.topics_frequency_per_dates[topic_id,date],decimals=2)

    #related docs    
    def closest_docs(self,doc_id,nb_docs): 
        weights = self.related_docs[:,int(doc_id)]
        weights[int(doc_id)] = 1000
        docs = np.argsort(weights)
        return docs[:self.nb_docs]

    #words
    def nb_docs_for_word(self,word_id):
        vector = self.tfidf_matrix.getcol(word_id)
        nb_docs = vector.count_nonzero()
        return nb_docs





            
        
        
        
        
        
                

    
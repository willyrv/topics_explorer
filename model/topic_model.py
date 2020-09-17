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
    '''Treatment of the LDA results'''
    def __init__(self,corpus,number_topics,nb_words,nb_docs):
        self.corpus = corpus  #: a Corpus object
        self.number_topics = number_topics  #: number of topics of the model
        self.nb_words = nb_words #:number of displayed words in the lists in topic,doc and word page
        self.nb_docs = nb_docs #:number of displayed documents in the lists in topic,doc and word page
        
        # Topic word and document topic distributions
        lda = LDA(n_components=number_topics, learning_method='batch')
        lda.fit(self.corpus.vector_space_data)
        
        self.topic_word_matrix = np.array(lda.components_) #: matrix of dimension K*N (K : number of topics, N : number of words) containing the distribution of words for each topic
        self.document_topic_matrix = np.array(lda.transform(self.corpus.vector_space_data)) #: matrix of dimension D*K (D : number of documents,K : number of topics) containing the distribution of topics for each document

        # tfidf 
        tfidf = TfIdf()
        self.tfidf_matrix = tfidf.fit_transform(self.corpus.vector_space_data)

        #top words and documents for topics
        list_top_words_all_topics = []
        list_top_docs_all_topics = []
        for topic_id in range(self.number_topics):
            weighted_docs = []
            vector_topic_dist = self.topic_word_matrix[topic_id,:]
            vector_doc_dist = self.document_topic_matrix[:,topic_id]
            weighted_words = []

            for word_id, weight_w in enumerate(vector_topic_dist):
                weighted_words.append((self.corpus.word_for_id(word_id), weight_w))
            weighted_words.sort(key=itemgetter(1),reverse=True)

            for doc_id,weight_d in enumerate(vector_doc_dist):
                weighted_docs.append((doc_id, weight_d))
            weighted_docs.sort(key=itemgetter(1),reverse=True)


            list_top_words_all_topics.append(weighted_words)
            list_top_docs_all_topics.append(weighted_docs)

        self.top_words_all_topics = list_top_words_all_topics #: list containing  K lists with the words classified by importance for each topic
        self.top_docs_all_topics = list_top_docs_all_topics #: list containing  K lists with the documents classified by importance for each topic

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
        self.topic_coordinates = embedding.fit_transform(matrix_topics) #: matrix of 2-dimensional coordinates for each topic based on the distance between the topics

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

        self.topics_frequency_per_dates = np.around(frequencies,decimals=2) #: matrix of dimension K*Y (K: number of topics, Y: number of years) containing the frequency of each topic for each year.
        self.topics_cumulative_frequencies = np.around(freq_cumul,decimals =2) #: same as topics_frequency_per_dates but with cumulative frequencies
        self.topics_proportion = np.sum(self.document_topic_matrix,axis=0)*100/np.shape(self.document_topic_matrix)[0] #: Vector with the proportion of each topic in the corpus

        #related docs : distance between docs
        matrix_docs = np.zeros((self.corpus.size,self.corpus.size))
        for i in range(self.corpus.size):
            doc_i = self.topic_distribution_for_doc(i)
            for j in range(i+1,self.corpus.size):
                doc_j = self.topic_distribution_for_doc(j)
                dist_ij = np.sum(np.abs(np.log(doc_i)-np.log(doc_j)))
                matrix_docs[i,j]=dist_ij
                matrix_docs[j,i]=dist_ij
                matrix_docs[i,i]=100000
        matrix_docs = np.argsort(matrix_docs,1)        
        self.related_docs = matrix_docs #: square matrix with sorted documents from the closest one to the most different one for each document

        
        
    #Topic word methods

    def word_distribution_for_topic(self,topic_id):

        '''return the distribution of words for the topic in argument'''

        return self.topic_word_matrix[topic_id,:]
    
    def topic_distribution_for_word(self,word_id):

        '''return the distribution of topics for the word in argument'''

        return self.topic_word_matrix[:,word_id]

    def frequency_word_for_topics(self,word_id):

        '''return the same as topic_distribution_for_word but in percentages'''

        vector = self.topic_distribution_for_word(word_id)
        freq = vector*100/np.sum(vector)
        return np.around(freq,decimals=2)

    def display_top_words_1topic(self,topic_id,nb_words):

        '''display the nb_words top words for the topic in argument'''

        top_words = [self.top_words_all_topics[topic_id][i][0] for i in range(nb_words)]
        return ', '.join(top_words)     
        
    #Document topic methods

    def topic_distribution_for_doc(self,doc_id):

        '''return the distribution of topics for the document in argument'''

        return self.document_topic_matrix[doc_id,:]

    def frequency_doc_for_topics(self,doc_id):

        '''return the same as topic_distribution_for_doc but in percentages'''

        vector = self.topic_distribution_for_doc(doc_id)
        freq = vector*100/np.sum(vector)
        return np.around(freq,decimals=2)
    
    #évolution importance topics

    def topic_frequency_per_dates(self, topic_id,date=None):
        if date==None:
            return self.topics_frequency_per_dates[topic_id,:]
        elif self.corpus.dates==False:
            raise Exception('dates are missing')
        else:
            return np.around(self.topics_frequency_per_dates[topic_id,date],decimals=2)

    #related docs    

    def closest_docs(self,doc_id): 

        '''return the documents sorted from the closest to the most different documents with the document in argument as a reference'''
        return self.related_docs[int(doc_id),:]

    #words

    def nb_docs_for_word(self,word_id):

        '''return the number of docs containing the word in argument'''

        vector = self.tfidf_matrix.getcol(word_id)
        nb_docs = vector.count_nonzero()
        return nb_docs

    def docs_for_word(self,word_id):

        '''return a list with the ids of all the documents containing the word in argument'''

        vector = self.corpus.vector_space_data.getcol(word_id)
        ind = sp.find(vector)
        list_docs = [(ind[0][i],ind[2][i]) for i in range(len(ind[0]))]
        return sorted(list_docs,key= lambda x : x[1],reverse=True)





            
        
        
        
        
        
                

    
from model.corpus import Corpus
from model.topic_model import TopicModel
from model.visualisation import Views
from wordcloud import WordCloud

import pickle

arxiv = './input/arxiv_test.csv'
ASRS = './input/ASRS_1000docs.csv'

nb_topics = 15
nb_words = 10
nb_docs = 10

model = TopicModel(Corpus(source_file_path=ASRS),nb_topics,nb_words,nb_docs)
view = Views(model)

f = open('assets/ASRS1000docs15topics.pickle','wb')
pickle.dump(view,f)
f.close()

complete_corpus = ','.join(view.model.corpus.data['text'])
wc = WordCloud(background_color="white", max_words=1000, contour_width=3, contour_color="steel blue")
cloud = wc.generate(complete_corpus)
cloud.to_file('assets/corpus.png')

for i in range(view.model.number_topics):
    freq_words = view.model.topic_word_matrix[0,:]
    d = {view.model.corpus.word_for_id(id): freq_words[id] for id in range(len(view.model.corpus.index_words))} 
    cloud_top = wc.generate_from_frequencies(d)
    cloud_top.to_file('assets/topic{}.png'.format(i))



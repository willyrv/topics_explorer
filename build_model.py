from model.corpus import Corpus
from model.topic_model import TopicModel
from model.visualisation import Views

import pickle

arxiv = './input/arxiv_test.csv'
ASRS = './input/ASRS_test.csv'

nb_topics = 15

model = TopicModel(Corpus(source_file_path=ASRS),nb_topics)
view = Views(model)

f = open('views_model.pickle','wb')
pickle.dump(view,f)
f.close()
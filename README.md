# Topics_explorer

Topics models are useful tools for discovering the latent topical structure of text corpora. Several models and algorithms have appeared in the recent years to approximate the latent topics and thus get more informations about the corpora structure. Topics explorer is a tool written in Python 3 licensed under the MIT license. Its objective is to permit a complete exploration of a text corpora by creating a topics model and exploring its results

The browser uses the Latent Dirichlet Allocation algorithm implemented in the python librairy sklearn. This method allows us to find the distribution over topics of a corpus, each topic being a distribution of words. This model provides very good results but these results can be really difficult to visualize. 

Some tools have already been built in order to visualize such results. We can note for instance, the online Topic visualization developped by Allison J. B. Chaney, the library TOM by Adrien Guille or the dfr-browser. Even if these tools provide good ways to visualize topics model, they have been built for a precise dataset and are really difficult to adapt to new data.

That is why Topics explorer provides a way to explore topics model's results from any datasets in an intuitive  and complete way. It is composed of 5 views : 

* overview : contains 4 ways of visualize the distribution of topics in the entire corpus. 
* topic : gives details such as top words, related documents, frequency evolution and wordcloud.
* document : permits to see the entire selected document, its distribution over topics and the closest documents to it.
* word : provides informations about a word such as the documents containing it, its relation to the different topics
* dictionary : contains a list of all the words used to build the topics model.


## Installation

We recommend you to create a virtual environment to install all the necessary packages. To do so, please follow this steps: 

```
git clone https://github.com/willyrv/topics_explorer
cd topics_explorer
python3 -m venv myvirtualenvironment
source myvirtualenvironment/bin/activate
pip install -r requirements.txt
```
Then to lauch the application, please run the following command :
```
python index.py
```
## Use topics explorer with your own data

The browser has been built using a topics model constructed with 15 topics from a dataset containing 1000 aviation safety reports which come from ASRS database. However, topics explorer allows users to upload their own datasets in order to visualize the topics model's results. The data should be uploaded as a csv file containing 4 columns separated by '|' :

```
id	title	            text                                    date
1	Document 1's title	This is the full content of document 1  Document 1's date
2	Document 2's title	This is the full content of document 2  Document 2's date
...
```
When a new file is uploaded, users can choose the number of topics they want and then, a topics model is created using LDA and save into a folder in local and can be find in the assets folder. Users have the possibility to choose the topics model they want to explore between the uploaded datasets.

## Documentation

All the necessary files to update the documentation using sphinx autodocs can be found in the documentation_generator folder. A current version of the documentation can be seen by looking at the following html file :
```
documentation_generator/build/html/index.html
```
To update this file, you have to execut this command :
```
cd documentation_generator
make html
```

## Similar applications

There are some other applications like this one. Here is a (non exhaustive) list. Please, feel free to suggest more if you know:

* https://agoldst.github.io/dfr-browser/demo/#/model/grid




corpus = open('./dataset2.csv').read()
corpus = corpus.lower()  # pre-processing, as we want to treat capital and lower words as same
docs = corpus.split('\n')  # splitting documents

from sklearn.feature_extraction.text import TfidfVectorizer
vec = CountVectorizer()
matrix_X = vec.fit_transform(docs)

features = vec.get_feature_names()
from sklearn.decomposition import LatentDirichletAllocation
lda = LatentDirichletAllocation(n_components = 20)
lda.fit(matrix_X)

features = vec.get_feature_names()
for tids, topic in enumerate(lda.components_):
    print('topic ID: ', tids)
    print([features[i] for i in topic.argsort()[:-6:-1]])
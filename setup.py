import nltk

# will take some time
# by default it downloads to appData\roaming\nltk_data

# might be able to just do nltk.download() for ease..

# pre-trained model for tokenizing, good for punctuations. http://www.nltk.org/api/nltk.tokenize.html?highlight=punkt
nltk.download('punkt')
# Lexical database used to determine base words. (stemming) https://www.nltk.org/api/nltk.corpus.reader.html#module-nltk.corpus.reader.wordnet
nltk.download('wordnet')
# Used in conjunction with others to tag words of their part of speech (noun, verb, etc)
nltk.download('averaged_perceptron_tagger')
# Used in conjunction with others to remove filler words. https://www.nltk.org/book/ch02.html#wordlist-corpora
nltk.download('stopwords')

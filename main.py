from newspaper import Article
import datetime
import json

# Handles summarization
import heapq
import nltk
# nltk.download('punkt')
# nltk.download('stopwords')
import re

article_data = {
    'title': 'No title found,',
    'author': 'No author found.',
    'publish_date': 'No publish date found.',
    'img_src': 'No image source found.',
    'text': 'No text found.'
}

def summarize(text):
    text = re.sub(r'\[[0-9]*\]', ' ', text)
    text = re.sub(r'\s+', ' ', text)

    # formatted text
    ftext = re.sub('[^a-zA-Z]', ' ', text)
    ftext = re.sub(r'\s+', ' ', ftext)

    sentence_list = nltk.sent_tokenize(text)

    stopwords = nltk.corpus.stopwords.words('english')

    word_frequencies = {}
    for word in nltk.word_tokenize(ftext):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]

    summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

    summary = {}
    summary['summary'] = ' '.join(summary_sentences)
    with open('json/summary.json', 'w') as outfile:
        json.dump(summary, outfile)

def getInitJSON(Url):
    ## BEGIN BUILDING INITIAL ARTICLE
    article = Article(Url) # Instantiate article
    article.download() # Required
    article.parse() # Required

    title = article.title
    author_head = article.authors[0] # This does not correctly parse all the time
    publish_date = article.publish_date
    img_src = article.top_image
    summary = article.summary
    text = article.text
    summary = summarize(text)

    try:
        article_data['title'] = title
        article_data['author'] = author_head
        # datetime objs are not serializable
        article_data['publish_date'] = publish_date.strftime("%Y-%m-%d")
        article_data['img_src'] = img_src
        article_data['text'] = text
    except AttributeError:
        pass # This is fine
    ## END BUILDING INITIAL ARTICLE

    with open('json/init.json', 'w') as outfile:
        json.dump(article_data, outfile)

getInitJSON(input("Enter a Url: \n"))

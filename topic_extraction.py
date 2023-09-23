import re
import string
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import decomposition


def clean_text(s):
    """
    Removes formatting
    """
    s = s.lower()
    s = re.sub("<(.|\n|’)*?>", "", s)
    s = s.replace("“", '"').replace("”", '"').replace("’", "'")
    s = s.replace("\n", "")

    s = s.split()
    s = " ".join(s)
    s = re.sub(f"[{re.escape(string.punctuation)}]", "", s)
    return s


def remove_stop_words(s):
    """
    Removes stop words
    """
    stop_words = set(stopwords.words("english"))
    s = s.split()
    s = [w for w in s if not w.lower() in stop_words]
    s = " ".join(s)
    return s


def sanitize_text(text):
    lemmatizer = WordNetLemmatizer()
    # Sanitizes and tokenizes text
    preface_tokens = sent_tokenize(text)
    preface_tokens = [clean_text(w) for w in preface_tokens]
    preface_tokens = [remove_stop_words(w) for w in preface_tokens]
    preface_tokens = [lemmatizer.lemmatize(w) for w in preface_tokens]
    return preface_tokens


def get_topics(tokens):
    # Calculates vectors
    tfv = TfidfVectorizer(tokenizer=word_tokenize, token_pattern=None)
    corpus_transformed = tfv.fit_transform(tokens)
    svd = decomposition.TruncatedSVD(n_components=10)
    corpus_svd = svd.fit(corpus_transformed)
    # Get topic scores
    feature_scores = dict(zip(tfv.get_feature_names_out(), corpus_svd.components_[0]))
    topic_output = sorted(feature_scores, key=feature_scores.get, reverse=True)[:5]
    return topic_output


def main():
    f = open("sample.txt", "r")
    text = f.read()

    preface_tokens = sanitize_text(text)
    topics = get_topics(preface_tokens)

    print(topics)


if __name__ == "__main__":
    main()


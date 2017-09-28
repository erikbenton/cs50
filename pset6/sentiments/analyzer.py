import nltk

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""

        self.positives = []
        self.negatives = []
        self.read_words(positives, self.positives)
        self.read_words(negatives, self.negatives)

    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""
        sum = 0
        text = text.strip('"')
        text = text.lower()
        tokenizer = nltk.tokenize.TweetTokenizer()
        words = tokenizer.tokenize(text)

        for word in words:
            if word in self.positives:
                sum = sum + 1
            elif word in self.negatives:
                sum = sum - 1
        return sum

    def read_words(self, text, list):
        with open(text,'r') as f:
            for line in f:
                for word in line.split('\n'):
                    if(word.startswith(';') == False):
                        list.append(word.strip())
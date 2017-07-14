import nltk

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        self.positives = set()
        file = open(positives, "r")
        for line in file:
            if line.startswith(';') == False:
                self.positives.add(line.rstrip("\n"))
        file.close()
        
        self.negatives = set()
        file = open(negatives, "r")
        for line in file:
            if line.startswith(';') == False:
                self.negatives.add(line.rstrip("\n"))
        file.close()

    def analyze(self, text):
        """Analyze text for sentiment, returning its result."""
        tokenizer = nltk.tokenize.TweetTokenizer()
        tokens = tokenizer.tokenize(text)
        result = 0
        for word in tokens:
            if word.lower() in self.positives:
                result += 1
            elif word.lower() in self.negatives:
                result -= 1
            else:
                continue
        
        return result

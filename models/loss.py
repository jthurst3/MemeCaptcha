

# simplest loss function
# TODO: make other (better) loss functions
def count_loss(Y, Y_pred):
    """returns the percentage of words in Y_pred that are also in Y, and
    vice-versa"""
    words = words(Y)
    words_pred = words(Y_pred)
    return (percent_membership(words, words_pred)+percent_membership(words_pred,words))/2.0

def percent_membership(words1, words2):
    """given two word sets, returns the percentage of words in words1 that are
    also in words2. Return type is of type float."""
    wc = 0
    for word in words1:
        if word in words2:
            wc += 1
    return float(wc)/len(words2)

def words(sentence):
    """returns a set of words found in the sentence"""
    # TODO: make this better
    words = sentence.split(" ")
    s = set()
    for word in words:
        s.add(word)
    return s



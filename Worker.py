#!/usr/bin/python3

import re, random, sys

tempMapping = {}
mapping = {}
startWords = []

# Compare words independent of their capitalization.
def fixCaps(word):
    if word.isupper() and word != "I":
        word = word.lower()
    elif word [0].isupper():
        word = word.lower().capitalize()
    else:
        word = word.lower()
    return word


# Given history = ["the", "sun", "is"] and word = "xyz", we add "xyz" to
# the entries for ["the", "sun", "is"], ["sun", "in"], and ["in"].
def addItemToTempMapping(history, word):

    ''' Temporary mapping for words that we've encountered recently.'''

    global tempMapping
    while len(history) > 0:
        first = toHashKey(history)
        if first in tempMapping:
            if word in tempMapping[first]:
                tempMapping[first][word] += 1.0
            else:
                tempMapping[first][word] = 1.0
        else:
            tempMapping[first] = {}
            tempMapping[first][word] = 1.0
        history = history[1:]


# Returns the contents of the file, split into a list of words and punctuation
def wordlist(filename):


    f = open(filename, 'r')
    wordlist = [fixCaps(w) for w in re.findall(r"[\w']+|[.,!?;]", f.read())]
    f.close()
    return wordlist

# Tuples can be hashed; lists can't. We need hashable values for dict keys.
def toHashKey(lst):


    return tuple(lst)

# Returns the next word in the sentence (chosen randomly), given the previous ones.
def next(prevList):

    '''Finds the next word according to probabilistic values in the mapping'''

    totSum = 0.0
    retval = ""
    index = random.random()

    while toHashKey(prevList) not in mapping:
        prevList.pop(0)

    # Get a random word from the mapping, given prevList
    for k, v in mapping[toHashKey(prevList)].items():
        totSum += v
        if totSum >= index and retval == "":
            retval = k
    return retval

# Building and normalizing the mapping.
def buildMapping(wordlist, markovLength):

    '''Generates a bigram to unigram mapping and normalizes all weights to ensure fair generation. Commenting out
        the normalizing step will lead to duplicate sentences being generated all the time.'''

    global tempMapping

    startWords.append(wordlist [0])

    for i in range(1, len(wordlist) - 1):

        if i <= markovLength:
            history = wordlist[: i + 1]
        else:
            history = wordlist[i - markovLength + 1 : i + 1]
        follow = wordlist[i + 1]

        # if the last literal was a period, add the next word to the start list
        if history[-1] == "." and follow not in ".,!?;":
            startWords.append(follow)
        addItemToTempMapping(history, follow)

    # Normalize the values in tempMapping, put them into mapping
    for first, followset in tempMapping.items():
        total = sum(followset.values())
        mapping[first] = dict([(k, v / total) for k, v in followset.items()])

def genSent(markovLength):

    '''Generates a random sentence from the given corpus. Default corpus is A brief history of time by Stephen Hawking'''

    curr = random.choice(startWords)
    sent = curr.capitalize()
    prevList = [curr]

    # Keep adding words until we hit a period
    while (curr not in "."):

        curr = next(prevList)
        prevList.append(curr)

        if len(prevList) > markovLength:
            prevList.pop(0)
        if (curr not in ".,!?;"):
            sent += " "
        sent += curr
    return sent

def main():
    if len(sys.argv) < 2:
        sys.stderr.write('Usage: ' + sys.argv [0] + ' chain_length=1\n')
        sys.exit(1)

    filename = sys.argv[1]
    markovLength = 1
    if len (sys.argv) == 3:
        markovLength = int(sys.argv [2])

    buildMapping(wordlist(filename), markovLength)
    print (genSent(markovLength))

if __name__ == "__main__":
    main()

# Topic - Markov Sentence Generator
# Authors : Dhaval, Murtaza

import sys,re,nltk,random
from collections import Counter,defaultdict

removeThis = ['[',']','(',')','"','/','{','}','\'',':',';',',',"''"]

gramToTag = { 'S' : [],'NP' : ['NNP','NNPS'], 'N' : ['NNS','NN'], 'SYM' : ['SYM'], 'PNP' : ['PRP','PRP$'], 'Det' : ['Det'], 'CD' : ['CD'],
              'CC' : ['CC','IN'], 'VV' : ['RBR','RBS','RP'], 'TO' : ['to'], 'Interj' : ['UH'], 'V' : ['VB','VBD','VBG','VBN','VBP','VBN'],
              'WH': ['WDT','WP','WP$','WRB']
              }

class CFG(object):
    def __init__(self):
        self.dict = defaultdict(list)

    def addProd(self,lhs,rhs):
        prods = rhs.split('|')
        for prod in prods:
            self.dict[lhs].append(tuple(prod.split()))

    def genRandom(self,symbol):
        sentence = ''
        randProd = random.choice(self.dict[symbol])
        for sym in randProd:
            if sym in self.dict:
                sentence+=self.genRandom(sym)
            else:
                sentence += sym + ' '
        return sentence


class Generator(object):

    def __init__(self,inputSent,sysArgs):
        self.inputSent = inputSent
        self.mode = sysArgs[0]
        self.length = sysArgs[1]

    def buildSent(self):
        pass

    def display(self):
        pass


def test():

    fileid = 'austen-emma.txt'
    sentences = []
    tagToWord = defaultdict(list)
    emma = nltk.corpus.gutenberg.sents(fileid)
    sentences = [" ".join(list_of_words) for list_of_words in emma]
    sentences = [str(x.encode('UTF8')) for x in sentences]

    for s in sentences[:5]:
        tokens = nltk.word_tokenize(s)
        # tokens = s.strip().split()
        for items in removeThis:
            if items in tokens:
                tokens.remove(items)
        tagged = nltk.pos_tag(tokens)
        for tuples in tagged:
            if tuples[0] not in tagToWord[tuples[1]]:
                tagToWord[tuples[1]].append(tuples[0])

    return tagToWord

def allWords(gram, tagToWord):
    res=""
    for tag in gramToTag[gram]:
        for words in tagToWord[tag]:
            res+=words
            res+="|"
    return res[:-1]

def main():
    # inputSent, mode = sys.arg[1], sys.arg[2], sys.arg[3]

    tagToWord = test()

    p = CFG()
    p.addProd('S','NP VP')
    p.addProd('S','NP VP')
    p.addProd('NP','Det N |Det N')
    p.addProd('VP','V NP |VP')
    p.addProd('NP',allWords('NP',tagToWord))
    p.addProd('V', allWords('V', tagToWord))
    p.addProd('N',allWords('N',tagToWord))
    p.addProd('Det', allWords('Det', tagToWord))

    print(p.genRandom('S'))

    # if mode == '-v':
    #     generate1 = Generator(None,sys[1:])
    # else:
    #     generate1 = Generator(None,sys[1:])

    # generate1.buildSent()
    # generate1.display()

if __name__ == '__main__':
    main()

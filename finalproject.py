#
# Final Project (finalproject.py)
#
# Name: Andrew James
#
#
#
#
#

import math
import time

VOWELS = ['a','e','i','o','u']

class TextModel():
    """ TextModel Class which creates dictionary based models for attributes
        of a given piece of writing
    """
    
    
    def __init__(self, model_name):
        """ Model constructor which cotains the model's name
            as well as various attribute dictionaries
        """
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.proper_nouns = {}

    def __repr__(self):
        """Return a string representation of the TextModel."""
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += '  number of stems: ' + str(len(self.stems)) + '\n'
        s += '  number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s += '  number of proper nouns: ' + str(len(self.proper_nouns)) + '\n'
        return s

    def add_string(self, s):
        """Analyzes the string txt and adds its pieces
           to all of the dictionaries in this text model.
        """
        s = s.replace('!','.')
        s = s.replace('?','.')
        sentences = s.split('.')
        sentences = sentences[:-1]
        
        for i in range(len(sentences)):
            sentences[i] = sentences[i].split()
            if len(sentences[i]) not in self.sentence_lengths:
                self.sentence_lengths[len(sentences[i])] = 1
            else:
                self.sentence_lengths[len(sentences[i])] += 1
            for j in range(1,len(sentences[i])):
                sentences[i][j] = almost_clean_text(sentences[i][j])
                if len(sentences[i][j]) > 0:
                    if 64 < ord(sentences[i][j][0]) < 91:
                        if sentences[i][j] not in self.proper_nouns:
                            self.proper_nouns[sentences[i][j]] = 1
                        else:
                            self.proper_nouns[sentences[i][j]] += 1    

        s = clean_text(s)
        word_list = s.split()

        for w in word_list:
            if w not in self.words:
                self.words[w] = 1
            else:
                self.words[w] += 1
            if len(w) not in self.word_lengths:
                self.word_lengths[len(w)] = 1
            else:
                self.word_lengths[len(w)] += 1
            if stem(w) not in self.stems:
                self.stems[stem(w)] = 1
            else:
                self.stems[stem(w)] += 1

    def add_file(self, filename):
        """ takes a plaintext file and processes it to a single string
            and subsequently uses the add_string() method on that string
        """
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        txt = f.read()
        f.close()
        self.add_string(txt)

    def save_model(self):
        """ saves each attribute dictionary to a corresponding
            plain-text file
        """
        words = open(self.name + '_' + 'words', 'w')
        words.write(str(self.words))
        words.close()
        word_lengths = open(self.name + '_' + 'word_lengths', 'w')
        word_lengths.write(str(self.word_lengths))
        word_lengths.close()
        stems = open(self.name + '_' + 'stems', 'w')
        stems.write(str(self.stems))
        stems.close()
        sentence_lengths = open(self.name + '_' + 'sentence_lengths', 'w')
        sentence_lengths.write(str(self.sentence_lengths))
        sentence_lengths.close()
        proper_nouns = open(self.name + '_' + 'proper_nouns', 'w')
        proper_nouns.write(str(self.proper_nouns))
        proper_nouns.close()

    def read_model(self):
        """ reads saved model information and stores each read file
            in a corresponding dictionary
        """
        f = open(self.name + '_' + 'words', 'r')
        d_str = f.read()
        f.close()
        self.words = dict(eval(d_str))
        f = open(self.name + '_' + 'word_lengths', 'r')
        d_str = f.read()
        f.close()
        self.word_lengths = dict(eval(d_str))
        f = open(self.name + '_' + 'stems', 'r')
        d_str = f.read()
        f.close()
        self.stems = dict(eval(d_str))
        f = open(self.name + '_' + 'sentence_lengths', 'r')
        d_str = f.read()
        f.close()
        self.sentence_lengths = dict(eval(d_str))
        f = open(self.name + '_' + 'proper_nouns', 'r')
        d_str = f.read()
        f.close()
        self.proper_nouns = dict(eval(d_str))

    def similarity_scores(self, other):
        """ returns thellist of scores for each dictionary comparison
        """
        sim_scores = []
        sim_scores += [round(compare_dictionaries(other.words,self.words), 3)]
        sim_scores += [round(compare_dictionaries(other.word_lengths,self.word_lengths), 3)]
        sim_scores += [round(compare_dictionaries(other.stems,self.stems), 3)]
        sim_scores += [round(compare_dictionaries(other.sentence_lengths,self.sentence_lengths), 3)]
        sim_scores += [round(compare_dictionaries(other.proper_nouns,self.proper_nouns), 3)]
        return sim_scores

    def classify(self, source1, source2):
        """ compares a TextModel object to two other source TextModels to
            determine which source it is more similar to
        """
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        print('Scores for ' + source1.name + ':', scores1)
        print('Scores for ' + source2.name + ':', scores2)
        weighted_sum1 = scores1[0] + scores1[1] + scores1[2] + scores1[3] + scores1[4]
        weighted_sum2 = scores2[0] + scores2[1] + scores2[2] + scores2[3] + scores2[4]
        if weighted_sum1 >= weighted_sum2:
            print(self.name +' is more likely to have come from ' + source1.name)
        else:
            print(self.name +' is more likely to have come from ' + source2.name)
        
def clean_text(txt):
    """ cleans text by removing basic puntuation and parentheses
        and changing the text to all lowercase
    """
    txt = txt.replace('.', '')
    txt = txt.replace('?', '')
    txt = txt.replace(',', '')
    txt = txt.replace('!', '')
    txt = txt.replace('(', '')
    txt = txt.replace(')', '')
    txt = txt.replace('"', '')
    txt = txt.replace(':', '')
    txt = txt.replace(';', '')
    txt = txt.replace('-', ' ')
    txt = txt.lower()
    return txt

def almost_clean_text(txt):
    """ cleans text by removing basic puntuation and parentheses
    """
    txt = txt.replace('.', '')
    txt = txt.replace('?', '')
    txt = txt.replace(',', '')
    txt = txt.replace('!', '')
    txt = txt.replace('(', '')
    txt = txt.replace(')', '')
    txt = txt.replace('"', '')
    txt = txt.replace(':', '')
    txt = txt.replace(';', '')
    txt = txt.replace('-', ' ')
    return txt

def stem(s):
    """ A slightly modified implementation of the Porter stemming algorithm
        which can be read here:
        https://www.cs.toronto.edu/~frank/csc2501/Readings/R2_Porter/Porter-1980.pdf
    """
    if '\'' in s:
        l=s.split('\'')
        return stem(l[0])        
    if s[-2:] == 'ed':
        if (s[-3:-1] == 'ee') and m_value(s[:-3]) > 0:
            return stem(s[:-1]+'e')
        for c in VOWELS:
            if c in s[1:-2]:
                if s[-4:-2] in ['at','bl','iz']:
                    return stem(s[:-1])
                elif (s[-4] == s[-3]) and (s[-4] not in (VOWELS+['l','s','z'])):
                    return stem(s[:-3])
                else:
                    return stem(s[:-2])
    if s[-3:] == 'ing':
        for c in VOWELS:
            if c in s[1:-3]:
                if s[-5:-3] in ['at','bl','iz']:
                    return stem(s[:-3] + 'e')
                elif (s[-5] == s[-4]) and (s[-4] not in ['a','e','i','o','u','l','s','z']):
                    return stem(s[:-4])
                elif (len(s[:-3]) >= 2) and s[-5] in VOWELS and s[-4] not in VOWELS:
                    return stem(s[:-3] + 'e')                    
                else:
                    return stem(s[:-3])
    if s[-1:] == 'y':
        for c in VOWELS:
            if c in s:
                return stem(s[:-1]+'i')

    if len(s) > 9:
        if m_value(s[:-7]) > 0:
            if s[-7:] == 'ational':
                return stem(s[:-5] + 'e')
            elif s[-7:] == 'ization':
                return stem(s[:-5] + 'e')
            elif s[-7:] == 'iveness':
                return stem(s[:-4])
            elif s[-7:] == 'fulness':
                return stem(s[:-4])
            elif s[-7:] == 'ousness':
                return stem(s[:-4])
    
    if len(s) > 8:
        if m_value(s[:-6]) > 0:
            if s[-6:] == 'tional':
                return stem(s[:-2])
            elif s[-6:] == 'biliti':
                return stem(s[:-5] + 'le')

    if len(s) > 7:
        if m_value(s[:-5]) > 0:
            if s[-5:] == 'entli':
                return stem(s[:-2])
            elif s[-5:] == 'ousli':
                return stem(s[:-2])
            elif s[-5:] == 'ation':
                return stem(s[:-3] + 'e')
            elif s[-5:] == 'alism':
                return stem(s[:-3])
            elif s[-5:] == 'aliti':
                return stem(s[:-3])
            elif s[-5:] == 'iviti':
                return stem(s[:-3] + 'e')

    if len(s) > 6:
        if m_value(s[:-4]) > 0:
            if s[-4:] == 'enci':
                return stem(s[:-1] + 'e')
            elif s[-4:] == 'anci':
                return stem(s[:-1] + 'e')
            elif s[-4:] == 'izer':
                return stem(s[:-1])
            elif s[-4:] == 'abli':
                return stem(s[:-1] + 'e')
            elif s[-4:] == 'alli':
                return stem(s[:-2])
            elif s[-4:] == 'ator':
                return stem(s[:-2] + 'e')
            
    if len(s) > 5:
        if m_value(s[:-3]) > 0:
            if s[-3:] == 'eli':
                return stem(s[:-2])
            
    if len(s) > 7:
        if m_value(s[:-5]) > 0:
            if s[-5:] == 'icate':
                return stem(s[:-3])
            elif s[-5:] == 'ative':
                return stem(s[:-5])
            elif s[-5:] == 'alize':
                return stem(s[:-3])
            elif s[-5:] == 'iciti':
                return stem(s[:-3])
    if len(s) > 6:
        if m_value(s[:-4]) > 0:
            if s[-4:] == 'ical':
                return stem(s[:-2])
            elif s[-4:] == 'ness':
                return stem(s[:-4])
    if len(s) > 5:
        if m_value(s[:-3]) > 0:
            if s[-3:] == 'ful':
                return stem(s[:-3])

    if len(s) > 3:
        if m_value(s[:-2]) > 1:
            if s[-2:] == 'al':
                return stem(s[:-2])
            elif s[-2:] == 'er':
                return stem(s[:-2])
            elif s[-2:] == 'ic':
                return stem(s[:-2])
            elif s[-2:] == 'ou':
                return stem(s[:-2])

    if len(s) > 7:
        if m_value(s[:-5]) > 1:
            if s[-4:] == 'ement':
                return stem(s[:-5])
    if len(s) > 6:
        if m_value(s[:-4]) > 1:
            if s[-4:] == 'ance':
                return stem(s[:-4])
            elif s[-4:] == 'able':
                return stem(s[:-4])
            elif s[-4:] == 'ence':
                return stem(s[:-4])
            elif s[-4:] == 'ible':
                return stem(s[:-4])
            elif s[-4:] == 'ment':
                return stem(s[:-4])
            elif s[-4:] == 'sion':
                return stem(s[:-3])
            elif s[-4:] == 'tion':
                return stem(s[:-3])
    if len(s) > 5:
        if m_value(s[:-3]) > 1:
            if s[-3:] == 'ant':
                return stem(s[:-3])
            elif s[-3:] == 'ent':
                return stem(s[:-3])
            elif s[-3:] == 'ism':
                return stem(s[:-3])
            elif s[-3:] == 'ate':
                return stem(s[:-3])
            elif s[-3:] == 'iti':
                return stem(s[:-3])
            elif s[-3:] == 'ous':
                return stem(s[:-3])
            elif s[-3:] == 'ive':
                return stem(s[:-3])
            elif s[-3:] == 'ize':
                return stem(s[:-3])

    if s[-4:] == 'sses':
        return stem(s[:-2])
    elif s[-3:] == 'ies':
        return stem(s[:-2])
    elif s[-1:] == 's' and s[-2:-1] != 's':
        return stem(s[:-1])

    if len(s) > 3:
        if s[-1] == 'e' and m_value(s[:-1]) > 1:
            return stem(s[:-1])
        elif s[-1] == 'e' and m_value(s[:-1]) == 1 and (s[-2] in VOWELS or s[-3] not in VOWELS or s[-4] in VOWELS):
            return stem(s[:-1])
    return s
    
def m_value(s):
    """ counts the number of adjacent consonant-vowel pairs in a row
    """
    m = 0
    i = 0
    while (i+1) < (len(s)):
        max_m = 0
        if (s[i] in VOWELS) and (s[i+1] not in VOWELS):
            m += 1
        elif (s[i] not in VOWELS) and (s[i+1] in VOWELS):
            m += 1 
        else:
            max_m = m
            m = 0
        i += 1
    return m

def compare_dictionaries(d1, d2):
    """ compares the similarity of two dictionaries by comparing
        their key-value pairs and returns a score
    """
    score = 0
    total = sum(d1.values())
    if total == 0:
        return 0
    for key in d2:
        if key in d1:
            score += math.log(d1[key]/total)*d2[key]
        else:
            score += math.log(0.5/total)*d2[key]
    return score    # returning the negative log of the absolute value to keep scores closer to 0
      
def test1():
    """ test cases
    """
    model = TextModel('A. Poor Righter')
    model.add_string("The partiers love the pizza party.")
    print(model)
    model1 = TextModel('A. Poor Righter')
    model1.add_string("The partiers love the pizza party.")
    model1.save_model()
    model2 = TextModel('A. Poor Righter')
    model2.read_model()
    print(model2)
    print(model2.words)
    print(model2.word_lengths)
    print(model1.stems)
    print(model1.sentence_lengths)
    print(model1.proper_nouns)
    model3 = TextModel('Sample News')
    model3.add_file('sample_text.txt')
    print(model3.stems)
    print(model3.sentence_lengths)
    print(model3.word_lengths)
    print(model3.proper_nouns)
    print(compare_dictionaries(model3.words,model.words))

def test2():
    """ your docstring goes here """
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)

def stemming_tests():
    """ tests of average runtimes for the stem() function
    """
    RUNTIMES = []
    i=0
    source1 = TextModel('Marx')
    source1.add_file('marx.txt')
    for key in source1.words:
        i+=1
        t = time.clock()
        stem(key)
        t = time.clock() - t
        RUNTIMES += [t]
    print(sum(RUNTIMES)/len(RUNTIMES))
    print(max(RUNTIMES))
    print(i)
    

def run_tests():
    """ your docstring goes here """
    source1 = TextModel('Marx')
    source1.add_file('marx.txt')

    source2 = TextModel('Engels')
    source2.add_file('engels.txt')

    new1 = TextModel('The Communist Manifesto')
    new1.add_file('test.txt')
    new1.classify(source1, source2)

    new2 = TextModel('The Accumulation of Capital by Rosa Luxemburg')
    new2.add_file('luxemburg.txt')
    new2.classify(source1, source2)

    new3 = TextModel('Essays on Working-Class and International Revolution, 1904-1917 by Leon Trotsky')
    new3.add_file('trotsky.txt')
    new3.classify(source1, source2)

    new4 = TextModel('A Letter to American Workingmen, from the Socialist Soviet Republic of Russia by Vladimir Lenin')
    new4.add_file('lenin.txt')
    new4.classify(source1, source2)
    

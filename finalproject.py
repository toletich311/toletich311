#
#
#
# finalproject.py - Final Project
#
#

import math

def clean_text(txt):
    """ takes a string of text txt as a parameter 
        returns a list containing the words in txt after punctuation has been removed
    """
    s = txt
    for symbol in """.,?"'!;:""":
        s = s.replace(symbol, '')
        
    s= s.lower()
    s= s.split(' ')
    return s

def stem(s):
    """ accepts a string a as a parameter, returns the stem of s
    """
    if s[-1]=='s':
        s= s[:-1]
    if s[-2:]=='es':
        s= s[:-2]
    if s[-3:]== 'ing':
        s= s[:-3]
    if s[-1] =='y':
        s=s[:-1]+ 'i'
    if s[-2:]=='er':
        s = s[:-2]
    if s[-3:]=='ish':
        s=s[:-3]
    if s[-2:]=='ed' and s[-3:-2] not in 'aeiou':
        s=s[:-2]
    if s[-4:]=='ment':
        s=s[:-4]
    return s

def compare_dictionaries(d1, d2):
    """ take two feature dictionaries d1 and d2 as inputs, 
        and it should compute and return their log similarity score
    """
    if d1 == {}:
        return -50
    score =0.0
    total = 0
    for x in d1:
        total += d1[x]
        
    for y in d2:
        if y in d1:
            score += d2[y]* math.log(d1[y]/total)
        else:
            score += d2[y]* math.log(0.5 / total)
    return score
            
    
class TextModel: 
    """ initial version of TextModel class
    """
    def __init__(self, model_name):
       
       """ constructor to add attrubutes to TextModel object
       """
       words = {}
       word_lengths = {}
       stems = {}
       sentence_lengths = {}
       phrase_lengths = {}
       
       self.words = words
       self.word_lengths = word_lengths
       self.name = model_name
       self.stems = stems
       self.sentence_lengths= sentence_lengths
       self.phrase_lengths = phrase_lengths
       
     
    def __repr__(self):
        """ returns a string representation of object in TextModel class
        """
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s+= '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s+= '  number of stems: '+str(len(self.stems))+'\n'
        s+= '  number of sentence lengths: '+str(len(self.sentence_lengths))+'\n'
        s+= '  number of phrases: '+str(len(self.phrase_lengths))+'\n'
        
        return s
    
    def add_string(self, s):
        """ Analyzes the string txt and adds its pieces
            to all of the dictionaries in this text model.
        """
        unclean = s.split(' ')
        
        s_count = 0
        for w in unclean:

            if w[-1] not in '.?!':
                s_count+=1
            else:
                s_count +=1
                if s_count in self.sentence_lengths:
                    self.sentence_lengths[s_count]+=1
                else:
                    self.sentence_lengths[s_count]=1
                s_count = 0
                
        p_count = 0
        for w in unclean:
            
            if w[-1] not in ',.!?':
                p_count+=1
            else:
                p_count +=1
                if p_count in self.phrase_lengths:
                    self.phrase_lengths[p_count]+=1
                else:
                    self.phrase_lengths[p_count]=1
                p_count = 0
                
                    
        

        word_list = clean_text(s)

        for w in word_list:
            
            if w in self.words:
                self.words[w]+=1
            else:
                self.words[w] = 1
            
            if len(w) in self.word_lengths:
                self.word_lengths[len(w)]+=1
            else:
                self.word_lengths[len(w)]= 1
        
        
        for w in word_list:
            stm = stem(w)
            if stm in self.stems:
                self.stems[stm]+=1
            else:
                self.stems[stm]=1
        
                
    def add_file(self, filename):
        """ adds all of the text in the file identified by filename to the model
        """
        
        file = open(filename, 'r', encoding='utf8', errors='ignore')
        text = file.read()
        file.close()
        
        self.add_string(text)
    
    def save_model(self):
        """ writes dictionaries of called object as easily readible files
        """
        d_words = self.words 
        d_word_lengths = self.word_lengths
        d_stems= self.stems
        d_sentences = self.sentence_lengths
        d_phrases = self.phrase_lengths
        
        
        fw = open(self.name + '_words', 'w')     
        fw.write(str(d_words))              
        fw.close()  
        
        fwl = open(self.name + '_word_lengths', 'w')     
        fwl.write(str(d_word_lengths))             
        fwl.close() 
        
        f = open(self.name + '_stems', 'w')
        f.write(str(d_stems))
        f.close()
        
        f = open(self.name + '_sentences', 'w')
        f.write(str(d_sentences))
        f.close()
        
        f=open(self.name + '_phrases', 'w')
        f.write(str(d_phrases))
        f.close()
        
        
    
    def  read_model(self):
        """ reads and stores dictionaries from files into object of TextModel Class
        """
        fwr = open(self.name +'_words', 'r')    
        d_words = fwr.read()           
        fwr.close()
        self.words = dict(eval(d_words))  

        fwlr = open(self.name +'_word_lengths', 'r')    
        d_word_lengths = fwlr.read()          
        fwlr.close()
        self.word_lengths = dict(eval(d_word_lengths))     
        
        f = open(self.name + '_stems', 'r')
        d_stems = f.read()
        self.stems= dict(eval(d_stems))
        
        f = open(self.name + '_sentences', 'r')
        d_sentences = f.read()
        self.sentence_lengths= dict(eval(d_sentences))
        
        f = open(self.name + '_phrases', 'r')
        d_phrases = f.read()
        self.phrase_lengths= dict(eval(d_phrases))
    
    def similarity_scores(self, other):
        """ computes and returns a list of log similarity scores 
            measuring the similarity of self and other
        """
        
        word_score = []
        word_score += [compare_dictionaries(other.words, self.words)]
        word_score += [compare_dictionaries(other.word_lengths, self.word_lengths)]
        word_score += [compare_dictionaries(other.stems, self.stems)]
        word_score += [compare_dictionaries(other.sentence_lengths, self.sentence_lengths)]
        word_score += [compare_dictionaries(other.phrase_lengths, self.phrase_lengths)]
        
        return word_score
        
    def classify(self, source1, source2):
        """ compares the called TextModel object to two other “source” TextModel objects 
            determines which of these other TextModels is the more likely source of the called TextModel.
        """
        
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        
        print('scores for ', source1.name, ': ', scores1)
        print('scores for ', source2.name, ': ', scores2)
        
        s1_great=0
        s2_great=0
        for x in scores1:
            for y in scores2:
                if x>y:
                    s1_great+=1
                else:
                    s2_great+=1
                    
        if s1_great>s2_great:
            print(self.name, ' is more likely to have come from ', source1.name)
        else:
            print(self.name, ' is more likely to have come from ', source2.name)
            
            
def run_tests():
    """ tests program with my text models, ASAP_Rocky_Model and lil_peep_model both 
        contain four different samples of text within"""
        
    source1 = TextModel('ASAPRocky')
    source1.add_file('ASAP_Rocky_Model.txt')

    source2 = TextModel('lilpeep')
    source2.add_file('lil_peep_model.txt')

    new1 = TextModel('peepTest')
    new1.add_file('test1_lp.txt')
    new1.classify(source1, source2)
    
    new2 = TextModel('meTest')
    new2.add_file('test2_me.txt')
    new2.classify(source1, source2)
    
    new3 = TextModel('rockyTest')
    new3.add_file('test3_ar.txt')
    new3.classify(source1, source2)
    
    new4 = TextModel('harryTest')
    new4.add_file('test4_hs.txt')
    new4.classify(source1, source2)
                    
                    
                    
                    
        
        
        
        
        
        
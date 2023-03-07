class ReadEliminateSignFromPaper:
    def __init__(self, file):
        # chnaging the way of file I/O is possible
        with open(file, 'r', encoding='utf8') as f:
            paper = f.readlines() # a list that contains paragraph-wise elements. note: each paragraph has different number of sentences
            
        self.sign_dict = dict() # a dictionary whose key and value are the eliminated sign and the number of that sign, respectively
        self.sentences = list() # a list that contains sentence-wise elements
        # changing data-type or name of variables above is possible
        
        #########################################################
        # complete the code below, following assignment guideline
        for i in range(len(paper)):
            sentence=paper[i]
            if sentence[len(sentence)-1]=='\n':
                sentence=sentence[:len(sentence)-1]
            ret=''
            start=0
            for j in range(len(sentence)):
                if sentence[j]==' ':
                    word=sentence[start:j]
                    push=self.find_eliminate_sign(word)
                    ret = ret+push+' '
                    if push[len(push)-1]=='.':
                        ret = ret[:len(ret)-1]
                        self.sentences.append(ret)
                        ret=''
                    start=j+1
            word=sentence[start:len(paper[i])]
            push=self.find_eliminate_sign(word)
            ret = ret+push
            self.sentences.append(ret)

                    
            
        #########################################################
    
    """it is impossible to change the name of methods (functions) below"""
    def find_eliminate_sign(self, word):
        '''find all signs and eliminate them from given "word"
           (except the period(.) that makes the End Of Sentence)
           and return it
        '''
        
        no_sign_word = '' # changing this variable also okay
        #########################################################
        # complete the code below, following assignment guideline
        last=0
        for i in range(len(word)):
            b=word[i]
            if(b.isalnum()==False):
                if b=='.' and i==len(word)-1:
                    continue
                if b in self.sign_dict:
                    save = self.sign_dict[b]
                    self.sign_dict[b] = save+1
                else:
                    self.sign_dict[b] = 1
                if(last != i):
                    no_sign_word = no_sign_word + word[last:i]
                last = i+1
        if last!=len(word):
            no_sign_word = no_sign_word + word[last:len(word)]
        #########################################################
        return no_sign_word
    
    def get_sorted_sign(self):
        '''return a list 
           that contains (eliminated sign, the number of that sign) tuples 
           and is sorted by the number in descending
        '''
        #########################################################
        # complete the code below, following assignment guideline
        ret=sorted(self.sign_dict.items(), key=lambda x:x[1], reverse=True)
        return ret
        #########################################################
    
    def __len__(self):
        '''return the number of sentences'''
        #########################################################
        # complete the code below, following assignment guideline
        
        return len(self.sentences)
        #########################################################
        
    def __getitem__(self, idx):
        """return a sentence that corresponds to the given index "idx" """
        #########################################################
        # complete the code below, following assignment guideline
        return self.sentences[idx]
        #########################################################

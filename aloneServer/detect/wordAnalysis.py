from multiprocessing import Process, current_process
from time import ctime
import nltk
from konlpy.tag import Twitter; nlp = Twitter()

class WordAnalysis(Process):
    def __init__(self, _wordString, _q):
        Process.__init__(self)
        self.str = _wordString
        self.tmp_data = None
        self.q = _q

    def run(self):
        self.curProcss = current_process().name
        nouns = nlp.nouns(self.str)
        nouns = [each_word for each_word in nouns if len(each_word) > 0]
        ko = nltk.Text(nouns)

        self.tmp_data = ko.vocab()
        print("[{0}]{1} ==> Word Analysising....".format(ctime(), self.curProcss))
        self.q.put(dict(self.tmp_data))
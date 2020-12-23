#-*- coding:utf-8 _*-  
""" 
@author:charlesXu
@file: Chatbot_graph.py 
@desc:
@time: 2019/03/15 
"""

from models.bot.Question_classifier import *
from models.bot.Question_parser import *
from models.bot.Answer_search import *


class ChatBotGraph():
    '''
    问答类
    '''
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionParser()
        self.searcher = AnswerSearcher()

    def chat_main(self, sent):
        answer = '您好，我是小笨医药智能助理，希望可以帮到您。祝您身体棒棒！'
        res_classify = self.classifier.classify(sent)
        if not res_classify:
            return answer
        res_sql = self.parser.parser_main(res_classify)
        final_answers = self.searcher.search_main(res_sql)
        if not final_answers:
            return answer
        else:
            return '\n'.join(final_answers)
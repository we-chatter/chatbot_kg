# -*- coding: utf-8 -*-

'''
@Author  :   Xu
 
@Software:   PyCharm
 
@File    :   kbqa_predict.py
 
@Time    :   2020/3/25 2:00 下午
 
@Desc    :
 
'''

from models.bot import ChatBotGraph


handler = ChatBotGraph()

def get_answer(msg):
    '''

    :param msg:
    :return:
    '''

    answer = handler.chat_main(msg)

    return answer

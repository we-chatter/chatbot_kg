# -*- coding: utf-8 -*-

"""
@Author  :   Xu
 
@Software:   PyCharm
 
@File    :   pre_load.py
 
@Time    :   2020/12/23 3:21 下午
 
@Desc    :
 
"""
import thulac
import logging

from models.util.Neo_utils import Neo4j


neo_con = Neo4j()
neo_con.connectDB()

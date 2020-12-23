# -*- coding: utf-8 -*-

"""
@Author  :   Xu

@Software:   PyCharm

@File    :   run_server.py

@Time    :   2020/8/26 2:50 下午

@Desc    :

"""
import datetime
import json
import os
import sys
import logging

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)

from config import CONFIG

from sanic import Sanic, response
from sanic.response import text, HTTPResponse
from sanic.request import Request

from models.toolkit.pre_load import neo_con
from models.util.process import sortDict

from utils.LogUtils import Logger

logger = logging.getLogger(__name__)

app = Sanic(__name__)
app.config.from_object(CONFIG)

db = neo_con


@app.route("/")
async def test(request):
    return text('Welcome to the chatbot knowledge platform')


@app.post('/detail')
async def show_detail(request: Request) -> HTTPResponse:
    """
    实体详情查询
    :return:
    """
    localtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        querys = request.json["entity"]
        result = db.matchHudongItembyTitle(querys)
        res_dic = {
            "result": result,
            "time": localtime
        }
        log_res = json.dumps(res_dic, ensure_ascii=False)
        logger.info(log_res)
        return response.json(res_dic,
                             dumps=json.dumps)
    except Exception as e:
        logger.info('Error is {}'.format(e))
        res_dic = {
            "result": 'Failure',
            "msg": str(e),
            "time": localtime
        }

        return response.json(res_dic)


@app.post('/searchEntity')
async def search_entity(request: Request) -> HTTPResponse:
    """
    实体查询
    """
    localtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        querys = request.json["entity"]
        result = db.getEntityRelationbyEntity(querys)
        if len(result) == 0:
            result = '数据库中暂未添加该实体'
        else:
            result = sortDict(result)
        res_dic = {
            "result": result,
            "time": localtime
        }
        log_res = json.dumps(res_dic, ensure_ascii=False)
        logger.info(log_res)
        return response.json(res_dic,
                             dumps=json.dumps)
    except Exception as e:
        logger.info('Error is {}'.format(e))
        res_dic = {
            "result": 'Failure',
            "msg": str(e),
            "time": localtime
        }

        return response.json(res_dic)

@app.post('/kbqa')
async def kbqa(request: Request) -> HTTPResponse:
    """
    实体查询
    """
    localtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        querys = request.json["entity"]
        result = db.getEntityRelationbyEntity(querys)
        if len(result) == 0:
            result = '数据库中暂未添加该实体'
        else:
            result = sortDict(result)
        res_dic = {
            "result": result,
            "time": localtime
        }
        log_res = json.dumps(res_dic, ensure_ascii=False)
        logger.info(log_res)
        return response.json(res_dic,
                             dumps=json.dumps)
    except Exception as e:
        logger.info('Error is {}'.format(e))
        res_dic = {
            "result": 'Failure',
            "msg": str(e),
            "time": localtime
        }

        return response.json(res_dic)


@app.post('/searchRelation')
async def search_relation(request: Request) -> HTTPResponse:
    """
    实体查询
    """
    localtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        entity1 = request.json["entity1"]
        entity2 = request.json["entity2"]
        relation = request.json["relation"]
        # 若只输入entity1,则输出与entity1有直接关系的实体和关系
        searchResult = '请检查参数数据'
        if len(entity1) != 0 and len(relation) == 0 and len(entity2) == 0:
            searchResult = db.findRelationByEntity(entity1)
            searchResult = sortDict(searchResult)
            if len(searchResult) == 0:
                searchResult = '未查询到关系数据'
        # 若只输入entity2则,则输出与entity2有直接关系的实体和关系
        if len(entity2) != 0 and len(relation) == 0 and len(entity1) == 0:
            searchResult = db.findRelationByEntity2(entity2)
            searchResult = sortDict(searchResult)
            if len(searchResult) == 0:
                searchResult = '未查询到关系数据'
        # 若输入entity1和relation，则输出与entity1具有relation关系的其他实体
        if len(entity1) != 0 and len(relation) != 0 and len(entity2) == 0:
            searchResult = db.findOtherEntities(entity1, relation)
            searchResult = sortDict(searchResult)
            if len(searchResult) == 0:
                searchResult = '未查询到关系数据'
        # 若输入entity2和relation，则输出与entity2具有relation关系的其他实体
        if len(entity2) != 0 and len(relation) != 0 and len(entity1) == 0:
            searchResult = db.findOtherEntities2(entity2, relation)
            searchResult = sortDict(searchResult)
            if len(searchResult) == 0:
                searchResult = '未查询到关系数据'
        # 若输入entity1和entity2,则输出entity1和entity2之间的最短路径
        if len(entity1) != 0 and len(relation) == 0 and len(entity2) != 0:
            searchResult = db.findRelationByEntities(entity1, entity2)
            if len(searchResult) > 0:
                searchResult = sortDict(searchResult)
            else:
                searchResult = '未查询到关系数据'
        # 若输入entity1,entity2和relation,则输出entity1、entity2是否具有相应的关系
        if len(entity1) != 0 and len(entity2) != 0 and len(relation) != 0:
            searchResult = db.findEntityRelation(entity1, relation, entity2)
        # 全为空
        if len(entity1) != 0 and len(relation) != 0 and len(entity2) != 0:
            searchResult = '未查询到关系数据'
        res_dic = {
            "result": searchResult,
            "time": localtime
        }
        log_res = json.dumps(res_dic, ensure_ascii=False)
        logger.info(log_res)
        return response.json(res_dic,
                             dumps=json.dumps)
    except Exception as e:
        logger.info('Error is {}'.format(e))
        res_dic = {
            "result": 'Failure',
            "msg": str(e),
            "time": localtime
        }

        return response.json(res_dic)

# To Do
@app.post('/updateData')
async def update_entity(request: Request) -> HTTPResponse:
    """
    实体查询
    """
    localtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        querys = request.json["entity"]
        result = db.getEntityRelationbyEntity(querys)
        if len(result) == 0:
            result = '数据库中暂未添加该实体'
        else:
            result = sortDict(result)
        res_dic = {
            "result": result,
            "time": localtime
        }
        log_res = json.dumps(res_dic, ensure_ascii=False)
        logger.info(log_res)
        return response.json(res_dic,
                             dumps=json.dumps)
    except Exception as e:
        logger.info('Error is {}'.format(e))
        res_dic = {
            "result": 'Failure',
            "msg": str(e),
            "time": localtime
        }

        return response.json(res_dic)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9022, auto_reload=True, workers=4)

# -*- coding: utf-8 -*-

'''
@Author  :   Xu
 
@Software:   PyCharm
 
@File    :   test.py
 
@Time    :   2020/3/30 8:46 下午
 
@Desc    :
 
'''

from harvesttext import HarvestText
ht = HarvestText()


para = "上港的武磊和恒大的郜林，谁是中国最好的前锋？那当然是武磊武球王了，他是射手榜第一，原来是弱点的单刀也有了进步"
entity_mention_dict = {'武磊':['武磊','武球王'],'郜林':['郜林','郜飞机'],'前锋':['前锋'],'上海上港':['上港'],'广州恒大':['恒大'],'单刀球':['单刀']}
entity_type_dict = {'武磊':'球员','郜林':'球员','前锋':'位置','上海上港':'球队','广州恒大':'球队','单刀球':'术语'}
ht.add_entities(entity_mention_dict,entity_type_dict)
print("\nSentence segmentation")
print(ht.seg(para,return_sent=True))    # return_sent=False时，则返回词语列表



# 在现有实体库的基础上随时新增，比如从新词发现中得到的漏网之鱼
ht.add_new_entity("颜骏凌", "颜骏凌", "球员")
docs = ["武磊和颜骏凌是队友",
		"武磊和郜林都是国内顶尖前锋"]
G = ht.build_entity_graph(docs)
print(dict(G.edges.items()))
G = ht.build_entity_graph(docs, used_types=["球员"])
print(dict(G.edges.items()))
使用说明：
from test_domain_v2 import domain_classfiy

domain_classfiy函数输入输出说明：
输入：
    uid_list:uid列表 [uid1,uid2,uid3,...]
    uid_weibo:分词之后的词频字典  {uid1:{'key1':f1,'key2':f2...}...}

输出：
    domain：标签字典  {uid1:[label1,label2,label3...],uid2:[label1,label2,label3...]...}

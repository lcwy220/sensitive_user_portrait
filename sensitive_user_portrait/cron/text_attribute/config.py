# -*- coding: UTF-8 -*-

politics_en2ch_dict = {"left": u"左派", "mid":u"中立", "right":u"右派"}

#topic en2ch dict
topic_en2ch_dict = {'fear-of-violence':u'暴恐', 'heresy':u'邪教', 'ideology':u'意识形态', \
        'livelihood':u'民生', 'religion':u'宗教', 'life':u'其他'}

#activeness weight dict used by evaluate_index.py
activeness_weight_dict = {'activity_time':0.3, 'activity_geo':0.2, 'statusnum':0.5}
#importance weight dict
importance_weight_dict = {'fansnum':0.2, 'domain':0.5, 'topic':0.3}
#topic weight dict

topic_weight_dict = {'暴恐':0.8,'邪教':0.6,'意识形态':0.8,'民生':0.6,'宗教':0.7,'其他':0.3}


#domain en2ch dict
domain_en2ch_dict = {"writer":u'作家写手', 'professor':u'专家学者', 'root':u'草根红人', 'religion':u'宗教人士', \
                    'lawyer':u'维权律师', 'well-known': u'公知分子', 'non-public':u'非公企业主', 'media':u'独立媒体人', \
                    'official-media':u'官方媒体', 'governer':u'公职人员', 'star':u'文体明星', 'welfare':u'社会公益', 'other':u'其他'}


#domain weight dict
domain_weight_dict = {'作家写手':0.6, '专家学者':0.7, '草根红人':0.6, '宗教人士':0.7, '维权律师':0.8, '公知分子':0.8,\
        '非公企业主':0.4, '独立媒体人':0.6, '官方媒体':0.6, '公职人员':0.6, '文体明星':0.3, '其他':0.2, '社会公益':0.3}

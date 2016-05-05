# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.path.append('./../../')
from global_utils import es_user_profile as es

index_info = {
    "mappings":{
        "bci":{
            "properties":{
                "bci_week_sum":{
                    "type":"double",
                },
                "bci_month_sum":{
                    "type":"double",
                },
                "bci_day_change":{
                    "type":"double",
                },
                "bci_week_change":{
                    "type":"double",
                },
                "bci_week_ave":{
                    "type":"double",
                },
                "bci_week_var":{
                    "type":"double",
                },
                "bci_month_change":{
                    "type":"double",
                },
                "bci_month_ave":{
                    "type":"double",
                },
                "bci_month_var":{
                    "type":"double",
                },
                "weibo_count_week_sum":{
                    "type":"double",
                },
                "weibo_count_month_sum":{
                    "type":"double",
                },
                "weibo_count_day_change":{
                    "type":"double",
                },
                "weibo_count_week_change":{
                    "type":"double",
                },
                "weibo_count_week_ave":{
                    "type":"double",
                },
                "weibo_count_week_var":{
                    "type":"double",
                },
                "weibo_count_month_change":{
                    "type":"double",
                },
                "weibo_count_month_ave":{
                    "type":"double",
                },
                "weibo_count_month_var":{
                    "type":"double",
                }
            }
        }
    }
}

def mappings(index_name):
    exist_bool = es.indices.exists(index=index_name)
    if not exist_bool:
        es.indices.create(index=index_name, body=index_info, ignore=400)
    return "1"

if __name__ == "__main__":
    mappings("bci_history")


from alinow_backend_proto.item_pb2 import *
from alinow_backend_proto.common_pb2 import *
#from item_pb2 import *
#from common_pb2 import *
import sys

def GetScore(visit_info):
    return ((pow(visit_info.click_count, 2) + 1)/(pow(visit_info.pv_count, 1.5) + 10))*max(visit_info.weight, 0.00001)
def GetNewsScore(visit_info):
    if visit_info.pv_count==0:
        return 1
    return (pow(visit_info.click_count+1, 1+visit_info.weight))/visit_info.pv_count
def Sort(user_feature_list):
    ret = UserFeatureList()
    features = sorted(user_feature_list.feature, key=lambda x: x.feature_name.startswith('news') and GetNewsScore(x.visit_info) or GetScore(x.visit_info), reverse=True)
    for f in features:
        ret.feature.add().CopyFrom(f)
    return ret

#@return: user_feature_list
def MergeFeature(user_feature_list, item_feature_list, card_feature, favor_type):
    pos = {}
    for i in range(0, len(user_feature_list.feature)):
        pos[user_feature_list.feature[i].feature_name] = i
    act = (1, (favor_type == 'like' and 3 or (favor_type == 'click' and 1 or 0))) #TODO add like field
    
    #double score for news cardfeature 
    if card_feature.startswith("news") and favor_type!='show':
        ife = ItemFeature()
        ife.feature_name = card_feature
        ife.weight = 0
        item_feature_list.feature.add().CopyFrom(ife)
    
    for f in item_feature_list.feature:
        if f.feature_name in pos:
            p = pos[f.feature_name]
            user_feature_list.feature[p].visit_info.pv_count += act[0]
            user_feature_list.feature[p].visit_info.click_count += act[1]
            user_feature_list.feature[p].visit_info.weight = max(user_feature_list.feature[p].visit_info.weight, f.weight)
        else:
            uf = UserFeature()
            uf.feature_name = f.feature_name
            vi = VisitInfo()
            vi.pv_count, vi.click_count = act
            vi.weight = f.weight
            uf.visit_info.CopyFrom(vi)
            user_feature_list.feature.add().CopyFrom(uf)
            
    return Sort(user_feature_list)
    
def main():
    ufl = UserFeatureList()
    uf = UserFeature()
    vi = VisitInfo()
    vi.pv_count = 1
    vi.click_count = 3
    vi.weight = 1
    uf.feature_name = "newsAAA"
    uf.visit_info.CopyFrom(vi)
    ufl.feature.add().CopyFrom(uf)
    vi.pv_count = 1
    vi.click_count = 4
    vi.weight = 1
    uf.feature_name = "bbb"
    uf.visit_info.CopyFrom(vi)
    ufl.feature.add().CopyFrom(uf)
    
    ifl = ItemFeatureList()
    ife = ItemFeature()
    ife.feature_name = "newsAAA"
    ife.weight = 1
    ifl.feature.add().CopyFrom(ife)
    ife.feature_name = "bbb"
    ife.weight = 1
    ifl.feature.add().CopyFrom(ife)
    
    print Sort(ufl)
    print MergeFeature(Sort(ufl), ifl, 'aaa', 'click')

if __name__ == "__main__":   
    sys.exit( main() )

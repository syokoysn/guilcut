import pandas as pd 
import numpy as np

def make_sequence(I, df_item_data):
    '''順序制約のある組みのtupleを保持したリストを作成
    
    
    '''
    df = df_item_data
    use_stack = set([df.loc[df.ITEM_ID == i, 'STACK'][i] for i in I ])
    sequence = []
    for s in use_stack :
        flag = df[df.STACK == s].ITEM_ID.tolist()
        for i in range(len(flag)-1):
            if (flag[i] in I) & (flag[i+1]in I) :
                sequence.append((flag[i],flag[i+1]))
    return  sequence
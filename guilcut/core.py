import pandas as pd
import numpy as np


def make_sequence(I, df_item_data):
    """順序制約のある組みのtupleを保持したリストを作成"""
    df = df_item_data
    use_stack = set([df.loc[df.ITEM_ID == i, "STACK"][i] for i in I])
    sequence = []
    for s in use_stack:
        flag = df[df.STACK == s].ITEM_ID.tolist()
        for i in range(len(flag) - 1):
            if (flag[i] in I) & (flag[i + 1] in I):
                sequence.append((flag[i], flag[i + 1]))
    return sequence


def sequence_pair(L1, L2):
    """
    相対位置の関係より，自分より右か，したかに配置する情報を取得する関数
    """
    b = {j: i for i, j in enumerate(L2)}
    res = {i: [[], []] for i in L1}
    for i in range(len(L1)):
        for j in range(i + 1, len(L1)):
            if b[L1[i]] < b[L1[j]]:
                # 右に配置
                res[L1[i]][1].append(L1[j])
            else:
                # 下に配置
                res[L1[i]][0].append(L1[j])
    return res

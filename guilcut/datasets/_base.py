
from os.path import dirname
import pandas as pd


def load_roadef2018(kind='A',number=0):

    dir_name = dirname(__file__)+f'/data/roadef2018/dataset_{kind}/'

    batch_path = dir_name + kind + str(number)+'_batch.csv'
    defect_path = dir_name + kind + str(number)+'_defects.csv'
    if number==0:
        if kind=='A':
            n = 20
        else:
            n= 15
        result = {}
        for i in range(1,n+1):
            batch_path = dir_name + kind + str(i)+'_batch.csv'
            defect_path = dir_name + kind + str(i)+'_defects.csv'
            result[i] = {'batch': pd.read_csv(batch_path, sep=';'), 'defect': pd.read_csv(defect_path, sep=';')}
        return result
    return {'batch': pd.read_csv(batch_path, sep=';'), 'defect': pd.read_csv(defect_path, sep=';')}
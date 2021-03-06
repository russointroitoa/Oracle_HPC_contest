import pandas as pd
from scipy import *
from scipy.sparse import *
from tqdm.auto import tqdm
import os

"""
For each test name assigns the overall name popularity.
"""

def name_popularity(isValidation, path=""):
    if isValidation:
        train_path = os.path.join(path,'train.csv')
        test_path = os.path.join(path, 'test.csv')
        df_train = pd.read_csv(train_path, escapechar="\\")
        df_test = pd.read_csv(test_path, escapechar="\\")
        #df_train = pd.read_csv('../dataset/validation/train.csv', escapechar="\\")
        #df_test = pd.read_csv('../dataset/validation/test.csv', escapechar="\\")
    else:
        df_train = pd.read_csv('../dataset/original/train.csv', escapechar="\\")
        df_test = pd.read_csv('../dataset/original/test.csv', escapechar="\\")

    df_train = df_train.sort_values(by=['record_id']).reset_index(drop=True)
    df_test = df_test.sort_values(by=['record_id']).reset_index(drop=True)
    # concat dataframes to compute the overall popularity
    full = df_train.name.append(df_test.name).reset_index(drop=True)
    full = [str(x).lower() for x in full]
    names = dict(zip(list(set(full)), [0 for x in range(len(list(set(full))))]))
    for name in tqdm(full):
        names[name]+=1
    # feature creation
    feature = pd.DataFrame()
    feature['name'] = names.keys()
    feature['name_popularity'] = names.values()
    # now merge with test
    df_test.name = df_test.name.astype(str)
    df_test.name = df_test.name.str.lower()
    final_feature = df_test[['record_id', 'name']]
    final_feature = pd.merge(final_feature, feature, how='left', on=['name']).fillna(0)
    final_feature = final_feature[['record_id','name_popularity']]
    print(final_feature)

    if isValidation:
        feat_path = os.path.join(path, 'feature/name_popularity.csv')
        final_feature.to_csv(feat_path, index=False)
    else:
        final_feature.to_csv('../dataset/original/feature/name_popularity.csv', index = False)


name_popularity(True, path="../dataset/validation")
name_popularity(True, path="../dataset/validation_2")
name_popularity(True, path="../dataset/validation_3")
name_popularity(False)

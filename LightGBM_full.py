import pandas as pd
import numpy as np
import lightgbm as lgb
import time

train_1 = pd.read_csv("dataset/validation_2/train_complete.csv")
train_2 = pd.read_csv("dataset/validation_3/train_complete.csv")
val = pd.read_csv("dataset/validation/train_complete.csv")
test = pd.read_csv("dataset/original/test_complete.csv")

train = pd.concat([train_1, train_2])


group = train.groupby('queried_record_id').size().values
eval_group = val.groupby('queried_record_id').size().values

params = {
        'boosting_type':'gbdt',
        'num_leaves':31,
        'max_depth':-1,
        'learning_rate':0.1,
        'n_estimators':100,
        'objective':None,
        'class_weight':None,
        'min_split_gain':0.0,
        'min_child_weight':0.001,
        'min_child_samples':20,
        'subsample':1.0,
        'subsample_freq':0,
        'colsample_bytree':1.0,
        'reg_alpha':0.0,
        'reg_lambda':0.0,
        'random_state':None,
        'n_jobs':-1,
        'silent':True,
        'importance_type':'split'
}

ranker = lgb.LGBMRanker(params, device='gpu')
print('Start LGBM...')
t1 = time.time()
ranker.fit(train.drop(['queried_record_id', 'target', 'predicted_record_id','predicted_record_id_record', 'linked_id_idx'], axis=1),
           train['target'], group=group,
           eval_set=[(val.drop(['queried_record_id', 'target', 'predicted_record_id','predicted_record_id_record', 'linked_id_idx'], axis=1), val['target'])],
           eval_group=[eval_group])
t2 = time.time()
print(f'Learning completed in {int(t2-t1)} seconds.')
predictions = ranker.predict(test.drop(['queried_record_id', 'linked_id_idx', 'predicted_record_id','predicted_record_id_record'], axis=1))
test['predictions'] = predictions
df_predictions = test[['queried_record_id', 'predicted_record_id', 'predicted_record_id_record', 'predictions']]

rec_pred = []
for (l,p,record_id) in zip(df_predictions.predicted_record_id, df_predictions.predictions, df_predictions.predicted_record_id_record):
    rec_pred.append((l, p, record_id))

df_predictions['rec_pred'] = rec_pred
group_queried = df_predictions[['queried_record_id', 'rec_pred']].groupby('queried_record_id').apply(lambda x: list(x['rec_pred']))
df_predictions = pd.DataFrame(group_queried).reset_index().rename(columns={0 : 'rec_pred'})

def reorder_preds(preds):
    ordered_lin = []
    ordered_score = []
    ordered_record = []
    for i in range(len(preds)):
        l = sorted(preds[i], key=lambda t: t[1], reverse=True)
        lin = [x[0] for x in l]
        s = [x[1] for x in l]
        r = [x[2] for x in l]
        ordered_lin.append(lin)
        ordered_score.append(s)
        ordered_record.append(r)
    return ordered_lin, ordered_score, ordered_record

df_predictions['ordered_linked'], df_predictions['ordered_scores'], df_predictions['ordered_record'] = reorder_preds(df_predictions.rec_pred.values)
#df_predictions = df_predictions[['queried_record_id', 'ordered_preds']].rename(columns={'ordered_preds': 'predicted_record_id'})

#new_col = []
#for t in tqdm(df_predictions.predicted_record_id):
#    new_col.append(' '.join([str(x) for x in t]))

#df_predictions.predicted_record_id = new_col
df_predictions.to_csv('lgb_predictions_full.csv', index=False)


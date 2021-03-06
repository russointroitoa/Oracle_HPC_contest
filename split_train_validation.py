import pandas as pd
from sklearn.model_selection import train_test_split
import os

train = pd.read_csv("dataset/original/train.csv", escapechar="\\")

X_train, X_val, y_train, y_val = train_test_split(train, train['linked_id'] , test_size=0.33, random_state=42)
if not os.path.isdir("dataset/validation"):
    os.makedirs("dataset/validation")
    os.makedirs("dataset/validation/feature")
X_train.to_csv('dataset/validation/train.csv', index=False)
X_val.to_csv('dataset/validation/test.csv', index=False)


train = pd.read_csv("dataset/validation/train.csv", escapechar="\\")
test = pd.read_csv("dataset/validation/test.csv", escapechar="\\")

X_train, X_val, y_train, y_val = train_test_split(train, train['linked_id'] , test_size=0.5, random_state=42)

if not os.path.isdir("dataset/validation_2"):
    os.makedirs("dataset/validation_2")
    os.makedirs("dataset/validation_2/feature")

complete_train_1 = pd.concat([X_train, test])
complete_train_1.to_csv("dataset/validation_2/train.csv", index=False)
X_val.to_csv("dataset/validation_2/test.csv", index=False)

if not os.path.isdir("dataset/validation_3"):
    os.makedirs("dataset/validation_3")
    os.makedirs("dataset/validation_3/feature")


complete_train_2 = pd.concat([X_val, test])
complete_train_2.to_csv("dataset/validation_3/train.csv", index=False)
X_train.to_csv("dataset/validation_3/test.csv", index=False)

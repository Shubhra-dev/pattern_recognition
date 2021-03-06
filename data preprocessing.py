# -*- coding: utf-8 -*-
"""
# Read Data
"""

import pandas as pd
from pandas.api.types import is_string_dtype

crx = pd.read_csv('crx.csv', na_values='?')
post = pd.read_csv('post-operative.csv')

for col in post.columns:
  post[col] = post[col].str.strip()

for col in crx.columns:
  if (is_string_dtype(crx[col].dtype)):
    crx[col] = crx[col].str.strip()

"""# Split Data"""

from sklearn.model_selection import train_test_split

crx_x = crx.loc[:, crx.columns != 'Class']
crx_y = crx['Class']

post_x = post.loc[:, post.columns != 'Label']
post_y = post['Label']

# print(post_y.unique())

# train_x, test_x, train_y, test_y = train_test_split(post_x, post_y, test_size=0.1, stratify=post_y, random_state=1)
train_x, test_x, train_y, test_y = train_test_split(crx_x, crx_y, test_size=0.1, stratify=crx_y, random_state=1)

"""# Handle Missing Values (DROP)"""

train = pd.concat([train_x, train_y], axis=1)
test = pd.concat([test_x, test_y], axis=1)

drop_train = train.dropna()
drop_test = test.dropna()

drop_train_x = drop_train.loc[:, drop_train.columns != 'Class']
drop_train_y = drop_train['Class']

drop_test_x = drop_test.loc[:, drop_test.columns != 'Class']
drop_test_y = drop_test['Class']

drop_train_x.reset_index(inplace=True)
drop_test_x.reset_index(inplace=True)

"""# Handle Missing Value (Imputation)"""

from sklearn.impute import SimpleImputer
from pandas.api.types import is_string_dtype

si_train_x = pd.DataFrame()
si_test_x = pd.DataFrame()

for col in train_x.columns:
  if (is_string_dtype(train_x[col].dtype)):
    si = SimpleImputer(strategy='most_frequent')
  else:
    si = SimpleImputer(strategy='mean')

  si.fit(train_x[[col]])
  si_train_x[col] = si.transform(train_x[[col]]).flatten()
  si_test_x[col] = si.transform(test_x[[col]]).flatten()

print(si_train_x)

"""# Convert continuous features (Binarizer)"""

from sklearn.preprocessing import Binarizer

categorical_features = ['A1', 'A4', 'A5', 'A6', 'A7', 'A9', 'A10', 'A12', 'A13']

b_drop_train_x = pd.DataFrame()
b_drop_test_x = pd.DataFrame()

b_si_train_x = pd.DataFrame()
b_si_test_x = pd.DataFrame()

for col in si_train_x.columns:
  if col not in categorical_features:
    bin = Binarizer(threshold=drop_train_x[col].mean())
    # bin.fit()
    b_drop_train_x[col] = bin.transform(drop_train_x[[col]]).flatten()
    b_drop_test_x[col] = bin.transform(drop_test_x[[col]]).flatten()

    bin = Binarizer(threshold=si_train_x[col].mean())
    # bin.fit()
    b_si_train_x[col] = bin.transform(si_train_x[[col]]).flatten()
    b_si_test_x[col] = bin.transform(si_test_x[[col]]).flatten()
  else:
    b_drop_train_x[col] = drop_train_x[col].copy()
    b_drop_test_x[col] = drop_test_x[col].copy()

    b_si_train_x[col] = si_train_x[col].copy()
    b_si_test_x[col] = si_test_x[col].copy()

print(b_si_train_x.isnull().values.any())

"""# Convert continuous features (Quantization)"""

from sklearn.preprocessing import KBinsDiscretizer

categorical_features = ['A1', 'A4', 'A5', 'A6', 'A7', 'A9', 'A10', 'A12', 'A13']

q_drop_train_x = pd.DataFrame()
q_drop_test_x = pd.DataFrame()

q_si_train_x = pd.DataFrame()
q_si_test_x = pd.DataFrame()

for col in si_train_x.columns:
  if col not in categorical_features:
    bin = KBinsDiscretizer(n_bins=5, encode='ordinal', strategy='uniform')
    bin.fit(drop_train_x[[col]])
    q_drop_train_x[col] = bin.transform(drop_train_x[[col]]).flatten()
    q_drop_test_x[col] = bin.transform(drop_test_x[[col]]).flatten()

    bin = Binarizer(threshold=si_train_x[col].mean())
    bin.fit(si_train_x[[col]])
    q_si_train_x[col] = bin.transform(si_train_x[[col]]).flatten()
    q_si_test_x[col] = bin.transform(si_test_x[[col]]).flatten()
  else:
    q_drop_train_x[col] = drop_train_x[col].copy()
    q_drop_test_x[col] = drop_test_x[col].copy()

    q_si_train_x[col] = si_train_x[col].copy()
    q_si_test_x[col] = si_test_x[col].copy()
  
print(q_si_train_x.isnull().values.any())
print(q_drop_train_x)
print(q_si_train_x)

"""# Handle Text Features """

from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
le.fit(train_y)
train_y = le.transform(train_y)
test_y = le.transform(test_y)

le.fit(drop_train_y)
drop_train_y = le.transform(drop_train_y)
drop_test_y = le.transform(drop_test_y)

categorical_features = ['A1', 'A4', 'A5', 'A6', 'A7', 'A9', 'A10', 'A12', 'A13']

print(b_drop_train_x)

l_b_drop_train_x = pd.DataFrame()
l_b_drop_test_x = pd.DataFrame()

l_b_si_train_x = pd.DataFrame()
l_b_si_test_x = pd.DataFrame()

l_q_drop_train_x = pd.DataFrame()
l_q_drop_test_x = pd.DataFrame()

l_q_si_train_x = pd.DataFrame()
l_q_si_test_x = pd.DataFrame()

for col in train_x.columns:
  if col in categorical_features:
    le.fit(b_drop_train_x[col])
    l_b_drop_train_x[col] = le.transform(b_drop_train_x[col])
    l_b_drop_test_x[col] = le.transform(b_drop_test_x[col])

    le.fit(q_drop_train_x[col])
    l_q_drop_train_x[col] = le.transform(q_drop_train_x[col])
    l_q_drop_test_x[col] = le.transform(q_drop_test_x[col])

    le.fit(b_si_train_x[col])
    l_b_si_train_x[col] = le.transform(b_si_train_x[col])
    l_b_si_test_x[col] = le.transform(b_si_test_x[col])

    le.fit(q_si_train_x[col])
    l_q_si_train_x[col] = le.transform(q_si_train_x[col])
    l_q_si_test_x[col] = le.transform(q_si_test_x[col])

  else:
    l_q_drop_train_x[col] = q_drop_train_x[col].copy()
    l_q_drop_test_x[col] = q_drop_test_x[col].copy()

    l_q_si_train_x[col] = q_si_train_x[col].copy()
    l_q_si_test_x[col] = q_si_test_x[col].copy()

    l_b_drop_train_x[col] = b_drop_train_x[col].copy()
    l_b_drop_test_x[col] = b_drop_test_x[col].copy()

    l_b_si_train_x[col] = b_si_train_x[col].copy()
    l_b_si_test_x[col] = b_si_test_x[col].copy()

print(l_b_si_train_x.isnull().values.any())
print(l_q_si_train_x.isnull().values.any())
print(l_b_drop_train_x.isnull().values.any())
print(l_q_drop_train_x.isnull().values.any())

"""# Train using Decision Tree, Random Forest"""

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

rf1 = RandomForestClassifier(n_estimators=1000, n_jobs=-1, verbose=0)
rf2 = RandomForestClassifier(n_estimators=1000, n_jobs=-1, verbose=0)
rf3 = RandomForestClassifier(n_estimators=1000, n_jobs=-1, verbose=0)
rf4 = RandomForestClassifier(n_estimators=1000, n_jobs=-1, verbose=0)

rf1.fit(l_b_drop_train_x, drop_train_y)
rf2.fit(l_b_si_train_x, train_y)
rf3.fit(l_q_drop_train_x, drop_train_y)
rf4.fit(l_q_si_train_x, train_y)

"""# Prediction"""

from sklearn.metrics import accuracy_score

p1 = rf1.predict(l_b_drop_test_x)
p2 = rf2.predict(l_b_si_test_x)
p3 = rf3.predict(l_q_drop_test_x)
p4 = rf4.predict(l_q_si_test_x)

a1 = accuracy_score(drop_test_y, p1)
a2 = accuracy_score(test_y, p2)
a3 = accuracy_score(drop_test_y, p3)
a4 = accuracy_score(test_y, p4)

print(a1, a2, a3, a4)

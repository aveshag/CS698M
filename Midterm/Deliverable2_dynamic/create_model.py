
# creating model from training data

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import BaggingClassifier
import pickle

tr_data = pd.read_csv('data_train.csv')
feature_name = list(tr_data.columns.values)

train_data = tr_data.values
X_train = train_data[:,1:]
y_train = train_data[:,0]

# print(feature_name)

print('Dimensions of the Train Data:',train_data.shape)



# Create the model with 100 trees

# model = BaggingClassifier(n_estimators = 100)  1

# model = GradientBoostingClassifier(n_estimators = 100) 1

# model = AdaBoostClassifier(n_estimators = 100,   1
#                            learning_rate = 1) 

# model = DecisionTreeClassifier()      1

model = RandomForestClassifier(n_estimators = 100, 
                               criterion = 'gini',
                               bootstrap = True,
                               max_features = 'sqrt')
# Fit on training data
model.fit(X_train, y_train)

filename = 'model.sav'
pickle.dump(model, open(filename, 'wb'))





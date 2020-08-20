
# creating model for testing

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

# model = BaggingClassifier(n_estimators = 100)    0.9838457529963522

# model = GradientBoostingClassifier(n_estimators = 100)   0.9729025534132361

# model = AdaBoostClassifier(n_estimators = 100,
#                            learning_rate = 1)      0.9609171443460135

# model = DecisionTreeClassifier()   0.9765502866076081

# 0.986451276706618
model = RandomForestClassifier(n_estimators = 100, 
                               criterion = 'gini',
                               bootstrap = True,
                               max_features = 'sqrt')
# Fit on training data
model.fit(X_train, y_train)

filename = 'model.sav'
pickle.dump(model, open(filename, 'wb'))





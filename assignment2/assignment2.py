# Aaron Yerke, HW 2 for ML 2019
# 1. (50 points) Implement gradient descent-based logistic regression in Python. Use
# ∆J = 0.00001 as the stopping criterion.
# 2. (50 points total distributed as below) Apply your code from question 2 to the iris virginica and virsicolor flowers. Specifically, randomly select 99 of these flowers for training your logistic model and use the remaining one flower for testing. You only need to do training once and testing once with your specific choice of the training flowers and testing flowers. That is to say, you don’t need to do the leave-one-out cross validation 100 times.
# (a) (15 points) After your training, plot the total cost J vs iterations for your 99 training flowers for four scenarios.
# (b) (20 points) Predict the flower type of your testing flower for each of the four scenarios.
# (c) (15 points) Apply sklearn.linear model.LogisticRegression to your specific choice of training flowers. With the intercept and coefficients produced by sklearn, calculate the total final cost J for your 99 flowers.

# --------------------------------------------------------------------------
# Import external libraries
# --------------------------------------------------------------------------
# for my code
import os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import chain
# for comparison
import scipy.stats as stats
from sklearn import linear_model
# for dataset
from sklearn.datasets import load_iris
from sklearn import preprocessing

# --------------------------------------------------------------------------
# Some useful functions
# --------------------------------------------------------------------------
def logit(p):
    return np.log(p/(1-p))

def sigmoid(line):
    return 1/(1 + np.exp(-line))

def loss_j(y,y_hat):
#    total_cost = 0
#    for row in range(X.shape[0]):
##        print(f"coef.T: {coef.T}, np.array(X.iloc[row,]): {np.array(X.iloc[row,])}")
#        term = np.log(sigmoid((np.dot( coef.T, np.array(X.iloc[row,])))))
#        total_cost += y.iloc[row,] * term + (1-y.iloc[row,] * (term))
#    return - total_cost/X.shape[0]
#    return 1/len(y) * np.sum((y @ np.log(sigmoid(X@coef)) - (1-y) @ np.log(1-sigmoid(X@coef)) ))
    return -np.mean(y*np.log(y_hat) + (1-y) * np.log(1-y_hat))

# --------------------------------------------------------------------------
# set up log reg class
# --------------------------------------------------------------------------
class my_logistic_reg:
    def __init__(self, lr = 0.001, n_iter = 1000, dj_stop = 0.0001):
        self.slopes = None
        self.y_intercept = None
        self.lr = lr
        self.n_iter = n_iter
        self.dj_stop = dj_stop

    def fit_model(self, my_x, my_y):
        n_samples, n_features = my_x.shape
        # init parameters
        self.slopes = np.zeros(n_features)
        self.y_intercept = 1
        #stop the grad descent ∆J = 0.00001
#        d_slope = np.ones(n_features)
#        di = 1
        self.cost_j = []
        
        print(f'{self.dj_stop} and {self.dj_stop} {len(self.cost_j)} {self.n_iter}')

        # gradient descent   
        while len(self.cost_j) < self.n_iter:#this is basically a for-loop that will go n iterations
            # approximate y with linear combination of slope and x, plus y_intercept
            lin_model = np.dot(my_x, self.slopes) + self.y_intercept
            # apply sigmoid function
            y_predicted = sigmoid(lin_model)
            loss = loss_j(my_y, y_predicted)          
            # compute gradients
            dz = y_predicted -my_y
            d_slope = (1 / n_samples) * np.matmul(my_x.T, dz)
            d_intercept = np.sum(dz)
            
            # update parameters
            print(f"slopes1: {self.slopes}")
            self.slopes -= self.lr * d_slope
            print(f"slopes2: {self.slopes}")
            self.y_intercept -= self.lr * d_intercept
            print(f"in iters {len(self.cost_j)}")
            if len(self.cost_j) == 0:
                self.cost_j.append(loss)
                print("in iffffffffffffffffffffffffffffffffff")
            else:
                self.cost_j.append(loss)
                print(f"difffffffff: {loss - self.cost_j[-2]}")
                if abs(loss - self.cost_j[-2]) < self.dj_stop:
                    print(f'done with while iters:{len(self.cost_j)}')
#                    print(self.slopes)
#                    print(self.y_intercept)
#                    print(len(self.cost_j))
#                    print(self.cost_j)
                    break#get out of while loop
        print(self.cost_j)
                
    def test_model(self):
        pass
    
    def plot_cost(self):
        pass
    
    def _grad_des(self):
        pass
# --------------------------------------------------------------------------
# create training and testingdatasets
# --------------------------------------------------------------------------
iris = load_iris()
df = pd.DataFrame(iris.data, columns = iris['feature_names'])
df['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)
df = df[df.species != "setosa"]
df = df.reset_index(drop = True)
df['species'] = df['species'].map({'versicolor': 1, 'virginica': 0})
df.to_csv('testing.tsv', sep='\t')
#print(df.shape[0])

df_x = df.iloc[:,list(range(df.shape[1]-1))]
#normalize data to max value
x = df_x.values #returns a numpy array
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
df_x = pd.DataFrame(x_scaled)
print(f'df_x.shape: {df_x.shape}')
df_y = df.iloc[:,df.shape[1]-1]
print(f'df_y.shape: {df_y.shape}')

test_index = np.random.randint(low = 0, high = df.shape[0] - 1, size = 1 )[0]
print(test_index)
train_index = filter(lambda a: a != test_index, range(df.shape[0]))
print(train_index)

train_x = df_x.drop(test_index, axis = 0)
print(f'train_x.shape: {train_x.shape}')
train_y = df_y.drop(test_index, axis = 0)
print(f'train_y.shape: {train_y.shape}')
test_x = df_x.drop(train_index, axis = 0)
print(f'test_x.shape: {test_x.shape}')
test_y = df_y.drop(filter(lambda a: a != test_index, range(df.shape[0])), axis = 0)
print(f'test_y.shape: {test_y.shape}')

# --------------------------------------------------------------------------
# main method
# --------------------------------------------------------------------------

my_lr = my_logistic_reg()
my_lr.fit_model(train_x, train_y)


# --------------------------------------------------------------------------
# run professional log reg model
# --------------------------------------------------------------------------
#print('pro_stuff')
#skl_log = linear_model.LogisticRegression(solver="lbfgs")
#skl_log.fit(X=train_x, y=train_y)
#skl_pred = skl_log.predict(test_x)
#print(f'sklearn log rediction: {skl_pred}')
#print(f'Correct answer: {test_y}, {test_y == skl_pred}')
#print(skl_log.coef_)
#print(skl_log.intercept_)
#skl_log_cost = loss_j(train_x, train_y, skl_log.coef_)
#print(f'2(c) the total final cost J: {skl_log_cost}')
   

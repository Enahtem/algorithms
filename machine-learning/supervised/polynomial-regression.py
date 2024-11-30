###Imports
import math
import random
import numpy as np

###Constants
#Initial Input
x0 = 0
#Final Input
xN = 1
#Number Inputs
N = 101
#Function
def y(x):
    return np.sin(x)
#Output Scaling Uncertainty
d=0.05


###Data Generation
#Generating Input Array
x=np.linspace(x0,xN,N);

#Generating Output Array
t=y(x)+np.random.normal(0,d,size=x.shape)

#Initial and Final Model Orders
Mi=1
Mf=20

best_M = float('-inf')
min_AIC = float('inf')

for M in range(Mi,Mf+1):
    #Model Order
    print("Model Order: ",M)
    
    ###Model Training

    #Frequentist Method: Maximum Likelihood
    #Linear Algebra Least Squares
    #Vandermonde Matrix
    A = np.zeros((len(x), M+1))
    for i in range(M+1):
        A[:,i]=x**i

    #Calculating Maximum Likelihood Polynomial Weights
    #Maximum Likelihood Weights
    w_ml = np.dot(np.linalg.inv(np.dot(np.transpose(A),A)),np.dot(np.transpose(A),t))
    print(w_ml)

    #Partial Bayesian Method: Maximum Posterior
    # Linear Algebra Ridge Regression
    #Points Precision
    alpha = 20
    #Weights Precision
    beta = 100
    # Regularization Parameter
    lambda_reg = alpha/beta
    # Posterior Covariance Matrix
    S = np.linalg.inv(beta*np.dot(np.transpose(A),A)+alpha*np.identity(M+1))
    #Maximum Posterior Weights
    w_map = beta*np.dot(S, np.dot(np.transpose(A),t))

    print(w_map)
    #Complete Bayesian Method

    x_new = 0.5
    phi=np.array([x_new**i for i in range(M+1)])
    mean = np.dot(np.transpose(phi), w_map)
    variance = 1/beta + np.dot(np.transpose(phi), np.dot(S,phi))
    print(mean)
    print(variance)

    ###Model Selection
    #Cross Validation
    #Akaike Information Criterion
    AIC = -1*beta/2*np.linalg.norm(np.dot(A, w_ml)-t)+N/2*np.log(beta/(2*np.pi))-M
    print("AIC: ",AIC)
    if AIC<min_AIC:
        min_AIC = AIC
        best_M = M

print(best_M)

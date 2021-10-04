#! /usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min




s = np.load("scan.npy")
a = np.load("angles.npy")
s = s.flatten()
a = a.flatten()

#print(x.shape,y.shape)
xy = np.array([a,s])

xy = xy.reshape(141,2)
mms = MinMaxScaler()
mms.fit(xy)

data = mms.transform(xy)

#s = []


km = KMeans(n_clusters=2,max_iter=500)
km = km.fit(xy)



c = km.cluster_centers_
closest,temp = pairwise_distances_argmin_min(c,xy)

print(closest, temp,xy[closest,:])

plt.scatter(a,s)
plt.scatter(c[:,0],c[:,1],c='k')
plt.show()




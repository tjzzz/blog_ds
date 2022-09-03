
基于实例的学习，其学习的不是明确的泛化模型，而是样本之间的关系。

k近邻方法：先找到与未知样本最接近的k个实例，再根据少数服从多数的准则，给未知样本打上标签。

* 超参数k
* 距离度量
* 高维灾难


k近邻方法和传统的参数方法不同，参数模型在求得参数后，任务就完成了。新来了一个样本后直接拿训练好的参数进行预测即可；而k近邻不同，它需要将数据存储下来，每来了一个新样本后，要计算离他最近的k个实例。

sklearn中`sklearn.neighbors`模块

应用

* 无监督的`NearestNeighbors `

具体计算的时候可以选择不同的计算方法，'algorithm' =['auto', 'ball_tree', 

* 有监督的

KNeighborsClassifier: 可以指定参数k
RadiusNeighborsClassifier: 可以指定查询的固定半径r

```python
## 官网的示例demo
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn import neighbors, datasets

n_neighbors = 15

# import some data to play with
iris = datasets.load_iris()

# we only take the first two features. We could avoid this ugly
# slicing by using a two-dim dataset
X = iris.data[:, :2]
y = iris.target

h = .02  # step size in the mesh

# Create color maps
cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF'])
cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])

for weights in ['uniform', 'distance']:
    # we create an instance of Neighbours Classifier and fit the data.
    clf = neighbors.KNeighborsClassifier(n_neighbors, weights=weights)
    clf.fit(X, y)

    # Plot the decision boundary. For that, we will assign a color to each
    # point in the mesh [x_min, x_max]x[y_min, y_max].
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.figure()
    plt.pcolormesh(xx, yy, Z, cmap=cmap_light)

    # Plot also the training points
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=cmap_bold,
                edgecolor='k', s=20)
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.title("3-Class classification (k = %i, weights = '%s')"
              % (n_neighbors, weights))

plt.show()
```





最近邻回归
KNeighborsRegressor
RadiusNeighborsRegressor



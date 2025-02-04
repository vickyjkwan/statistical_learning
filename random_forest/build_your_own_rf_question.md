## Build a Random Forest

You will be using our implementation of Decision Trees to implement a Random Forest.

You can use the `DecisionTree` class from `DecisionTree.py` with the following code:

```python
dt = DecisionTree()
dt.fit(X_train, y_train)
predicted_y = dt.predict(X_test)
```

You can also visualize a Decision Tree by printing it. This may be helpful for understanding your Random Forest.

```python
print dt
```

While you're getting your code to work, use the play golf data set that we used for implementing Decision Trees.

There's a file called `RandomForest.py` which contains a skeleton of the code. Your goal is to fill it in so that you can run it with the following lines of code:

```python
from RandomForest import RandomForest
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd

df = pd.read_csv('data/playgolf.csv')
y = df.pop('Result').values
X = df.values
X_train, X_test, y_train, y_test = train_test_split(X, y)

rf = RandomForest(num_trees=10, num_features=2)
rf.fit(X_train, y_train)
y_predict = rf.predict(X_test)
print "score:", rf.score(X_test, y_test)
```

### A. Implement *Tree Bagging*

Bagging, or *bootstrap aggregating*, is taking several random samples *with replacement* from the data set and building a model for each sample. Each of these models gets a vote on the prediction.

Sampling with replacement means that we can repeat data points. In the basic random forest, we will always use a sample size that is the same as the size of the original data set. Many data points will not be included in each sample and many will be repeated.

1. Implement the `build_forest` method. For right now, we will be ignoring the `num_features` parameter. Here is the pseudocode:

	    Repeat num_trees times:
	        Create a random sample of the data with replacement
	        Build a decision tree with that sample
	    Return the list of the decision trees created


### B. Implement random feature selection

For random forests, we need to modify our decision trees a little bit. At each node, they need to randomly choose a subset of the features to use.

1. Modify the `DecisionTree` class so that it takes an additional parameter: `num_features`. This is the number of features to consider at each node in choosing the best split. Which features to consider is randomly chosen at each node. You will need to modify the `__init__`, method to take a `num_features` parameter. In `_choose_split_index`, you should randomly select `num_features` of the potential features to consider. Only calculate and compare the features that were randomly chosen, so that the feature you choose is one of the randomly chosen features.

2. Modify `build_forest` in your `RandomForest` class to pass the `num_features` parameter to the Decision Trees.


### C. Implement classification and scoring

1. In the `predict` method, you should have each Decision Tree classify each data point. Choose the label with the majority of trees. Break ties by choosing one of the labels arbitrarily.

2. In the `score` method, you should first classify the data points and count the percent of them which match the given labels.


### D. Try a bigger data set

You won't be able to get great results cross validating with the play golf data set since it's so small. In the data folder, there's a dataset called 'congressional_voting.csv'. This contains congressman, how they voted on different issues and their party.

Here are what the 17 columns refer to:

* Class Name: 2 (democrat, republican)
* handicapped-infants: 2 (y,n)
* water-project-cost-sharing: 2 (y,n)
* adoption-of-the-budget-resolution: 2 (y,n)
* physician-fee-freeze: 2 (y,n)
* el-salvador-aid: 2 (y,n)
* religious-groups-in-schools: 2 (y,n)
* anti-satellite-test-ban: 2 (y,n)
* aid-to-nicaraguan-contras: 2 (y,n)
* mx-missile: 2 (y,n)
* immigration: 2 (y,n)
* synfuels-corporation-cutback: 2 (y,n)
* education-spending: 2 (y,n)
* superfund-right-to-sue: 2 (y,n)
* crime: 2 (y,n)
* duty-free-exports: 2 (y,n)
* export-administration-act-south-africa: 2 (y,n)

The dataset came from UCI [here](https://archive.ics.uci.edu/ml/datasets/Congressional+Voting+Records).

1. Based on the votes on the 16 issues, predict the party using your implementation of Random Forest. Start with 10 trees and a maximum of 5 features.

2. Compare how well the Random Forest does versus the Decision Tree.

3. Try modifying the number of trees and see how it affects your accuracy.

4. Calculate the accuracy for each of your decision trees on the test set and compare it to the accuracy of the random forest on the test set.

5. Predict how the congressmen will vote on a particular issue given the remaining columns.


### Extra Credit: out-of-bag error and feature importance

1. Out-of-bag error is a clever way of validating your model by testing individual trees based on samples that weren't including in their training set. It is described in [Applied Data Science](http://columbia-applied-data-science.github.io/appdatasci.pdf) (9.4.3) and [Breiman's notes](http://www.stat.berkeley.edu/~breiman/RandomForests/cc_home.htm#ooberr).

2. Feature importance is a way of determining which features contribute the most to being able to predict the result. It is discussed in [Breiman's notes](http://www.stat.berkeley.edu/~breiman/RandomForests/cc_home.htm#varimp). You can compare what features you get with Breiman's method vs [sklearn](http://scikit-learn.org/stable/modules/ensemble.html#feature-importance-evaluation).

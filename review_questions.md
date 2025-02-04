# Cross Validation

- explain train/test splits:
  - Fitting our model to a given dataset is not enough. We would also like to know the predictive power of our model. To save time and money, we could reserve a smaller portion of our dataset for testing purposes. We then use the training portion as we desire to look for an optimal model, followed by testing our model on the testing portion. This split among the dataset is called a train/test split.
- explain how to get an honest sense of how well a model is doing
  - The predictive accuracy among other metrics shows how well a model is doing in terms of predicting some outcomes based on our hypotheses and selected features. We usually test this accuracy by fitting our model to the test dataset, and calculate a chosen error. Oftentimes, errors can be calculated using mean squared errors.
- state the purposes of Cross Validation
  - To re-use our data when the situation is not 'data-rich', cross validation provides us with a more efficient way of fitting model to the data that's available to us, compared with the traditional one split between training and testing data. Cross validation requires us to partition our datasets into k parts (called k-fold), then train-test our models with iterations. At each iteration, we train on the (k-1) parts of our data, and test it on the remaining part. Each of the k folds is used exactly once, thus providing a robust testing environment for our model.
- explain k in “k-fold cross validation”
  - See above.
- describe the sources of model error
  - There are two sources of model error: 1) from inevitable external noises, 2) from systematic errors of our model.
- describe overfitting and underfitting
  - When a model has been trained for too many times or its complexity is too high, overfitting happens. In this case, the model can very well predict the training data, but when applied to testing data, it's expected to deviate/have large variances from the true results. The degrees that model fits very closely to the training set is called a low bias, while the large variances of the testing data is called high variance. This is a bias-variance trade-off. Underfitting is the reverse.
- explain how to compare models and select the best one


# Regularization

- explain ridge regression and lasso regression:
  - Ridge regression and lasso regression both minimizes the model rss while penalizing the magnitudes of coefficients. Ridge regression takes an L2-norm on the beta coefficients while lasso takes L1-norm. Ridge regression works well for preventing overfitting. It takes all features in thus not computationally cheap for datasets with features of millions or more. Lasso regression works for cases in which features are of millions and we are looking for a sparse solution. This has a computational advantage over ridge regression.
- tune the bias/variance of a regression model:
  - We would try to eliminate some of the beta coefficients which are very much close to zero. This means that the variables associated with these coefficients are of little predicting power to our responses. We can reduce our model complexity in this way to avoid a large variance from our model, thus avoiding overfitting.
- choose the best regularization hyper-parameter for regression:

# Boosting
- What is boosting technique?
  - Boosting is an ensemble technique with which we can start our model predictions with a set of weak learners, whose predictions are only a little better than random guesses. These weak learns have high biases and low variances. After training iterations, we will arrive at a strong learner whose predictions are arbitrarily close to the real responses. This process is expected to reduce bias and variance in supervised learning.
- Boosting for regression problems (GradientBoosting Regressor):
  - Gradient boosting is an gradient descent algorithm with boosting technique. Gradient tree boosting utilizes decision trees as its weak learners. In the regression cases, the weak learners were fitted to data with minimized MSE (mean squared error). Each of the following weak learns 'learns' a better model by correcting its predecessor's MSE.
- Boosting for classification problems (GradientBoostingClassifier)
  - In the case of classification problems, instead of MSE, we can test models for metrics including precision, recall, accuracy, f1 score, etc.
- Difference between AdaBoost and Gradient Boosting
  - They both use weak learners to arrive at a strong learner by aggregating (addition). They differ at the iterative process where the weak learners are created. Adaboost creates weak learners by changing the weights attached to each instance. By increasing the weights of wrong predictions (difficult ones) and decreasing the weights of correct predictions (easy ones), Adaboost aggregate weak learners by their (contribution) votes to the strong learner. If a weak learner has strong performance (a high alpha-weight), it has more contribution to the strong learner. These updated weights indicates a changing sample distribution.
  - During the gradient boosting iterative process, instead of changing sample distribution, the weak learners are trained on the remaining errors (pseudo-residuals) of the strong learner. The weak learners' contributions are not evaluated on its performance on the sample distribution, but by using the gradient descent optimization process. The final outcome is the one minimizing the overall error of the strong learner.
- Understand hyperparameters associated to Boosting
  (learning rate, number of estimators ...)
- GridSearch for optimal hyperparameters for Boosting:
- Performance of Boosting compared to other machine learning algorithms
- Difference between gradient boosting and random forest:
  1. Gradient boosting is a sequential algorithm while random forest grows trees parallel. In random forests each tree is growing independently. To achieve high accucary, RF uses BAGGING (bootstrap aggregating) but is prone to overfitting.
    - BAGGING: drawing sample from training data uniformly and with replacement.
  2. Gradient boosting has shallow trees as its weak learners (stumps with only 2 leaves). It reduces error by reducing bias. RF uses full grown trees with low bias and high variance. RF reduces error by reducing variance. The trees in RF are designed to be uncorrelated, thus maximizing the decrease in variance.


# Tuning hyper-parameters
- General Approach for Parameter Tuning
  - There are two types of parameter to be tuned here – tree based and boosting parameters.
    1. Choose a relatively high learning rate. Generally the default value of 0.1 works but somewhere between 0.05 to 0.2 should work for different problems
    2. Determine the optimum number of trees for this learning rate. This should range around 40-70. Remember to choose a value on which your system can work fairly fast. This is because it will be used for testing various scenarios and determining the tree parameters.
    3. Tune tree-specific parameters for decided learning rate and number of trees. Note that we can choose different parameters to define a tree and I’ll take up an example here.
    4. Lower the learning rate and increase the estimators proportionally to get more robust models.
    5. Fix learning rate and number of estimators for tuning tree-based parameters
    6. In order to decide on boosting parameters, we need to set some initial values of other parameters. Lets take the following values:
        1. min_samples_split = 500 : This should be ~0.5-1% of total values. Since this is imbalanced class problem, we’ll take a small value from the range.
        2. min_samples_leaf = 50 : Can be selected based on intuition. This is just used for preventing overfitting and again a small value because of imbalanced classes.
        3. max_depth = 8 : Should be chosen (5-8) based on the number of observations and predictors. This has 87K rows and 49 columns so lets take 8 here.
        4. max_features = ‘sqrt’ : Its a general thumb-rule to start with square root.
        5. subsample = 0.8 : This is a commonly used used start value.
  Please note that all the above are just initial estimates and will be tuned later. Lets take the default learning rate of 0.1 here and check the optimum number of trees for that. For this purpose, we can do a grid search and test out values from 20 to 80 in steps of 10.

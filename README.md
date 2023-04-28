# Match to Match Prediction

## How to run the pipeline

When training over the years `2016` to `2018` for testing on the year `2019`

1. Check that these files exist in the data folder

-   [x] aus-open-player-stats-2015.csv
-   [x] aus-open-player-stats-2016.csv
-   [x] aus-open-player-stats-2017.csv
-   [x] m2016.csv
-   [x] m2017.csv
-   [x] m2018.csv
-   [x] m2019.csv

2. Open the notebook `neural_network.ipynb` / `svm.ipynb` / `gradient_boost.ipynb`

3. Check that the `Inputs` heading contains the right parameters.

4. Run the notebook until a preview of the variable `r_16_merge` is displayed.

5. Compare it to the tournament result.

### When adding more data,

-   Download match outcome data from this [website](http://www.tennis-data.co.uk/ausopen.php)
-   If adding data for the year 2015, Save it as `m2015.csv`
-   Run the main.py as

```bash
python3 main.py --year 2014
python3 all_pressure.py --year 2014
```

-   Continue from `Step 2`

## Model used

-   Neural Network
    -   Hyperparameters
        -   activation=`logistic`
        -   solver=`adam`
        -   learning_rate=`adaptive`
        -   max_iter=`10000`
        -   warm_start=`True`
        -   hidden_layer_sizes=`(128,50,2)`
-   Support Vector Machine (linear kernel)
    -   Hyperparameters
        -   kernel=`linear`
        -   C=`0.001`
        -   max_iter=`1000000`
-   Gradient Boost
    -   Hyperparameters
        -   n_estimators=`10000`
        -   learning_rate=`0.00001`
        -   criterion=`squared_error`
        -   loss=`exponential`

## Assumptions

-   People with no stats have been considered as walkovers

## Summary

### Australian Open 2019

| Model          | Round of 16 | Round of 32 | Round of 64 |
| -------------- | ----------- | ----------- | ----------- |
| _Baseline_     | _8_         | _22_        | _43_        |
| Neural Network | **10**      | **23**      | 50          |
| SVM (Linear)   | 9           | **23**      | 50          |
| Gradient Boost | **10**      | 22          | **54**      |

### Australian Open 2018

| Model          | Round of 16 | Round of 32 | Round of 64 |
| -------------- | ----------- | ----------- | ----------- |
| _Baseline_     | _11_        | _20_        | _34_        |
| Neural Network | 6           | 17          | 40          |
| SVM (Linear)   | 5           | 20          | **46**      |
| Gradient Boost | 8           | **22**      | **46**      |

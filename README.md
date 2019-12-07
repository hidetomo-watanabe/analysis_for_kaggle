# analysis_for_kaggle
### overview
- single model
  - regression
  - classification(multilabel/multiclass)
- ensemble model

### available model
##### classification
- log_reg
  - LogisticRegression
- log_reg_cv
  - LogisticRegressionCV
- svc
  - SVC
- l_svc
  - LinearSVC
- rf_clf
  - RandomForestClassifier
- gbdt_clf
  - GradientBoostingForestClassifier
- knn_clf
  - KNeighborsClassifier
- g_nb
  - GaussianNB
- perceptron
  - Perceptron
- sgd_clf
  - SGDClasssifier
- dt_clf
  - DecisionTreeClasssifier
- xgb_clf
  - XGBClasssifier
- lgb_clf
  - LGBMClasssifier
- catb_clf
  - CatBoostClasssifier
- rgf_clf
  - RGFClasssifier
- keras_clf
  - KerasClasssifier

##### regression
- linear_reg
  - LinearRegression
- lasso
  - Lasso
- ridge
  - Ridge
- svr
  - SVR
- l_svr
  - LinearSVR
- rf_reg
  - RandomForestRegressor
- gbdt_reg
  - GradientBoostingForestRegressor
- knn_reg
  - KNeighborsRegressor
- sgd_reg
  - SGDRegressor
- dt_reg
  - DecisionTreeRegressor
- xgb_reg
  - XGBRegressor
- lgb_reg
  - LGBMRegressor
- catb_reg
  - CatBoostRegressor
- rgf_reg
  - RGFRegressor
- keras_reg
  - KerasRegressor

### CUI flow
- cp analysis_for_kaggle/configs/config.json.org configs/config.json
- **update config.json**
- python analysis_for_kaggle/predict.py

### environment
- https://github.com/hidetomo-watanabe/analysis_dockerfiles

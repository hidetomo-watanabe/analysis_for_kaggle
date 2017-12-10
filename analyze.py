import sys
import math
import json
import configparser
import myfuncs
import numpy as np
import pandas as pd
from IPython.display import display
from subprocess import check_output
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import Perceptron
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier
"""
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline
"""


def get_base_model(modelname):
    if modelname == 'log_reg':
        return LogisticRegression()
    elif modelname == 'svc':
        return SVC()
    elif modelname == 'l_svc':
        return LinearSVC()
    elif modelname == 'rf_clf':
        return RandomForestClassifier()
    elif modelname == 'gbdt_clf':
        return GradientBoostingClassifier()
    elif modelname == 'knn_clf':
        return KNeighborsClassifier()
    elif modelname == 'g_nb':
        return GaussianNB()
    elif modelname == 'preceptron':
        return Perceptron()
    elif modelname == 'sgd_clf':
        return SGDClassifier()
    elif modelname == 'dt_clf':
        return DecisionTreeClassifier()


def display_dfs(dfs):
    for df in dfs:
        display(df.head())
        display(df.describe())


def replace_dfs(dfs, target, config, *, mean=None):
    """
        config is dict
    """
    output = []
    for df in dfs:
        for i, value1 in enumerate(df[target].values):
            for key, value2 in config.items():
                # mean
                if value2 == 'mean':
                    value2 = mean
                # translate
                if key == 'isnan':
                    if math.isnan(value1):
                        df[target].values[i] = value2
                else:
                    if value1 == key:
                        df[target].values[i] = value2
        output.append(df)
    return output


def categorize_dfs(dfs, target, config):
    """
        config is list
    """
    output = []
    for df in dfs:
        for value2 in config:
            df['%s_%s' % (target, value2)] = [0] * len(df[target].values)
        for i, value1 in enumerate(df[target].values):
            for value2 in config:
                if value1 == value2:
                    df['%s_%s' % (target, value2)].values[i] = 1
        del df[target]
        output.append(df)
    return output


def to_float_dfs(dfs, pred_col, id_col):
    output = []
    for df in dfs:
        for key in df.keys():
            if key == pred_col or key == id_col:
                continue
            df[key] = df[key].astype(float)
        output.append(df)
    return output

if __name__ == '__main__':
    # input
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    else:
        config_path = './config.ini'

    # definition
    cp = configparser.SafeConfigParser()
    cp.read(config_path)
    # data
    data_path = cp.get('data', 'path')
    pred_col = cp.get('data', 'pred_col')
    id_col = cp.get('data', 'id_col')
    adversarial = cp.get('data', 'adversarial')
    if adversarial:
        adversarial = json.loads(adversarial)
    # model
    base_model = get_base_model(cp.get('model', 'base'))
    scoring = cp.get('model', 'scoring')
    cv = cp.getint('model', 'cv')
    params = json.loads(cp.get('model', 'params'))
    # traslate
    trans_adhoc = json.loads(cp.get('translate', 'adhoc'))
    trans_replace = json.loads(cp.get('translate', 'replace'))
    trans_del = json.loads(cp.get('translate', 'del'))
    trans_category = json.loads(cp.get('translate', 'category'))

    # data list
    print('### DATA LIST')
    print(check_output(['ls', data_path]).decode('utf8'))
    train_df = pd.read_csv('%s/train.csv' % data_path)
    test_df = pd.read_csv('%s/test.csv' % data_path)

    # init overview
    print('### INIT OVERVIEW')
    display_dfs([train_df, test_df])

    # data translation
    # replace
    for key, value in trans_replace.items():
        # mean
        if train_df.dtypes[key] == 'object':
            key_mean = None
        else:
            key_mean = train_df[key].mean()
        train_df, test_df = replace_dfs(
            [train_df, test_df], key, value, mean=key_mean)
    # adhoc
    for value in trans_adhoc:
        train_df, test_df = eval(
            'myfuncs.%s' % value)([train_df, test_df], train_df)
    # category
    for key, values in trans_category.items():
        train_df, test_df = categorize_dfs([train_df, test_df], key, values)
    # del
    for value in trans_del:
        del train_df[value]
        del test_df[value]
    # float
    train_df, test_df = to_float_dfs([train_df, test_df], pred_col, id_col)

    # translation overview
    print('### TRANSLATION OVERVIEW')
    display_dfs([train_df, test_df])

    """
    # simple visualization
    print('### SIMPLE VISUALIZATION')
    for key in train_df.keys():
        if key == pred_col or key == id_col:
            continue
        g = sns.FacetGrid(train_df, col=pred_col)
        g.map(plt.hist, key, bins=20)
    """

    # create ndarray
    Y_train = train_df[pred_col].values
    id_pred = test_df[id_col].values
    del train_df[pred_col]
    del train_df[id_col]
    del test_df[id_col]
    X_train = train_df.values
    X_test = test_df.values

    # translate ndarray to standard
    ss = StandardScaler()
    ss.fit(X_train)
    X_train = ss.transform(X_train)
    X_test = ss.transform(X_test)

    # data validation
    def _get_adversarial_score(train_num, X_train, X_test, adversarial):
        # create data
        tmp_X_train = X_train[:train_num]
        X_adv = np.concatenate((tmp_X_train, X_test), axis=0)
        target_adv = np.concatenate(
            (np.zeros(train_num), np.ones(len(X_test))), axis=0)
        # fit
        gs = GridSearchCV(
            get_base_model(adversarial['model']),
            adversarial['params'],
            cv=adversarial['cv'],
            scoring=adversarial['scoring'], n_jobs=-1)
        gs.fit(X_adv, target_adv)
        return gs.best_score_

    print('### DATA VALIDATION')
    if adversarial:
        print('with adversarial')
        data_unit = 100
        adv_scores = []
        for i in range(0, len(X_train) // data_unit):
            tmp_train_num = len(X_train) - i * 100
            adv_score = _get_adversarial_score(
                tmp_train_num, X_train, X_test, adversarial)
            print('train num: %s, adv score: %s' % (tmp_train_num, adv_score))
            adv_scores.append(adv_score)
        train_num = len(X_train) - np.argmax(adv_scores) * 100
        X_train = X_train[:train_num]
        Y_train = Y_train[:train_num]
    else:
        print('no data validation')
    print('adopted train num: %s' % len(X_train))

    # fit
    print('### FIT')
    gs = GridSearchCV(base_model, params, cv=cv, scoring=scoring, n_jobs=-1)
    gs.fit(X_train, Y_train)
    print('X train shape: %s' % str(X_train.shape))
    print('Y train shape: %s' % str(Y_train.shape))
    print('best params: %s' % gs.best_params_)
    print('best score of trained grid search: %s' % gs.best_score_)
    best_model = gs.best_estimator_
    print('best model: %s' % best_model)

    # predict and create output
    Y_pred = best_model.predict(X_test)
    f = open('outputs/tmp.csv', 'w')
    f.write('%s,%s' % (id_col, pred_col))
    for i in range(len(id_pred)):
        f.write('\n')
        f.write('%s,%s' % (id_pred[i], Y_pred[i]))
    f.close()

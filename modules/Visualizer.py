import numpy as np
from sklearn.model_selection import learning_curve
import matplotlib.pyplot as plt
import seaborn as sns
from logging import getLogger


logger = getLogger('predict').getChild('Visualizer')
try:
    from .ConfigReader import ConfigReader
except Exception:
    logger.warn('IN FOR KERNEL SCRIPT, ConfigReader import IS SKIPPED')


class Visualizer(ConfigReader):
    def __init__(self):
        self.configs = {}

    def visualize_train_raw_histgram(self, train_df):
        for key in train_df.keys():
            if key == self.id_col:
                continue
            g = sns.FacetGrid(train_df, col=self.pred_col)
            g.map(plt.hist, key, bins=20)

    def visualize_train_raw_heatmap(self, train_df):
        plt.figure(figsize=(10, 10))
        sns.heatmap(
            train_df.drop(self.id_col, axis=1).corr(),
            fmt="1.2f", annot=True, lw=0.7, cmap='YlGnBu')

    def visualize_learning_curve(
        self, title, estimator, X_train, Y_train, scorer, cv, n_jobs=-1
    ):
        ylim = (0.7, 1.01)
        train_sizes = np.linspace(.1, 1.0, 5)

        plt.figure()
        plt.title(title)
        plt.ylim(*ylim)
        plt.xlabel("Training examples")
        plt.ylabel("Score")
        train_sizes, train_scores, test_scores = learning_curve(
            estimator, X_train, Y_train, scoring=scorer,
            cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
        train_scores_mean = np.mean(train_scores, axis=1)
        train_scores_std = np.std(train_scores, axis=1)
        test_scores_mean = np.mean(test_scores, axis=1)
        test_scores_std = np.std(test_scores, axis=1)
        plt.grid()

        plt.fill_between(
            train_sizes, train_scores_mean - train_scores_std,
            train_scores_mean + train_scores_std, alpha=0.1,
            color="r")
        plt.fill_between(
            train_sizes, test_scores_mean - test_scores_std,
            test_scores_mean + test_scores_std, alpha=0.1, color="g")
        plt.plot(
            train_sizes, train_scores_mean, 'o-', color="r",
            label="Training score")
        plt.plot(
            train_sizes, test_scores_mean, 'o-', color="g",
            label="Cross-validation score")

        plt.legend(loc="best")
        return plt

    def visualize_y_train_pred_data(self, Y_train, Y_train_pred):
        g = sns.jointplot(Y_train, Y_train_pred, kind='kde')
        g.set_axis_labels('Y_train', 'Y_train_pred')
        g.fig.suptitle('estimator')

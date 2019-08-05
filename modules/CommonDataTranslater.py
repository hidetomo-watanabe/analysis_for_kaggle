import os
import pandas as pd
from IPython.display import display
from logging import getLogger

logger = getLogger('predict').getChild('CommonDataTranslater')
try:
    from .ConfigReader import ConfigReader
except ImportError:
    logger.warn('IN FOR KERNEL SCRIPT, ConfigReader import IS SKIPPED')


class CommonDataTranslater(ConfigReader):
    def __init__(self, kernel=False):
        self.kernel = kernel
        self.BASE_PATH = '%s/..' % os.path.dirname(os.path.abspath(__file__))
        if self.kernel:
            self.OUTPUT_PATH = '.'
        else:
            self.OUTPUT_PATH = '%s/outputs' % self.BASE_PATH
        self.configs = {}

    def display_data(self):
        if self.configs['pre']['train_mode'] == 'clf':
            logger.info('train pred counts')
            for pred_col in self.pred_cols:
                logger.info('%s:' % pred_col)
                if pred_col not in self.train_df.columns:
                    logger.warn('NOT %s IN TRAIN DF' % pred_col)
                    continue
                display(self.train_df[pred_col].value_counts())
                display(self.train_df[pred_col].value_counts(normalize=True))
        elif self.configs['pre']['train_mode'] == 'reg':
            logger.info('train pred mean, std')
            for pred_col in self.pred_cols:
                logger.info('%s:' % pred_col)
                display('mean: %f' % self.train_df[pred_col].mean())
                display('std: %f' % self.train_df[pred_col].std())
        else:
            logger.error('TRAIN MODE SHOULD BE clf OR reg')
            raise Exception('NOT IMPLEMENTED')
        for label, df in [('train', self.train_df), ('test', self.test_df)]:
            logger.info('%s:' % label)
            display(df.head())
            display(df.describe(include='all'))
        return

    def get_data_for_view(self):
        output = {
            'train_df': self.train_df,
            'test_df': self.test_df,
        }
        return output

    def create_data_for_view(self):
        train_path = self.configs['data']['train_path']
        test_path = self.configs['data']['test_path']
        delim = self.configs['data'].get('delimiter')
        if delim:
            self.train_df = pd.read_csv(train_path, delimiter=delim)
            self.test_df = pd.read_csv(test_path, delimiter=delim)
        else:
            self.train_df = pd.read_csv(train_path)
            self.test_df = pd.read_csv(test_path)
        return

    def get_data_for_model(self):
        output = {
            'feature_columns': self.feature_columns,
            'test_ids': self.test_ids,
            'X_train': self.X_train,
            'Y_train': self.Y_train,
            'X_test': self.X_test,
        }
        return output

    def get_pre_processers(self):
        output = {}
        if hasattr(self, 'x_scaler'):
            output['x_scaler'] = self.x_scaler
        if hasattr(self, 'y_scaler'):
            output['y_scaler'] = self.y_scaler
        if hasattr(self, 'dimension_model'):
            output['dimension_model'] = self.dimension_model
        return output

    def get_post_processers(self):
        output = {}
        if hasattr(self, 'y_scaler'):
            output['y_scaler'] = self.y_scaler
        return output
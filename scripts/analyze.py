import sys
import os
import traceback
BASE_PATH = '%s/..' % os.path.dirname(os.path.abspath(__file__))
sys.path.append('%s/modules' % BASE_PATH)
from Analyzer import Analyzer
from Notifier import Notifier

if __name__ == '__main__':
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    else:
        config_path = '%s/scripts/config.json' % BASE_PATH
    try:
        analyzer_obj = Analyzer()
        analyzer_obj.read_config_file(config_path)

        print('### INIT')
        analyzer_obj.get_raw_data()
        analyzer_obj.display_data()
        print('')

        print('### TRANSLATE')
        analyzer_obj.trans_raw_data()
        analyzer_obj.display_data()
        print('')

        # print('### VISUALIZE TRAIN DATA')
        # analyzer_obj.visualize_train_data()
        # print('')

        print('### NORMALIZE')
        analyzer_obj.get_fitting_data()
        analyzer_obj.normalize_fitting_data()
        print('')

        print('### VALIDATE')
        analyzer_obj.is_ok_with_adversarial_validation()
        print('')

        print('### FIT')
        analyzer_obj.calc_best_model('tmp.pickle')

        # print('### VISUALIZE TRAIN PRED DATA')
        # analyzer_obj.visualize_train_pred_data()
        # print('')

        print('### OUTPUT')
        analyzer_obj.calc_output()
        analyzer_obj.write_output('tmp.csv')

    except Exception as e:
        print('[ERROR] %s' % e)
        traceback.print_exc()
    finally:
        notifier_obj = Notifier()
        notifier_obj.read_config_file(config_path)
        notifier_obj.notify_slack()
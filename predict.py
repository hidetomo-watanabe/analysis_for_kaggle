import sys
import traceback
from modules.Predicter import Predicter
from modules.Notifier import Notifier
from modules.MyLogger import MyLogger

logger = MyLogger().get_logger('predict')

if __name__ == '__main__':
    logger.info('# START')

    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    else:
        config_path = './configs/config.json'
    try:
        predicter_obj = Predicter()
        predicter_obj.read_config_file(config_path)

        logger.info('### INIT')
        predicter_obj.get_raw_data()
        predicter_obj.display_data()

        logger.info('### TRANSLATE')
        predicter_obj.trans_raw_data()
        predicter_obj.display_data()

        logger.info('##### NORMALIZE')
        predicter_obj.get_fitting_data()
        predicter_obj.normalize_fitting_data()
        predicter_obj.reduce_dimension()

        # logger.info('### VISUALIZE TRAIN DATA')
        # predicter_obj.visualize_train_data()

        logger.info('### VALIDATE')
        predicter_obj.is_ok_with_adversarial_validation()

        logger.info('### FIT')
        predicter_obj.calc_ensemble_model()

        # logger.info('### VISUALIZE LEARNING CURVES')
        # predicter_obj.visualize_learning_curves()

        logger.info('### PREDICT')
        predicter_obj.calc_output()

        # logger.info('### VISUALIZE TRAIN PRED DATA')
        # predicter_obj.visualize_train_pred_data()

        logger.info('### OUTPUT')
        predicter_obj.write_output()

    except Exception as e:
        logger.error('%s' % e)
        traceback.print_exc()
    finally:
        notifier_obj = Notifier()
        notifier_obj.read_config_file(config_path)
        notifier_obj.notify_slack()
    logger.info('# FINISHED')

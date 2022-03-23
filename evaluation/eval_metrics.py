import sklearn
import numpy as np


def get_evaluation_report(y_pred: np.array, y_true: np.array, task: str, prefix: str = '') -> dict:
    """
    Get values for common evaluation metrics.
    :param y_pred: predicted values
    :param y_true: true values
    :param task: ML task to solve
    :param prefix: prefix to be added to the key if multiple eval metrics are collected
    :return: dictionary with common metrics
    """
    if len(y_pred) == (len(y_true)-1):
        print('y_pred has one element less than y_true (e.g. due to batch size config) -> dropped last element')
        y_true = y_true[:-1]
    if task == 'classification':
        eval_report_dict = {
            prefix + 'accuracy': sklearn.metrics.accuracy_score(y_true=y_true, y_pred=y_pred),
            prefix + 'f1_score': sklearn.metrics.f1_score(y_true=y_true, y_pred=y_pred, average='micro'),
            prefix + 'precision': sklearn.metrics.precision_score(y_true=y_true, y_pred=y_pred,
                                                                  zero_division=0, average='micro'),
            prefix + 'recall': sklearn.metrics.recall_score(y_true=y_true, y_pred=y_pred,
                                                            zero_division=0, average='micro'),
            prefix + 'mcc': sklearn.metrics.matthews_corrcoef(y_true=y_true, y_pred=y_pred)
        }
    else:
        eval_report_dict = {
            prefix + 'mse': sklearn.metrics.mean_squared_error(y_true=y_true, y_pred=y_pred),
            prefix + 'rmse': sklearn.metrics.mean_squared_error(y_true=y_true, y_pred=y_pred, squared=False),
            prefix + 'r2_score': sklearn.metrics.r2_score(y_true=y_true, y_pred=y_pred),
            prefix + 'explained_variance': sklearn.metrics.explained_variance_score(y_true=y_true, y_pred=y_pred)
        }
    return eval_report_dict

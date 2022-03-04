import argparse
import os
import pandas as pd

from utils import helper_functions


def check_and_create_directories(arguments: argparse.Namespace):
    """
    Function to check if required subdirectories exist at base_dir and to create them if not
    :param arguments: all arguments provided by the user
    """
    # add all required directories (directories within will be created automatically)
    required_subdirs = [
        'results/' + arguments.genotype_matrix.split('.')[0] + '/' + arguments.phenotype_matrix.split('.')[0] + '/' +
        arguments.phenotype
    ]

    datasplit_string = arguments.datasplit + '/' \
                       + helper_functions.get_subpath_for_datasplit(arguments=arguments, datasplit=arguments.datasplit)

    # add subfolder for each model in case 'all' models shoudl be optimized
    if arguments.models == 'all':
        models = helper_functions.get_list_of_implemented_models()
    else:
        models = arguments.models
    for model_name in models:
        required_subdirs.append(required_subdirs[0] + '/' + model_name + '/' + datasplit_string)
    for subdir in required_subdirs:
        if not os.path.exists(arguments.base_dir + subdir):
            os.makedirs(arguments.base_dir + subdir)
            print('Created folder ' + arguments.base_dir + subdir)


def check_all_specified_arguments(arguments: argparse.Namespace):
    """
    Function to check all specified arguments for plausibility
    :param arguments: all arguments provided by the user
    """
    # Check existence of genotype and phenotype file
    if not os.path.isfile(arguments.base_dir + '/data/' + arguments.genotype_matrix):
        raise Exception('Specified genotype file ' + arguments.genotype_matrix + ' does not exist in '
                        + arguments.base_dir + 'data/. Please check spelling.')
    if not os.path.isfile(arguments.base_dir + '/data/' + arguments.phenotype_matrix):
        raise Exception('Specified phenotype file ' + arguments.phenotype_matrix + ' does not exist in '
                        + arguments.base_dir + 'data/. Please check spelling.')
    # Check existence of specified phenotype in phenotype file
    phenotype_file = pd.read_csv(arguments.base_dir + '/data/' + arguments.phenotype_matrix)
    if arguments.phenotype not in phenotype_file.columns:
        raise Exception('Specified phenotype ' + arguments.phenotype + ' does not exist in phenotype file '
                        + arguments.base_dir + 'data/' + arguments.phenotype_matrix + '. Check spelling.')

    # Check meaningfulness of specified values
    if not (0 <= arguments.maf_percentage <= 20):
        raise Exception('Specified maf value of ' + str(arguments.maf) + ' is invalid, has to be between 0 and 20.')
    if not (5 <= arguments.test_set_size_percentage <= 30):
        raise Exception('Specified test set size in percentage ' + str(arguments.test_set_size_percentage) +
                        ' is invalid, has to be between 5 and 30.')
    if not (5 <= arguments.validation_set_size_percentage <= 30):
        raise Exception('Specified validation set size in percentage ' + str(arguments.validation_set_size_percentage) +
                        ' is invalid, has to be between 5 and 30.')
    if not (3 <= arguments.n_outerfolds <= 10):
        raise Exception('Specified number of outerfolds ' + str(arguments.n_outerfolds) +
                        ' is invalid, has to be between 3 and 10.')
    if not (3 <= arguments.n_innerfolds <= 10):
        raise Exception('Specified number of innerfolds/folds ' + str(arguments.n_innerfolds) +
                        ' is invalid, has to be between 3 and 10.')
    if arguments.n_trials < 10:
        raise Exception('Specified number of trials with ' + str(arguments.n_trials) + ' is invalid, at least 10.')

    # Check spelling of datasplit and model
    if arguments.datasplit not in ['nested-cv', 'cv-test', 'train-val-test']:
        raise Exception('Specified datasplit ' + arguments.datasplit + ' is invalid, '
                        'has to be: nested_cv | cv-test | train-val-test')
    if (arguments.models != 'all') and \
            (any(model not in helper_functions.get_list_of_implemented_models() for model in arguments.models)):
        raise Exception('At least one specified model in "' + str(arguments.models) +
                        '" not found in implemented models nor "all" specified.' +
                        ' Check spelling or if implementation exists. Implemented models: ' +
                        ''.join(helper_functions.get_list_of_implemented_models()))

    # Check encoding
    if arguments.encoding is not None:
        if arguments.encoding not in ['raw', '012', 'onehot']:
            raise Exception('Specified encoding ' + arguments.encoding + ' is not valid. See help.')
        else:
            if arguments.models == 'all' or len(arguments.models) > 1:
                raise Exception('If "all" models are specified, standard encodings are used. Do not specify --encoding')
            else:
                if arguments.encoding not in \
                        helper_functions.get_mapping_name_to_class()[arguments.models[0]].possible_encodings:
                    raise Exception(arguments.encoding + ' is not valid for ' + arguments.models[0] +
                                    '. Check possible_encodings in model file.')

    # Only relevant for neural networks
    if arguments.batch_size is not None:
        if not (2**3 <= arguments.batch_size <= 2**8):
            raise Exception('Specified batch size ' + str(arguments.batch_size) +
                            ' is invalid, has to be between 8 and 256.')
    if arguments.n_epochs is not None:
        if not (50 <= arguments.n_epochs <= 1000000):
            raise Exception('Specified number of epochs ' + str(arguments.n_epochs) +
                            ' is invalid, has to be between 50 and 1.000.000.')

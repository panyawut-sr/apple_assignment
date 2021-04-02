import argparse

arg_lists = []
parser = argparse.ArgumentParser(description='RAM')

def str2bool(v):
    return v.lower() in ('true', '1')

def add_argument_group(name):
    arg = parser.add_argument_group(name)
    arg_lists.append(arg)
    return arg

# data params
data_arg = add_argument_group('Data Params')
data_arg.add_argument('--train_data', type=str, default='train.txt',
                      help='Data for training')
data_arg.add_argument('--test_data', type=str, default='test.txt',
                      help='Data for testing')
data_arg.add_argument('--evaluate_data', type=str, default='evaluate.txt',
                      help='Data for evaluation')
data_arg.add_argument('--sentence', type=str, default='ตั้งปลุกตีห้า',
                      help='Target sentence')

# training params
train_arg = add_argument_group('Training Params')
train_arg.add_argument('--mode', type=str, default="Train",
                       help='1.Train  2. Evaluate   3.TestSample   4.TestFile')
train_arg.add_argument('--alpha', type=float, default=1.0,
                       help='Additive (Laplace/Lidstone) smoothing parameter (0 for no smoothing).')
train_arg.add_argument('--fit_prior', type=str2bool, default=True,
                       help='Whether to learn class prior probabilities or not. If false, a uniform prior will be used.')

# other params
misc_arg = add_argument_group('Misc.')
misc_arg.add_argument('--load_trained_model_path', type=str, default='model.sav',
                      help='Directory for loading model')
misc_arg.add_argument('--save_model_path', type=str, default='model.sav',
                      help='Directory for saving the model')
misc_arg.add_argument('--result_path', type=str, default='results.txt',
                      help='Directory for saving the restuls')
                      

def get_config():
    config, unparsed = parser.parse_known_args()
    return config, unparsed

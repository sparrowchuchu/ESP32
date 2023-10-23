import keras_lite_convertor as kc

path_name = 'gesture_data'
Data_reader = kc.Data_reader(path_name, 
                             mode='categorical',
                             label_name=['right','down','stop',
                                         'left','up'])
data, label = Data_reader.read(random_seed=12)

from optparse import OptionParser
from pydub import AudioSegment
from keras.models import load_model
from utility import functions, globalvars

import librosa
import numpy as np
import sys
import cPickle


'''
Predict for one sample data
'''
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-p', '--predicted_wav_path', dest='wav_path', default='')
    parser.add_option('-l', '--load_data', action='store_true', dest='load_data')
    parser.add_option('-e', '--feature_extract', action='store_true', dest='feature_extract')
    parser.add_option('-m', '--model_path', dest='model_path', default='')
    parser.add_option('-c', '--nb_classes', dest='nb_classes', type='int', default=7)

    (options, args) = parser.parse_args(sys.argv)

    wav_path = options.wav_path
    load_data = options.load_data
    feature_extract = options.feature_extract
    model_path = options.model_path
    nb_classes = options.nb_classes

    globalvars.nb_classes = nb_classes

    y, sr = librosa.load(wav_path, sr=16000)
    wav = AudioSegment.from_file(wav_path)
    if feature_extract:
        f = functions.feature_extract((y, sr), nb_samples=1, dataset='prediction')
    else:
        print("Loading features from file...")
        f = cPickle.load(open('prediction_features.p', 'rb'))

    u = np.full((f.shape[0], globalvars.nb_attention_param), globalvars.attention_init_value,
                dtype=np.float64)

    # load model
    model = load_model(model_path)

    # prediction
    results = model.predict([u, f], batch_size=128, verbose=1)

    for result in results:
        print(result)

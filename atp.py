import argparse
import os
import json
from atp import ThresholdPredictor


def train_threshold_predictor(density_map_path, thresholds_path):
    with open(thresholds_path, 'r') as fp:
        json_data = json.load(fp)

    D = get_files(density_map_path, ['mrc', 'map'])
    T = [next(t[1] for t in json_data.items() if t[0] in d) for d in D]

    tp = ThresholdPredictor()
    tp.train(D, T)
    tp.save('./model.json')



def get_files(path, allowed_extensions):
    """Returns files in path with allowed extension"""
    return [os.path.join(path, f) for f in os.listdir(path) if f.split('.')[-1] in allowed_extensions]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Automatic Threshold Level Selection')
    parser.add_argument('density_maps', type=str, help='Folder containing density maps')
    parser.add_argument('thresholds', type=str, help='JSON file containing suitable threshold for density maps')

    args = parser.parse_args()
    train_threshold_predictor(args.density_maps, args.thresholds)

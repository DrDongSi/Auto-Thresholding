import json
from .metrics import sa_v, r_nz
from scipy.optimize import root_scalar
from numpy.linalg import lstsq


def get_threshold_predictor(name, M=None):
    """
    Re-instantiates trained threshold predictor based on JSON file and given
    metrics

    Parameters
    ----------
    name: str
        Path to JSON file containing target metric values

    M: list
        List of metrics used to calculate threshold. It is important that the
        target metric values from the JSON file were calculated using these
        exact metrics

    Returns
    ----------
    predictor: ThresholdPredictor
        Trained threshold predictor
    """
    with open(name, 'r') as f:
        json_data = json.load(f)
        return ThresholdPredictor(M, json_data['M_t'], json_data['W'])


class ThresholdPredictor:
    """
    Threshold predictor can be used to automatically predict a threshold level
    for a given density map

    In order to predict thresholds the predictor has to be trained first to
    calculate the metric target values. This can be done through the 'train'
    method.

    The calculated metric target value can be saved to a JSON file using 'save'.
    To re-instantiate the predictor with those target values use 'load'.
    """

    def __init__(self, M=None, M_t=None, W=None):
        """
        Sets the metrics and metric target values

        Parameters
        ----------
        M: list
            Metric functions that will be used by the predictor. By
            default this is the surface area to volume (SA:V) ratio and the
            remaining to non-zero (R:NZ) ratio
        M_t: list
            Defines the metric target values. If they are not set the
            predictor has to be trained first.
        W: list
            List of weights to calculate the weighted average of the thresholds
            calculated by each metric
        """
        self.M = M if M else [sa_v, r_nz]
        self.M_t = M_t
        self.W = W

    def train(self, D, T):
        """
        Calculates target values for all metrics based on given training data

        Evaluates metrics for each density map and its suitable threshold level
        and sets the metric target value to the average

        Parameters
        ----------
        D: list
            List of density maps for which metrics are evaluated for

        T: list
            List of suitable threshold levels for density maps. Thresholds have
            to align with density maps (e.g. T[0] is suitable threshold level
            for D[0]).
        """
        self.M_t = []
        for m in self.M:
            self.M_t.append(sum(m(D[i], T[i]) for i in range(len(D))) / len(D))

        a = []
        for d in D:
            a.append([root_scalar(lambda t: self.M_t[i] - self.M[i](d, t), bracket=[0, 10]).root
                      for i in range(len(self.M))])

        self.W = lstsq(a, T, rcond=None)[0].tolist()

    def predict(self, d):
        """
        Predicts the threshold level for the given density map

        This method requires the metric target values to be set. This is done
        by training the predictor with the 'train' method.

        Parameter
        ---------
        d: Density map
            Density map for which threshold level is predicted

        Returns
        ---------
        t: ThresholdResult
            Result containing threshold level as well as list of boolean flags
            indicating which metrics converged to their target metric value
        """
        thresholds, converged = [], []
        for i in range(len(self.M)):
            res = root_scalar(lambda t: self.M_t[i] - self.M[i](d, t), bracket=[0, 10])
            thresholds.append(res.root)
            converged.append(res.converged)

        return ThresholdResult(sum(thresholds[i] * self.W[i] for i in range(len(thresholds))) / sum(self.W), converged)

    def save(self, name):
        """
        Saves target metric values to JSON file. This can later be used to
        re-instantiate the threshold predictor without training it.

        Parameters
        ----------
        name: str
            Path where JSON file is saved at
        """
        with open(name, 'w') as f:
            json.dump({
                'M_t': self.M_t,
                'W': self.W
            }, f)


class ThresholdResult:
    """Results of threshold prediction"""

    def __init__(self, threshold, converged):
        """
        Parameters
        ----------
        threshold: float
            Predicted threshold level

        converged: list
            List of boolean flags indicating which metric converged to its
            target metric value
        """
        self.threshold = threshold
        self.converged = converged

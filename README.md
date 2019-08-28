## Citation
Paper citation with more information: Jonas Pfab, Dong Si. (2019). Automated Threshold Selection for Cryo-EM Density Maps. 10.1101/657395.

# Auto-Thresholding
Automatic Thresholding for Cryo-EM Maps

## Installing Required Pacakges
In order to use the automated threshold prediction we need to install all required Python packages (Python version of 3.5 or higher is required). This can be done by creating a virtual environment with `python3 -m venv env` and activating it with `source ./env/bin/activate`. Once the virtual Python environment is activated, the required packages can be installed with pip using `pip install -r requirements.txt`.

Additionally, we need to have Chimera installed on the system and a symbolic link to the chimera binary file in `/usr/local/bin/chimera` must exist.

## Usage

In order to use the automated threshold prediction we have to import the `ThresholdPredictor` class from the `atp` package. It contains the functions for training and prediction. In order to train the predictor and save the calculated paramters in a JSON file the following code can be used. It requires `D` to contain the path to a list of training density maps and `T` to be a dict storing a suitable threshold for every density map in `D`.

```
> from atp import ThresholdPredictor
> tp = ThresholdPredictor()
> tp.train(D, T)
> tp.save('PATH_FOR_JSON')
```

To predict the threshold value for a new density map `d` we can restore the trained threshold predictor from the saved JSON file as shown in the following.

```
> from atp import get_threshold_predictor
> tp = get_threshold_predictor('PATH_FOR_JSON')
> tp.predict(d)
```

The `atp.py` script at the root of the project contains code to easily train a threshold predictor. It can be invoked as following.

`python atp.py PATH_TO_DENSITY_MAPS PATH_TO_THRESHOLDS_JSON`

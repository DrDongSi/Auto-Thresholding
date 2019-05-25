from copy import deepcopy
import numpy as np
import subprocess
import mrcfile
import os


def sa_v(density_map, threshold):
    chimera_script = open('./measure.cmd', 'w')
    chimera_script.write('open ' + density_map + '\n'
                         'volume #0 level ' + str(threshold) + '\n'
                         'measure volume #0\n'
                         'measure area #0\n')
    chimera_script.close()

    output = subprocess.check_output(['/usr/local/bin/chimera', '--nogui', chimera_script.name])

    volume, surface_area = None, None
    lines = str(output).split('\\n')
    for line in lines:
        if 'area' in line and surface_area is None:
            surface_area = float(line.split(' = ')[-1])
        elif 'volume' in line and volume is None:
            volume = float(line.split(' = ')[-1])

    os.remove(chimera_script.name)

    return float('inf') if volume == 0 else surface_area / volume


def r_nz(density_map, threshold):
    map_data = deepcopy(mrcfile.open(density_map, mode='r').data).ravel()

    return len(np.where(map_data > threshold)[0]) / len(np.where(map_data > 0)[0])

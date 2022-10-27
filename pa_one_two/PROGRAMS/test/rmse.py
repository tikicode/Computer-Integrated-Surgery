import numpy as np
from pathlib import Path
import pa_one_two.PROGRAMS.cis.file_rw as frw


def test_rmse(name):
    data_dir = Path('../DATA/PA2')
    output_dir = Path('../../OUTPUT/PA2')
    our_output_one = output_dir / f"{name}-output-1.txt"
    our_output_two = output_dir / f"{name}-output-2.txt"
    output_one = data_dir / f"{name}-output1.txt"
    output_two = data_dir / f"{name}-output2.txt"

    debug_cexp = frw.getOutput(output_one)
    our_cexp = frw.getOutput(our_output_one)
    debug_em = frw.getOutput(output_two)
    our_em = frw.getOutput(our_output_two)

    rmse_one = np.sqrt(np.mean((debug_cexp - our_cexp) ** 2))
    rmse_two = np.sqrt(np.mean((debug_em - our_em) ** 2))

    f = open(f"{output_dir}/{name}-rmse.txt", 'w')
    f.write('{0}\n'.format(name + "-rmse.txt"))
    f.write('RMSE 1: {0}, RMSE 2: {1}\n'.format(format(rmse_one, '.2f'), format(rmse_two, '.2f')))
    f.close()


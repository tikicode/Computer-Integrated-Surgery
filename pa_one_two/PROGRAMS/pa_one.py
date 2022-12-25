import click
from pathlib import Path
import cis.prob456 as prob
import cis.file_rw as io
import numpy as np


@click.command()
@click.option("--data_dir", "data_dir", "-d", default="DATA/PA1", help="Input DATA directory")
@click.option("--output_dir", "output_dir", "-o",
              default="../OUTPUT/PA1",
              help="Output directory")
@click.option("--name", "name", "-n", default="pa1-debug-g", help="Name of file")
def main(data_dir: str, output_dir: str, name: str):
    """Main method for running the program

    Parameters
    _________
    data_dir : Path
        The path to the DATA directory
    output_dir : Path
        The path to the output directory
    name : str
        The name of the file
    """
    data_dir = Path(data_dir)
    output_dir = Path(output_dir)
    if not output_dir.exists():
        output_dir.mkdir()

    cal_body = data_dir / f"{name}-calbody.txt"
    cal_reading = data_dir / f"{name}-calreadings.txt"
    em_pivot = data_dir / f"{name}-empivot.txt"
    opt_pivot = data_dir / f"{name}-optpivot.txt"

    c_exp = prob.prob_four(cal_body, cal_reading)
    probe = prob.prob_five(em_pivot)
    beacon = prob.prob_six(opt_pivot, cal_body)

    write_output(c_exp, probe, beacon, output_dir, name)
    if name.find("debug") != -1:
        mse(c_exp, probe, beacon, output_dir, data_dir, name)


def write_output(c_exp: np.ndarray, probe: np.ndarray, beacon: np.ndarray, output_dir: str, name: str):
    """Method for writing file outputs

    Parameters
    _________
    c_exp : np.ndarray
        The solution to problem 4, expected values for a distortion calibration DATA set
    probe : np.ndarray
        The solution to problem 5, position of the EM probe relative to the EM tracker base
    beacon : np.ndarray
        The solution to problem 6, position of the optical tracker beacon in EM tracker coordinates for each
        observation frame of optical tracker DATA
    """
    f = open(f"{output_dir}/{name}-output-1.txt", 'w')
    f.write('{0}, {1}, {2}\n'.format(c_exp[0].points.shape[0], len(c_exp), f"{name}-output-1.txt"))
    f.write('{0},   {1},   {2}\n'.format(format(probe[0], '.2f'), format(probe[1], '.2f'), format(probe[2], '.2f')))
    f.write('{0},   {1},   {2}\n'.format(format(beacon[0], '.2f'), format(beacon[1], '.2f'), format(beacon[2], '.2f')))
    for r in range(len(c_exp)):
        for c in range(c_exp[0].points.shape[0]):
            f.write('{0},   {1},   {2}\n'.format(format(c_exp[r].points[c][0], '.2f'),
                                                 format(c_exp[r].points[c][1], '.2f'),
                                                 format(c_exp[r].points[c][2], '.2f')))
    f.close()


def mse(c_exp: np.ndarray, probe: np.ndarray, beacon: np.ndarray, output_dir: str, data_dir: str, name: str):
    """Method for calculating the mean squared error between the output of the program and the debug output

    Parameters
    _________
    c_exp : np.ndarray
        The solution to problem 4, expected values for a distortion calibration DATA set
    probe : np.ndarray
        The solution to problem 5, position of the EM probe relative to the EM tracker base
    beacon : np.ndarray
        The solution to problem 6, position of the optical tracker beacon in EM tracker coordinates for each
        observation frame of optical tracker DATA
    output_dir : Path
        The path to the output directory
    data_dir : Path
        The path to the DATA directory
    name : str
        The name of the file
    """
    data_dir = Path(data_dir)
    ans = data_dir / f"{name}-output1.txt"
    post_em, post_opt, cs = io.get_answer_pa1(ans)
    mse_post_em = np.mean((probe - post_em) ** 2)
    mse_post_opt = np.mean((beacon - post_opt) ** 2)
    c_exp_pc = []
    for i in range(len(c_exp)):
        c_exp_pc.append(c_exp[i].points)
    c_exp = np.array(c_exp_pc)
    c_exp = c_exp.reshape((216, 3))
    mse_cs = np.mean((c_exp - cs) ** 2)

    f = open(f"{output_dir}/{name}-mse.txt", 'w')
    f.write('{0}\n'.format(name + "-mse.txt"))
    f.write('MSE of EM pivot post position: {0} \n'.format(format(mse_post_em, '.4f')))
    f.write('MSE of Optical pivot post position: {0} \n'.format(format(mse_post_opt, '.4f')))
    f.write('MSE of calculated EM observed coordinates: {0} \n'.format(format(mse_cs, '.4f')))
    f.close()


if __name__ == "__main__":
    main()

import click
from pathlib import Path
import cis.pa2probs as pa2
import cis.prob456 as pa1
import numpy as np


@click.command()
@click.option("--data_dir", "data_dir", "-d", default="DATA/PA2", help="Input DATA directory")
@click.option("--output_dir", "output_dir", "-o",
              default="../OUTPUT/PA2",
              help="Output directory")
@click.option("--name", "name", "-n", default="pa2-unknown-j", help="Name of file")
def main(data_dir, output_dir, name):
    data_dir = Path(data_dir)
    output_dir = Path(output_dir)
    if not output_dir.exists():
        output_dir.mkdir()

    cal_body = data_dir / f"{name}-calbody.txt"
    cal_reading = data_dir / f"{name}-calreadings.txt"
    ct_fids = data_dir / f"{name}-ct-fiducials.txt"
    em_fids = data_dir / f"{name}-em-fiducialss.txt"
    em_nav = data_dir / f"{name}-EM-nav.txt"
    em_pivot = data_dir / f"{name}-empivot.txt"
    opt_pivot = data_dir / f"{name}-optpivot.txt"

    c_exp = pa1.prob_four(cal_body, cal_reading)
    c_exp_pts = np.zeros(shape=(len(c_exp) * c_exp[0].points.shape[0], 3))
    for i in range(len(c_exp)):
        index = c_exp[0].points.shape[0] * i
        c_exp_pts[index:index + c_exp[0].points.shape[0]] = c_exp[i].points
    probe = pa1.prob_five(em_pivot)
    beacon = pa1.prob_six(opt_pivot, cal_body)
    coefficients, p_tip_em, base_em, em_pivot_undistorted, q_min, q_max, q_exp_min, q_exp_max = \
        pa2.prob_three(cal_reading, em_pivot, c_exp_pts)
    b_j = pa2.prob_four(em_fids, q_min, q_max, q_exp_min, q_exp_max, coefficients,
                        p_tip_em, em_pivot_undistorted)
    F_reg = pa2.prob_five(ct_fids, b_j)
    b_nav = pa2.prob_six(em_nav, em_pivot_undistorted, p_tip_em, F_reg, coefficients, q_min, q_max,
                         q_exp_min, q_exp_max)

    write_output_one(c_exp, probe, beacon, output_dir, name)
    write_output_two(b_nav, output_dir, name)


def write_output_one(c_exp, probe, beacon, output_dir, name):
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
    f.write('{0}, {1}, {2}\n'.format(c_exp[0].points.shape[0], len(c_exp), name + "-output-1.txt"))
    f.write('{0},   {1},   {2}\n'.format(format(probe[0], '.2f'), format(probe[1], '.2f'), format(probe[2], '.2f')))
    f.write('{0},   {1},   {2}\n'.format(format(beacon[0], '.2f'), format(beacon[1], '.2f'), format(beacon[2], '.2f')))
    for r in range(len(c_exp)):
        for c in range(c_exp[0].points.shape[0]):
            f.write('{0},   {1},   {2}\n'.format(format(c_exp[r].points[c][0], '.2f'),
                                                 format(c_exp[r].points[c][1], '.2f'),
                                                 format(c_exp[r].points[c][2], '.2f')))
    f.close()


def write_output_two(b_nav, output_dir, name):
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
    f = open(f"{output_dir}/{name}-output-2.txt", 'w')
    f.write('{0}, {1}\n'.format(len(b_nav), name + "-output-2.txt"))
    for i in range(len(b_nav)):
        f.write('{0},    {1},    {2}\n'.format(format(b_nav[i][0], '.2f'),
                                               format(b_nav[i][1], '.2f'),
                                               format(b_nav[i][2], '.2f')))
    f.close()


if __name__ == "__main__":
    main()

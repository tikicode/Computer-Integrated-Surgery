import pathlib

import click
from pathlib import Path
import cis.prob456 as prob


@click.command()
@click.option("--data_dir", "data_dir", "-d", default="DATA/PA1", help="Input DATA directory")
@click.option("--output_dir", "output_dir", "-o",
              default="/Users/avnukala/Desktop/CIS I /Computer-Integrated-Surgery/pa_one_two/OUTPUT/PA1",
              help="Output directory")
@click.option("--name", "name", "-n", default="pa1-debug-g", help="Name of file")
def main(data_dir, output_dir, name):
    print(pathlib.Path.cwd())
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


def write_output(c_exp, probe, beacon, output_dir, name):
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


if __name__ == "__main__":
    main()

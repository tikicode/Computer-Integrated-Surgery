import pa_one.PROGRAMS.prob456 as prob
import click
from pathlib import Path


@click.command()
@click.option("--data_dir", "data_dir", "-d", default="data", help="Input data directory")
@click.option("--output_dir", "output_dir", "-o", default="OUTPUT", help="Output directory")
@click.option("--name", "name", "-n", default="pa1-debug-a", help="Name of file")
def main(data_dir, output_dir, name):
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
    beacon = prob.prob_six(opt_pivot, cal_body, cal_reading)


def write_output(c_exp, probe, beacon, output_dir, name):
    f = open(f"{output_dir}/{name}-our-sol", 'w')
    f.write('{0} {1} {2}\n'.format(len(c_exp[0].points[0]), len(c_exp), name))
    f.write('{0:.2f} {1:.2f} {2:.2f}\n'.format(probe[0], probe[1], probe[2]))
    f.write('{0:.2f} {1:.2f} {2:.2f}\n'.format(beacon[0], beacon[1], beacon[2]))
    for r in range(len(c_exp)):
        for c in range(len(c_exp[0].points[1])):
            f.write('{0:.2f} {1:.2f} {2:.2f}\n'.format(c_exp[r].points[0][c], c_exp[r].points[1][c],
                                                       c_exp[r].points[2][c]))
    f.close()


if __name__ == "__main__":
    main()

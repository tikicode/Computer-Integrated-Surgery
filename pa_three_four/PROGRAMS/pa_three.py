import click
from pathlib import Path
import cis.pc_io as io
import cis.icp as icp
import cis.frame as frame
import numpy as np


@click.command()
@click.option("--data_dir", "data_dir", "-d", default="DATA/", help="Input DATA directory")
@click.option("--output_dir", "output_dir", "-o",
              default="../OUTPUT/PA3",
              help="Output directory")
@click.option("--name", "name", "-n", default="pa2-unknown-j", help="Name of file")
def main(data_dir, output_dir, name):
    data_dir = Path(data_dir)
    output_dir = Path(output_dir)
    if not output_dir.exists():
        output_dir.mkdir()

    body_a = data_dir / f"Problem3-BodyA.txt"
    body_b = data_dir / f"Problem3-BodyB.txt"
    mesh = data_dir / f"Problem3Mesh.sur"
    sample_readings = data_dir / f"{name}-Unknown-SampleReadingsTest.txt"

    a_leds, a_tip = io.import_rigid_body(body_a)
    b_leds, b_tip = io.import_rigid_body(body_b)
    vertices, indices, triangles = io.import_surface_mesh(mesh)
    a_read, b_read, d_read = io.import_sample_readings(sample_readings, len(a_leds), len(b_leds))
    d_ks = icp.find_rigid_body_pose(a_read, b_read, a_tip, a_leds, b_leds)
    c_ks = np.zeros(shape=(len(d_ks), 3))
    for i in range(len(a_read)):
        F_reg = frame.Frame(np.identity(3), np.zeros(3))
        s_k = icp.find_sample_points(F_reg, d_ks[i])
        c_ks[i] = (icp.find_closest_point(vertices, indices, s_k).reshape(1, 3))
    mag_difs = icp.find_euclidian_distance(d_ks, c_ks)
    io.output_pa34(output_dir, name, c_ks, d_ks, mag_difs, len(a_read))


if __name__ == "__main__":
    main()

import click
from pathlib import Path
import cis.pc_io as io
import cis.icp as icp
import cis.icp_reg as ir
import time


@click.command()
@click.option("--data_dir", "data_dir", "-d", default="DATA/", help="Input DATA directory")
@click.option("--sample_readings_type", "sample_readings_type", "-t", default="Debug",
              help="Debug or Unknown")
@click.option("--output_dir", "output_dir", "-o",
              default="../OUTPUT/PA4",
              help="Output directory")
@click.option("--name", "name", "-n", default="PA4-A", help="Name of file")
def main(data_dir, sample_readings_type, output_dir, name):
    """Main method for PA4

    Parameters
    ----------
    data_dir : str
        The directory of the DATA files
    sample_readings_type : str
        The name of the sample readings file
    output_dir : str
        The directory to output the data
    name : str
        The name of the data output file
    """
    data_dir = Path(data_dir)
    output_dir = Path(output_dir)
    if not output_dir.exists():
        output_dir.mkdir()

    body_a = data_dir / f"Problem4-BodyA.txt"
    body_b = data_dir / f"Problem4-BodyB.txt"
    mesh = data_dir / f"Problem4MeshFile.sur"
    sample_readings = data_dir / f"{name}-{sample_readings_type}-SampleReadingsTest.txt"

    print(name)
    # Read in the data
    a_leds, a_tip = io.import_rigid_body(body_a)
    b_leds, b_tip = io.import_rigid_body(body_b)
    vertices, indices, triangles = io.import_surface_mesh(mesh)
    a_read, b_read, d_read = io.import_sample_readings(sample_readings, len(a_leds), len(b_leds))
    # Run ICP and compute s_ks and c_ks
    st_e = time.time()
    # Set max iteration limit to 100
    F, c_ks, d_ks = ir.ICP(a_read, b_read, a_tip, a_leds, b_leds, vertices, indices, 100)
    s_ks = F.compose_transform(d_ks)
    mag_dif = icp.find_euclidian_distance(s_ks, c_ks)
    et_e = time.time()

    print(f"ICP took {et_e - st_e:.2f} seconds")
    io.output_pa34(output_dir, name, s_ks, c_ks, mag_dif, len(a_read))


if __name__ == "__main__":
    main()

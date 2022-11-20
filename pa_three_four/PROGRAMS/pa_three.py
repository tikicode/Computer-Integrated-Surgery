import click
from pathlib import Path
import cis.pc_io as io
import cis.icp as icp
import cis.frame as frame
import cis.thang as thang
import cis.cov_tree as ct
import numpy as np
import time


@click.command()
@click.option("--data_dir", "data_dir", "-d", default="DATA/", help="Input DATA directory")
@click.option("--sample_readings_type", "sample_readings_type", "-t", default="Debug",
              help="Debug or Unknown")
@click.option("--output_dir", "output_dir", "-o",
              default="../OUTPUT/PA3",
              help="Output directory")
@click.option("--name", "name", "-n", default="PA3-A-Debug", help="Name of file")
def main(data_dir, sample_readings_type, output_dir, name):
    """Main method for PA3

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

    body_a = data_dir / f"Problem3-BodyA.txt"
    body_b = data_dir / f"Problem3-BodyB.txt"
    mesh = data_dir / f"Problem3Mesh.sur"
    sample_readings = data_dir / f"{name}-{sample_readings_type}-SampleReadingsTest.txt"

    # Read in the data
    print(name)
    a_leds, a_tip = io.import_rigid_body(body_a)
    b_leds, b_tip = io.import_rigid_body(body_b)
    vertices, indices, triangles = io.import_surface_mesh(mesh)
    a_read, b_read, d_read = io.import_sample_readings(sample_readings, len(a_leds), len(b_leds))
    st_s = time.time()
    d_ks_s, c_ks_s, mag_dif_s = simple_ICP(a_read, b_read, a_tip, a_leds, b_leds, vertices, indices)
    et_s = time.time()
    print(f"Simple ICP took {et_s - st_s:.2f} seconds")
    st_e = time.time()
    d_ks_e, c_ks_e, mag_dif_e = efficient_ICP(a_read, b_read, a_tip, a_leds, b_leds, vertices, indices)
    et_e = time.time()
    print(f"Efficient ICP took {et_e - st_e:.2f} seconds")
    io.output_pa3(output_dir, name, d_ks_e, c_ks_e, mag_dif_e, len(a_read))
    print(f"MSE between simple and efficient ICP output c_k coordinates: {np.mean((c_ks_e - c_ks_s)**2):.2f}")


def simple_ICP(a_read, b_read, a_tip, a_leds, b_leds, vertices, indices):
    """Simple ICP method for PA3

    Parameters
    ----------
    a_read : np.ndarray
        The readings from the first rigid body
    b_read : np.ndarray
        The readings from the second rigid body
    a_tip : np.ndarray
        The tip of the first rigid body
    a_leds : np.ndarray
        The LEDs of the first rigid body
    b_leds : np.ndarray
        The LEDs of the second rigid body
    vertices : np.ndarray
        The vertices of the surface mesh
    indices : np.ndarray
        The indices of the surface mesh

    Returns
    -------
    d_ks : np.ndarray
        The points on the surface mesh
    c_ks : np.ndarray
        The points on the rigid body
    mag_dif : np.ndarray
        The magnitude of the difference between the points
    """
    return icp.ICP_linear(a_read, b_read, a_tip, a_leds, b_leds, vertices, indices)


def efficient_ICP(a_read, b_read, a_tip, a_leds, b_leds, vertices, indices):
    """Efficient ICP method for PA3

    Parameters
    ----------
    a_read : np.ndarray
        The readings from the first rigid body
    b_read : np.ndarray
        The readings from the second rigid body
    a_tip : np.ndarray
        The tip of the first rigid body
    a_leds : np.ndarray
        The LEDs of the first rigid body
    b_leds : np.ndarray
        The LEDs of the second rigid body
    vertices : np.ndarray
        The vertices of the surface mesh
    indices : np.ndarray
        The indices of the surface mesh

    Returns
    -------
    d_ks : np.ndarray
        The points on the surface mesh
    c_ks : np.ndarray
        The points on the rigid body
    mag_dif : np.ndarray
        The magnitude of the difference between the points
    """
    d_ks = icp.find_rigid_body_pose(a_read, b_read, a_tip, a_leds, b_leds)
    closest = []
    # Create an array of Thing objects representing the triangles of the mesh
    ts = np.array([thang.Thang(vertices[indices[i]]) for i in range(len(indices))])
    # Create a CovTree object from the array of Thing objects
    root = ct.CovTreeNode(ts, len(ts))
    previous_closest = ts[0].corners[0]
    # Find bounds and compute the closest point to the rigid body for each point on the surface mesh
    for _, s in enumerate(d_ks):
        bound = np.linalg.norm(s - previous_closest)
        closest.append(root.find_closest_point(s, bound, previous_closest))
        previous_closest = closest[-1]
    c_ks = np.array(closest)
    # Compute the magnitude of the difference between the points
    mag_dif = icp.find_euclidian_distance(c_ks, d_ks)
    return d_ks, c_ks, mag_dif


if __name__ == "__main__":
    main()

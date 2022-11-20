import pandas as pd
import numpy as np
from pathlib import Path


def import_rigid_body(fName: Path):
    """Method for importing rigid body design data

    Parameters
    _________
    fName : Path
        The name of the DATA file

    Returns
    _________
    np.ndarray
         Point clouds representing the xyz coordinates of the marker LEDs in body coordinates and the xyz coordinate
         of the tip in body coordinates
    """
    headers = pd.read_csv(fName, header=None, names=["Nm", np.nan], nrows=1, delim_whitespace=True)
    # number of headers
    Nm = int(headers["Nm"][0])
    text = pd.read_csv(fName, header=None, names=["xi", "yi", "zi"], skiprows=1, delim_whitespace=True)
    marker_leds = np.array(text[["xi", "yi", "zi"]][:Nm])
    tip_in_body = np.array(text[["xi", "yi", "zi"]][Nm:])
    return marker_leds, tip_in_body


def import_surface_mesh(fName: Path):
    """Method for importing body surface definition data

    Parameters
    _________
    fName : Path
        The name of the DATA file

    Returns
    _________
    np.ndarray
         Point clouds representing the xyz coordinates of vertices in CT coordinates and the xyz coordinates= of the

    """
    headers = pd.read_csv(fName, header=None, names=["Nv"], nrows=1, delim_whitespace=True)
    # number of vertices
    Nv = int(headers["Nv"][0])
    text = pd.read_csv(fName, header=None, names=["xi", "yi", "zi"], skiprows=1, nrows=Nv, delim_whitespace=True)
    ct_vertices = np.array(text[["xi", "yi", "zi"]][:])
    headers = pd.read_csv(fName, header=None, names=["Nt"], skiprows=Nv + 1, nrows=1, delim_whitespace=True)
    Nt = int(headers["Nt"][0])
    text = pd.read_csv(fName, header=None, names=["i1", "i2", "i3", "n1", "n2", "n3"], skiprows=Nv + 2, nrows=Nt,
                       delim_whitespace=True)
    indices = np.array(text[["i1", "i2", "i3"]][:])
    triangles = np.array(text[["n1", "n2", "n3"]][:])
    return ct_vertices, indices, triangles


def import_sample_readings(fName: Path, Na: int, Nb: int):
    """Method for importing sample readings

    Parameters
    _________
    fName : Path
        The path of the DATA file
    Na : int
        The number of A body marker LED coordinates per frame
    Nb : int
        The number of B body marker LED coordinates per frame


    Returns
    _________
    np.ndarray
         Point clouds representing frames of xyz coordinates of A body LED markers, B body LED markers, and D
         (unneeded) body LED markers
    """
    headers = pd.read_csv(fName, header=None, names=["Ns", "n_s", np.nan], nrows=1)
    # number of leds and samples
    Ns = int(headers["Ns"][0])
    n_s = int(headers["n_s"][0])
    text = pd.read_csv(fName, header=None, names=["xi", "yi", "zi"], skiprows=1)
    A_readings, B_readings, D_readings = [], [], []
    for i in range(n_s):
        A_readings.append(np.array(text[["xi", "yi", "zi"]][i * Ns: Na + i * Ns]))
        B_readings.append(np.array(text[["xi", "yi", "zi"]][Na + i * Ns: Na + Nb + i * Ns]))
        D_readings.append(np.array(text[["xi", "yi", "zi"]][Na + Nb + i * Ns: Na + Nb + Ns + i * Ns]))
    return A_readings, B_readings, D_readings


def output_pa3(output_dir: Path, name: str, ds: np.ndarray, cs: np.ndarray, mag_dif: np.ndarray, samples: int):
    """Method for outputting PA34 data

    Parameters
    _________
    output_dir : Path
        The directory to output the data
    name : str
        The name of the data output file
    cs : np.ndarray
        The xyz coordinates on the surface mesh found from F_reg * d_k
    ds : np.ndarray
        The xyz coordinates of the tip with respect to rigid body B
    mag_dif : np.ndarray
        The magnitude of the difference between the tip in CT coordinates and the tip in DCS coordinates
    samples : int
        The number of samples in the output
    """

    f = open(f"{output_dir}/{name}-output.txt", 'w')
    f.write('{0} {1}\n'.format(samples, name + "-output.txt"))
    for n in range(samples):
        f.write('  {0:>8}{1:>9}{2:>9}{3:>13}{4:>9}{5:>9}{6:>10}\n'.format(format(ds[n][0], '.2f'),
                                                                          format(ds[n][1], '.2f'),
                                                                          format(ds[n][2], '.2f'),
                                                                          format(cs[n][0], '.2f'),
                                                                          format(cs[n][1], '.2f'),
                                                                          format(cs[n][2], '.2f'),
                                                                          format(mag_dif[n], '.3f')))
    f.close()


def read_answer_pa3(fName: Path):
    """Method for reading the answer file for PA3

    Parameters
    _________
    fName : Path
        The path of the answer file

    Returns
    _________
    np.ndarray
         Point clouds representing the xyz coordinates of the tip in CT coordinates
    """
    text = pd.read_csv(fName, header=None, names=["d_xi", "d_yi", "d_zi", "c_xi", "c_yi", "c_zi", "mag_dif"], skiprows=1,
                       delim_whitespace=True)
    ds = np.array(text[["d_xi", "d_yi", "d_zi"]][:])
    cs = np.array(text[["c_xi", "c_yi", "c_zi"]][:])
    mags = np.array(text["mag_dif"][:])
    return ds, cs, mags

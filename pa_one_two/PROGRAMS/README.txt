Source Files
_____________
cis.file_rw : This file contains the methods for reading data in from the data files and converting to Point Clouds
cis.frame : Contains a Frame class and methods for frame transformations
cis.pivot_cal : This file contains the method for pivot calibration
cis.point_set : Contains a class for point clouds and a point cloud registration method
cis.prob456 : Contains the solutions for problems 4,5, and 6
pa_one.py : The executable program for this project

Setup
______
Before running, please execute the following from the top level directory
conda env -f create environment.yml
conda activate CIS2022


Instructions for Running
_________________________
The executable is located directly under the PROGRAMS folder.

cd PROGRAMS
Usage: python pa_one.py -n FILENAME -o OUTPUT_DIRECTORY -d DATA_DIRECTORY

Options:
    --data_dir, -d TXT      The input data directory (default: data)
    --output_dir -o TXT     The output directory (default: myfolder)
    --name -n TXT           The file name (default: pa1-debug-a)

Example: python pa_one.py -n pa1-unknown-k -o /Users/avnukala/Desktop


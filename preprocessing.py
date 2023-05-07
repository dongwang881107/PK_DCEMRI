# Pre-processing DCE-MRI data collected from Gulou Hospital
# The necessary parameters must be saved into a mat file to fed into DCEMRI.ji as follows
# * t: time vector representing the dcedata samples
# * TR: repetition time of DCE scan
# * DCEdata: DCE data as a 3-D array (1 time by 2 space dimensions)
# * DCEflip: flip angle of DCE data in degree
# * R1 information provided by one of the following
# *  R10 and S0, representing pre-calculated R1 relaxation maps
# *  T1data, indicating that a multi-flip scan, and T1flip
# * Cp: Arterial input function as a vector, resampled to the DCE time points
# Dong Wang
# 04/27/2023

import argparse
import pydicom
import glob
import numpy as np

from scipy.io import savemat

# compute t from dicom files
def time2seconds(time):
    int_part = time.split('.')[0]
    float_part = time.split('.')[1]
    hour = int(int_part[0:2])
    minute = int(int_part[2:4])
    second = int(int_part[4:6])
    int_part = str(3600*hour + 60*minute + second)
    time = int_part + '.' + float_part
    return float(time)

# 
def main(args):
    data_path = args.data_path
    dce_path = args.dce_path
    cp_path = args.cp_path
    slice_idx = args.slice_idx
    num_timepoints = args.num_timepoints
    num_slices = args.num_slices

    file_paths = sorted(glob.glob(data_path+'/*.dcm'))

    # extract dicom information
    dcm = pydicom.dcmread(file_paths[0])
    rows = int(dcm.Rows)
    cols = int(dcm.Columns)
    DCEflip = float(dcm.FlipAngle)
    TR = float(dcm.RepetitionTime)/1000

    # extract DCE data and time points
    DCEdata = np.zeros([num_timepoints,rows,cols]) # DCE data
    t = np.zeros([num_timepoints,1]) # time points
    for i, file_path in enumerate(file_paths):
        if (i-slice_idx)%num_slices == 0:
            dcm = pydicom.dcmread(file_path)
            idx = int((i-slice_idx)/num_slices)
            DCEdata[idx,:,:] = dcm.pixel_array
            t[idx,0] = time2seconds(str(dcm.AcquisitionTime))
    t = t - t[0]

    # simulation of T1data
    # use the first frame as the pre-contrast T1data
    num_t1 = 10
    T1data = np.zeros([num_t1,rows,cols])
    for i in range(num_t1):
        T1data[i,:,:] = DCEdata[0,:,:] + 2*np.random.rand(rows,cols) - 1
    T1flip = np.array([DCEflip]*num_t1) + 2*np.random.rand(1) - 1

    # simulation of Cp, peak at time point 14
    # ! need to use new methods to compute Cp
    Cp = np.load(cp_path)

    # save to mat file
    dce = {"t":t, "TR":TR, "DCEdata":DCEdata, "DCEflip":DCEflip, "T1data":T1data, "T1flip":T1flip, "Cp":Cp}
    savemat(dce_path, dce)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='PK_DCEMRI')

    parser.add_argument('--data_path', type=str, default='/Users/dong/Documents/Data/DCE-MRI/AN DIAN JING_2003110946_121757/DCE_TRA_MOCO_Fast_8001', help='path of dicom data')
    parser.add_argument('--dce_path', type=str, default='./data/demo.mat', help='path of saved DCEMRI in mat file')
    parser.add_argument('--slice_idx', type=int, default=17, help='index of slice to perform quantitative analysis')
    parser.add_argument('--cp_path', type=str, default='/Users/dong/Documents/Data/DCE-MRI/cp.npy', help='path of cp file')
    parser.add_argument('--num_timepoints', type=int, default=150, help='number of time points')
    parser.add_argument('--num_slices', type=int, default=40, help='number of slices')

    args = parser.parse_args()

    main(args)

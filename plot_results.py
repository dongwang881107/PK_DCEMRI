# Plot results of DCE-MRI quantification
# Dong Wang
# 04/27/2023

import argparse
import glob
import pydicom
import os
import mat73
import numpy as np
import matplotlib.pyplot as plt
import imageio
from scipy.io import loadmat

# # Create a Function to Plot Time-Dependent Frames
# def create_frame(t):
#     fig = plt.figure(figsize=(6, 6))
#     plt.plot(x[:(t+1)], y[:(t+1)], color = 'grey' )
#     plt.plot(x[t], y[t], color = 'black', marker = 'o' )
#     plt.xlim([0,5])
#     plt.xlabel('x', fontsize = 14)
#     plt.ylim([0,5])
#     plt.ylabel('y', fontsize = 14)
#     plt.title(f'Relationship between x and y at step {t}',
#               fontsize=14)
#     plt.savefig(f'./img/img_{t}.png', 
#                 transparent = False,  
#                 facecolor = 'white')
#     plt.close()

def read_mat(mat_path):
    try:
        mat = mat73.loadmat(mat_path)
    except:
        mat = loadmat(mat_path)
    return mat

def _plot(fig, save_plot=False, save_path=None):
    if save_plot:
        plt.show(block=False)
        plt.pause(1)
        plt.close('all')
        plot_name = os.path.join(save_path, 'pk.png')
        fig.savefig(plot_name, bbox_inches='tight')
    else:
        plt.show()

# run main function
def main(args):
    dce_path = args.dce_path
    pk_path = args.pk_path
    slice_idx = args.slice_idx

    # load dce data
    dce = read_mat(dce_path)['DCEdata']

    # load pk parameters reconstructed by algorithms
    pk_r = read_mat(pk_path)
    Ktrans_r = pk_r['Kt']
    ve_r = pk_r['ve']
    ct_r = pk_r['Ct']

    # load pk parameters provided by the hospital
    if 'brain' in dce_path:
        pk_h_paths = glob.glob(args.data_path+'/DCE_Result*')
        for i in range(len(pk_h_paths)):
            if 'Ktrans' in pk_h_paths[i]:
                Ktrans_h = pydicom.dcmread(pk_h_paths[i]+'/'+str(slice_idx).rjust(8,'0')+'.dcm').pixel_array
            elif 'Ve' in pk_h_paths[i]:
                ve_h = pydicom.dcmread(pk_h_paths[i]+'/'+str(slice_idx).rjust(8,'0')+'.dcm').pixel_array
            else:
                continue

    # # plot S(x,t), Ct(x,t) in gif
    # _, ax = plt.subplots(nrows=1, ncols=2)
    # for i in range(dce.shape[0]):
    #     ax[0].cla()
    #     im0 = ax[0].imshow(np.squeeze(dce[i,70:120,70:120]), cmap='gray')
    #     # im0.set_clim(0,200000)
    #     ax[0].axis('off')
    #     ax[0].set_title('$S(x,t)$')
    #     ax[1].cla()
    #     im1 = ax[1].imshow(np.squeeze(ct_r[i,70:120,70:120]), cmap='gray')
    #     # im1.set_clim(0,200000)
    #     ax[1].axis('off')
    #     ax[1].set_title('$C_t(x,t)$')
    #     plt.pause(0.5)

    # plot Ktrans and Ve
    if 'brain' in dce_path:
        pk_list = [Ktrans_r, ve_r, Ktrans_h, ve_h]
        title_list = ['$K^{\mathrm{trans}}$ by DCEMRI.jl', '$v_\mathrm{e}$ by DCEMRI.jl',\
                    '$K^{\mathrm{trans}}$ by hospital', '$v_\mathrm{e}$ by hospital']

        f = plt.figure(figsize=(8,8))
        for i in range(len(pk_list)):
            plt.subplot(2,2,i+1)
            plt.imshow(pk_list[i])
            plt.axis('off')
            if i>1:
                plt.clim(0,1000)
            plt.title(title_list[i], fontsize=15)
            plt.colorbar()
    else:
        pk_list = [Ktrans_r, ve_r]
        title_list = ['$K^{\mathrm{trans}}$ by DCEMRI.jl', '$v_\mathrm{e}$ by DCEMRI.jl']

        f = plt.figure(figsize=(12,4))
        for i in range(len(pk_list)):
            plt.subplot(1,2,i+1)
            plt.imshow(pk_list[i])
            plt.axis('off')
            plt.title(title_list[i])
            plt.colorbar()

    _plot(f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='PK_DCEMRI')

    parser.add_argument('--data_path', type=str, default='/Users/dong/Documents/Data/DCE-MRI/AN DIAN JING_2003110946_121757', help='path of dicom data')
    parser.add_argument('--dce_path', type=str, default='./data/demo.mat', help='path of DCEMRI data in mat file')
    parser.add_argument('--pk_path', type=str, default='./results/demo_pk.mat', help='path of pk parameters in mat file')
    parser.add_argument('--slice_idx', type=int, default=17, help='index of slice to perform quantitative analysis')

    args = parser.parse_args()

    main(args)

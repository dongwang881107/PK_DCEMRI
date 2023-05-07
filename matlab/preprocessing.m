% Preprocess DCE-MRI data collected from Gulou Hostpial
% Dong Wang
% 04/25/2023

clear;
clc;

%% Read data
data_path = '/Users/dong/Documents/Data/DCE-MRI/AN DIAN JING_2003110946_121757/DCE_TRA_MOCO_Fast_8001';
img_paths = dir(strcat(data_path,'/*.dcm'));

%% Reshap data into spatial-temporal format
dcemri = zeros(256,222,40,150);
for i = 1:size(img_paths)
    z_idx = mod(i-1,40)+1;
    t_idx = floor((i-1)/40)+1;
    img_path = strcat(data_path,'/',img_paths(i).name);
    dcemri(:,:,z_idx,t_idx) = dicomread(img_path);
end

slice_num = 18;
% Pharmacokinetics modeling for DCE-MRI
% Dong Wang
% 04/25/2023

clear;
clc;
addpath('./src/');

%% Load DCE MRI data
% data_name = 'breast';
% data_path = strcat('./data/',data_name,'_dce.mat');
% load(data_path);
% DCEdata = shiftdim(abs(data),2);
% 
% %% Load DCE parameters for PK modeling
% params_path = strcat('./data/',data_name,'_params.mat');
% load(params_path);
% 
% %% Save DCE data and parameters into one .mat file
% outfile = strcat('./results/',data_name,'_pk.mat');
% temp_path = './results/temp.mat';
% save(temp_path, 't', 'Cp', 'TR', ...
%     'T1data', 'T1flip', ...
%     'DCEdata','DCEflip', ...
%     'outfile');

%% Run DCE fitting
run_julia('./src/dcefit.jl');

%% Load PK parameters
% load(outfile,"Kt","ve");

% f = figure;
% fs = 15;
% subplot(121);imshow(Kt(:,1:120),[]);
% colormap('parula');colorbar;
% title('K^{trans}',FontSize=fs);
% subplot(122);imshow(ve(:,1:120),[]);
% colormap('parula');colorbar;
% title('V_e',FontSize=fs);

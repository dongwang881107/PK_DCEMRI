#!'/Applications/Julia-1.5.app/Contents/Resources/julia/bin/julia'
using DCEMRI
results = fitdata(datafile="./data/brain1.mat",workers=4)
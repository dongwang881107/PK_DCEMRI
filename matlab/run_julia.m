function [status, result] = run_julia(scriptname)
julia_path = '/Applications/Julia-1.5.app/Contents/Resources/julia/bin/julia';
[status, result] = system([julia_path, ' ', scriptname],'-echo');

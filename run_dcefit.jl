using DCEMRI
using ArgParse

function parse_commandline()
    s = ArgParseSettings()
    @add_arg_table s begin
        "--dce_path", "-d"
            help = "path of dce file"
            # arg_type = String
            default = "./data/demo.mat"
        "--pk_path", "-p"
            help = "path of pk file"
            # arg_type = String
            default = "./results/demo_pk.mat"
    end
    return parse_args(s)
end

function main()
    parsed_args = parse_commandline()

    dce_path = parsed_args["dce_path"]
    pk_path = parsed_args["pk_path"]

    results = fitdata(datafile=dce_path, outfile=pk_path, workers=4)
end

main()
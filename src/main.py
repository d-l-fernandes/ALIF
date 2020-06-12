import sys

import LStore
import LipCbrAnalysis
import TRexFitter
import Plotting

def main(argv):

    script_file = argv[1]

    with open(script_file) as f:
        for i, line in enumerate(f):
            line = line.strip()
            if line and line[0] == "%":
                continue
            if line[:3] == "Job":
                if "job" in locals():
                    print("Running {} job".format(job_name))
                    job.run()
                    del job

                line = [l.strip() for l in line.split(":")]

                if len(line) != 2 and line[0] != "":
                    error_string = "Invalid option in line {} ".format(i)
                    error_string += "of file {}".format(script_file)
                    raise ValueError(error_string)

                if line[1] == "LStore":
                    job = LStore.LStore()
                    job_name = "LStore"
                elif line[1] == "LipCbrAnalysis":
                    job = LipCbrAnalysis.LipCbrAnalysis()
                    job_name = "LipCbrAnalysis"
                elif line[1] == "TRexFitter":
                    job = TRexFitter.TRexFitter()
                    job_name = "TRexFitter"
                elif line[1] == "Plotting":
                    job = Plotting.Plotting()
                    job_name = "Plotting"
            else:
                line = [l.strip() for l in line.split(":")]

                if len(line) != 2 and line[0] != "":
                    error_string = "Invalid option in line {} ".format(i)
                    error_string += "of file {}".format(script_file)
                    raise ValueError(error_string)

                if len(line) == 2:
                    job.add_option([line[0].strip(), line[1].strip()])
                    print("Added {} option to {} job".format(line[0], job_name))
        else:
            print("Running {} job".format(job_name))
            job.run()
            del job


if __name__ == "__main__":
    main(sys.argv)

"""LipCbrAnalysis class."""
import Job
import systematics

# import sys
import os
import glob
import shutil
import time
import subprocess
import random


class LipCbrAnalysis(Job.Job):
    """Class that makes the LipCbrAnalysis submit files and runs them."""

    job_name = "LipCbrAnalysis"

    required_options = ["Output", "Description", "CutFile", "Samples"]

    possible_trees = ['nominal', 'particleLevel', 'all']
    samples_variables = ["HistoFile", "SampleCode", "Type"]

    analysis_code_path = "../../analysis_deploy/AnalysisCode/"
    analysis_code_to_results = "../../results/"
    scratch_path = "../../analysis_deploy/scratch/"
    max_cuts_file = analysis_code_path + "MaxCuts.cxx"
    cut_file_path = analysis_code_path + "DoCuts/"
    cut_file_symlink = analysis_code_path + "docuts.cxx"
    cut_symlink_relative_path = "DoCuts/"

    def __init__(self):
        """Initialize optional option values and adds possible options."""
        super().__init__()
        self.possible_options += ["CutFile", "Samples", "Tree", "SystTree",
                                  "SystWeight", "SamplesToRun", "RegionsToRun",
                                  "Compile"]
        self.syst_weight = []
        self.tree = 'nominal'
        self.samples_to_run = 'all'
        self.regions_to_run = 'all'
        self.compile = True

    def set_options(self):
        super().set_options()

        # Required options
        self.cut_file = self.options_dict["CutFile"]
        self.samples_file = self.options_dict["Samples"]

        # Not required options
        if "Tree" in self.options_dict:
            self.tree = self.options_dict["Tree"]
            if self.tree not in self.possible_trees:
                raise ValueError("Tree '{}' not valid. Choose from {}".format(
                    self.tree, self.possible_trees))

        if "SystTree" in self.options_dict:
            if self.options_dict["SystTree"] == 'all':
                self.tree = systematics.syst_trees
            else:
                self.tree = [syst.strip()
                             for syst in
                             self.options_dict["SystTree"].split(',')]

                self.check_systematics(self.tree, 'tree')

        if "SystWeight" in self.options_dict:
            if self.tree != "nominal" and self.tree != 'all':
                error_string = "Tree '{}' ".format(self.tree)
                error_string += "incompatible with systematic weights. "
                error_string += "Only 'nominal' and 'all' are compatible."
                raise ValueError(error_string)

            if "weight" in self.options_dict["SystWeight"]:
                error_string = "Remove 'weight' from systematic weights."
                raise ValueError(error_string)

            if self.options_dict["SystWeight"] == 'all':
                self.syst_weight = systematics.syst_weights
            else:
                self.syst_weight = [syst.strip()
                                    for syst in
                                    self.options_dict["SystWeight"].split(',')]

                self.check_systematics(self.syst_weight, 'weight')

        if "SamplesToRun" in self.options_dict:
            if 'all' not in self.options_dict["SamplesToRun"]:
                self.samples_to_run = \
                    [sample.strip()
                     for sample in
                     self.options_dict["SamplesToRun"].split(',')]
                for i, sample in enumerate(self.samples_to_run):
                    if sample == "data":
                        continue
                    try:
                        self.samples_to_run[i] = int(self.samples_to_run[i])
                    except ValueError:
                        raise ValueError("SampleToRun {} not valid".format(
                            self.samples_to_run[i]))

        if "RegionsToRun" in self.options_dict:
            if 'all' not in self.options_dict["RegionsToRun"]:
                self.regions_to_run = \
                    [region.strip()
                     for region in
                     self.options_dict["RegionsToRun"].split(',')]

        if "Compile" in self.options_dict:
            aux = self.options_dict["Compile"].upper()
            if aux != "TRUE" and aux != "FALSE":
                raise ValueError(self.make_invalid_argument_string("Compile",
                    aux))
            if aux == "FALSE":
                self.compile = False

    def get_regions_and_max_cuts(self):
        """Get regions name and code from CutFile as well as MaxCuts."""
        self.files_to_copy.append(self.cut_file_path + self.cut_file)
        self.max_cuts, self.regions = self.parse_cut_file(
            self.cut_file_path + self.cut_file)

        if self.regions_to_run != 'all':
            self.regions = {k:v for (k,v) in self.regions.items()
                            if v in self.regions_to_run}

        if not self.regions:
            error_string = "Invalid RegionsToRun arguments. Regions list if"
            error_string += " empty."
            raise ValueError(error_string)

        with open(self.analysis_code_path+"MaxCuts.cxx", 'w') as f:
            f.write("MaxCuts = {};".format(self.max_cuts))

    def link_cutfile_and_compile(self):
        """Creates soft links to the cut file and changes the name of the
        FCNCqzl executable. This makes it possible for different executables
        to be run at the same time."""
        try:
            os.unlink(self.cut_file_symlink)
        except FileNotFoundError:
            pass
        os.symlink(self.cut_symlink_relative_path + self.cut_file,
                   self.cut_file_symlink)
        subprocess.run(["make", "clean"],
                       cwd=self.analysis_code_path)
        proc = subprocess.run(["make"], stderr=subprocess.PIPE,
                              cwd=self.analysis_code_path)

        if proc.stderr:
            err = proc.stderr.decode('utf8')
            raise RuntimeError("Error when compiling AnalysisCode:\n {}".
                               format(err))

        shutil.move(self.analysis_code_path + "FCNCqzl",
                    self.analysis_code_path + "FCNCqzl_" + self.output)

    def make_submit_job(self, sample, region, syst_weight="", syst_tree=""):
        option_string = "time ./FCNCqzl_{} --User=\"DataYear={}\" ".format(
            self.output, self.year)
        option_string += "--User=\"LepType=00\" "

        if syst_weight and syst_tree:
            error_string = "Only systematic weight or systematic tree possible"
            error_string += ". Never both at the same time."
            raise RuntimeError(error_string)

        if sample["SampleCode"] == 1:
            option_string += "--isData=1 "
            name = 'nominal'
        elif self.tree == "particleLevel":
            option_string += "--isTruth=1 "
            option_string += "--Sample={} ".format(sample["SampleCode"])
            option_string += "--MCYear={} ".format(self.mc_year)
            name = 'nominal'
        else:
            option_string += "--Sample={} ".format(sample["SampleCode"])
            option_string += "--MCYear={} ".format(self.mc_year)
            name = 'nominal'
            if syst_weight != "":
                option_string += "--SystWeight={} ".format(syst_weight)
                name = syst_weight
            if syst_tree != "":
                option_string += "--SystTree={} ".format(syst_tree)
                name = syst_tree

        option_string += "--Region={} ".format(region[0])
        scratch_name = "../scratch/{}/MC{}_{}_{}_{}.txt".format(
            self.output, self.mc_year, self.year,
            region[1], sample["HistoFile"])
        option_string += "--SetSystematicsFileName={} ".format(scratch_name)
        option_string += "--OutputFileName={}\n".format(name)

        return option_string

    def make_submit_files(self):
        self.submit_dir_path = self.output_folder + "submit_files/"

        # Delete submit folder if it exists
        if self.compile:
            if os.path.exists(self.submit_dir_path):
                shutil.rmtree(self.submit_dir_path)
                os.makedirs(self.submit_dir_path)
            else:
                os.makedirs(self.submit_dir_path)

        submit_file_name = "submit_MC{}_{}".format(self.mc_year, self.year)
        submit_file_name += "_{}_{}.sh"

        initial_string = "#!/bin/bash\n"
        initial_string += "#$ -l h_rt=20:00:00\n"
        initial_string += "#$ -V\n"
        initial_string += "#$ -cwd\n"
        # From results/output/submit_files
        initial_string += "cd ../" + self.analysis_code_path + "\n"

        # Filter the samples from samples_to_run variable
        if type(self.samples_to_run) == list:
            self.samples_list = list(filter(
                lambda x: x["SampleCode"] in self.samples_to_run,
                self.samples_list))
            if 'data' in self.samples_to_run:
                self.samples_list.append({"HistoFile": 'data',
                                          "SampleCode": 1,
                                          "Type": "data"})
        # if samples_to_run == 'all'
        else:
            self.samples_list.append({"HistoFile": 'data',
                                      "SampleCode": 1,
                                      "Type": "data"})

        syst_trees_submit = []
        syst_weights_submit = []

        if self.tree == 'all':
            syst_trees_submit = systematics.syst_trees
            syst_weights_submit = systematics.syst_weights
        else:
            if type(self.tree) == list:
                syst_trees_submit = self.tree
            if self.syst_weight:
                syst_weights_submit = self.syst_weight

        # Makes the submit files
        for sample in self.samples_list:
            submit_file_number = 1
            for r in self.regions:
                folder_string = "mkdir -p {}{}/MC{}/{}/{}/{}\n".format(
                    self.analysis_code_to_results, self.output,
                    self.mc_year, self.year, self.regions[r],
                    sample["HistoFile"])
                region_l = [r, self.regions[r]]
                cond = self.tree == 'all' or self.tree == 'particleLevel'
                cond = cond or \
                    (self.tree == 'nominal' and not syst_weights_submit)
                if cond:
                    with open(
                        self.submit_dir_path + submit_file_name.format(
                            sample["HistoFile"],
                            submit_file_number), 'w') as f:
                        f.write(initial_string)
                        f.write(folder_string)
                        f.write(self.make_submit_job(sample, region_l))
                    submit_file_number += 1

                cond = sample["HistoFile"] != "data"
                cond = cond and sample["Type"] != "SYSTEMATIC"
                if cond:
                    for weight in syst_weights_submit:
                        with open(
                            self.submit_dir_path + submit_file_name.format(
                                sample["HistoFile"],
                                submit_file_number), 'w') as f:
                            f.write(initial_string)
                            f.write(folder_string)
                            f.write(self.make_submit_job(sample, region_l,
                                                         syst_weight=weight))
                        submit_file_number += 1

                    for tree in syst_trees_submit:
                        with open(
                            self.submit_dir_path + submit_file_name.format(
                                sample["HistoFile"],
                                submit_file_number), 'w') as f:
                            f.write(initial_string)
                            f.write(folder_string)
                            f.write(self.make_submit_job(sample, region_l,
                                                         syst_tree=tree))
                        submit_file_number += 1

    def make_scratch_files(self):
        scratch_dir = self.scratch_path + self.output + "/"

        if self.compile:
            if os.path.exists(scratch_dir):
                shutil.rmtree(scratch_dir)
                os.makedirs(scratch_dir)
            else:
                os.makedirs(scratch_dir)

        for sample in self.samples_list:
            for r in self.regions.values():
                scratch_name = "MC{}_{}_{}_{}.txt".format(
                    self.mc_year, self.year, r, sample["HistoFile"])
                with open(scratch_dir + scratch_name, 'w') as f:
                    f.write("000000 {}{}/MC{}/{}/{}/{}/".format(
                        self.analysis_code_to_results, self.output,
                        self.mc_year, self.year, r, sample["HistoFile"]))

    def prepare_and_run_jobs(self):
        self.make_submit_files()
        self.make_scratch_files()

        time.sleep(15)

        submit_list = glob.glob(self.submit_dir_path + "submit*.sh")
        # I think sometimes there are errors related to too many processes
        # trying to access the same file (in the case if syst_weights and
        # syst_trees). This might fix them
        random.shuffle(submit_list)
        for submit_file in submit_list:

            # When you want to run different sample files with the
            # same compiled exec, or when you want to run nominal +
            # systematic weights (hence the data exception)
            if not self.compile:
                is_to_run = False
                for sample in self.samples_list:
                    if sample["HistoFile"] == "data":
                        continue
                    if sample["HistoFile"] in submit_file:
                        is_to_run = True
                        break

                if not is_to_run:
                    continue

            index = submit_file.find("submit_files/")
            while True:
                proc = subprocess.run(['qstat'], stdout=subprocess.PIPE)
                out = proc.stdout.decode('utf8')
                number_of_jobs = out.count('\n')
                if number_of_jobs > 80:
                    time.sleep(300)
                else:
                    break
            subprocess.run(["qsub", submit_file[index+13:]],
                           cwd=self.submit_dir_path)
            time.sleep(5)

        time.sleep(10)

    def run(self, test=False):
        super().run(test)
        self.get_samples_variables(test)
        self.get_regions_and_max_cuts()

        if self.compile:
            self.link_cutfile_and_compile()

        self.prepare_and_run_jobs()

        self.copy_files_to_output_folder()

import Job

import os

class LStore(Job.Job):
    """Class that interfaces between LStore and LipCbrAnalysis"""

    job_name = "LStore"
    required_options = ["Output", "Description"]

    # Arguments of each sample that are taken from a samples file
    samples_variables = ["HistoFile", "DSID", "SampleCode", "MCName"]

    def __init__(self):
        super().__init__()
        self.possible_options += ["Samples", "SystWeights", "SystTrees"]
        self.syst_trees = False
        self.syst_weights = False
        self.samples_file = ""

    def set_options(self):
        super().set_options()

        # Not required options
        if "SystTrees" in self.options_dict:
            aux = self.options_dict["SystTrees"].upper()
            if aux != "TRUE" and aux != "FALSE":
                raise ValueError(self.make_invalid_argument_string("SystTrees",
                    aux))
            if aux == "TRUE":
                self.syst_trees = True

        if "SystWeights" in self.options_dict:
            aux = self.options_dict["SystWeights"].upper()
            if aux != "TRUE" and aux != "FALSE":
                raise ValueError(self.make_invalid_argument_string("SystWeights",
                    aux))
            if aux == "TRUE":
                self.syst_weights = True

        if "Samples" in self.options_dict:
            self.samples_file = self.options_dict["Samples"]


    def make_systematic_trees(self):
        """To be done in the future. Right now it was done manually.
        Don't forget to copy file created to output folder"""
        pass

    def make_systematic_weights(self):
        """To be done in the future. Right now it was done manually
        Don't forget to copy file created to output folder"""
        pass

    def get_samples_variables(self, test=False):
        super().get_samples_variables(test)
        if test:
            self.files_to_copy.append(self.test_text_files_path + \
                    self.samples_file)
            self.samples_list = self.parse_samples_file(
                    self.test_text_files_path + self.samples_file)
        else:
            self.files_to_copy.append(self.input_text_files_path + \
                    self.samples_file)
            self.samples_list = self.parse_samples_file(
                    self.input_text_files_path + self.samples_file)

        for sample in self.samples_list:
            if "MCName" not in sample:
                sample["MCName"] = set()

    def translate_dsid(self):
        """Gets the DSID from lstore_samples file and adds the corresponding
        MCName to the sample
        """
        if self.mc_year == 15:
            lstore_samples = "/lstore/atlas/sg/sw_samples/"
            lstore_samples += "DefineSamples/DefineSamples_MC_15_samples.txt"
        elif self.mc_year == 16:
            lstore_samples = "/lstore/atlas/sg/AT-21.2-2lep/"
            lstore_samples += "DefineSamples/DefineSamples_MC_16_samples.txt"

        mcname_not_found = set()
        with open(lstore_samples) as f:
            # Check if any MCName is not in file
            for sample in self.samples_list:
                for mcname in sample["MCName"]:
                    if mcname not in f.read():
                        mcname_not_found.add(mcname)

            # Translation
            for lines in f:
                lines = lines.split(" ")
                for sample in self.samples_list:
                    if int(lines[3]) in sample["DSID"]:
                        sample["MCName"].add(lines[0])
                        sample["DSID"].remove(int(lines[3]))

        # Checks if any DSID was not found
        dsid_not_found = set()
        for sample in self.samples_list:
            if sample["DSID"]:
                dsid_not_found = dsid_not_found.union(sample["DSID"])

        if dsid_not_found:
            raise LookupError("DSID {} not found in file {}".format(
                dsid_not_found, lstore_samples))
        if mcname_not_found:
            raise LookupError("MCName {} not found in file {}".format(
                mcname_not_found, lstore_samples))

    def make_samples_cxx_file(self, test=False):
        self.get_samples_variables(test)
        self.translate_dsid()

        def make_sample_condition(sample):
            if "HistoFile" not in sample:
                raise TypeError("Missing HistoFile in a sample")
            if "SampleCode" not in sample:
                raise TypeError("Missing SampleCode in a sample")
            if not sample["MCName"]:
                raise TypeError("No sample ID's in a sample")

            condition_string = "/* {} */\n".format(sample["HistoFile"])
            condition_string += "if (Sample == {}) {{\n".format(
                    sample["SampleCode"])
            for mcname in sample["MCName"]:
                condition_string +="    {} = 1;\n".format(mcname)
            condition_string += "}\n\n"

            return condition_string

        samples_symlink_name = "samples_MC{}.cxx".format(self.mc_year)
        samples_path = "../../analysis_deploy/AnalysisCode/"
        samples_cxx_path = samples_path + "Samples/"
        link_file_relative_path = "Samples/"

        samples_cxx_name = self.output + "_samples.cxx"
        with open(samples_cxx_path + samples_cxx_name, 'w') as f:
            for sample in self.samples_list:
                f.write(make_sample_condition(sample))

        try:
            os.unlink(samples_path + samples_symlink_name)
        except FileNotFoundError:
            pass

        os.symlink(link_file_relative_path + samples_cxx_name,
                samples_path+samples_symlink_name)

        self.files_to_copy.append(samples_cxx_path+samples_cxx_name)


    def run(self, test=False):
        super().run(test)

        if self.syst_trees:
            self.make_systematic_trees()
        if self.syst_weights:
            self.make_systematic_weights()
        if self.samples_file:
            self.make_samples_cxx_file(test)

        self.copy_files_to_output_folder()

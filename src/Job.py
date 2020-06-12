from tempfile import mkstemp

import shutil
from shutil import move

import os
from os import fdopen, remove

import systematics


class Job:
    """Parent class of every job."""

    job_name = "Job"
    input_text_files_path = "../input_txt/"
    test_text_files_path = "../test/text_files/"

    # Without any of these options, an exception is raised
    required_options = ["Output", "Description"]

    # With an option that is different from all of these an exception is raised
    # If you want to add another option, you should add its name here
    # You can also add to the children classes
    possible_options = ["Output", "Description", "Year", "MCYear"]

    possible_years = [15, 16, 17, 1516, 151617]
    possible_mc_years = [15, 16]

    def __init__(self):
        # Options dictionary
        self.options_dict = {}

        # Default values of options
        self.year = 1516
        self.mc_year = 16

        self.output_folder = "../../results/"
        # Files to copy to results/job_name folder
        self.files_to_copy = []

    def add_option(self, option):
        self.options_dict[option[0]] = option[1]

    @classmethod
    def verify_required_options(cls, options_dict):
        """Class especific verify required options

        See if all the required options are present
        """

        missing_required_options = [opt for opt in cls.required_options
                                    if opt not in options_dict]

        if missing_required_options:
            raise TypeError("Missing required options {} in job {}".format(
                missing_required_options, cls.job_name))

    @classmethod
    def verify_invalid_options(cls, options_dict):
        """Class especific verify invalid options

        See if there is any option that is not in the possible options
        """

        invalid_options = [opt for opt in options_dict
                           if opt not in cls.possible_options]

        if invalid_options:
            raise TypeError("Invalid options {} in job {}".format(
                invalid_options, cls.job_name))

    def check_required_options(self):
        """Wrapper around verify_required_options"""

        self.verify_required_options(self.options_dict)

    def check_invalid_options(self):
        """Wrapper around verify_invalid_options"""

        self.verify_invalid_options(self.options_dict)

    @classmethod
    def make_invalid_argument_string(cls, option_name, option):
        error_string = "Invalid argument for {} option in".format(option_name)
        error_string += " job {}: {}".format(cls.job_name, option)

        return error_string

    @staticmethod
    def check_systematics(syst_list, syst_type):
        """Checks if syst_list has any elements that are not in systematics.py
        syst_type can be 'weight' or 'tree'
        """
        if syst_type == 'weight':
            syst_check = systematics.syst_weights
        elif syst_type == 'tree':
            syst_check = systematics.syst_trees

        syst_missing = list(filter(lambda x: x not in syst_check, syst_list))

        if syst_missing:
            error_string = "Systematic {}s {} were not found in ".format(
                syst_type, syst_missing)
            error_string += "systematics.py"
            raise LookupError(error_string)

    def set_options(self):
        self.check_invalid_options()
        self.check_required_options()

        # Required options
        self.output = self.options_dict["Output"]
        self.description = self.options_dict["Description"]

        # Not required options
        if "Year" in self.options_dict:
            self.year = int(self.options_dict["Year"])
            if self.year not in self.possible_years:
                raise ValueError("Year {} not valid. Choose from {}".format(
                    self.year, self.possible_years))

        if "MCYear" in self.options_dict:
            self.mc_year = int(self.options_dict["MCYear"])
            if self.mc_year not in self.possible_mc_years:
                raise ValueError("MCYear {} not valid. Choose from {}".format(
                    self.mc_year, self.possible_mc_years))

    @staticmethod
    def find_write_line(fl, name):
        """Finds line where to write output name in results.txt file and returns
        True if it should be replaced
        """

        if os.stat(fl).st_size == 0:
            return (0, False)

        name = name.split(".")

        with open(fl, 'r') as f:
            for i, line in enumerate(f):
                line = line.split(":")[0].split(".")
                if line == name:
                    return (i, True)
                for name_part, line_part in zip(name, line):
                    if name_part < line_part:
                        return (i, False)
                    elif name_part > line_part:
                        break
                    else:
                        continue
            else:
                return (i + 1, False)

    def set_job_output_description(self, test=False):
        if test:
            control_file = self.output_folder + 'results_test.txt'
        else:
            control_file = self.output_folder + 'results.txt'

        # Create file if it does not exist
        f = open(control_file, 'a')
        f.close()

        output_line, replace = self.find_write_line(control_file, self.output)

        fh, abs_path = mkstemp()
        with fdopen(fh, 'w') as new_file:
            if os.stat(control_file).st_size == 0:
                new_file.write("{}: {}\n".format(self.output, self.description))
            else:
                with open(control_file) as old_file:
                    for i, line in enumerate(old_file):
                        if i == output_line:
                            if replace:
                                new_file.write("{}: {}\n".format(self.output,
                                                                 self.description))
                                continue
                            else:
                                new_file.write("{}: {}\n".format(self.output,
                                                                 self.description))
                        new_file.write(line)
                    if i == output_line - 1:
                        new_file.write("{}: {}\n".format(self.output,
                                                         self.description))

        remove(control_file)
        move(abs_path, control_file)

    def create_output_folder(self):
        self.output_folder += self.output + "/"

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def copy_files_to_output_folder(self):
        for f in self.files_to_copy:
            shutil.copy(f, self.output_folder)

    @classmethod
    def parse_samples_file(cls, samples_file):
        """Gets DSIDs and/or MCNames of samples, defined in a samples file"""

        def make_dsid_interval(interval):
            interval = interval.split("-")
            if len(interval) == 1:
                return {int(interval[0])}
            elif len(interval) == 2:
                return set(range(int(interval[0]), int(interval[1])+1))
            else:
                error_string = "Bad DSID number in line {}".format(i)
                error_string += " of samples file of job {}".format(
                    cls.job_name)
                raise TypeError(error_string)

        samples_list = []
        variables = {}

        in_DSID = False
        in_MCName = False
        with open(samples_file) as f:
            for i, lines in enumerate(f):
                if not lines.strip():  # empty line
                    samples_list.append(variables)
                    variables = {}
                    continue
                lines = lines.split(":")
                cond = in_DSID or in_MCName
                if lines[0].strip() in cls.samples_variables or cond:
                    if len(lines) == 2:
                        if lines[0].strip() == "DSID":
                            variables["DSID"] = make_dsid_interval(
                                lines[1].strip())
                            in_DSID = True
                        elif lines[0].strip() == "MCName":
                            variables["MCName"] = \
                                {lines[1].strip()}
                            in_MCName = True
                        else:
                            try:
                                variables[lines[0].strip()] = \
                                    int(lines[1].strip())
                            except ValueError:
                                variables[lines[0].strip()] = \
                                    lines[1].strip()
                            in_DSID = False
                            in_MCName = False
                    elif len(lines) == 1:
                        if in_DSID:
                            variables["DSID"] = variables["DSID"].union(
                                make_dsid_interval(
                                    lines[0].strip()))
                        if in_MCName:
                            variables["MCName"].add(
                                lines[0].strip())
                    else:
                        error_string = "Too many ':' in line {}".format(i)
                        error_string += " of samples file of job {}".format(
                            cls.job_name)
                        raise TypeError(error_string)
            else:
                samples_list.append(variables)

        return samples_list

    def get_samples_variables(self, test=False):
        if test:
            self.files_to_copy.append(self.test_text_files_path +
                                      self.samples_file)
            self.samples_list = self.parse_samples_file(
                self.test_text_files_path + self.samples_file)
        else:
            self.files_to_copy.append(self.input_text_files_path +
                                      self.samples_file)
            self.samples_list = self.parse_samples_file(
                self.input_text_files_path + self.samples_file)

    @staticmethod
    def parse_cut_file(cut_file, need_source_code=False):
        """See the number of cuts in cut file and returns it, along with
        the regions of the analysis

        The source code option was in case I wanted to do a pdf with the cuts
        of each region. Never implemented it, though.
        """
        regions = {}

        with open(cut_file) as f:
            max_cuts = f.read().count("LastCut++;")

        if need_source_code:
            source_code = ['' for cut in range(max_cuts)]

        cut = 0
        in_regions = False

        with open(cut_file) as f:
            for line in f:
                if need_source_code:
                    source_code[cut] += line

                if line.strip() == "LastCut++;":
                    cut += 1

                if line.strip() == "Begin Regions":
                    in_regions = True
                    continue
                if in_regions:
                    if line.strip() == "End Regions":
                        in_regions = False
                    else:
                        line = line.split(':')
                        regions[line[0].strip()] = line[1].strip()

        if need_source_code:
            return max_cuts, regions, source_code
        else:
            return max_cuts, regions

    def run(self, test=False):
        self.set_options()
        self.set_job_output_description(test)
        self.create_output_folder()

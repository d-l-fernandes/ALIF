import Job
import systematics

import subprocess
import time
import shutil
import os
from functools import reduce

from ROOT import TFile

import numpy as np


class TRexFitter(Job.Job):
    """Class that prepares the histograms and config files for the TRexFitter
    job"""

    job_name = "TRexFitter"
    required_options = ["Output", "Description", "Samples", "Regions",
        "NormFactors", "Input"]

    samples_variables = ["Type", "Title", "HistoFile", "FillColor",
            "Group"]
    luminosity = {15: 3.2, 16: 32.9, 17: 43.8, 1516: 36.2, 151617: 80.0}

    trex_path = "../../TRExFitter/"
    trex_to_results = "../results/"

    def __init__(self):
        super().__init__()
        self.possible_options += ["Samples", "Input", "Regions", "NormFactors",
                "SystTree", "SystWeight", "SystAnalysis", "Asimov", "Fit",
                "Limit","ShowData", "Luminosity", "FullAsimov", "POI",
                "ReadFrom", "FileSuffix", "ShowYields", "PrepareSamples",
                "NewFileSuffix", "StatOnly"]
        self.asimov = False
        self.full_asimov = False
        self.syst_weight = []
        self.syst_tree = []
        #self.syst_analysis = []
        self.syst_analysis_file = ""
        self.fit = ["SPLUSB", "CRSR"]
        self.limit = False
        self.show_data = True
        self.lumi_label = 0
        self.poi = "#mu"
        self.read_from = "HIST"
        self.file_suffix = ""
        self.new_file_suffix = ""
        self.show_yields = True
        self.prepare_samples = True
        self.stat_only = False

    def set_options(self):
        super().set_options()

        # Required options
        self.samples_file = self.options_dict["Samples"]
        self.regions_file = self.options_dict["Regions"]
        self.norm_factors_file = self.options_dict["NormFactors"]
        self.input_file = self.options_dict["Input"]

        # Not required options
        if "Asimov" in self.options_dict:
            aux = self.options_dict["Asimov"].upper()
            if aux != "TRUE" and aux != "FALSE":
                raise ValueError(self.make_invalid_argument_string("Asimov",
                    aux))
            if aux == "TRUE":
                self.asimov = True

        if "SystWeight" in self.options_dict:
            if "weight" in self.options_dict["SystWeight"]:
                error_string = "Remove 'weight' from systematic weights"
                raise ValueError(error_string)

            if self.options_dict["SystWeight"] == 'all':
                self.syst_weight = systematics.syst_weights
            else:
                self.syst_weight =  [syst.strip() \
                        for syst in self.options_dict["SystWeight"].split(',')]

                self.check_systematics(self.syst_weight, 'weight')

        if "SystTree" in self.options_dict:
            if self.options_dict["SystTree"] == 'all':
                self.syst_tree = systematics.syst_trees
            else:
                self.syst_tree =  [syst.strip() \
                        for syst in self.options_dict["SystTree"].split(',')]

                self.check_systematics(self.syst_tree, 'tree')

        if "SystAnalysis" in self.options_dict:
            self.syst_analysis_file = self.options_dict["SystAnalysis"]

        #if "SystAnalysis" in self.options_dict:
        #    if not systematics.syst_analysis:
        #        error_string = "No analysis systematics"
        #        raise LookupError(error_string)
#
        #    if self.options_dict["SystAnalysis"] == 'all':
        #        self.syst_analysis = systematics.syst_analysis
        #    else:
        #        self.syst_analysis =  [syst.strip() \
        #                for syst in self.options_dict["SystAnalysis"].split(',')]
        #        for i, syst in enumerate(self.syst_analysis):
        #            wanted_syst = filter(lambda x: x["Title"] == syst,
        #                    systematics.syst_analysis)
        #            if wanted_syst:
        #                self.syst_analysis[i] = wanted_syst[0]
        #            else:
        #                error_string = "Systematic '{}' not found ".format(syst)
        #                error_string += "in systematics.py"
        #                raise LookupError(error_string)

        if "Fit" in self.options_dict:
            aux = [opt.strip().upper()
                    for opt in self.options_dict["Fit"].split('/')]

            if len(aux) != 2:
                raise ValueError(self.make_invalid_argument_string("Fit",
                    '/'.join(aux)))
            if aux[0] != "SPLUSB" and aux[0] != "BONLY":
                error_string = "Invalid first argument for 'Fit'. Only "
                error_string += "SPLUSB and BONLY possible"
                raise ValueError(error_string)

            if aux[1] != "CRSR" and aux[1] != "CRONLY":
                error_string = "Invalid second argument for 'Fit'. Only "
                error_string += "CRSR and CRONLY possible"
                raise ValueError(error_string)

            self.fit = aux

        if "Limit" in self.options_dict:
            aux = self.options_dict["Limit"].upper()
            if aux != "TRUE" and aux != "FALSE":
                raise ValueError(self.make_invalid_argument_string("Limit",
                    aux))
            if aux == "TRUE":
                self.limit = True

        if "ShowData" in self.options_dict:
            aux = self.options_dict["ShowData"].upper()
            if aux != "TRUE" and aux != "FALSE":
                raise ValueError(self.make_invalid_argument_string("ShowData",
                    aux))
            if aux == "FALSE":
                self.show_data = False

        if "Luminosity" in self.options_dict:
            try:
                self.lumi_label = float(self.options_dict["Luminosity"])
            except ValueError:
                error_string = "Invalid value for Luminosity option. "
                error_string += "Only int or float allowed."
                raise ValueError(error_string)

        if "FullAsimov" in self.options_dict:
            if self.asimov:
                raise ValueError("Can't have Asimov and FullAsimov both True")
            aux = self.options_dict["FullAsimov"].upper()
            if aux != "TRUE" and aux != "FALSE":
                raise ValueError(self.make_invalid_argument_string("FullAsimov",
                    aux))
            if aux == "TRUE":
                self.full_asimov = True

        if "POI" in self.options_dict:
            self.poi = self.options_dict["POI"]

        if "ReadFrom" in self.options_dict:
            possible_values = ["HIST", "NTUP"]
            aux = self.options_dict["ReadFrom"].upper()
            if aux not in possible_values:
                error_string = "Invalid value from ReadFrom option. "
                error_string = "Values allowed: {}".format(possible_values)
                raise ValueError(error_string)
            else:
                self.read_from = aux

        if "FileSuffix" in self.options_dict:
            self.file_suffix = self.options_dict["FileSuffix"]

        if "ShowYields" in self.options_dict:
            aux = self.options_dict["ShowYields"].upper()
            if aux != "TRUE" and aux != "FALSE":
                raise ValueError(self.make_invalid_argument_string("ShowYields",
                    aux))
            if aux == "FALSE":
                self.show_yields = False

        if "PrepareSamples" in self.options_dict:
            aux = self.options_dict["PrepareSamples"].upper()
            if aux != "TRUE" and aux != "FALSE" and aux != "ONLY":
                raise ValueError(self.make_invalid_argument_string("PrepareSamples",
                    aux))
            if aux == "FALSE":
                self.prepare_samples = False
            elif aux == "ONLY":
                self.prepare_samples = "ONLY"

        if "NewFileSuffix" in self.options_dict:
            self.new_file_suffix = self.options_dict["NewFileSuffix"]

        if "StatOnly" in self.options_dict:
            aux = self.options_dict["StatOnly"].upper()
            if aux != "TRUE" and aux != "FALSE":
                raise ValueError(self.make_invalid_argument_string("StatOnly",
                    aux))
            if aux == "TRUE":
                self.stat_only = True


    # Histogram related functions
    @staticmethod
    def fill_empty_bins(histo):
        n_bins = histo.GetNbinsX()
        for i in range(n_bins + 1):
            bin_content = histo.GetBinContent(i)
            if bin_content <= 0:
                histo.SetBinContent(i, 1e-12)
                histo.SetBinError(i, 1e-12)

    @staticmethod
    def scale_histo(histo, scale_factor):
        histo.Scale(scale_factor)

    @staticmethod
    def scale_binbybin_histo(histo, scale_dict):
        n_bins = histo.GetNbinsX()
        for i in range(n_bins + 1):
            if i in scale_dict:
                scale_factor = scale_dict[i]
                bin_content = histo.GetBinContent(i)
                bin_error = histo.GetBinError(i)
                histo.SetBinContent(i, bin_content * scale_factor)
                histo.SetBinError(i, bin_error * scale_factor)

    @staticmethod
    def cut_histo(histo, bins_to_keep):
        n_bins = histo.GetNbinsX()
        for i in range(n_bins + 1):
            if i not in bins_to_keep:
                histo.SetBinContent(i,0)
                histo.SetBinError(i,0)

    @staticmethod
    def get_input_histo(f, histo_name, read_from, aux_f=0):
        if read_from == "HIST":
            output = f.Get(histo_name)
        else:
            if aux_f:
                copy_hist = aux_f.Get("sel00_{}".format(histo_name))
            else:
                copy_hist = f.Get("sel00_{}".format(histo_name))
            output = copy_hist.Clone()
            output.Reset()
            output.SetName(histo_name)
            del copy_hist
            tree = f.Get("SelectedEvents")
            for event in tree:
                output.Fill(getattr(event, histo_name), getattr(event,"Weight"))

        return output


    # Input file related functions
    def prepare_input(self, test=False):
        self.get_histo_names(test)
        self.parse_input_file(test)
        self.create_directory_structure()
        if self.prepare_samples:
            self.make_histograms()

    def make_histograms(self):
        folder_template = "../../results/{}/MC{}/{}/{}/{}/"
        for option in self.input_file_options:
            input_folder = folder_template.format(option["Folder"],
                    self.mc_year, self.year, option["Region"],
                    option["Sample"])
            output_folder = folder_template.format(self.output,
                    self.mc_year, self.year, option["Region"],
                    option["Sample"])

            # In case of null pointer
            # print(input_folder)

            if not option["ExcludeFromSystematics"]:
                histo_file_list = self.syst_weight + self.syst_tree + \
                        ["nominal"]
            else:
                histo_file_list = ["nominal"]

            for histo_file in histo_file_list:
                print(input_folder + histo_file + self.file_suffix
                    + ".root/", end='')

                # Needs a file with sel00_histo_file to get correct
                # histogram axes
                if self.read_from == "NTUP" and self.file_suffix:
                    aux_file = TFile.Open(input_folder + "{}.root".format(
                                          histo_file))

                if self.file_suffix:
                    input_file = TFile.Open(input_folder + "{}.root".format(
                        histo_file+self.file_suffix))
                else:
                    input_file = TFile.Open(input_folder + "{}.root".format(
                        histo_file))

                if self.new_file_suffix:
                    output_file = TFile.Open(output_folder + "{}.root".format(
                        histo_file+self.new_file_suffix), "recreate")
                elif self.file_suffix:
                    output_file = TFile.Open(output_folder + "{}.root".format(
                        histo_file+self.file_suffix), "recreate")
                else:
                    output_file = TFile.Open(output_folder + "{}.root".format(
                        histo_file), "recreate")

                for h_name in self.region_histo_map[option["Region"]]:
                    print(h_name)
                    if self.read_from == "NTUP" and self.file_suffix:
                        input_histo = self.get_input_histo(input_file, h_name,
                                                      self.read_from, aux_file)
                    else:
                        input_histo = self.get_input_histo(input_file, h_name,
                                                      self.read_from)

                    output_file.cd()
                    output_histo = input_histo.Clone()

                    self.fill_empty_bins(output_histo)

                    if option["Scale"]:
                        self.scale_histo(output_histo, option["Scale"])
                    if option["Cut"]:
                        self.cut_histo(output_histo, option["Cut"])
                    if option["ScaleBinByBin"]:
                        self.scale_binbybin_histo(output_histo,
                                option["ScaleBinByBin"])

                    output_file.Write()
                input_file.Close()
                output_file.Close()

        if self.full_asimov:
            for r, h_list in self.region_histo_map.items():
                output_folder = folder_template.format(self.output,
                        self.mc_year,self.year, r, "data")

                if self.new_file_suffix:
                    output_file = TFile.Open(
                        output_folder + "nominal{}.root".format(self.new_file_suffix),
                        "recreate")
                elif self.file_suffix:
                    output_file = TFile.Open(
                        output_folder + "nominal{}.root".format(self.file_suffix),
                        "recreate")
                else:
                    output_file = TFile.Open(output_folder + "nominal.root",
                        "recreate")

                for h_name in h_list:
                    for i,sample in enumerate(self.samples_list):

                        if sample["Type"] == "SYSTEMATIC":
                            continue
                        input_folder = folder_template.format(self.output,
                                self.mc_year, self.year, r, sample["HistoFile"])

                        if self.new_file_suffix:
                            input_file = TFile.Open(
                                input_folder + "nominal{}.root".format(self.new_file_suffix))
                        elif self.file_suffix:
                            input_file = TFile.Open(
                                input_folder + "nominal{}.root".format(self.file_suffix))
                        else:
                            input_file = TFile.Open(input_folder + "nominal.root")

                        input_histo = input_file.Get(h_name)
                        output_file.cd()
                        if i == 0:
                            output_histo = input_histo.Clone()
                        else:
                            output_histo.Add(input_histo)

                        input_file.Close()

                    output_file.Write()

                output_file.Close()

    def create_directory_structure(self):
        folder_name = "../../results/{0}/MC{1}/{2}/".format(self.output,
                self.mc_year, self.year)
        for r in self.regions:
            for sample in self.samples_list:
                leaf_name = folder_name + "{}/{}/".format(r,
                        sample["HistoFile"])

                if not os.path.exists(leaf_name):
                    os.makedirs(leaf_name)

            if not self.asimov:
                leaf_name = folder_name + "{}/{}/".format(r,
                        'data')
                if not os.path.exists(leaf_name):
                    os.makedirs(leaf_name)

    def get_histo_names(self, test=False):
        """Gets histogram names from regions file"""
        if test:
            regions_file_name = self.test_text_files_path + self.regions_file
        else:
            regions_file_name = self.input_text_files_path + self.regions_file

        self.histo_names = []
        self.regions = []
        with open(regions_file_name) as f:
            for lines in f:
                lines = lines.strip('\n').strip()
                lines = lines.split(":")
                if lines[0] == "HistoName":
                    self.histo_names.append(lines[1].strip().strip('"'))
                elif lines[0] == "HistoPathSuff":
                    self.regions.append(lines[1].strip().strip('"').strip('/'))

        self.region_histo_map = {}
        for i, r in enumerate(self.regions):
            if r in self.region_histo_map:
                self.region_histo_map[r].append(self.histo_names[i])
            else:
                self.region_histo_map[r] = []
                self.region_histo_map[r].append(self.histo_names[i])

    @staticmethod
    def get_mu_value(folder_name):

        folder_name = folder_name.split("@")

        fit_file_name = "../../results/{0}/{0}_TRexFitter/Fits/job_{0}.txt".format(
                folder_name[0])


        if len(folder_name) == 2:
            scale_variable = folder_name[1]
        else:
            scale_variable = "#mu"

        with open(fit_file_name) as f:
            for line in f:
                line = line.strip().split()
                if line == "":
                    continue
                if line[0] == scale_variable:
                    return float(line[1])
            else:
                raise LookupError("No {} found in file {}".format(scale_variable,
                    fit_file_name))

    def get_scale_factor(self, scale_string):

        def find_matching_closing_bracket(s):
            open_brackets = 1
            for i, ch in enumerate(s):
                if ch == "(":
                    open_brackets += 1
                elif ch == ")":
                    open_brackets -= 1
                    if open_brackets == 0:
                        return i+1
            else:
                error_string = "No matching closing parens in scale factor of"
                error_string += " job {}".format(self.output)
                raise IndexError(error_string)

        def get_operands(s):
            operands = []

            in_operand = False
            i = 0
            operand_begin = i
            while i < len(s):
                if s[i] == "(":
                    closing_bracket = find_matching_closing_bracket(s[i+1:])
                    operands.append(s[i:i+closing_bracket+1])
                    i += closing_bracket
                elif s[i] == " ":
                    if in_operand:
                        operands.append(s[operand_begin:i])
                    in_operand = False
                else:
                    if not in_operand:
                        operand_begin = i
                    in_operand = True
                i += 1
            else:
                if in_operand:
                    operands.append(s[operand_begin:])

            return operands

        def calculate_operand(oper):
            # Operand is another calculation
            if "(" in oper:
                return self.get_scale_factor(oper)
            elif '"' in oper:
                return self.get_mu_value(oper.strip('"'))
            else:
                return float(oper)

        # No calculations
        if "(" not in scale_string:
            return calculate_operand(scale_string.strip())

        # Remove outer parentheses
        scale_string = scale_string.strip()[1:-1]

        # Get operator
        operator = scale_string.strip()[0]

        # Remove operator
        scale_string = scale_string.strip()[1:].strip()

        operands = get_operands(scale_string)

        if operator == "+":
            result =  reduce(lambda a, x: a + calculate_operand(x),
                    operands, 0)
        elif operator == "*":
            result =  reduce(lambda a, x: a * calculate_operand(x),
                    operands, 1)
        elif operator == "-":
            result =  reduce(lambda a, x: a - calculate_operand(x),
                    operands[1:], calculate_operand(operands[0]))
        elif operator == "/":
            result =  reduce(lambda a, x: a / calculate_operand(x),
                    operands[1:], calculate_operand(operands[0]))
        elif operator == "v":
            if len(operands) != 1:
                raise ValueError("v operator only takes one operand")
            result = np.sqrt(calculate_operand(operands[0]))

        return round(result, 5)

    def update_input_file_options(self, opt_dict):

        def check_if_input_folder_exists(folder_name):
            folder_name = "../../results/" + folder_name

            return os.path.exists(folder_name)

        if "Sample" not in opt_dict:
            opt_dict["Sample"] = 'all'
        if "Region" not in opt_dict:
            opt_dict["Region"] = 'all'

        if opt_dict["Sample"] == 'all':
            updated_input_options = self.input_file_options
        else:
            samples_to_update = [sample.strip()
                    for sample in opt_dict["Sample"].split(",")]
            updated_input_options = list(filter(lambda x:
                    x["Sample"] in samples_to_update, self.input_file_options))

        if opt_dict["Region"] != 'all':
            regions_to_update = [region.strip()
                    for region in opt_dict["Region"].split(",")]
            updated_input_options = list(filter(lambda x:
                    x["Region"] in regions_to_update, updated_input_options))


        if "Folder" in opt_dict:
            # Check if opt_dict["Folder"] exists
            if not check_if_input_folder_exists(opt_dict["Folder"]):
                raise RuntimeError("results/{} does not exist".format(
                    opt_dict["Folder"]))

            for opt in updated_input_options:
                opt["Folder"] = opt_dict["Folder"]

        if "Scale" in opt_dict:
            scale_factor = self.get_scale_factor(opt_dict["Scale"])

            for opt in updated_input_options:
                opt["Scale"] = scale_factor

        if "Cut" in opt_dict:
            opt_dict["Cut"] = [opt.strip()
                    for opt in opt_dict["Cut"].split(",")]

            cut_list = []
            for cut in opt_dict["Cut"]:
                cut = cut.split("-")
                if len(cut) == 1:
                    cut_list += [int(cut[0])]
                elif len(cut) == 2:
                    cut_list += list(range(int(cut[0]), int(cut[1])+1))

            for opt in updated_input_options:
                opt["Cut"] = cut_list[:]

        if "ExcludeFromSystematics" in opt_dict:
            cond = opt_dict["ExcludeFromSystematics"].upper()
            if cond == "TRUE":
                cond = True
            elif cond == "FALSE":
                cond = False

            for opt in updated_input_options:
                opt["ExcludeFromSystematics"] = cond

        if "ScaleBinByBin" in opt_dict:
            opt_dict["ScaleBinByBin"] = [opt.strip()
                    for opt in opt_dict["ScaleBinByBin"].split(",")]
            bins = {}

            for b in opt_dict["ScaleBinByBin"]:
                b = b.split("->")

                bins[int(b[0])] = self.get_scale_factor(b[1])

            for opt in updated_input_options:
                opt["ScaleBinByBin"] = bins

        if "ExcludeFromRegions" in opt_dict:
            cond = opt_dict["ExcludeFromRegions"].upper()
            if cond == "TRUE":
                cond = True
            elif cond == "FALSE":
                cond = False

            for opt in updated_input_options:
                opt["ExcludeFromRegions"] = cond

        if "Signal" in opt_dict:
            cond = opt_dict["Signal"].upper()
            if cond == "TRUE":
                cond = True
            elif cond == "FALSE":
                cond = False

            for opt in updated_input_options:
                opt["Signal"] = cond

    def parse_input_file(self, test=False):
        if test:
            input_file_name = self.test_text_files_path + self.input_file
        else:
            input_file_name = self.input_text_files_path + self.input_file

        self.files_to_copy.append(input_file_name)

        self.input_file_options = []
        # Default value for input options for every sample in samples_list
        for sample in self.samples_list:
            for region in self.regions:
                opt_dict = {}
                opt_dict["Sample"] = sample["HistoFile"]
                opt_dict["Region"] = region
                opt_dict["Folder"] = ""
                opt_dict["Scale"] = 1
                opt_dict["Cut"] = []
                opt_dict["ScaleBinByBin"] = {}
                if sample["Type"] == "SYSTEMATIC":
                    opt_dict["ExcludeFromSystematics"] = True
                    opt_dict["Type"] = "SYSTEMATIC"
                else:
                    opt_dict["ExcludeFromSystematics"] = False
                    opt_dict["Type"] = "SAMPLE"
                opt_dict["ExcludeFromRegions"] = False
                opt_dict["Signal"] = False
                self.input_file_options.append(opt_dict)

        # Default value for data
        if (not self.asimov) and (not self.full_asimov):
            for region in self.regions:
                opt_dict = {}
                opt_dict["Sample"] = "data"
                opt_dict["Region"] = region
                opt_dict["Folder"] = ""
                opt_dict["Scale"] = 1
                opt_dict["Cut"] = []
                opt_dict["ScaleBinByBin"] = {}
                opt_dict["ExcludeFromSystematics"] = True
                opt_dict["ExcludeFromRegions"] = False
                opt_dict["Signal"] = False
                opt_dict["Type"] = "DATA"
                self.input_file_options.append(opt_dict)

        opt_dict = {}
        with open(input_file_name) as f:
            for lines in f:
                lines = lines.strip()
                if not lines:
                    self.update_input_file_options(opt_dict)
                    opt_dict = {}
                    continue
                lines = lines.split(":")
                opt_dict[lines[0].strip()] = lines[1].strip()
            else:
                self.update_input_file_options(opt_dict)

        missing_folder_option = list(filter(lambda x: not x["Folder"],
                self.input_file_options))

        if missing_folder_option:
            error_string = "Missing 'Folder' option in input file of TRexFitter"
            error_string += " job."
            raise TypeError(error_string)

        # Gets Samples excluded from systematics
        self.excluded_samples = {x["Sample"]
                for x in self.input_file_options
                if x["ExcludeFromSystematics"] and x["Type"] == "SAMPLE"}

        # Gets excluded regions from each sample
        for sample in self.samples_list:
            excluded_regions = [input_opt["Region"]
                    for input_opt in list(filter(
                        lambda x: x["Sample"] == sample["HistoFile"] and
                                  x["ExcludeFromRegions"],
                                  self.input_file_options))]
            if excluded_regions:
                sample["Exclude"] = ",".join(excluded_regions)

        # Changes samples Type to SIGNAL if it has Signal == True
        # Changes original SIGNAL to BACKGROUND
        samples_to_signal = {x["Sample"]
                for x in self.input_file_options if x["Signal"]}

        if samples_to_signal:
            signal_samples = list(filter(lambda x: x["Type"] == "SIGNAL",
                self.samples_list))
            samples_to_change = list(filter(lambda x:
                x["HistoFile"] in samples_to_signal, self.samples_list))

            for sample in signal_samples:
                sample["Type"] = "BACKGROUND"

            for sample in samples_to_change:
                sample["Type"] = "SIGNAL"


    # Functions that make the strings for the config file
    @staticmethod
    def make_header_string(section):
        header_string = "%"*(len(section)+4) + "\n"
        header_string += "% {} %\n".format(section)
        header_string += "%"*(len(section)+4) + "\n\n"

        return header_string

    @staticmethod
    def make_section_string(header_name, section_name, options):
        section_string = "{}: \"{}\"\n".format(header_name, section_name)
        for opt in options:
            section_string += "  {}: {}\n".format(opt, options[opt])
        section_string += "\n"

        return section_string

    def make_job_string(self):
        opt_dict = {"Label": "\"{}\"".format(self.output),
                    "CmeLabel": "\"13 TeV\"",
                    #"CMELabel": "\"13 TeV\"",
                    "ReadFrom": "HIST",
                    "POI": "\"{}\"".format(self.poi),
                    "HistoPath": "\"{}{}/MC{}/{}/\"".format(
                        self.trex_to_results, self.output, self.mc_year,
                        self.year),
                    "HistoChecks": "NOCRASH",
                    "SplitHistoFiles": "TRUE",
                    "DebugLevel": "0",
                    "AtlasLabel": "Work in Progress",
                    }
        if self.show_yields:
            opt_dict["PlotOptions"] = "YIELDS"

        if self.lumi_label:
            lumi = "scaled to {}".format(self.lumi_label)
        else:
            lumi = self.luminosity[self.year]

        if self.syst_weight or self.syst_tree or self.syst_analysis_file:
            #opt_dict["SystCategoryTables"] = "TRUE"
            #opt_dict["SystPruningNorm"] = "0.005"
            #opt_dict["SystPruningShape"] = "0.001"
            opt_dict["CorrelationThreshold"] = "0.15"


        opt_dict["LumiLabel"] = "\"{} fb^{{-1}}\"".format(lumi)

        return self.make_header_string("Job") + \
            self.make_section_string("Job", "job_" + self.output, opt_dict)

    def make_myoptions_string(self):
        opt_dict = {"NoPrePostFit": "1",
                    #"ShowJobName": "0",
                    }

        if (not self.show_data) or self.asimov:
            #opt_dict["PlotData"] = "0"
            opt_dict["ShowRatio"] = "0"
        else:
            opt_dict["ShowRatio"] = "1"

        return self.make_header_string("My Options") + \
            self.make_section_string("Options", "myoptions_" + \
                self.output, opt_dict)

    def make_fit_string(self):
        opt_dict = {"FitType": self.fit[0],
                    "FitRegion": self.fit[1]
                    }

        if self.asimov:
            opt_dict["FitBlind"] = "TRUE"

        #if self.stat_only:
        #    opt_dict["StatOnlyFit"] = "TRUE"
        #opt_dict["DoNonProfileFit"] = "TRUE"

        return self.make_header_string("Fit") + \
            self.make_section_string("Fit", "fit_" + self.output, opt_dict)

    def make_limit_string(self):
        opt_dict = {"LimitType": "ASYMPTOTIC"}

        if self.asimov:
            opt_dict["LimitBlind"] = "TRUE"

        return self.make_header_string("Limit") + \
            self.make_section_string("Limit", "limit_" + self.output, opt_dict)

    def make_regions_string(self, test=False):
        regions_string = self.make_header_string("Regions")

        if test:
            self.files_to_copy.append(self.test_text_files_path + \
                    self.regions_file)

            with open(self.test_text_files_path + self.regions_file) as f:
                regions_string += f.read()
        else:
            self.files_to_copy.append(self.input_text_files_path + \
                    self.regions_file)
            with open(self.input_text_files_path + self.regions_file) as f:
                regions_string += f.read()

        regions_string += "\n"
        return regions_string

    def make_samples_string(self):
        samples_string = self.make_header_string("Samples")

        if not self.asimov or self.full_asimov:
            opt_dict = {"Type": "DATA",
                        "Title": "\"Data\"",
                        "HistoPath": "\"data\""
                        }
            if self.new_file_suffix:
                histofile = "\"nominal{}\"".format(self.new_file_suffix)
            elif self.file_suffix:
                histofile = "\"nominal{}\"".format(self.file_suffix)
            else:
                histofile = "\"nominal\""

            opt_dict["HistoFile"] = histofile
            samples_string += self.make_section_string("Sample", "data",
                    opt_dict)

        for sample in self.samples_list:
            opt_dict = {}
            if sample["Type"].upper() == "SYSTEMATIC":
                continue
            for opt in sample:
                if opt == "HistoFile":
                    if self.new_file_suffix:
                        histofile = "\"nominal{}\"".format(self.new_file_suffix)
                    elif self.file_suffix:
                        histofile = "\"nominal{}\"".format(self.file_suffix)
                    else:
                        histofile = "\"nominal\""
                    opt_dict["HistoFile"] = histofile
                    opt_dict["HistoPath"] = '"{}"'.format(sample[opt])
                    continue
                if opt == "Title":
                    opt_dict["Title"] = '"{}"'.format(sample[opt])
                    continue
                opt_dict[opt] = sample[opt]

            samples_string += self.make_section_string("Sample",
                    sample["HistoFile"], opt_dict)

        return samples_string

    def make_norm_factors_string(self, test=False):
        norm_factors_string = self.make_header_string("NormFactors")

        if test:
            self.files_to_copy.append(self.test_text_files_path + \
                    self.norm_factors_file)

            with open(self.test_text_files_path + self.norm_factors_file) as f:
                norm_factors_string += f.read()
        else:
            self.files_to_copy.append(self.input_text_files_path + \
                    self.norm_factors_file)
            with open(self.input_text_files_path + self.norm_factors_file) as f:
                norm_factors_string += f.read()

        norm_factors_string += "\n"
        return norm_factors_string

    def make_systematic_analysis_string(self):
        syst_analysis_string = self.make_header_string("Analysis Systematics")

        self.files_to_copy.append(self.input_text_files_path + \
                self.syst_analysis_file)
        with open(self.input_text_files_path + self.syst_analysis_file) as f:
            syst_analysis_string += f.read()

        syst_analysis_string += "\n"
        return syst_analysis_string

    #def make_systematic_analysis_string(self):
    #    syst_analysis_string = self.make_header_string("Analysis Systematics")
    #
    #    for analysis_dict in self.syst_analysis:
    #        syst_analysis_string += self.make_section_string("Systematic",
    #                analysis_dict["Title"], analysis_dict)
    #
    #    return syst_analysis_string

    def make_systematic_weights_string(self):
        syst_weights_string = self.make_header_string("Systematic Weights")

        for weight in self.syst_weight:
            opt_dict = {}

            down_index = weight.find("down")
            DOWN_index = weight.find("DOWN")

            if down_index != -1:
                opt_dict["Title"] = '{}'.format(weight[:down_index-1])
                opt_dict["HistoFileUp"] = '"' + weight[:down_index] + "up" + \
                        weight[down_index+4:] + '"'
            elif DOWN_index != -1:
                opt_dict["Title"] = '{}'.format(weight[:DOWN_index-1])
                opt_dict["HistoFileUp"] = '"' + weight[:DOWN_index] + "UP" + '"'
                if "pileup" in weight:
                    opt_dict["Smoothing"] = "40"
            else:
                # For weights that have "up" in the name
                continue

            opt_dict["Type"] = "HISTO"
            opt_dict["Symmetrisation"] = "TwoSided"
            opt_dict["Category"] = "Instrumental"
            opt_dict["HistoFileDown"] = '"{}"'.format(weight)

            if self.new_file_suffix:
                opt_dict["HistoFileUp"] = \
                    opt_dict["HistoFileUp"][:-1] + self.new_file_suffix + '"'
                opt_dict["HistoFileDown"] = \
                    opt_dict["HistoFileDown"][:-1] + self.new_file_suffix + '"'
            elif self.file_suffix:
                opt_dict["HistoFileUp"] = \
                    opt_dict["HistoFileUp"][:-1] + self.file_suffix + '"'
                opt_dict["HistoFileDown"] = \
                    opt_dict["HistoFileDown"][:-1] + self.file_suffix + '"'

            if self.excluded_samples:
                opt_dict["Exclude"] = ','.join(self.excluded_samples)

            syst_weights_string += self.make_section_string("Systematic",
                    opt_dict["Title"], opt_dict)

        return syst_weights_string

    def make_systematic_trees_string(self):
        syst_trees_string = self.make_header_string("Systematic Trees")

        for tree in self.syst_tree:
            opt_dict = {}

            down_index = tree.find("down")
            Down_index = tree.find("Down")

            if down_index != -1:
                opt_dict["Title"] = '{}'.format(tree[:down_index])
                opt_dict["HistoFileUp"] = '"' + tree[:down_index] + "up" + '"'
                opt_dict["HistoFileDown"] = '"{}"'.format(tree)
                opt_dict["Symmetrisation"] = "TwoSided"
            elif Down_index != -1:
                opt_dict["Title"] = '{}'.format(tree[:Down_index-1])
                opt_dict["HistoFileUp"] = '"' + tree[:Down_index] + "UP" + '"'
                opt_dict["HistoFileDown"] = '"{}"'.format(tree)
                opt_dict["Symmetrisation"] = "TwoSided"
            # Only has up
            elif tree == "JET_JER_SINGLE_NP__1up":
                opt_dict["Title"] = '"{}"'.format(tree)
                opt_dict["HistoFileUp"] = '"{}"'.format(tree)
                opt_dict["Symmetrisation"] = "OneSided"
            elif "up" in tree or "UP" in tree:
                continue
            else:
                opt_dict["Title"] = '"{}"'.format(tree)
                opt_dict["HistoFileUp"] = '"{}"'.format(tree)
                opt_dict["Symmetrisation"] = "OneSided"

            opt_dict["Smoothing"] = "40"
            opt_dict["Type"] = "HISTO"
            opt_dict["Category"] = "Instrumental"

            if self.new_file_suffix:
                opt_dict["HistoFileUp"] = \
                    opt_dict["HistoFileUp"][:-1] + self.new_file_suffix + '"'
                opt_dict["HistoFileDown"] = \
                    opt_dict["HistoFileDown"][:-1] + self.new_file_suffix + '"'
            elif self.file_suffix:
                opt_dict["HistoFileUp"] = \
                    opt_dict["HistoFileUp"][:-1] + self.file_suffix + '"'
                opt_dict["HistoFileDown"] = \
                    opt_dict["HistoFileDown"][:-1] + self.file_suffix + '"'

            if self.excluded_samples:
                opt_dict["Exclude"] = ','.join(self.excluded_samples)

            syst_trees_string += self.make_section_string("Systematic",
                    opt_dict["Title"], opt_dict)

        return syst_trees_string

    def make_config_file(self, test=False):

        self.config_name = "config_{}.config".format(self.output)

        with open(self.output_folder + self.config_name, 'w') as f:
            f.write(self.make_job_string())
            f.write(self.make_myoptions_string())
            f.write(self.make_fit_string())
            if self.limit:
                f.write(self.make_limit_string())
            f.write(self.make_regions_string(test))
            f.write(self.make_samples_string())
            f.write(self.make_norm_factors_string(test))
            if self.syst_weight:
                f.write(self.make_systematic_weights_string())
            if self.syst_tree:
                f.write(self.make_systematic_trees_string())
            if self.syst_analysis_file:
                f.write(self.make_systematic_analysis_string())

    def run_TRex(self):

        trex_home = "/home/lipc/atlas/dfernandes/"
        trex_home += "analyses/sw_13TeV/analysisAlgo/TRExFitter"
        os.environ["TREXFITTER_HOME"] = trex_home

        if self.limit:
            trex_opts = ['h', 'd', 'w', 'f',
                         #'i',
                         'l', 'p']
        else:
            trex_opts = [
                'h',
                'd',
                'w',
                'f',
                #'i',
                'p'
                ]

        for opt in trex_opts:

            # Tries to make plots until no error is given (it happens sometimes)
            if opt == "d" or opt == 'p':
                i = 0
                while True:
                    i += 1
                    proc = subprocess.run(['./myFit.exe', opt,
                        self.trex_to_results + self.output + '/' + self.config_name],
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                        cwd=self.trex_path)
                    out = proc.stdout.decode("utf8")
                    if "segmentation violation" not in out:
                        print(out)
                        break

                    print("Seg violation... Trying again. (Tried {} time(s))".format(i))
            elif opt == "i":
                subprocess.run(['./myFit.exe', opt,
                    self.trex_to_results + self.output + '/' + self.config_name,
                    "GroupedImpact=\"Gammas\""],
                    cwd=self.trex_path)

                if self.syst_tree or self.syst_weight or self.syst_analysis_file:
                    subprocess.run(['./myFit.exe', opt,
                        self.trex_to_results + self.output + '/' + self.config_name,
                        "GroupedImpact=\"FullSyst\"",],
                        cwd=self.trex_path)
            else:
                subprocess.run(['./myFit.exe', opt,
                    self.trex_to_results + self.output + '/' + self.config_name],
                    cwd=self.trex_path)

        folder_name = self.output_folder + "{}_TRexFitter".format(self.output)
        if os.path.exists(folder_name):
            shutil.rmtree(folder_name)

        shutil.move(self.trex_path + "job_" + self.output, folder_name)

    def run(self, test=False):
        # Waits if LipCbrAnalysis is running
        while True:
            proc = subprocess.run(['qstat'], stdout=subprocess.PIPE)
            out = proc.stdout.decode('utf8')
            number_of_jobs = out.count('\n')
            if number_of_jobs != 0:
                break
                # time.sleep(60)
            else:
                break

        super().run(test)
        self.get_samples_variables(test)
        self.prepare_input(test)

        if self.prepare_samples != "ONLY":
            self.make_config_file(test)

        self.copy_files_to_output_folder()

        if self.prepare_samples != "ONLY":
            self.run_TRex()

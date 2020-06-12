import Job

import os
import shutil
import glob
import subprocess

from collections import OrderedDict

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from ROOT import TFile
import root_numpy

class Plotting(Job.Job):
    """Class that does the plotting of all the variables and compares them"""

    job_name = "Plotting"

    required_options = ["Output", "Description", "Samples", "CutFile", "Input"]

    samples_variables = ["Type", "Title", "HistoFile", "Group"]
    possible_plot_tests = ["Ratio"]

    analysis_code_path = "../../analysis_deploy/AnalysisCode/"
    cut_file_path = analysis_code_path + "DoCuts/"

    def __init__(self):
        super().__init__()
        self.possible_options += ["Samples", "CutFile", "Input", "PlotAll",
                "ShowData", "PlotSignalStacked", "FromCut", "OrderSamples",
                "PlotTest", "ShowOverUnderFlow", "Cuts"]
        self.show_data = True
        self.plot_all = False
        self.plot_signal_stacked = True
        self.plot_test = ""
        self.from_cut = 0
        self.order_samples = False
        self.show_over_under_flow = False
        self.cuts = []

    def set_options(self):
        super().set_options()

        # Required options
        self.samples_file = self.options_dict["Samples"]
        self.cut_file = self.options_dict["CutFile"]
        self.input_file = self.options_dict["Input"]

        # Not required options
        if "ShowData" in self.options_dict:
            aux = self.options_dict["ShowData"].upper()
            if aux != "TRUE" and aux != "FALSE":
                raise ValueError(self.make_invalid_argument_string("ShowData",
                    aux))
            if aux == "FALSE":
                self.show_data = False

        if "PlotAll" in self.options_dict:
            aux = self.options_dict["PlotAll"].upper()
            if aux != "TRUE" and aux != "FALSE":
                raise ValueError(self.make_invalid_argument_string("PlotAll",
                    aux))
            if aux == "TRUE":
                self.plot_all = True

        if "PlotSignalStacked" in self.options_dict:
            aux = self.options_dict["PlotSignalStacked"].upper()
            if aux != "TRUE" and aux != "FALSE":
                raise ValueError(self.make_invalid_argument_string("PlotSignalStacked",
                    aux))
            if aux == "FALSE":
                self.plot_signal_stacked = False

        if "PlotTest" in self.options_dict:
            if self.options_dict["PlotTest"] not in self.possible_plot_tests:
                raise ValueError(self.make_invalid_argument_string("PlotTest",
                    self.options_dict["PlotTest"]))
            else:
                self.plot_test = self.options_dict["PlotTest"]

        if "FromCut" in self.options_dict:
            try:
                self.from_cut = int(self.options_dict["FromCut"])
            except ValueError:
                raise ValueError(self.make_invalid_argument_string("FromCut",
                    self.options_dict["FromCut"]))

        if "OrderSamples" in self.options_dict:
            aux = self.options_dict["OrderSamples"].upper()
            if aux != "TRUE" and aux != "FALSE":
                raise ValueError(self.make_invalid_argument_string("OrderSamples",
                    aux))
            if aux == "TRUE":
                self.order_samples = True

        if "ShowOverUnderFlow" in self.options_dict:
            aux = self.options_dict["ShowOverUnderFlow"].upper()
            if aux != "TRUE" and aux != "FALSE":
                raise ValueError(self.make_invalid_argument_string("ShowOverUnderFlow",
                    aux))
            if aux == "TRUE":
                self.show_over_under_flow = True

        if "Cuts" in self.options_dict:
            self.cuts = [c.strip() for c in self.options_dict["Cuts"].split(",")]

            for i, c in enumerate(self.cuts):
                try:
                    self.cuts[i] = int(self.cuts[i])
                except ValueError:
                    raise ValueError("Cuts {} not valid.".format(
                        self.cuts[i]))

    def get_samples_variables(self, test=False):
        super().get_samples_variables(test)

        # Add Data
        if self.show_data:
            data_dict = {}
            data_dict["Type"] = "DATA"
            data_dict["Title"] = "Data"
            data_dict["HistoFile"] = "data"
            self.samples_list.append(data_dict)

        # Groups
        self.groups = {x["Group"] for x in self.samples_list
                if "Group" in x and x["Type"] != "SYSTEMATIC"}

        # Ungrouped samples
        self.ungrouped_samples_list = list(filter(lambda x:
            "Group" not in x and x["Type"] != "SYSTEMATIC", self.samples_list))

        # Assign color to variables and Groups
        n_samples = len(self.groups) + len(self.ungrouped_samples_list)

        cmap = self.get_cmap(n_samples + 1)
        self.sample_colors = {}
        for i, g in enumerate(self.groups):
            self.sample_colors[g] = cmap(i)
        for i, s in enumerate(self.ungrouped_samples_list):
            # For Latex
            if "#" in s["Title"]:
                title = "$"+s["Title"].replace("#", "\\")+"$"
                s["Title"] = title # To be able to filter when plotting
            else:
                title = s["Title"]
            self.sample_colors[title] = cmap(i + len(self.groups))

    @staticmethod
    def get_cmap(n, name='hsv'):
        '''Returns a function that maps each index in 0, 1,..., n-1 to a
        distinct RGB color; the keyword argument name must be a standard mpl
        colormap name.'''
        return plt.cm.get_cmap(name, n)

    def get_regions_and_max_cuts(self):
        """Gets regions name and code from CutFile as well as MaxCuts"""
        self.files_to_copy.append(self.cut_file_path + self.cut_file)
        self.max_cuts, self.regions = self.parse_cut_file(self.cut_file_path + \
                self.cut_file)

        if self.max_cuts < self.from_cut:
            error_string = "FromCut option greater than MaxCuts"
            raise ValueError(error_string)

        if not self.cuts:
            self.cut_interval = list(range(self.from_cut, self.max_cuts+1))
        else:
            invalid_cut = list(filter(lambda c:
                c > self.max_cuts, self.cuts))
            if invalid_cut:
                raise ValueError("Cuts options has value greater than MaxCuts")
            else:
                self.cut_interval = self.cuts


        self.regions = list(self.regions.values())

    def prepare_input(self, test=False):
        self.parse_input_file(test)
        self.get_histo_names_and_titles()
        self.create_plot_folders()

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

        if "Test" in opt_dict:
            cond = opt_dict["Test"].upper()
            if cond == "TRUE":
                cond = True
            elif cond == "FALSE":
                cond = False

            for opt in updated_input_options:
                opt["Test"] = cond

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
                opt_dict["Test"] = False
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
            error_string = "Missing 'Folder' option in input file of Plotting"
            error_string += " job."
            raise TypeError(error_string)

        # Change Test option of data to False
        data = list(filter(lambda x: x["Sample"] == "data",
            self.input_file_options))

        for opt in data:
            opt["Test"] = False

    def get_histo_names_and_titles(self):
        input_sample = self.input_file_options[0]

        folder_name = "../../results/{}/MC{}/{}/{}/{}/".format(
                input_sample["Folder"], self.mc_year, self.year,
                input_sample["Region"], input_sample["Sample"])

        f = TFile.Open(folder_name + "nominal.root")

        self.histo_names = [el.GetName() for el in f.GetListOfKeys()]
        self.histo_titles = [el.GetTitle() for el in f.GetListOfKeys()]

        f.Close()

    def create_plot_folders(self):
        if self.plot_all:
            self.folder_plot_all = self.output_folder + "Plotting_All/"
            if os.path.exists(self.folder_plot_all):
                shutil.rmtree(self.folder_plot_all)
                os.makedirs(self.folder_plot_all)
            else:
                os.makedirs(self.folder_plot_all)

        if self.plot_test:
            self.folder_plot_test = self.output_folder + \
                    "Plotting_" + self.plot_test + "/"
            if os.path.exists(self.folder_plot_test):
                shutil.rmtree(self.folder_plot_test)
                os.makedirs(self.folder_plot_test)
            else:
                os.makedirs(self.folder_plot_test)

    def plot_every_variable(self):
        for cut in self.cut_interval:
            histo_names_to_use = list(
                    filter(lambda name: "sel{:02d}".format(cut) in name,
                        self.histo_names))
            histo_titles_to_use = list(
                    filter(lambda name: "sel{:02d}".format(cut) in name,
                        self.histo_titles))
            for r in self.regions:
                for name, title in zip(histo_names_to_use, histo_titles_to_use):
                    samples_values = self.get_samples_values(r, name)
                    if self.show_over_under_flow:
                        title += " With Over/Underflow"
                    self.plot_variable(samples_values, r, name, title)

    def get_samples_values(self, region, histo_name):
        def get_input_opt(sample):
            wanted_option = list(filter(lambda x:
                x["Sample"] == sample["HistoFile"] and x["Region"] == region,
                self.input_file_options))

            return wanted_option[0]

        sample_values = {}

        folder_template = "../../results/{}/"  # Folder option
        folder_template += "MC{}/{}/{}/".format(self.mc_year, self.year, region)
        folder_template += "{}/" # HistoFile option

        # Groups
        for g in self.groups:
            samples = list(filter(lambda x:
                "Group" in x and x["Group"] == g, self.samples_list))
            group_values = np.array([])
            for s in samples:
                s_input = get_input_opt(s)
                s_values = self.get_histo_values(s_input, histo_name)
                if group_values.size == 0:
                    group_values = np.copy(s_values)
                else:
                    group_values += s_values
            sample_values[g] = group_values

        # Ungrouped
        for s in self.ungrouped_samples_list:
            s_input = get_input_opt(s)

            # For Latex
            if "#" in s["Title"]:
                title = "$"+s["Title"].replace("#", "\\")+"$"
            else:
                title = s["Title"]
            sample_values[title] = \
                    self.get_histo_values(s_input, histo_name)

        if self.order_samples:
            ordered_sample_values = OrderedDict(
                    sorted(sample_values.items(), key=lambda x: np.sum(x[1]),
                        reverse=True))
        else:
            ordered_sample_values = OrderedDict(sample_values.items())

        return ordered_sample_values

    def plot_variable(self, samples_values, region, histo_name, histo_title):
        bin_center = self.get_bins_center(histo_name)
        width = bin_center[1] - bin_center[0]

        bottom = np.zeros(bin_center.shape)

        # The order of the plots of which the legends are attributted to is:
        # plt.plot, plt.step, plt.bar
        # That is why, later on, the elements of legend get moved around
        legend = list(samples_values.keys())


        has_non_stacked_signal = False

        for i,values in enumerate(samples_values.values()):

            # Get Type of sample (DATA, SIGNAL, BACKGROUND)
            # Ungrouped Samples
            type_of_sample = list(filter(lambda x: x["Title"] == legend[i],
                self.ungrouped_samples_list))
            if type_of_sample:
                type_of_sample = type_of_sample[0]["Type"]
            else:
                # Grouped samples
                type_of_sample = list(filter(lambda x: "Group" in x and
                    x["Group"] == legend[i],
                    self.samples_list))
                if type_of_sample:
                    type_of_sample = type_of_sample[0]["Type"]
                else:
                    type_of_sample = ""

            # Plots Data if it is in ungrouped_samples_list
            if type_of_sample == "DATA":
                plt.plot(bin_center, values, marker='o', color='black',
                        markersize=3, linewidth=0)
                continue
            elif (not self.plot_signal_stacked) and type_of_sample == "SIGNAL":
                has_non_stacked_signal = True
                signal_index = i
                signal_values = np.copy(values)
                continue

            plt.bar(bin_center, values, bottom=bottom, width=width,
                    color=self.sample_colors[legend[i]])
            bottom += values

        if has_non_stacked_signal:
            legend.insert(0, legend[signal_index])
            del legend[signal_index+1]
            if np.max(signal_values) != 0:
                signal_values *= np.max(bottom) / np.max(signal_values)
            plt.step(bin_center + width/2, signal_values,
                    color=self.sample_colors[legend[0]])

        if "Data" in legend:
            legend = ["Data"] + legend[:len(legend)-1]

        plt.xlabel(histo_name)
        plt.ylabel("Events")
        plt.title(histo_title)
        plt.legend(legend)

        plt.savefig("{}{}_{}.png".format(self.folder_plot_all, region,
            histo_name))
        plt.close("all")

    def get_bins_center(self, histo_name):
        input_sample = self.input_file_options[0]

        folder_name = "../../results/{}/MC{}/{}/{}/{}/".format(
                input_sample["Folder"], self.mc_year, self.year,
                input_sample["Region"], input_sample["Sample"])

        f = TFile.Open(folder_name + "nominal.root")

        histo = f.Get(histo_name)
        n_bins = histo.GetNbinsX()
        if self.show_over_under_flow:
            bin_center = np.asarray([histo.GetBinCenter(i)
                for i in range(0,n_bins+2)])
        else:
            bin_center = np.asarray([histo.GetBinCenter(i)
                for i in range(1,n_bins+1)])

        f.Close()

        return bin_center

    def get_histo_values(self, sample, histo_name):
        folder_name = "../../results/{}/MC{}/{}/{}/{}/".format(
                sample["Folder"], self.mc_year, self.year,
                sample["Region"], sample["Sample"])

        f = TFile.Open(folder_name + "nominal.root")

        histo = f.Get(histo_name)
        #bin_content = root_numpy.hist2array(histo)
        n_bins = histo.GetNbinsX()
        if self.show_over_under_flow:
            bin_content = np.asarray([histo.GetBinContent(i)
                for i in range(0,n_bins+2)])
        else:
            bin_content = np.asarray([histo.GetBinContent(i)
                for i in range(1,n_bins+1)])

        f.Close()

        return bin_content

    def create_tex_every_variable(self):
        tex_file_name = "every_variable.tex"
        self.folder_plot_all = "../../results/{}/Plotting_All/".format(
                self.output)

        with open(self.folder_plot_all+tex_file_name, 'w') as f:
            include_string = "\\includegraphics[width=.35\\textwidth]{{{}}}\n"
            f.write("\\documentclass{article}\n")
            f.write("\\usepackage{graphicx}\n")
            f.write("\\begin{document}\n")

            for region in self.regions:
                f.write("\\section{{{}}}\n".format(region))
                for cut in self.cut_interval:
                    f.write("\\subsection{{Cut {}}}\n".format(cut))
                    file_name = "{}_sel{:02d}*.png".format(region, cut)
                    for plot in glob.glob(self.folder_plot_all + file_name):
                        index = plot.find("Plotting_All/")
                        f.write(include_string.format(plot[index+13:]))

            f.write("\\end{document}\n")

        subprocess.run(["pdflatex", tex_file_name],
                cwd=self.folder_plot_all)



    def run(self, test=False):
        super().run(test)
        self.get_samples_variables(test)
        self.get_regions_and_max_cuts()
        self.prepare_input(test)

        if self.plot_all:
            self.plot_every_variable()
            self.create_tex_every_variable()

        self.copy_files_to_output_folder()

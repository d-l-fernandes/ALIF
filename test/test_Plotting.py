import unittest
import sys
sys.path.insert(0, '../src/')

import filecmp
import os
import shutil
import numpy as np

from ROOT import TFile, TH1D

import Plotting

class TestOptionsInput(unittest.TestCase):

    def setUp(self):
        self.job = Plotting.Plotting()

    def test_add_option(self):
        self.job.add_option(["Year", "151617"])
        self.assertEqual(self.job.options_dict["Year"], "151617")

    def test_check_required_option_error(self):
        self.job.add_option(["Year", "151617"])
        self.assertRaises(TypeError, lambda: self.job.check_required_options())

    def test_check_required_option(self):
        self.job.add_option(["Output", "001"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["CutFile", "test"])
        self.assertTrue(lambda: self.job.check_required_options())

    def test_check_invalid_option_error(self):
        self.job.add_option(["Output", "001"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["CutFile", "test"])
        self.job.add_option(["WowDude!", "check it out"])
        self.assertRaises(TypeError, lambda: self.job.check_invalid_options())

    def test_set_option_Year(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Year", "151617"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["CutFile", "test"])
        self.job.set_options()
        self.assertEqual(151617, self.job.year)

    def test_set_option_Year_error(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Year", "2000"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["CutFile", "test"])
        self.assertRaises(ValueError, lambda: self.job.set_options())

    def test_set_option_MCYear(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["MCYear", "15"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["CutFile", "test"])
        self.job.set_options()
        self.assertEqual(15, self.job.mc_year)

    def test_set_option_MCYear_error(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["MCYear", "2000"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["CutFile", "test"])
        self.assertRaises(ValueError, lambda: self.job.set_options())

    def test_set_option_ShowData(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["CutFile", "test"])
        self.job.add_option(["ShowData", "false"])
        self.job.set_options()
        self.assertEqual(False, self.job.show_data)

    def test_set_option_ShowData_error(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["CutFile", "test"])
        self.job.add_option(["ShowData", "2000"])
        self.assertRaises(ValueError, lambda: self.job.set_options())

    def test_set_option_PlotAll(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["CutFile", "test"])
        self.job.add_option(["PlotAll", "true"])
        self.job.set_options()
        self.assertEqual(True, self.job.show_data)

    def test_set_option_PlotAll_error(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["CutFile", "test"])
        self.job.add_option(["PlotAll", "2000"])
        self.assertRaises(ValueError, lambda: self.job.set_options())

    def test_set_option_ShowOverUnderFlow(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["CutFile", "test"])
        self.job.add_option(["ShowOverUnderFlow", "true"])
        self.job.set_options()
        self.assertEqual(True, self.job.show_over_under_flow)

    def test_set_option_ShowOverUnderFlow_error(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["CutFile", "test"])
        self.job.add_option(["ShowOverUnderFlow", "2000"])
        self.assertRaises(ValueError, lambda: self.job.set_options())

    def test_set_option_Cuts(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["CutFile", "test"])
        self.job.add_option(["Cuts", "2,3,4"])
        self.job.set_options()
        self.assertEqual([2,3,4], self.job.cuts)

    def test_set_option_Cuts_error(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["CutFile", "test"])
        self.job.add_option(["Cuts", "a,2,3"])
        self.assertRaises(ValueError, lambda: self.job.set_options())


class TestOutputDescriptionWriting(unittest.TestCase):

    def setUp(self):
        self.job = Plotting.Plotting()
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["CutFile", "test"])

    def test_set_job_output_description_root_alone(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.set_options()

        file_name = self.job.output_folder + "results_test.txt"
        f = open(file_name, 'w')
        f.close()

        self.job.set_job_output_description(test=True)
        self.assertTrue(filecmp.cmp(file_name, "text_files/results_test1.txt",
            False))

    def test_set_job_output_description_branch_alone(self):
        self.job.add_option(["Output", "000.000"])
        self.job.add_option(["Description", "test2"])
        self.job.set_options()

        file_name = self.job.output_folder + "results_test.txt"
        with open(file_name, 'w') as f:
            f.write("000: test\n")

        self.job.set_job_output_description(test=True)
        self.assertTrue(filecmp.cmp(file_name, "text_files/results_test2.txt",
            False))

    def test_set_job_output_description_root_not_alone(self):
        self.job.add_option(["Output", "001"])
        self.job.add_option(["Description", "test2"])
        self.job.set_options()

        file_name = self.job.output_folder + "results_test.txt"
        with open(file_name, 'w') as f:
            f.write("000: test\n")
            f.write("002: test3\n")

        self.job.set_job_output_description(test=True)
        self.assertTrue(filecmp.cmp(file_name, "text_files/results_test3.txt"))

    def test_set_job_output_description_branch_not_alone(self):
        self.job.add_option(["Output", "001.001"])
        self.job.add_option(["Description", "test6"])
        self.job.set_options()

        file_name = self.job.output_folder + "results_test.txt"
        with open(file_name, 'w') as f:
            f.write("000: test\n")
            f.write("001: test2\n")
            f.write("001.000: test4\n")
            f.write("001.002: test5\n")
            f.write("002: test3\n")

        self.job.set_job_output_description(test=True)
        self.assertTrue(filecmp.cmp(file_name, "text_files/results_test4.txt"))

class TestOSFunctions(unittest.TestCase):

    def setUp(self):
        self.job = Plotting.Plotting()
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["CutFile", "test"])

    def test_create_output_folder(self):
        self.job.add_option(["Output", "test"])
        self.job.add_option(["Description", "test"])
        self.job.set_options()
        self.job.create_output_folder()
        self.assertTrue(os.path.exists(self.job.output_folder))

    def test_copy_files_to_output_folder(self):
        self.job.add_option(["Output", "test"])
        self.job.add_option(["Description", "test"])
        self.job.set_options()
        self.job.create_output_folder()
        self.job.files_to_copy.append("./text_files/copy_test.txt")
        file_name = "copy_test.txt"
        self.job.copy_files_to_output_folder()
        self.assertTrue(os.path.exists(self.job.output_folder + file_name))
        os.remove(self.job.output_folder + file_name)

    def test_create_plot_folders(self):
        self.job.add_option(["Output", "test"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["PlotAll", "True"])
        self.job.add_option(["PlotTest", "Ratio"])
        self.job.set_options()
        self.job.create_output_folder()
        self.job.create_plot_folders()
        plot_all_path = "../../results/test/Plotting_All"
        plot_test_path = "../../results/test/Plotting_Ratio"
        self.assertTrue(os.path.exists(plot_all_path))
        self.assertTrue(os.path.exists(plot_test_path))
        os.rmdir(plot_all_path)
        os.rmdir(plot_test_path)

class TestFileParsing(unittest.TestCase):

    def setUp(self):
        self.job = Plotting.Plotting()
        self.job.add_option(["Output", "test"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["CutFile", "test"])

    def test_get_samples_variables(self):
        self.job.add_option(["ShowData", "False"])
        self.job.add_option(["Samples", "test_samples.txt"])
        self.job.set_options()
        self.job.get_samples_variables(test=True)
        self.assertEqual(self.job.samples_list[0]["Type"],"BACKGROUND")
        self.assertEqual(self.job.samples_list[0]["Title"],"WtZ")
        self.assertEqual(self.job.samples_list[0]["HistoFile"],"background_WtZ")
        self.assertEqual(self.job.samples_list[0]["Group"],"OtherMC")
        self.assertEqual(self.job.samples_list[1]["Type"],"SIGNAL")
        self.assertEqual(self.job.samples_list[1]["Title"],"$t\\bar{t}\\rightarrow sWbW$")
        self.assertEqual(self.job.samples_list[1]["HistoFile"],"signal_sW")
        self.assertEqual(self.job.groups,{"OtherMC"})
        self.assertEqual(self.job.ungrouped_samples_list,
                [self.job.samples_list[1]])

    def test_get_regions_and_max_cut(self):
        self.job.add_option(["Samples", "test_samples.txt"])
        self.job.add_option(["CutFile", "test_docuts.cxx"])
        self.job.set_options()
        self.job.get_regions_and_max_cuts()
        self.assertEqual(self.job.max_cuts, 7)
        self.assertEqual(self.job.regions, ['SR','bWbWCR','WtCR','ZjetsCR'])

class TestInputFileFunctions(unittest.TestCase):

    def setUp(self):
        self.job = Plotting.Plotting()
        self.job.add_option(["Output", "test"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test_samples.txt"])
        self.job.add_option(["CutFile", "test_docuts.cxx"])
        self.job.add_option(["ShowData", "False"])
        if os.path.exists("../../results/test2"):
            shutil.rmtree("../../results/test2/")

    def test_parse_input_file_all(self):
        self.job.add_option(["Input", "input_file1.txt"])
        self.job.set_options()
        self.job.get_samples_variables(True)
        self.job.get_regions_and_max_cuts()
        self.job.parse_input_file(True)
        self.assertEqual(len(self.job.input_file_options), 8)
        for opt in self.job.input_file_options:
            self.assertEqual(opt["Folder"], "test")

    def test_parse_input_file_Test(self):
        self.job.add_option(["Input", "input_file_plot_1.txt"])
        self.job.set_options()
        self.job.get_samples_variables(True)
        self.job.get_regions_and_max_cuts()
        self.job.parse_input_file(True)
        self.assertEqual(len(self.job.input_file_options), 8)
        for opt in self.job.input_file_options:
            if opt["Sample"] == "signal_sW" and opt["Region"] == "SR":
                self.assertEqual(opt["Test"], True)
            else:
                self.assertEqual(opt["Test"], False)

class TestHistoFunctions(unittest.TestCase):

    def setUp(self):
        self.job = Plotting.Plotting()
        self.job.add_option(["Output", "test3"])
        self.job.add_option(["Description", "test3"])
        self.job.add_option(["Samples", "test_samples_3.txt"])
        self.job.add_option(["Input", "input_file_plot_2.txt"])
        self.job.add_option(["CutFile", "test_docuts_2.cxx"])
        self.job.add_option(["ShowData", "False"])
        self.job.add_option(["PlotAll", "True"])

        self.sW_path = "../../results/test4/MC16/1516/SR/signal_sW/"
        self.WtZ_path = "../../results/test4/MC16/1516/SR/background_WtZ/"
        self.Zjets_path = "../../results/test4/MC16/1516/SR/background_Zjets/"

        if os.path.exists("../../results/test4"):
            shutil.rmtree("../../results/test4/")
        if os.path.exists("../../results/test3"):
            shutil.rmtree("../../results/test3/")

        self.histo_name = "sel01_test_histo_name"

        for path in [self.sW_path, self.WtZ_path, self.Zjets_path]:
            os.makedirs(path)
            output_file = TFile.Open(path + "nominal.root", "recreate")
            histo = TH1D(self.histo_name, "sel01: test", 5, -0.5, 4.5)
            for i in range(6):
                if path == self.sW_path:
                    histo.SetBinContent(i, 1)
                else:
                    histo.SetBinContent(i, 2)
                histo.SetBinError(i, 0.5)
            output_file.Write()
            output_file.Close()

        self.job.set_options()
        self.job.get_samples_variables(True)
        self.job.get_regions_and_max_cuts()
        self.job.parse_input_file(True)

    def test_get_histo_names_and_titles(self):
        self.job.get_histo_names_and_titles()

        self.assertEqual(self.job.histo_names, ["sel01_test_histo_name"])
        self.assertEqual(self.job.histo_titles, ["sel01: test"])

    def test_get_bins_center(self):
        bin_center = self.job.get_bins_center(self.histo_name)

        check_bin_center = np.array([0,1,2,3,4])
        self.assertTrue(np.array_equal(bin_center,check_bin_center))

    def test_get_histo_values(self):
        sample = self.job.input_file_options[2]

        bin_values = self.job.get_histo_values(sample, self.histo_name)
        check_bin_values = np.array([1,1,1,1,1])
        self.assertTrue(np.array_equal(bin_values,check_bin_values))

    def test_get_samples_values(self):
        check_values = self.job.get_samples_values("SR","sel01_test_histo_name")

        self.assertTrue(np.array_equal(check_values["OtherMC"],
            np.array([4,4,4,4,4])))
        self.assertTrue(np.array_equal(check_values["$t\\bar{t}\\rightarrow sWbW$"],
            np.array([1,1,1,1,1])))

    def test_plot_every_variable(self):
        self.job.get_histo_names_and_titles()
        self.job.create_output_folder()
        self.job.create_plot_folders()
        self.job.plot_every_variable()

        file_name = "../../results/test3/Plotting_All/SR_sel01_test_histo_name.png"
        self.assertTrue(os.path.exists(file_name))

    def tearDown(self):
        if os.path.exists("../../results/test4"):
            shutil.rmtree("../../results/test4/")
        if os.path.exists("../../results/test3"):
            shutil.rmtree("../../results/test3/")

if __name__ == '__main__':
    unittest.main()

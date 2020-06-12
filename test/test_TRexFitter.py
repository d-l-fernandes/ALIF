import unittest
import sys
sys.path.insert(0, '../src/')

import filecmp
import os
import shutil

from ROOT import TFile, TH1D

import TRexFitter

class TestOptionsInput(unittest.TestCase):

    def setUp(self):
        self.job = TRexFitter.TRexFitter()

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
        self.job.add_option(["Regions", "test"])
        self.job.add_option(["NormFactors", "test"])
        self.job.add_option(["Input", "test"])
        self.assertTrue(lambda: self.job.check_required_options())

    def test_check_invalid_option_error(self):
        self.job.add_option(["Output", "001"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Regions", "test"])
        self.job.add_option(["NormFactors", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["WowDude!", "check it out"])
        self.assertRaises(TypeError, lambda: self.job.check_invalid_options())

    def test_set_option_Year(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Regions", "test"])
        self.job.add_option(["NormFactors", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["Year", "151617"])
        self.job.set_options()
        self.assertEqual(151617, self.job.year)

    def test_set_option_Year_error(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Regions", "test"])
        self.job.add_option(["NormFactors", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["Year", "2000"])
        self.assertRaises(ValueError, lambda: self.job.set_options())

    def test_set_option_MCYear(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Regions", "test"])
        self.job.add_option(["NormFactors", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["MCYear", "15"])
        self.job.set_options()
        self.assertEqual(15, self.job.mc_year)

    def test_set_option_MCYear_error(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Regions", "test"])
        self.job.add_option(["NormFactors", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["MCYear", "2000"])
        self.assertRaises(ValueError, lambda: self.job.set_options())

    def test_set_option_Asimov(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Regions", "test"])
        self.job.add_option(["NormFactors", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["Asimov", "true"])
        self.job.set_options()
        self.assertEqual(True, self.job.asimov)

    def test_set_option_Asimov_error(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Regions", "test"])
        self.job.add_option(["NormFactors", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["Asimov", "2000"])
        self.assertRaises(ValueError, lambda: self.job.set_options())

    def test_set_option_SystAnalysis(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Regions", "test"])
        self.job.add_option(["NormFactors", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["SystAnalysis", "test.txt"])
        self.job.set_options()
        self.assertEqual(self.job.syst_analysis_file, "test.txt")

    def test_set_option_SystWeight_error_weight(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Regions", "test"])
        self.job.add_option(["NormFactors", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["SystWeight", "weight_test"])
        self.assertRaises(ValueError, lambda: self.job.set_options())

    def test_set_option_SystWeight(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Regions", "test"])
        self.job.add_option(["NormFactors", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["SystWeight", "bTagSF_77_eigenvars_B_up0"])
        self.job.set_options()
        self.assertEqual(self.job.syst_weight, ["bTagSF_77_eigenvars_B_up0"])

    def test_set_option_SystWeight_error_weight(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Regions", "test"])
        self.job.add_option(["NormFactors", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["SystWeight", "weight_test"])
        self.assertRaises(ValueError, lambda: self.job.set_options())

    def test_set_option_SystWeight_error_does_not_exist(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Regions", "test"])
        self.job.add_option(["NormFactors", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["SystWeight", "test"])
        self.assertRaises(LookupError, lambda: self.job.set_options())

    def test_set_option_SystTree(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Regions", "test"])
        self.job.add_option(["NormFactors", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["SystTree", "EG_RESOLUTION_ALL__1down"])
        self.job.set_options()
        self.assertEqual(self.job.syst_tree, ["EG_RESOLUTION_ALL__1down"])

    def test_set_option_SystTree_error_does_not_exist(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Regions", "test"])
        self.job.add_option(["NormFactors", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["SystTree", "test"])
        self.assertRaises(LookupError, lambda: self.job.set_options())

    def test_set_option_Fit(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Regions", "test"])
        self.job.add_option(["NormFactors", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["Fit", "BONLY/CRONLY"])
        self.job.set_options()
        self.assertEqual(self.job.fit, ["BONLY", "CRONLY"])

    def test_set_option_Fit_error_len(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Regions", "test"])
        self.job.add_option(["NormFactors", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["Fit", "BONLYCRONLY"])
        self.assertRaises(ValueError, lambda: self.job.set_options())

    def test_set_option_Fit_error_first(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Regions", "test"])
        self.job.add_option(["NormFactors", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["Fit", "test/CRONLY"])
        self.assertRaises(ValueError, lambda: self.job.set_options())

    def test_set_option_Fit_error_second(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Regions", "test"])
        self.job.add_option(["NormFactors", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["Fit", "SPLUSB/test"])
        self.assertRaises(ValueError, lambda: self.job.set_options())

    def test_set_option_Limit(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Regions", "test"])
        self.job.add_option(["NormFactors", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["Limit", "true"])
        self.job.set_options()
        self.assertEqual(True, self.job.limit)

    def test_set_option_Limit_error(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Regions", "test"])
        self.job.add_option(["NormFactors", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["Limit", "2000"])
        self.assertRaises(ValueError, lambda: self.job.set_options())

    def test_set_option_ShowData(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Regions", "test"])
        self.job.add_option(["NormFactors", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["ShowData", "false"])
        self.job.set_options()
        self.assertEqual(False, self.job.show_data)

    def test_set_option_ShowData_error(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Regions", "test"])
        self.job.add_option(["NormFactors", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["ShowData", "2000"])
        self.assertRaises(ValueError, lambda: self.job.set_options())

    def test_set_option_Luminosity(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Regions", "test"])
        self.job.add_option(["NormFactors", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["Luminosity", "150"])
        self.job.set_options()
        self.assertEqual(150, self.job.lumi_label)

    def test_set_option_Luminosity_error(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Regions", "test"])
        self.job.add_option(["NormFactors", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["Luminosity", "test"])
        self.assertRaises(ValueError, lambda: self.job.set_options())

    def test_set_option_FullAsimov(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Regions", "test"])
        self.job.add_option(["NormFactors", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["FullAsimov", "true"])
        self.job.set_options()
        self.assertEqual(True, self.job.full_asimov)

    def test_set_option_FullAsimov_error(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Regions", "test"])
        self.job.add_option(["NormFactors", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["FullAsimov", "2000"])
        self.assertRaises(ValueError, lambda: self.job.set_options())

    def test_set_option_FullAsimov_error_Asimov_True(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Regions", "test"])
        self.job.add_option(["NormFactors", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["FullAsimov", "True"])
        self.job.add_option(["Asimov", "True"])
        self.assertRaises(ValueError, lambda: self.job.set_options())

    def test_set_option_POI(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Regions", "test"])
        self.job.add_option(["NormFactors", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["POI", "norm_sW"])
        self.job.set_options()
        self.assertEqual("norm_sW", self.job.poi)

    def test_set_option_ReadFrom(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Regions", "test"])
        self.job.add_option(["NormFactors", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["ReadFrom", "NTUP"])
        self.job.set_options()
        self.assertEqual("NTUP", self.job.read_from)

    def test_set_option_ReadFrom_error(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Regions", "test"])
        self.job.add_option(["NormFactors", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["ReadFrom", "shit"])
        self.assertRaises(ValueError, lambda: self.job.set_options())

    def test_set_option_ReadFrom(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Regions", "test"])
        self.job.add_option(["NormFactors", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["FileSuffix", "_nn"])
        self.job.set_options()
        self.assertEqual("_nn", self.job.file_suffix)

    def test_set_option_ShowYields(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Regions", "test"])
        self.job.add_option(["NormFactors", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["ShowYields", "False"])
        self.job.set_options()
        self.assertEqual(False, self.job.show_yields)

    def test_set_option_ShowYields_error(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Regions", "test"])
        self.job.add_option(["NormFactors", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["ShowYields", "shit"])
        self.assertRaises(ValueError, lambda: self.job.set_options())

    def test_set_option_PrepareSamples(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Regions", "test"])
        self.job.add_option(["NormFactors", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["PrepareSamples", "False"])
        self.job.set_options()
        self.assertEqual(False, self.job.prepare_samples)

    def test_set_option_PrepareSamples(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Regions", "test"])
        self.job.add_option(["NormFactors", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["PrepareSamples", "Only"])
        self.job.set_options()
        self.assertEqual("ONLY", self.job.prepare_samples)

    def test_set_option_PrepareSamples_error(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Regions", "test"])
        self.job.add_option(["NormFactors", "test"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["PrepareSamples", "test"])
        self.assertRaises(ValueError, lambda: self.job.set_options())

class TestOutputDescriptionWriting(unittest.TestCase):

    def setUp(self):
        self.job = TRexFitter.TRexFitter()
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Regions", "test"])
        self.job.add_option(["NormFactors", "test"])
        self.job.add_option(["Input", "test"])

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
        self.job = TRexFitter.TRexFitter()
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Regions", "test"])
        self.job.add_option(["NormFactors", "test"])
        self.job.add_option(["Input", "test"])

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

class TestFileParsing(unittest.TestCase):

    def setUp(self):
        self.job = TRexFitter.TRexFitter()
        self.job.add_option(["Output", "test"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["NormFactors", "test"])
        self.job.add_option(["Input", "test"])

    def test_get_samples_variables(self):
        self.job.add_option(["Regions", "test"])
        self.job.add_option(["Samples", "test_samples.txt"])
        self.job.set_options()
        self.job.get_samples_variables(test=True)
        self.assertEqual(self.job.samples_list[0]["Type"],"BACKGROUND")
        self.assertEqual(self.job.samples_list[0]["Title"],"WtZ")
        self.assertEqual(self.job.samples_list[0]["HistoFile"],"background_WtZ")
        self.assertEqual(self.job.samples_list[0]["FillColor"],85)
        self.assertEqual(self.job.samples_list[0]["Group"],"OtherMC")
        self.assertEqual(self.job.samples_list[1]["Type"],"SIGNAL")
        self.assertEqual(self.job.samples_list[1]["Title"],"t#bar{t}#rightarrow sWbW")
        self.assertEqual(self.job.samples_list[1]["HistoFile"],"signal_sW")
        self.assertEqual(self.job.samples_list[1]["FillColor"],50)

class TestConfigFile(unittest.TestCase):

    def setUp(self):
        self.job = TRexFitter.TRexFitter()
        self.job.add_option(["Output", "test"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["NormFactors", "test_norm_factors.txt"])
        self.job.add_option(["Input", "test"])
        self.job.add_option(["Regions", "test_regions.txt"])
        self.job.add_option(["Samples", "test_samples.txt"])
        self.job.set_options()
        self.job.get_samples_variables(True)

    def test_make_header_string(self):
        test_string = self.job.make_header_string("Test")
        check_string =  "%%%%%%%%\n"
        check_string += "% Test %\n"
        check_string += "%%%%%%%%\n\n"

        self.assertEqual(test_string, check_string)

    def test_make_section_string(self):
        header_name = "Test"
        section_name = "test"
        opt_test = {"Test": "test"}
        test_string = self.job.make_section_string(header_name, section_name,
                opt_test)
        check_string = "Test: \"test\"\n"
        check_string += "  Test: test\n\n"

        self.assertEqual(test_string, check_string)

    def test_make_regions_string(self):
        check_string =  "%%%%%%%%%%%\n"
        check_string += "% Regions %\n"
        check_string += "%%%%%%%%%%%\n\n"
        check_string += "Region: \"test_region\"\n"
        check_string += "  Type: SIGNAL\n"
        check_string += "  HistoName: \"test_histo_name\"\n"
        check_string += "  HistoPathSuff: \"SR/\"\n\n"

        test_string = self.job.make_regions_string(True)
        self.assertEqual(test_string, check_string)

    def test_make_norm_factors_string(self):
        check_string =  "%%%%%%%%%%%%%%%\n"
        check_string += "% NormFactors %\n"
        check_string += "%%%%%%%%%%%%%%%\n\n"
        check_string += "NormFactor: \"#mu\"\n"
        check_string += "  Title: #mu\n"
        check_string += "  Nominal: 1\n"
        check_string += "  Min: 0.0001\n"
        check_string += "  Max: 10\n\n"
        test_string = self.job.make_norm_factors_string(True)
        self.assertEqual(test_string, check_string)

    def test_make_config_file(self):

        self.job.create_output_folder()
        self.job.make_config_file(True)
        path = "../../results/test/config_test.config"
        self.job.copy_files_to_output_folder()
        self.assertTrue(os.path.exists(path))
        os.remove(path)

class TestInputFileFunctions(unittest.TestCase):

    def setUp(self):
        self.job = TRexFitter.TRexFitter()
        self.job.add_option(["Output", "test"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["NormFactors", "test_norm_factors.txt"])
        self.job.add_option(["Regions", "test_regions2.txt"])
        self.job.add_option(["Samples", "test_samples.txt"])
        self.job.add_option(["Asimov", "True"])
        if os.path.exists("../../results/test2"):
            shutil.rmtree("../../results/test2/")

    def test_get_histo_names(self):
        self.job.add_option(["Input", "test"])
        self.job.set_options()
        self.job.get_samples_variables(True)
        self.job.get_histo_names(True)
        self.assertEqual(self.job.histo_names, ["test_histo_name1",
            "test_histo_name2"])
        self.assertEqual(self.job.regions, ["SR", "bWbWCR"])

    def test_parse_input_file_all(self):
        self.job.add_option(["Input", "input_file1.txt"])
        self.job.set_options()
        self.job.get_samples_variables(True)
        self.job.get_histo_names(True)
        self.job.parse_input_file(True)
        self.assertEqual(len(self.job.input_file_options), 4)
        for opt in self.job.input_file_options:
            self.assertEqual(opt["Folder"], "test")

    def test_parse_input_file_scale(self):
        self.job.add_option(["Input", "input_file2.txt"])
        self.job.set_options()
        self.job.get_samples_variables(True)
        self.job.get_histo_names(True)
        self.job.parse_input_file(True)
        self.assertEqual(len(self.job.input_file_options), 4)
        for opt in self.job.input_file_options:
            if opt["Sample"] == "signal_sW" and opt["Region"] == "SR":
                self.assertEqual(opt["Scale"], 1.9)
            elif opt["Sample"] == "background_WtZ" and opt["Region"] == "bWbWCR":
                self.assertEqual(opt["Scale"], 1.3)
            else:
                self.assertEqual(opt["Scale"], 1)

    def test_parse_input_file_scale_different_factor(self):
        self.job.add_option(["Input", "input_file2_1.txt"])
        self.job.set_options()
        self.job.get_samples_variables(True)
        self.job.get_histo_names(True)
        self.job.parse_input_file(True)
        self.assertEqual(len(self.job.input_file_options), 4)
        for opt in self.job.input_file_options:
            if opt["Sample"] == "signal_sW" and opt["Region"] == "SR":
                self.assertEqual(opt["Scale"], 1.9)
            elif opt["Sample"] == "background_WtZ" and opt["Region"] == "bWbWCR":
                self.assertEqual(opt["Scale"], 2.6)
            else:
                self.assertEqual(opt["Scale"], 1)

    def test_parse_input_file_scale_multiplication(self):
        self.job.add_option(["Input", "input_file6.txt"])
        self.job.set_options()
        self.job.get_samples_variables(True)
        self.job.get_histo_names(True)
        self.job.parse_input_file(True)
        self.assertEqual(len(self.job.input_file_options), 4)
        for opt in self.job.input_file_options:
            if opt["Sample"] == "signal_sW" and opt["Region"] == "SR":
                self.assertEqual(opt["Scale"], 0.78)
            else:
                self.assertEqual(opt["Scale"], 1)

    def test_parse_input_file_cut(self):
        os.makedirs("../../results/test2")
        self.job.add_option(["Input", "input_file3.txt"])
        self.job.set_options()
        self.job.get_samples_variables(True)
        self.job.get_histo_names(True)
        self.job.parse_input_file(True)
        self.assertEqual(len(self.job.input_file_options), 4)
        for opt in self.job.input_file_options:
            if opt["Sample"] == "signal_sW" and opt["Region"] == "bWbWCR":
                self.assertEqual(opt["Cut"], [3,5,6,7] )
            elif opt["Sample"] == "background_WtZ" and opt["Region"] == "SR":
                self.assertEqual(opt["Cut"], [2,3,4] )
            else:
                self.assertEqual(opt["Cut"], [])
            self.assertEqual(opt["Folder"], "test2")
        shutil.rmtree("../../results/test2/")

    def test_parse_input_file_ScaleBinByBin_Exclude(self):
        os.makedirs("../../results/test2")
        self.job.add_option(["Input", "input_file4.txt"])
        self.job.set_options()
        self.job.get_samples_variables(True)
        self.job.get_histo_names(True)
        self.job.parse_input_file(True)
        self.assertEqual(len(self.job.input_file_options), 4)
        for opt in self.job.input_file_options:
            if opt["Sample"] == "signal_sW" and opt["Region"] == "SR":
                self.assertEqual(opt["ExcludeFromSystematics"], True)
            self.assertEqual(opt["Folder"], "test2")
            self.assertEqual(opt["Cut"], [2,3,4] )
            self.assertEqual(opt["ScaleBinByBin"], {2:1.4, 4:1.3})
        shutil.rmtree("../../results/test2/")

    def test_parse_input_file_ExcludeFromRegions(self):
        self.job.add_option(["Input", "input_file7.txt"])
        self.job.set_options()
        self.job.get_samples_variables(True)
        self.job.get_histo_names(True)
        self.job.parse_input_file(True)
        self.assertEqual(len(self.job.input_file_options), 4)
        for opt in self.job.input_file_options:
            if opt["Sample"] == "background_WtZ" and opt["Region"] == "SR":
                self.assertEqual(opt["ExcludeFromRegions"], True)
        self.assertEqual("SR", self.job.samples_list[0]["Exclude"])

    def test_parse_input_file_Signal(self):
        self.job.add_option(["Input", "input_file8.txt"])
        self.job.set_options()
        self.job.get_samples_variables(True)
        self.job.get_histo_names(True)
        self.job.parse_input_file(True)
        self.assertEqual(len(self.job.input_file_options), 4)
        self.assertEqual("SIGNAL", self.job.samples_list[0]["Type"])
        self.assertEqual("BACKGROUND", self.job.samples_list[1]["Type"])

    def test_create_directory_structure(self):
        self.job.add_option(["Input", "test"])
        self.job.set_options()
        self.job.get_samples_variables(True)
        self.job.get_histo_names(True)
        self.job.create_directory_structure()
        folder_to_remove = "../../results/test/MC16"
        folder_name = "../../results/test/MC16/1516/"
        for r in self.job.regions:
            for sample in self.job.samples_list:
                self.assertTrue(os.path.exists(folder_name + r + "/" + \
                        sample["HistoFile"]))
        shutil.rmtree(folder_to_remove)

class TestHistoAlteration(unittest.TestCase):

    def setUp(self):
        self.job = TRexFitter.TRexFitter()
        self.job.add_option(["Output", "test3"])
        self.job.add_option(["Description", "test3"])
        self.job.add_option(["NormFactors", "test_norm_factors.txt"])
        self.job.add_option(["Regions", "test_regions.txt"])
        self.job.add_option(["Samples", "test_samples.txt"])
        self.job.add_option(["Input", "input_file5.txt"])
        self.job.add_option(["Asimov", "True"])

        sW_path = "../../results/test4/MC16/1516/SR/signal_sW/"
        WtZ_path = "../../results/test4/MC16/1516/SR/background_WtZ/"

        if os.path.exists("../../results/test4"):
            shutil.rmtree("../../results/test4/")
        if os.path.exists("../../results/test3"):
            shutil.rmtree("../../results/test3/")

        os.makedirs(sW_path)
        os.makedirs(WtZ_path)
        self.histo_name = "test_histo_name"

        for path in [sW_path, WtZ_path]:
            output_file = TFile.Open(path + "nominal.root", "recreate")
            histo = TH1D(self.histo_name, "test", 5, -0.5, 4.5)
            for i in range(6):
                histo.SetBinContent(i, 1)
                histo.SetBinError(i, 0.5)
            output_file.Write()
            output_file.Close()

        self.job.set_options()
        self.job.get_samples_variables(True)

    def test_histo_cut(self):
        self.job.prepare_input(True)
        path = "../../results/test3/MC16/1516/SR/background_WtZ/"

        output_file = TFile.Open(path + "nominal.root")
        histo = output_file.Get(self.histo_name)
        self.assertEqual(0, histo.GetBinContent(0))
        self.assertEqual(0, histo.GetBinError(0))
        self.assertEqual(0, histo.GetBinContent(1))
        self.assertEqual(0, histo.GetBinError(1))
        self.assertEqual(0, histo.GetBinContent(5))
        self.assertEqual(0, histo.GetBinError(5))
        output_file.Close()

    def test_histo_scale(self):
        self.job.prepare_input(True)
        path = "../../results/test3/MC16/1516/SR/signal_sW/"

        output_file = TFile.Open(path + "nominal.root")
        histo = output_file.Get(self.histo_name)
        for i in range(6):
            self.assertEqual(1.8, histo.GetBinContent(i))
            self.assertEqual(0.9, histo.GetBinError(i))
        output_file.Close()

    def test_histo_scale_binbybin(self):
        self.job.prepare_input(True)
        path = "../../results/test3/MC16/1516/SR/background_WtZ/"

        output_file = TFile.Open(path + "nominal.root")
        histo = output_file.Get(self.histo_name)
        self.assertEqual(1.4, histo.GetBinContent(2))
        self.assertEqual(0.7, histo.GetBinError(2))
        self.assertEqual(1.3, histo.GetBinContent(4))
        self.assertEqual(0.65, histo.GetBinError(4))
        output_file.Close()

    def tearDown(self):
        shutil.rmtree("../../results/test4")
        shutil.rmtree("../../results/test3")

class TestFullAsimov(unittest.TestCase):

    def setUp(self):
        self.job = TRexFitter.TRexFitter()
        self.job.add_option(["Output", "test3"])
        self.job.add_option(["Description", "test3"])
        self.job.add_option(["NormFactors", "test_norm_factors.txt"])
        self.job.add_option(["Regions", "test_regions.txt"])
        self.job.add_option(["Samples", "test_samples.txt"])
        self.job.add_option(["Input", "input_file5_1.txt"])
        self.job.add_option(["FullAsimov", "True"])

        sW_path = "../../results/test4/MC16/1516/SR/signal_sW/"
        WtZ_path = "../../results/test4/MC16/1516/SR/background_WtZ/"

        if os.path.exists("../../results/test4"):
            shutil.rmtree("../../results/test4/")
        if os.path.exists("../../results/test3"):
            shutil.rmtree("../../results/test3/")

        os.makedirs(sW_path)
        os.makedirs(WtZ_path)
        self.histo_name = "test_histo_name"

        for path in [sW_path, WtZ_path]:
            output_file = TFile.Open(path + "nominal.root", "recreate")
            histo = TH1D(self.histo_name, "test", 5, -0.5, 4.5)
            for i in range(6):
                histo.SetBinContent(i, 1)
                histo.SetBinError(i, 0.5)
            output_file.Write()
            output_file.Close()

        self.job.set_options()
        self.job.get_samples_variables(True)

    def test_data_full_asimov(self):
        self.job.prepare_input(True)
        path = "../../results/test3/MC16/1516/SR/data/"

        output_file = TFile.Open(path + "nominal.root")
        histo = output_file.Get(self.histo_name)
        for i in range(6):
            self.assertEqual(2.8, histo.GetBinContent(i))
        output_file.Close()

    def tearDown(self):
        shutil.rmtree("../../results/test4")
        shutil.rmtree("../../results/test3")

class TestSymbolicMath(unittest.TestCase):

    def setUp(self):
        self.job = TRexFitter.TRexFitter()

    def test_single_number(self):
        result = 5
        string = "5"
        self.assertEqual(result, self.job.get_scale_factor(string))

    def test_single_file(self):
        result = 1.3
        string = '"test"'
        self.assertEqual(result, self.job.get_scale_factor(string))

    def test_simple_sum(self):
        result = 2.3
        string = '(+ 1.1 1.2)'
        self.assertEqual(result, self.job.get_scale_factor(string))
        string = '( + 1.1 1.2 )'
        self.assertEqual(result, self.job.get_scale_factor(string))
        string = '( + 1.1   1.2 )'
        self.assertEqual(result, self.job.get_scale_factor(string))

    def test_simple_sum_file(self):
        result = 2.4
        string = '(+ 1.1 "test")'
        self.assertEqual(result, self.job.get_scale_factor(string))
        string = '( + 1.1   "test"  )'
        self.assertEqual(result, self.job.get_scale_factor(string))

    def test_simple_subtraction(self):
        result = -0.1
        string = '(- 1.1 1.2)'
        self.assertEqual(result, self.job.get_scale_factor(string))
        string = '( - 1.1 1.2 )'
        self.assertEqual(result, self.job.get_scale_factor(string))
        string = '( - 1.1   1.2 )'
        self.assertEqual(result, self.job.get_scale_factor(string))

    def test_simple_subtraction_file(self):
        result = -0.2
        string = '(- 1.1 "test")'
        self.assertEqual(result, self.job.get_scale_factor(string))
        string = '( - 1.1   "test"  )'
        self.assertEqual(result, self.job.get_scale_factor(string))

    def test_simple_multiplication(self):
        result = 3.6
        string = '(* 1.2 3)'
        self.assertEqual(result, self.job.get_scale_factor(string))
        string = '(  *   1.2   3  )'
        self.assertEqual(result, self.job.get_scale_factor(string))

    def test_simple_multiplication_file(self):
        result = 2.08
        string = '(* 1.6 "test")'
        self.assertEqual(result, self.job.get_scale_factor(string))

    def test_simple_division(self):
        result = 2.5
        string = '(/ 3 1.2)'
        self.assertEqual(result, self.job.get_scale_factor(string))
        string = '(  /   3  1.2  )'
        self.assertEqual(result, self.job.get_scale_factor(string))

    def test_simple_division_file(self):
        result = 2.0
        string = '(/ 2.6 "test")'
        self.assertEqual(result, self.job.get_scale_factor(string))

    def test_double_sum(self):
        result = 3.6
        string = '(+ 1.1 1.2 1.3)'
        self.assertEqual(result, self.job.get_scale_factor(string))
        string = '(  +   1.1   1.2    1.3   )'
        self.assertEqual(result, self.job.get_scale_factor(string))

    def test_double_sum_file(self):
        result = 3.6
        string = '(+ 1.1 "test" 1.2)'
        self.assertEqual(result, self.job.get_scale_factor(string))
        string = '(   +   1.1    "test"   1.2   )'
        self.assertEqual(result, self.job.get_scale_factor(string))

    def test_double_subtraction(self):
        result = -1.4
        string = '(- 1.1 1.2 1.3)'
        self.assertEqual(result, self.job.get_scale_factor(string))
        string = '(  -   1.1   1.2    1.3   )'
        self.assertEqual(result, self.job.get_scale_factor(string))

    def test_double_subtraction_file(self):
        result = -1.4
        string = '(- 1.1 "test" 1.2)'
        self.assertEqual(result, self.job.get_scale_factor(string))
        string = '(   -   1.1    "test"   1.2   )'
        self.assertEqual(result, self.job.get_scale_factor(string))

    def test_double_multiplication(self):
        result = 3.12
        string = '(* 2 1.2 1.3)'
        self.assertEqual(result, self.job.get_scale_factor(string))

    def test_double_multiplication_file(self):
        result = 3.12
        string = '(* 2 "test" 1.2)'
        self.assertEqual(result, self.job.get_scale_factor(string))

    def test_double_division(self):
        result = 1
        string = '(/ 2.6 1.3 2)'
        self.assertEqual(result, self.job.get_scale_factor(string))

    def test_double_division_file(self):
        result = 1
        string = '(/ 2.6 "test" 2)'
        self.assertEqual(result, self.job.get_scale_factor(string))

    def test_sum_multiplication(self):
        result = 6.24
        string = '(+ (* 2 1.2 1.3) (* 2 "test" 1.2))'
        self.assertEqual(result, self.job.get_scale_factor(string))

    def test_complex_expression(self):
        result = 5.9
        string = '(+  (* (- 5 2) "test") (/ (+ 1.6 1) "test"))'
        self.assertEqual(result, self.job.get_scale_factor(string))

    def test_sqrt1(self):
        result = 2
        string = '(v 4)'
        self.assertEqual(result, self.job.get_scale_factor(string))

    def test_sqrt2(self):
        result = 2
        string = '(v (* 2 2))'
        self.assertEqual(result, self.job.get_scale_factor(string))

    def test_sqrt_error(self):
        self.job.output = "test"
        string = '(v 2 2)'
        self.assertRaises(ValueError, lambda:
                self.job.get_scale_factor(string))

    def test_symbolic_math_bracket_error(self):
        self.job.output = "test"
        string = '(+  (* (- 5 2) "test") (/ (+ 1.6 1) "test")'
        self.assertRaises(IndexError, lambda:
                self.job.get_scale_factor(string))

if __name__ == '__main__':
    unittest.main()

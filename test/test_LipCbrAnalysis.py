import unittest
import sys
sys.path.insert(0, '../src/')

import filecmp
import os

import LipCbrAnalysis

class TestOptionsInput(unittest.TestCase):

    def setUp(self):
        self.job = LipCbrAnalysis.LipCbrAnalysis()

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
        self.job.add_option(["CutFile", "test"])
        self.assertTrue(lambda: self.job.check_required_options())

    def test_check_invalid_option_error(self):
        self.job.add_option(["Output", "001"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["CutFile", "test"])
        self.job.add_option(["WowDude!", "check it out"])
        self.assertRaises(TypeError, lambda: self.job.check_invalid_options())

    def test_set_option_Year(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Year", "151617"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["CutFile", "test"])
        self.job.set_options()
        self.assertEqual(151617, self.job.year)

    def test_set_option_Year_error(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["CutFile", "test"])
        self.job.add_option(["Year", "2000"])
        self.assertRaises(ValueError, lambda: self.job.set_options())

    def test_set_option_MCYear(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["CutFile", "test"])
        self.job.add_option(["MCYear", "15"])
        self.job.set_options()
        self.assertEqual(15, self.job.mc_year)

    def test_set_option_MCYear_error(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["CutFile", "test"])
        self.job.add_option(["MCYear", "2000"])
        self.assertRaises(ValueError, lambda: self.job.set_options())

    def test_set_option_Samples(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["CutFile", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.set_options()
        self.assertEqual(self.job.samples_file, "test")

    def test_set_option_Tree(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["CutFile", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Tree", "particleLevel"])
        self.job.set_options()
        self.assertEqual(self.job.tree, "particleLevel")

    def test_set_option_Tree_error(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["CutFile", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Tree", "test"])
        self.assertRaises(ValueError, lambda: self.job.set_options())

    def test_set_option_SystTree(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["CutFile", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Tree", "particleLevel"])
        self.job.add_option(["SystTree", "EG_RESOLUTION_ALL__1down"])
        self.job.set_options()
        self.assertEqual(self.job.tree, ["EG_RESOLUTION_ALL__1down"])

    def test_set_option_SystTree_error_does_not_exist(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["CutFile", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["Tree", "particleLevel"])
        self.job.add_option(["SystTree", "test"])
        self.assertRaises(LookupError, lambda: self.job.set_options())

    def test_set_option_SystWeight(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["CutFile", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["SystWeight", "bTagSF_77_eigenvars_B_up0"])
        self.job.set_options()
        self.assertEqual(self.job.syst_weight, ["bTagSF_77_eigenvars_B_up0"])

    def test_set_option_SystWeight_error_weight(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["CutFile", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["SystWeight", "weight_test"])
        self.assertRaises(ValueError, lambda: self.job.set_options())

    def test_set_option_SystWeight_error_does_not_exist(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["CutFile", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["SystWeight", "test"])
        self.assertRaises(LookupError, lambda: self.job.set_options())

    def test_set_option_SamplesToRun_all(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["CutFile", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["SamplesToRun", "all"])
        self.job.set_options()
        self.assertEqual(self.job.samples_to_run, "all")

    def test_set_option_SamplesToRun_int(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["CutFile", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["SamplesToRun", "1,2,5, 9"])
        self.job.set_options()
        self.assertEqual(self.job.samples_to_run, [1,2,5,9])

    def test_set_option_SamplesToRun_int_data(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["CutFile", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["SamplesToRun", "1,data,5, 9"])
        self.job.set_options()
        self.assertEqual(self.job.samples_to_run, [1,"data",5,9])

    def test_set_option_SamplesToRun_int_all(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["CutFile", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["SamplesToRun", "1,all,5, 9"])
        self.job.set_options()
        self.assertEqual(self.job.samples_to_run, "all")

    def test_set_option_SamplesToRun_error(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["CutFile", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["SamplesToRun", "1,test,5, 9"])
        self.assertRaises(ValueError, lambda: self.job.set_options())

    def test_set_option_RegionsToRun(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["CutFile", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["RegionsToRun", "SR,ZjetsCR"])
        self.job.set_options()
        self.assertEqual(self.job.samples_to_run, "all")

    def test_set_option_Compile(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["CutFile", "test"])
        self.job.add_option(["Compile", "false"])
        self.job.set_options()
        self.assertEqual(False, self.job.compile)

    def test_set_option_Compile_error(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test"])
        self.job.add_option(["CutFile", "test"])
        self.job.add_option(["Compile", "2000"])
        self.assertRaises(ValueError, lambda: self.job.set_options())

class TestOutputDescriptionWriting(unittest.TestCase):

    def setUp(self):
        self.job = LipCbrAnalysis.LipCbrAnalysis()
        self.job.add_option(["Samples", "test"])
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
        self.job = LipCbrAnalysis.LipCbrAnalysis()
        self.job.add_option(["Samples", "test"])
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

    def test_make_scratch_files(self):
        self.job.add_option(["Output", "test"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test_samples.txt"])
        self.job.add_option(["CutFile", "test_docuts.cxx"])
        self.job.add_option(["SamplesToRun", "300"])
        self.job.set_options()
        self.job.get_regions_and_max_cuts()
        self.job.get_samples_variables(test=True)
        self.job.make_scratch_files()
        string_check = "000000 ../../results/test/MC16/1516/SR/signal_sW/"
        with open("../../analysis_deploy/scratch/test/MC16_1516_SR_signal_sW.txt") as f:
            l = f.read()
        self.assertEqual(string_check, l)

    def test_make_scratch_files_IOError(self):
        self.job.add_option(["Output", "test"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test_samples.txt"])
        self.job.add_option(["CutFile", "test_docuts.cxx"])
        self.job.add_option(["SamplesToRun", "300"])
        self.job.set_options()
        self.job.get_regions_and_max_cuts()
        self.job.get_samples_variables(test=True)
        self.job.make_scratch_files()
        self.assertRaises(FileNotFoundError, lambda: open(
            "../../analysis_deploy/scratch/test/MC16_1516_background_SR_WtZ.txt"))

    def test_make_submit_files(self):
        self.job.add_option(["Output", "test"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test_samples.txt"])
        self.job.add_option(["CutFile", "test_docuts.cxx"])
        self.job.add_option(["SamplesToRun", "300"])
        self.job.set_options()
        self.job.create_output_folder()
        self.job.get_samples_variables(True)
        self.job.get_regions_and_max_cuts()
        self.job.make_submit_files()

    def test_make_submit_files_all(self):
        self.job.add_option(["Output", "test"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test_samples.txt"])
        self.job.add_option(["CutFile", "test_docuts.cxx"])
        self.job.add_option(["SamplesToRun", "300"])
        self.job.add_option(["Tree", "all"])
        self.job.set_options()
        self.job.create_output_folder()
        self.job.get_samples_variables(True)
        self.job.get_regions_and_max_cuts()
        self.job.make_submit_files()

class TestFileParsing(unittest.TestCase):

    def setUp(self):
        self.job = LipCbrAnalysis.LipCbrAnalysis()
        self.job.add_option(["Output", "test"])
        self.job.add_option(["Description", "test"])

    def test_get_samples_variables(self):
        self.job.add_option(["Samples", "test_samples.txt"])
        self.job.add_option(["CutFile", "test_cuts.cxx"])
        self.job.set_options()
        self.job.get_samples_variables(test=True)
        self.assertEqual(self.job.samples_list[0]["HistoFile"],"background_WtZ")
        self.assertEqual(self.job.samples_list[0]["SampleCode"],400)
        self.assertEqual(self.job.samples_list[1]["HistoFile"],"signal_sW")
        self.assertEqual(self.job.samples_list[1]["SampleCode"],300)

    def test_get_regions_and_max_cut(self):
        self.job.add_option(["Samples", "test_samples.txt"])
        self.job.add_option(["CutFile", "test_docuts.cxx"])
        self.job.set_options()
        self.job.get_regions_and_max_cuts()
        self.assertEqual(self.job.max_cuts, 7)
        self.assertEqual(self.job.regions, {'1': 'SR', '2': 'bWbWCR',
                                             '3': 'WtCR', '4': 'ZjetsCR'})

    def test_get_regions_and_max_cut_RegionsToRun(self):
        self.job.add_option(["Samples", "test_samples.txt"])
        self.job.add_option(["CutFile", "test_docuts.cxx"])
        self.job.add_option(["RegionsToRun", "SR"])
        self.job.set_options()
        self.job.get_regions_and_max_cuts()
        self.assertEqual(self.job.regions, {'1': 'SR'})

    def test_get_regions_and_max_cut_RegionsToRun_many(self):
        self.job.add_option(["Samples", "test_samples.txt"])
        self.job.add_option(["CutFile", "test_docuts.cxx"])
        self.job.add_option(["RegionsToRun", "SR, WtCR"])
        self.job.set_options()
        self.job.get_regions_and_max_cuts()
        self.assertEqual(self.job.regions, {'1': 'SR', '3': 'WtCR'})

    def test_get_regions_and_max_cut_RegionsToRun_error(self):
        self.job.add_option(["Samples", "test_samples.txt"])
        self.job.add_option(["CutFile", "test_docuts.cxx"])
        self.job.add_option(["RegionsToRun", "IDoNotExist"])
        self.job.set_options()
        self.assertRaises(ValueError, lambda:
                          self.job.get_regions_and_max_cuts())

class TestSubmitFunctions(unittest.TestCase):

    def setUp(self):
        self.job = LipCbrAnalysis.LipCbrAnalysis()
        self.job.add_option(["Output", "test"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Samples", "test_samples.txt"])
        self.job.add_option(["CutFile", "test_cuts.cxx"])
        self.job.set_options()

    def test_make_submit_job_data(self):
        sample = {"HistoFile": "data", "SampleCode": 1}
        region = ["1", "SR"]
        job_string = self.job.make_submit_job(sample, region)
        job_string_check = "time ./FCNCqzl_test --User=\"DataYear=1516\" "
        job_string_check += "--User=\"LepType=00\" --isData=1 --Region=1 "
        job_string_check += "--SetSystematicsFileName=../scratch/test/MC16_"
        job_string_check += "1516_SR_data.txt --OutputFileName=nominal\n"

        self.assertEqual(job_string, job_string_check)

    def test_make_submit_job_truth(self):
        self.job.tree = "particleLevel"
        sample = {"HistoFile": "test", "SampleCode": 999}
        region = ["1", "SR"]
        job_string = self.job.make_submit_job(sample, region)
        job_string_check = "time ./FCNCqzl_test --User=\"DataYear=1516\" "
        job_string_check += "--User=\"LepType=00\" --isTruth=1 "
        job_string_check += "--Sample=999 --MCYear=16 "
        job_string_check += "--Region=1 "
        job_string_check += "--SetSystematicsFileName=../scratch/test/MC16_"
        job_string_check += "1516_SR_test.txt --OutputFileName=nominal\n"

        self.assertEqual(job_string, job_string_check)

    def test_make_submit_job_nominal_sample(self):
        sample = {"HistoFile": "test", "SampleCode": 999}
        region = ["1", "SR"]
        job_string = self.job.make_submit_job(sample, region)
        job_string_check = "time ./FCNCqzl_test --User=\"DataYear=1516\" "
        job_string_check += "--User=\"LepType=00\" "
        job_string_check += "--Sample=999 --MCYear=16 "
        job_string_check += "--Region=1 "
        job_string_check += "--SetSystematicsFileName=../scratch/test/MC16_"
        job_string_check += "1516_SR_test.txt --OutputFileName=nominal\n"

        self.assertEqual(job_string, job_string_check)

    def test_make_submit_job_syst_weight(self):
        sample = {"HistoFile": "test", "SampleCode": 999}
        region = ["1", "SR"]
        job_string = self.job.make_submit_job(sample, region, syst_weight="doh")
        job_string_check = "time ./FCNCqzl_test --User=\"DataYear=1516\" "
        job_string_check += "--User=\"LepType=00\" "
        job_string_check += "--Sample=999 --MCYear=16 "
        job_string_check += "--SystWeight=doh --Region=1 "
        job_string_check += "--SetSystematicsFileName=../scratch/test/MC16_"
        job_string_check += "1516_SR_test.txt --OutputFileName=doh\n"

        self.assertEqual(job_string, job_string_check)

    def test_make_submit_job_syst_tree(self):
        sample = {"HistoFile": "test", "SampleCode": 999}
        region = ["1", "SR"]
        job_string = self.job.make_submit_job(sample, region, syst_tree="doh")
        job_string_check = "time ./FCNCqzl_test --User=\"DataYear=1516\" "
        job_string_check += "--User=\"LepType=00\" "
        job_string_check += "--Sample=999 --MCYear=16 "
        job_string_check += "--SystTree=doh --Region=1 "
        job_string_check += "--SetSystematicsFileName=../scratch/test/MC16_"
        job_string_check += "1516_SR_test.txt --OutputFileName=doh\n"

        self.assertEqual(job_string, job_string_check)

    def test_make_submit_job_error(self):
        sample = {"HistoFile": "test", "SampleCode": 999}
        region = ["1", "SR"]
        self.assertRaises(RuntimeError, lambda:
                self.job.make_submit_job(sample, region, syst_weight="doh",
                    syst_tree="doh"))

if __name__ == '__main__':
    unittest.main()

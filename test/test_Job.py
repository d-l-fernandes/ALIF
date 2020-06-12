import unittest
import sys
sys.path.insert(0, '../src/')

import filecmp
import os

import Job

class TestOptionsInput(unittest.TestCase):

    def setUp(self):
        self.job = Job.Job()

    def test_add_option(self):
        self.job.add_option(["Year", "151617"])
        self.assertEqual(self.job.options_dict["Year"], "151617")

    def test_check_required_option_error(self):
        self.job.add_option(["Year", "151617"])
        self.assertRaises(TypeError, lambda: self.job.check_required_options())

    def test_check_required_option(self):
        self.job.add_option(["Output", "001"])
        self.job.add_option(["Description", "test"])
        self.assertTrue(lambda: self.job.check_required_options())

    def test_check_invalid_option_error(self):
        self.job.add_option(["Output", "001"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["WowDude!", "check it out"])
        self.assertRaises(TypeError, lambda: self.job.check_invalid_options())

    def test_set_option_Year(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Year", "151617"])
        self.job.set_options()
        self.assertEqual(151617, self.job.year)

    def test_set_option_Year_error(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["Year", "2000"])
        self.assertRaises(ValueError, lambda: self.job.set_options())

    def test_set_option_MCYear(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["MCYear", "15"])
        self.job.set_options()
        self.assertEqual(15, self.job.mc_year)

    def test_set_option_MCYear_error(self):
        self.job.add_option(["Output", "000"])
        self.job.add_option(["Description", "test"])
        self.job.add_option(["MCYear", "2000"])
        self.assertRaises(ValueError, lambda: self.job.set_options())


class TestOutputDescriptionWriting(unittest.TestCase):

    def setUp(self):
        self.job = Job.Job()

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
        self.job = Job.Job()

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


if __name__ == '__main__':
    unittest.main()

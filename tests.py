import unittest
from max_words import *

TEST_DOCUMENTS_PATH = "./testing_docs"


class MyTest(unittest.TestCase):

    def test_are_there_files_for_testing(self):
        files = []

        for (dirpath, _, filenames) in walk(TEST_DOCUMENTS_PATH):
            # first loop will give top directory files only.
            # list comprension to add relative path to filename.
            files = ["{}/{}".format(dirpath, filename) for filename in
                     filenames]
            break

        self.assertTrue(len(files) > 0)

    def test_getting_file_names(self):
        self.assertTrue(len(get_files(TEST_DOCUMENTS_PATH)) > 0)

    def test_word_data_structure(self):
        ds = build_word_ds(get_files(TEST_DOCUMENTS_PATH))
        # get any item from dict:
        item = next(iter(ds.keys()))

        # print(type(ds[item]))
        # print(ds[item])
        self.assertTrue(type(ds[item]) is list)
        self.assertTrue(type(ds[item][0]) is int)
        self.assertTrue(type(ds[item][1]) is defaultdict)

        item2 = next(iter(ds[item][1]))
        self.assertTrue(type(ds[item][1][item2]) is set)


if __name__ == '__main__':
    unittest.main()

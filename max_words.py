"""
This solution is one possible version. The sentences in the files are loaded
to memory one file at a time (as opposed to loading all the
sentences from ALL files to memory).
This allows analysis of many files, as long as
each file can fit in memory (an average size of a large book (800 pages)
is about 1 Mb, so this should'nt be a problem).
The downside of this approach is
that files must be passed twice (once for building the data structure and
again for printing the lines) and increased file readings add to processing time.

An alternative approach could load all sentences to memory which could lead to
better performance in some cases. But, this approach could cause substantial slow-down
if the data structure becomes larger than RAM. 

For bigger collections it may well make sense to use some sort of persistence 
such as a database or a data-structure store?   

There is a trade-off between the approaches.


****** Notes:

1. The program runs with Python 3.

2. It assumes that nltk is installed.
    If it's not, you can get it with pip:
    sudo pip3 install nltk

3. The program should then run with the command:

    python3 max_words.py


"""

from os import walk
from collections import defaultdict
import re
import heapq
import nltk.data

DOCUMENTS_PATH = "./production_docs"
# DOCUMENTS_PATH = "./testing_docs"
NUMBER_OF_TOP_WORDS = 3


def print_top_words_in_files(path, number_of_top_words):
    """
    Print the most common words and the sentences they appear in
    in the files in the given path.

    :param number_of_top_words: number of top most common word to print out
    :param path: path to files
    """
    files_to_analyse = get_files(path)
    word_dict = build_word_dict(files_to_analyse)
    top_words = heapq.nlargest(number_of_top_words,
                               word_dict,
                               key=lambda key: word_dict[key][0])
    print_results(top_words, word_dict)


def get_files(path):
    """
    Return all files in top directory of the given path.
    Note: can be easily changed to search in all subdirectories if required.

    :param path: the path to search for files
    :return: list of file names with relative path
    """

    files = []

    for (dirpath, _, filenames) in walk(path):
        # first loop will give top directory files only.
        # list comprension to add relative path to filename.
        files = ["{}/{}".format(dirpath, filename) for filename in filenames]
        break

    return files


def build_word_dict(files):
    """
    Build a dictionary of words (word_dict) where each key is a word
    appearing in the files and each value is a list containing a counter,
    and, the location of the word in the files as following:

    word_dict {
        word_A: [
                    counter,    # the total number of times that the word appears in all the files
                    appears_in_documents_dict  # a dictionary of locations, see structure below
                ]
        word_B:...,
    }

    appears_in_documents_dict is a dictionary where the key is the document
    name and the value is a set of line numbers:

    appears_in_documents_dict {
        doc_A: {set of line numbers},
        doc_B: ...,
    }

    :param files: list of files from which the data structure is built
    :return word_dict: the data structure of words and their locations
    """

    word_dict = defaultdict(lambda: [0, defaultdict(set)])
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    for file in files:
        with open(file) as f:
            data = f.read()
            # break into sentences using nltk
            sentence_list = tokenizer.tokenize(data)

            for line_number, line in enumerate(sentence_list):
                # split sentences into words (including apostrophes)
                # and add to data structure:
                words = re.findall(r"[\w']+", line)
                for word in words:
                    # increment word count
                    word_dict[word][0] += 1
                    # add line number to the set of the file's line numbers
                    word_dict[word][1][file].add(line_number)

    return word_dict


def print_results(top_words, word_dict):
    """
    Print top words with the relevant sentences

    :param top_words: list of top words to print out
    :param word_dict: data structure that includes words and sentence locations
    """

    print("Top", NUMBER_OF_TOP_WORDS,
          "most common words "
          "(and the corresponding sentences) in descending order:\n")

    for word in top_words:

        word_location_dict = word_dict[word][1]
        documents = ', '.join(list(word_location_dict.keys()))
        sentences = get_sentences(word_location_dict)

        print(
            "The word '{}' Appears: {} times".format(word, word_dict[word][0]))
        print("In the following documents: {}".format(documents))
        print("In the following sentences:")
        for sentence in sentences:
            print(sentence)
        print("\n", "*" * 80, "\n")


def get_sentences(dict_of_files_and_line_numbers):
    """
    Returns a list of all the sentences which are pointed to in the
    dictionary given

    :param dict_of_files_and_line_numbers: dictionary where key is file name
                                           and the value is a set of line numbers in the file
    :return: all_lines: list of sentences
    """

    all_lines = []

    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    for file, line_numbers in dict_of_files_and_line_numbers.items():
        with open(file) as f:
            data = f.read()
            # break file into list of sentences
            sentence_list = tokenizer.tokenize(data)
            for line_number in line_numbers:
                # tokenizer keeps new lines within sentences, remove them:
                clean_sentence = re.sub(r'\n', ' ', sentence_list[line_number])
                all_lines.append("{} line:{}: {}".
                                 format(file,
                                        line_number,
                                        clean_sentence
                                        )
                                 )

    return all_lines


if __name__ == '__main__':
    print_top_words_in_files(DOCUMENTS_PATH, NUMBER_OF_TOP_WORDS)

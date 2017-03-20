#coding=utf-8
from common import *

WORD_INDEX_INFILE = 0

INDEX_IN_FILE = dict()
INDEX_IN_FILE["target_word"] = 1
INDEX_IN_FILE["score"] = 2
INDEX_IN_FILE["total_time"] = 3
INDEX_IN_FILE["correct_time"] = 4
INDEX_IN_FILE["continuous_correct_time"] = 5

INDEX_IN_LIST = dict()
INDEX_IN_LIST["target_word"] = 0
INDEX_IN_LIST["score"] = 1
INDEX_IN_LIST["total_time"] = 2
INDEX_IN_LIST["correct_time"] = 3
INDEX_IN_LIST["continuous_correct_time"] = 4


def main():
    choose_dict("bilingual")
    init_words()
    update_word_infos_by_time()
    encoding = choose_encoding()
    print "***** You can type in 'exit()' to end the dictation *****"
    words = get_word_infos(encoding, WORD_INDEX_INFILE, INDEX_IN_FILE)
    dictation(words, encoding, INDEX_IN_LIST, "bilingual")
    update_word_infos(words, encoding)
    if os.path.exists("key.inf"):
        os.remove("key.inf")


if __name__ == "__main__":
    main()

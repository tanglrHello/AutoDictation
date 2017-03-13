# coding=utf-8
import random
import os
from datetime import datetime

S_WORD_INDEX_INFILE = 0
T_WORD_INDEX_INFILE = 1
SCORE_INDEX_INFILE = 2
TOTAL_TIME_INDEX_INFILE = 3
CORRECT_TIME_INDEX_INFILE = 4
CONTINUOUS_CORRECT_TIME_INDEX_INFILE = 5

T_WORD_INDEX_INLIST = 0
SCORE_INDEX_INLIST = 1
TOTAL_TIME_INDEX_INLIST = 2
CORRECT_TIME_INDEX_INLIST = 3
CONTINUOUS_CORRECT_TIME_INDEX_INLIST = 4

def main():
    init_words()
    update_word_infos_by_time()
    encoding = choose_encoding()
    print "***** You can type in 'exit()' to end the dictation *****"
    words = get_word_infos(encoding)
    dictation(words, encoding)
    update_word_infos(words, encoding)
    if os.path.exists("key.inf"):
        os.remove("key.inf")


def choose_encoding():
    encoding = 0
    # choose system encoding type
    while True:
        encoding = raw_input(
            "Choose your system encoding type: 1. gbk(recommended for win systems) "
            "2. utf-8 (recommend for Unix/Linux/MacOS)")
        if encoding == '1' or encoding == '2':
            break
        else:
            print "please input 1 or 2"
    return encoding


# return a dict, each key is a source word, value is a list containing target word and its score
# such as {'中国' : ['China', 100]}
def get_word_infos(encoding):
    # get word pairs from file
    dictionary_file = open("dict.txt")
    words = {}
    for line in dictionary_file.readlines():
        if encoding == '1':
            line = line.decode('utf-8').encode('gbk')

        info = line.strip().split('\t')
        assert len(info) == 6

        source_word = info[S_WORD_INDEX_INFILE]
        target_words = info[T_WORD_INDEX_INFILE]
        score = float(info[SCORE_INDEX_INFILE])
        total_dict_time = float(info[TOTAL_TIME_INDEX_INFILE])
        correct_dict_time = float(info[CORRECT_TIME_INDEX_INFILE])
        continuous_correct_time = float(info[CONTINUOUS_CORRECT_TIME_INDEX_INFILE])

        words[source_word] = [target_words, score, total_dict_time, correct_dict_time, continuous_correct_time]

    return words


def dictation(words, encoding):
    all_words = words
    first_round = True

    words_to_dictate = init_real_dictate_words(words)

    if len(words_to_dictate) == 0:
        print "You don't need to do a dictation now. Come back later ~ ~ ~ ~"
        return

    normal_exit = True
    while len(words_to_dictate) != 0:
        wrong_words, continue_dictate = dictation_round(all_words, words_to_dictate, first_round, encoding)
        if not continue_dictate:
            normal_exit = False
            break

        print "you correctly remembered", len(words_to_dictate) - len(wrong_words), "words, wrong with", len(
            wrong_words), "words. Good Job! Just keeeeeeeep on!"

        if len(wrong_words) != 0:
            print "Let's try again for those naughty words~"
            raw_input("press any key to continue")
            print "++++++++++++++++++++++++++++++++++++++++++++++++++"

        words_to_dictate = wrong_words
        first_round = False

    if normal_exit:
        print "You have remembered all the words! So excellent!"
    else:
        print "You exit this dictation halfway. Remember go back again when you are free ~ ~"


def init_real_dictate_words(words):
    words_to_real_dictate = {}
    for word in words:
        score = words[word][SCORE_INDEX_INLIST]
        total_dictation_time = words[word][TOTAL_TIME_INDEX_INLIST]
        if score > 80 and total_dictation_time < 3:
            words_to_real_dictate[word] = words[word]
    return words_to_real_dictate


def dictation_round(all_words, words_to_dictate, first_round, encoding):
    wrong_words = {}

    word_list = words_to_dictate.items()
    random.shuffle(word_list)

    current_index = 1
    total_word_number = len(word_list)

    for word in word_list:
        source_word = word[0]
        target_words = word[1][T_WORD_INDEX_INLIST].split("/")

        print "(" + str(current_index) + "/" + str(total_word_number) + ")", source_word
        current_index += 1
        answer = raw_input()

        if answer == "exit()":
            return [], False

        # check answer
        for i, target_word in enumerate(target_words):
            if answer == target_word:
                if encoding == "1":
                    print u"√".encode("gbk"),
                else:
                    print u"√",

                if len(target_word) > 1:
                    print "Also:",

                for j in range(len(target_words)):
                    if i != j:
                        print target_words[j], "#",
                print ""

                score = all_words[source_word][SCORE_INDEX_INLIST]
                total_time = all_words[source_word][TOTAL_TIME_INDEX_INLIST]
                continuous_correct_time = all_words[source_word][CONTINUOUS_CORRECT_TIME_INDEX_INLIST]

                if first_round:
                    # update score
                    if score > 80 and total_time >= 3 and continuous_correct_time > 1:
                        all_words[source_word][SCORE_INDEX_INLIST] = 75
                    else:
                        all_words[source_word][SCORE_INDEX_INLIST] -= 10 * (1 + continuous_correct_time)

                # update dictate time
                all_words[source_word][TOTAL_TIME_INDEX_INLIST] += 1
                all_words[source_word][CORRECT_TIME_INDEX_INLIST] += 1
                # update continuous_correct_time
                all_words[source_word][CONTINUOUS_CORRECT_TIME_INDEX_INLIST] += 1

                break
        else:
            print "\n".join(target_words), "(reference)"
            print "X"
            wrong_words[source_word] = word[1]

            # update score
            if all_words[source_word][SCORE_INDEX_INLIST] < 80:
                all_words[source_word][SCORE_INDEX_INLIST] = 88
            else:
                all_words[source_word][SCORE_INDEX_INLIST] *= 1.1
            # update dictate time
            all_words[source_word][TOTAL_TIME_INDEX_INLIST] += 1
            # update continuous_correct_time
            all_words[source_word][CONTINUOUS_CORRECT_TIME_INDEX_INLIST] = 0

        total_time = all_words[source_word][TOTAL_TIME_INDEX_INLIST]
        correct_time = all_words[source_word][CORRECT_TIME_INDEX_INLIST]

        print "( History correct rate: ",  str(correct_time / total_time * 100) + "%)"
        print "-----------------------------------"

    return wrong_words, True


def update_word_infos(words, encoding):
    new_file = open("dict_new.txt", "w")
    for word in words:
        words[word] = [word] + [str(info) for info in words[word]]

        if encoding == "1":
            new_file.write(('\t'.join(words[word]) + "\n").decode("gbk").encode("utf-8"))
        else:
            new_file.write('\t'.join(words[word]) + "\n")

    new_file.close()

    os.remove("dict.txt")
    os.rename("dict_new.txt", "dict.txt")
    return


def init_words():
    # update words score
    word_file = open("dict.txt")
    new_file = open("dict_new.txt", "w")

    for line in word_file.readlines():
        word_info = line.strip().split("\t")
        if len(word_info) == 2:
            # 4th col records total dictate time
            # 5th col records correct time
            # 6th col records recent continuous correct time
            word_info += ['100', '0', '0', '0']
        elif len(word_info) == 3:
            word_info += ['0', '0', '0']
        elif len(word_info) == 6:
            pass
        else:
            assert False

        new_file.write("\t".join(word_info) + "\n")

    word_file.close()
    new_file.close()

    os.remove("dict.txt")
    os.rename("dict_new.txt", "dict.txt")


def update_word_infos_by_time():
    time_filename = "system.inf"
    time_diff = 0
    time_now = datetime.now()

    if not os.path.exists(time_filename):
        pass
    else:
        time_file = open("system.inf")
        last_login_time = datetime.now()
        for timeline in time_file.readlines():
            last_login_time = timeline

        # compute time diff by days
        last_login_time.strip().split()
        last_login_time_info = last_login_time.strip().split()[0].split('-')
        last_login_datetime = datetime(int(last_login_time_info[0]),
                                       int(last_login_time_info[1]),
                                       int(last_login_time_info[2]))
        time_diff = (time_now - last_login_datetime).days
        time_file.close()

    open("system.inf", 'a').write(str(time_now) + "\n")

    # count total words number
    word_file = open("dict.txt")
    word_number = 0
    for _ in word_file.readlines():
        word_number += 1
    word_file.close()

    # update words score
    word_file = open("dict.txt")
    new_file = open("dict_new.txt", "w")

    expected_dictate_number = 20.0
    score_diff = time_diff * (expected_dictate_number * 10) / word_number

    for word_info in word_file.readlines():
        word_info = word_info.strip().split('\t')
        if len(word_info) == 2:
            word_info.append("100")
        else:
            word_info[2] = str(float(word_info[2]) + score_diff)

        new_file.write("\t".join(word_info) + "\n")

    word_file.close()
    new_file.close()

    os.remove("dict.txt")
    os.rename("dict_new.txt", "dict.txt")
    return

main()

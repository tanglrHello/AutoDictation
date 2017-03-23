# coding=utf-8
import random
import os
from datetime import datetime


DICT_FILE = None


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


def choose_dict(type):
    global DICT_FILE
    files = os.listdir('.')
    file_index = 0

    if type == "bilingual":
        bi_dicts = filter(lambda x: x.endswith(".bi.txt"), files)
        if len(bi_dicts) == 1:
            DICT_FILE = bi_dicts[0]
            return
        elif len(bi_dicts) == 0:
            print "No available dict file!!!"
            exit()

    elif type == "monolingual":
        mo_dicts = filter(lambda x: x.endswith(".mo.txt"), files)
        if len(mo_dicts) == 1:
            DICT_FILE = mo_dicts[0]
            return
        elif len(mo_dicts) == 0:
            print "No available dict file!!!"
            exit()

    print "Please choose a dict file:"
    candidate_files = []
    for filename in files:
        if type == "bilingual":
            if filename.endswith(".bi.txt"):
                print str(file_index) + "\t" + filename
                file_index += 1
                candidate_files.append(filename)
        elif type == "monolingual":
            if filename.endswith(".mo.txt"):
                print str(file_index) + "\t" + filename
                file_index += 1
                candidate_files.append(filename)
        else:
            assert False

    choice = raw_input("Your choice: ")
    flag = False
    while flag == False:
        try:
            choice = int(choice)
            assert 0 <= choice <= file_index - 1
            flag = True
        except:
            choice = raw_input("Invalid choice. Please choose again: ")

    DICT_FILE = candidate_files[choice]


# return a dict, each key is a source word, value is a list containing target word and its score etc.
def get_word_infos(encoding, word_fileindex, index_in_file):
    # get word pairs from file
    global DICT_FILE
    dictionary_file = open(DICT_FILE)
    words = {}
    for line in dictionary_file.readlines():
        if encoding == '1':
            line = line.decode('utf-8').encode('gbk')

        if line.strip() == "":
            continue

        info = line.strip().split('\t')
        assert len(info) == 1 + len(index_in_file)

        source_word = info[word_fileindex]
        words[source_word] = []

        for key, index in sorted(index_in_file.items(), key = lambda x:x[1]):
            try:
                words[source_word].append(float(info[index]))
            except:
                words[source_word].append(info[index])

    return words


def dictation(words, encoding, index_in_list, type):
    all_words = words
    first_round = True

    words_to_dictate = init_real_dictate_words(words, index_in_list)

    if len(words_to_dictate) == 0:
        print "You don't need to do a dictation now. Come back later ~ ~ ~ ~"
        return

    normal_exit = True
    while len(words_to_dictate) != 0:
        wrong_words, continue_dictate = dictation_round(all_words, words_to_dictate, first_round, encoding, index_in_list, type)
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


def init_real_dictate_words(words, index_in_list):
    words_to_real_dictate = {}
    for word in words:
        score = words[word][index_in_list["score"]]
        total_dictation_time = words[word][index_in_list["total_time"]]

        if score > 80 or total_dictation_time < 3:
            words_to_real_dictate[word] = words[word]

    if len(words_to_real_dictate) > 50:
        word_list = sorted(words_to_real_dictate.items(), key=lambda x:float(x[1][index_in_list["score"]]))
        words_to_real_dictate = dict(word_list[:50])

    if len(words_to_real_dictate) < 20:
        word_list = words.items()
        to_add_num = min(20 - len(words_to_real_dictate), len(words) - len(words_to_real_dictate))
        while to_add_num > 0:
            word_info = random.choice(word_list)
            if word_info[0] not in words_to_real_dictate:
                words_to_real_dictate[word_info[0]] = word_info[1]
                to_add_num -= 1

    return words_to_real_dictate


def update_correct(all_words, source_word, index_in_list, first_round):
    score = all_words[source_word][index_in_list["score"]]
    total_time = all_words[source_word][index_in_list["total_time"]]
    continuous_correct_time = all_words[source_word][index_in_list["continuous_correct_time"]]

    if first_round:
        # update score
        if score > 80 and total_time >= 3 and continuous_correct_time > 1:
            all_words[source_word][index_in_list["score"]] = 75
        else:
            all_words[source_word][index_in_list["score"]] -= 10 * (1 + continuous_correct_time)

    # update dictate time
    all_words[source_word][index_in_list["total_time"]] += 1
    all_words[source_word][index_in_list["correct_time"]] += 1
    # update continuous_correct_time
    all_words[source_word][index_in_list["continuous_correct_time"]] += 1


def update_wrong(all_words, source_word, index_in_list):
    # update score
    if all_words[source_word][index_in_list["score"]] < 80:
        all_words[source_word][index_in_list["score"]] = 88
    else:
        all_words[source_word][index_in_list["score"]] *= 1.1
    # update dictate time
    all_words[source_word][index_in_list["total_time"]] += 1
    # update continuous_correct_time
    all_words[source_word][index_in_list["continuous_correct_time"]] = 0


def judge_for_bilingual(user_input, target_words, encoding):
    # check answer
    for i, target_word in enumerate(target_words):
        if user_input == target_word:
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

            return True

    return False


def dictate_one_bilingual(all_words, source_word, answer, index_in_list, encoding, first_round, wrong_words):
    target_words = all_words[source_word][index_in_list["target_word"]].split("/")
    if judge_for_bilingual(answer, target_words, encoding):
        update_correct(all_words, source_word, index_in_list, first_round)
    else:
        print "\n".join(target_words), "(reference)"
        print "X"
        wrong_words[source_word] = all_words[source_word]
        update_wrong(all_words, source_word, index_in_list)


def check_one_monolingual(all_words, word, answer, index_in_list, encoding, first_round, wrong_words):
    while answer != "n" and answer != "y":
        answer = raw_input("please input y or n: ")

    if answer == "y":
        update_correct(all_words, word, index_in_list, first_round)
    elif answer == "n":
        wrong_words[word] = all_words[word]
        update_wrong(all_words, word, index_in_list)


def dictation_round(all_words, words_to_dictate, first_round, encoding, index_in_list, type):
    wrong_words = {}

    word_list = words_to_dictate.items()
    random.shuffle(word_list)

    current_index = 1
    total_word_number = len(word_list)

    if type == "monolingual":
        i = 0
        for word in word_list:
            print word[0],
            i += 1
            if i % 5 == 0:
                print ""
        print ""

    for word in word_list:
        source_word = word[0]

        print "(" + str(current_index) + "/" + str(total_word_number) + ")", source_word
        current_index += 1
        answer = raw_input()

        if answer == "exit()":
            return [], False

        if type == "bilingual":
            dictate_one_bilingual(all_words, source_word, answer, index_in_list, encoding, first_round, wrong_words)
        else:
            check_one_monolingual(all_words, source_word, answer, index_in_list, encoding, first_round, wrong_words)

        total_time = all_words[source_word][index_in_list["total_time"]]
        correct_time = all_words[source_word][index_in_list["correct_time"]]

        print "( History correct rate: ",  str(correct_time / total_time * 100) + "%)"
        print "-----------------------------------"

    return wrong_words, True


def update_word_infos(words, encoding):
    global DICT_FILE

    new_file = open(DICT_FILE + ".new", "w")
    for word in words:
        words[word] = [word] + [str(info) for info in words[word]]

        if encoding == "1":
            new_file.write(('\t'.join(words[word]) + "\n").decode("gbk").encode("utf-8"))
        else:
            new_file.write('\t'.join(words[word]) + "\n")

    new_file.close()

    os.remove(DICT_FILE)
    os.rename(DICT_FILE + ".new", DICT_FILE)
    return


def init_words():
    global  DICT_FILE

    # update words score
    word_file = open(DICT_FILE)
    new_file = open(DICT_FILE + ".new", "w")

    for line in word_file.readlines():
        word_info = line.strip().split("\t")

        if DICT_FILE.endswith(".bi.txt"):
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
        elif DICT_FILE.endswith(".mo.txt"):
            if len(word_info) == 1:
                word_info += ['100', '0', '0', '0']
            elif len(word_info) == 2:
                word_info += ['0', '0', '0']
            elif len(word_info) == 5:
                pass
            else:
                assert False

        new_file.write("\t".join(word_info) + "\n")

    word_file.close()
    new_file.close()

    os.remove(DICT_FILE)
    os.rename(DICT_FILE + ".new", DICT_FILE)


def update_word_infos_by_time(score_file_index):
    global DICT_FILE

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
    word_file = open(DICT_FILE)
    word_number = 0
    for _ in word_file.readlines():
        word_number += 1
    word_file.close()

    # update words score
    word_file = open(DICT_FILE)
    new_file = open(DICT_FILE + ".new", "w")

    expected_dictate_number = 20.0
    score_diff = time_diff * (expected_dictate_number * 10) / word_number

    for word_info in word_file.readlines():
        word_info = word_info.strip().split('\t')
        word_info[score_file_index] = str(float(word_info[score_file_index]) + score_diff)

        new_file.write("\t".join(word_info) + "\n")

    word_file.close()
    new_file.close()

    os.remove(DICT_FILE)
    os.rename(DICT_FILE + ".new", DICT_FILE)
    return

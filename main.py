# coding=utf-8
import random
import os
from datetime import datetime


def main():
    update_word_infos_by_time()
    encoding = choose_encoding()
    words = get_word_infos(encoding)
    dictation(words)
    update_word_infos(words)


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
        assert len(info) == 3

        source_word = info[0]
        target_words = info[1]

        words[source_word] = [target_words, float(info[2])]

    return words


def dictation(words):
    words_to_dictate = words
    all_words = words
    first_round = True
    while len(words_to_dictate) != 0:
        wrong_words = dictation_round(all_words, words_to_dictate, first_round)

        print "you correctly remembered", len(words) - len(wrong_words), "words, wrong with", len(
            wrong_words), "words. Good Job! Just keeeeeeeep on!"

        if len(wrong_words) != 0:
            print "Let's try again for those naughty words~"
            raw_input("press any key to continue")
            print "+++++++++++++++++++++++++"

        words_to_dictate = wrong_words
        first_round = False

    print "You have remembered all the words! So excellent!"


def dictation_round(all_words, words_to_dictate, first_round):
    wrong_words = {}
    words_to_real_dictate = {}

    # if this is the first dictation round, only dictate words with score greater then 80
    # else: dictate all words
    if first_round:
        for word in words_to_dictate:
            if words_to_dictate[word][1] >= 80:
                words_to_real_dictate[word] = words_to_dictate[word]
    else:
        words_to_real_dictate = words_to_dictate

    word_list = words_to_real_dictate.items()
    random.shuffle(word_list)

    for word in word_list:
        source_word = word[0]
        target_words = word[1][0].split("/t")

        print source_word
        answer = raw_input()

        # check answer
        for i, target_word in enumerate(target_words):
            if answer == target_word:
                print "well done! This word can also be translated into:",
                for j in range(len(target_words)):
                    if i != j:
                        print target_words[j], "#"
                    print ""
                all_words[source_word][1] -= 10
                break
        else:
            print "wrong answer, remenber again:", "#".join(target_words)
            wrong_words[source_word] = word[1]
            # change the word score
            if first_round:
                all_words[source_word][1] *= 1.5

        print "**********"

    return wrong_words


def update_word_infos(words):
    new_file = open("dict_new.txt", "w")
    for word in words:
        target_words = words[word][0]
        score = words[word][1]
        new_file.write(word + "\t" + target_words + "\t" + str(score) + "\n")
    new_file.close()

    os.remove("dict.txt")
    os.rename("dict_new.txt", "dict.txt")
    return


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

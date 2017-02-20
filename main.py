import random

def main():
    # choose system encoding type
    while True:
        encoding = raw_input("Choose your system encoding type: 1. gbk(recommended for win systems) 2. utf-8 (recommend for Unix/Linux/MacOS)")
        if encoding == '1' or encoding == '2':
            break
        else:
            print "please input 1 or 2"

    # get word pairs from file
    dictionary_file = open("dict.txt")
    words = []
    for line in dictionary_file.readlines():
        if encoding == '1':
            line = line.decode('utf-8').encode('gbk')
        info = line.strip().split()
        assert len(info) == 2
        words.append(info)
    total_words_number = len(words)

    # auto dictation
    wrong_word_pairs = []
    while len(words) != 0:
        random.shuffle(words)
        for word in words: 
            chinese = word[0]
            english = word[1]
            print chinese
            answer = raw_input()

            # check answer
            if answer == word[1]:
                print "well done!"
            else:
                print "wrong answer, remenber again:", word[1]
                wrong_word_pairs.append(word)
            print "**********"
        print "you correctly remembered", total_words_number - len(wrong_word_pairs), "words, wrong with", len(wrong_word_pairs), "words. Good Job! Just keeeeeeeep on!"
        if len(wrong_word_pairs) != 0:
            print "Let's try again for those naughty words~"
            raw_input("press any key to continue")
            print "+++++++++++++++++++++++++"
        words = wrong_word_pairs
        wrong_word_pairs = []
    print "You have remembered all the words! So excellent!"

main()

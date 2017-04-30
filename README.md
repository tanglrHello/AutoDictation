# AutoDictation

This script is used for remembering new words/new sentences. You can creat your own dictionary by editting the content of dict.bi.txt. Attention, if you'd like to have a bilingual dictionary, keep the suffix of the txt file to be '.bi.txt'.

Our program support biligual mode(ForBilingual.py) and monolingual mode(ForMonolingual.py). If you want to use '.bi.txt', you should use 'python ForBilingual.py' to start it. 

If there are more than one .bi.txt in the same path, you are required to choose which one to use at the begining:

	Please choose a dict file:
	0	oral.bi.txt
	1	tofel.bi.txt
	Your choice: 

Attention, dict.bi.txt is encoded as a utf-8 file. 
You should put a word pair in a line, using a tab('\t') to separate Chinese word and English word. Like the examole given in dict.txt ( the first word will be shown to you, and you should input the second word interactively ):
	
	惊厥	convulsion
	腺癌	adenocarcinoma
	食管	esophagus
	腹泻	diarrhea
	胸骨柄	manubrium
	气胸	pneumothorax
	肺气肿	emphysema

If one word has two or more translations, use a slash('/') to seprate them, such as:

	你好	hi/hello

Your answer will be judged as correct as long as it matches one tranlation.
	

After the possible file choosing stage, you need to choose the encoding type of your system inorder to avoid messy code when displaying word of Chinese or other language.

	$ python main.py 
	Choose your system encoding type: 1. gbk(recommended for win systems) 2. utf-8 (recommend for Unix/Linux/MacOS)

You should type 1 or 2 now.

For bilingual mode, you are then required to further choose the dictation mode:

	Choose dictation mode: 1.spell mode 2.no spell mode: 

If you choose '1', you need to type in the whole translation in terminal, and the program will tell you whether you are right; If you choose '2', after showing each source word for you, the program will give you some time to recall the translation. When you finish recalling, press anykey to get the reference. And you need to judge by yourself. Then type in 'y' if you are right, or 'n' if you are wrong:

	(1/60) 谁也不想
	Nobody does. (reference)
	Are you right? y(yes) or n(no): y
	( History correct rate:  100.0%)

Then words in your dictionary will be shown to you one by one:
	
	(1/60) 校订，修正，复习
	review
	revision (reference)
	X
	( History correct rate:  0.0%)
	-----------------------------------
	(2/60) 房客；居住
	house
	tenant (reference)
	X
	( History correct rate:  0.0%)
	-----------------------------------
	(3/60) 规定；开处方
	prescribe
	√ 
	( History correct rate:  100.0%)

The program will tell you whether you have made a correct answer.
If you gave a wrong answer, this word will be tested again after the current round is over. If you make a mistake once more, it will be tested once again after the current round until you make it correctly.

After a dictation round, you will be shown how many words you have answered correctly and how many wrongly. Then you can press any key to start the next dictation round for those wrongly answered words.
	
	you correctly remembered 4 words, wrong with 3 words. Good Job! Just keeeeeeeep on!
	Let's try again for those naughty words~
	press any key to continue

When you have correctly remembered all words, the following information will be given:

	you correctly remembered 7 words, wrong with 0 words. Good Job! Just keeeeeeeep on!
	You have remembered all the words! So excellent!

Finally, keep the numbers in dictionary files unchanged. Now, enjoy your time~



# AutoDictation

This script is used for remembering new words. You can creat your own dictionary by editting the content of dict.txt.


Attention, dict.txt is encoded as a utf-8 file. 
You should put a word pair in a line, using a tab('\t') to separate Chinese word and English word. Like the examole given in dict.txt ( the first word will be shown to you, and you should input the second word interactively ):
	
	惊厥	convulsion
	腺癌	adenocarcinoma
	食管	esophagus
	腹泻	diarrhea
	胸骨柄	manubrium
	气胸	pneumothorax
	肺气肿	emphysema

Then run main.py in your terminal.

First you need to choose the encoding type of your system inorder to avoid messy code when displaying word of Chinese or other language.

	$ python main.py 
	Choose your system encoding type: 1. gbk(recommended for win systems) 2. utf-8 (recommend for Unix/Linux/MacOS)

You should type 1 or 2 now.

Then words in your dictionary will be shown to you one by one:
	
	腺癌
	adenocarcinoma
	well done!
	**********
	腹泻
	diarrhea
	well done!
	**********
	气胸
	pneumothoras
	wrong answer, remenber again: pneumothorax

The program will tell you whether you have made a correct answer.
If you gave a wrong answer, this word will be tested again after the current round is over. If you make a mistake once more, it will be tested once again after the current round until you make it correctly.

After a dictation round, you will be shown how many words you have answered correctly and how many wrongly. Then you can press any key to start the next dictation round for those wrongly answered words.
	
	you correctly remembered 4 words, wrong with 3 words. Good Job! Just keeeeeeeep on!
	Let's try again for those naughty words~
	press any key to continue

When you have correctly remembered all words, the following information will be given:

	you correctly remembered 7 words, wrong with 0 words. Good Job! Just keeeeeeeep on!
	You have remembered all the words! So excellent!




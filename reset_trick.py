import os

if not os.path.exists("key.inf"):
    print "You can't execute this program!"
    exit(1)
os.remove("key.inf")

dict_file = open("dict.txt")
new_file = open("new_dict.txt", "w")
for line in dict_file.readlines():
    line_info = line.split("\t")
    if len(line_info) == 2:
        new_file.write(line.strip() + "\t" + "80\n")
    else:
        line_info[2] = "80"
        new_file.write("\t".join(line_info) + "\n")
dict_file.close()
new_file.close()
os.remove("dict.txt")
os.rename("new_dict.txt", "dict.txt")

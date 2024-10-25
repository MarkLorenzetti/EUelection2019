import os
import unicodecsv as csv
import json
import glob

#wd = r'C:\Users\***\Desktop\Elezioni-Europee2019'
#os.chdir(wd)

print(" ")
print("The .csv file is going to be saved here: ", os.getcwd())
print(" ")
filename = str(input("Give a name to your file...")) + ".csv"

Num_files = len(glob.glob("*.txt"))
count = 0
files = glob.glob("*.txt")
print(" ")
print("The following '.txt' files are going to be processed: ")
print(" ")
for i in files:
	print(i)
print(" ")
print("Working progress...")
print(" ")

while count < Num_files:

	tweets_data = []
	
	data_file = open(files[count], "r", encoding='utf-8')
	for line in data_file:
		tweet = json.loads(line)
		tweets_data.append(tweet)

	data_file.close()

	header = ['id', 'country', 'time_stamp', 'lang', 'text']
	data_csv = open(filename, 'ab')
	csvwriter = csv.writer(data_csv)
	csvwriter.writerow(header)

	for entry in tweets_data:
		csvwriter.writerow([entry['id'], entry['place']['country'] if entry['place'] != None else None, entry['created_at'], entry['lang'], entry['full_text']])

	data_csv.close()
	
	count+=1
	print("File number", count, "collected")
	
print("Files preprocessed: ", count)
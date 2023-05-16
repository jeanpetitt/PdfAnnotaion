import csv,os
import PyPDF2
from langdetect import detect

path = f"{os.getcwd()}/jdataset" 

def annotateTable(file_csv):
    # lister les fichiers dans le dataset
	dataset = os.listdir(path)
	# trier le dataset par ordre alphabetique
	dataset.sort(reverse=False)
	print(len(dataset))
	header_table =["Table", "Nom source", "Auteur", "Date Publication", "Langage", "Pays", "Description Contenu", "Technique utilisé pour la collecte"]
	
	i=0
	with open(file_csv, "+w") as file:
		writer = csv.writer(file, delimiter=",")
		writer.writerow(header_table)
		for files in dataset:
			if files.endswith(".pdf"):
				# open a pdf file
				with open(f"{path}/{files}", "rb") as f:
					filename = files.split(".pdf")[0]
					# create and pdfreader object
					reader = PyPDF2.PdfReader(f)
					# verify if pdf has a title
					if '/Title' in reader.metadata:
						# get description
						title = reader.metadata['/Title']
						# get authors
						author = reader.metadata['/Author']
						# get language
						text = ''
						for page_num in range(len(reader.pages)):
							page = reader.pages[page_num]
							text = page.extract_text()
						
						language = detect(text)
						# get source
						# firts metho tha it is generalmethod
						source = reader.metadata['/Subject']
						# seconf method that ispersonalizemetho
						source_personalize = f"Food Production, Processing and Nutrition \nhttps://doi.org/10.1186/{filename}"
						# get publication date
						date = reader.metadata['/CreationDate']
						date_publication = date.split(":")[-1]
						dates = []
						original_date = ""
						for word in date_publication:
							dates.append(word)
							if len(dates) >= 14:
								break
						i = 0
						ds = ""
						year = ""
						month = ""
						day = ""
						hours = ""
						minute = ""
						second = ""
						for d in dates:
							i += 1
							if i == 4:
								year = dates[0] + dates[1] +dates[2] + dates[3]
							elif i == 6:
								month = dates[4] + dates[5]
							elif i == 8:
								day = dates[6] + dates[7]
							
							elif i == 10:
								hours = dates[8] + dates[9]
							elif i == 12:
								minute = dates[10] + dates[11]
							elif i == 14:
								second = dates[12] + dates[13]
							
						original_date = year +'/' + month +"/"  +day + " " + hours + ":"+minute+ ":"+ second
						writer.writerow([filename, source_personalize, author, original_date, language, "USA", title, "Automatic with colab"])

					else: 
						i += 1
						source_personalize = f"Food Production, Processing and Nutrition \nhttps://doi.org/10.1186/{filename}"
						print("*********************pas de titre", files)
						writer.writerow([filename, source_personalize, "", "", "English", "USA", "", "Automatic with colab"])
					f.close()


	print(i)

# _file = pd.read_csv("annotated_copy.csv")
# data_file=_file.loc[0:]
# print(data_file)
annotateTable("annotated.csv")

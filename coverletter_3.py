import re
import sys
import docx
from docx import Document
from docx2pdf import convert

if len(sys.argv) < 3:
    print('Not enough arguments given!')
    sys.exit()

for replaceArg in sys.argv[2:]:
    if len(replaceArg.split('=')) != 2:
        print('Faulty replace argument given')
        print('-> ', replaceArg)
        sys.exit()

file_path = sys.argv[1]

company_name = "deloitte"

if file_path.endswith('.docx'):
    doc = Document(file_path)
    occurences = {}
    for replaceArgs in sys.argv[2:]:
        replaceArg = replaceArgs.split('=')
        occurences[replaceArg[0]] = 0
        if replaceArg[0] == "COMPANY":
            company_name = replaceArg[1]
        for para in doc.paragraphs:
            for run in para.runs:
                if run.text:
                    replaced_text = re.sub(replaceArg[0], replaceArg[1], run.text, 999)
                    if replaced_text != run.text:
                        run.text = replaced_text
                        occurences[replaceArg[0]] += 1

    for word, count in occurences.items():
        print(f"The word {word} was found and replaced {count} times.")

    new_file_path = file_path.replace(".docx", "_new.docx")
    doc.save(new_file_path)
else:
    print('The file type is invalid, only .docx are supported')

convert(new_file_path, f"/Users/xinxuan/Desktop/General/Resume/Cover Letter {company_name}.pdf")

from openpyxl import load_workbook
import xml.etree.ElementTree as ET
import os
from docx import *



current_dir = os.path.dirname(__file__)
print current_dir
for s in os.listdir(current_dir):
    print s 
relative = 'Bi/CVS/10007/10007_Paul_Okweye.docx'
abs_dir = os.path.join(current_dir, relative)
docu = opendocx(abs_dir)
raw_string = (getdocumenttext(docu))
str = ''
for c in raw_string:
    str += c.encode('utf-8')
#print str
print '*'*80

article = 'article_eg.xlsx'
book = load_workbook(article)
sheet = book.worksheets[0]
for row in sheet.range('H2:H3'):
    for cell in row:
        print (cell.value)


print book.get_sheet_names()



book.save(filename = article)

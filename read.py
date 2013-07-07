from openpyxl import load_workbook
import xml.etree.ElementTree as ET
import os
from docx import *

# see http://code.activestate.com/recipes/576874-levenshtein-distance/
def levenshtein(s1, s2):
    l1 = len(s1)
    l2 = len(s2)

    matrix = [range(l1 + 1)] * (l2 + 1)
    for zz in range(l2 + 1):
      matrix[zz] = range(zz,zz + l1 + 1)
    for zz in range(0,l2):
      for sz in range(0,l1):
        if s1[sz] == s2[zz]:
          matrix[zz+1][sz+1] = min(matrix[zz+1][sz] + 1, matrix[zz][sz+1] + 1, matrix[zz][sz])
        else:
          matrix[zz+1][sz+1] = min(matrix[zz+1][sz] + 1, matrix[zz][sz+1] + 1, matrix[zz][sz] + 1)
   
   
    return matrix[l2][l1]

def clean_parse(s):
    s = s.replace(',',' ')
    s = s.replace(':',' ')
    s = s.replace('(',' ')
    s = s.replace(')',' ')
    s = s.replace(';',' ')
    s = s.replace('.',' ')
    s = s.replace('-',' ')
    return s
    
# obtin the current dirtory
current_dir = os.path.dirname(__file__)


# obtain the current directory name
# __file__ is the inner representation of this file
current_dir = os.path.dirname(os.path.abspath(__file__))
# join the path to go into the subfolder
cv_dir = os.path.join(current_dir, 'Bi/CVs/')

work_list = os.path.join(current_dir, 'wos_new.xlsx')
work_book = load_workbook(work_list)
sheet = work_book.worksheets[0]
for row in sheet.range('H2:H3'):
    for cell in row:
        ss = cell.value

tmp_name = os.walk(cv_dir)
for root, sub_dir, files_list in tmp_name:
    for file in files_list:
        if file[-4:] == 'docx':
            #print file
            file = os.path.join(root,file)
            # TODO: add exception handler and log file support
            document = opendocx(file)
            unparsed_text = getdocumenttext(document)
            parsed_text = ''
            for c in unparsed_text:
                parsed_text += c.encode("utf-8")
            parsed_text = clean_parse(parsed_text)
            #print parsed_text
            #print type(parsed_text)
            #exit(0)
            print levenshtein(str(ss), parsed_text)/float(len(parsed_text))
            
            
    


'''
#print os.path.dirname(test)
#for s in os.listdir(test):
#    print s 
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
'''
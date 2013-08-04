from openpyxl import load_workbook
from openpyxl.writer.excel import ExcelWriter
import xml.etree.ElementTree as ET
import os
from docx import *
from levenshtein import levenshtein

replace_ = [' ', '-', '_', '.', ',', '(', ')'];



def clean_parse(s):
    for char in replace_:
        if char in s:
            s = s.replace(char, '')
    return s




def main():
    # obtin the current dirtory
    #current_dir = os.path.dirname(__file__)


    # obtain the current directory name
    # __file__ is the inner representation of this file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # join the path to go into the subfolder
    cv_dir = os.path.join(current_dir, 'Bi/CVs/')

    work_path = os.path.join(current_dir, 'wos_new.xlsx')
    result_path = os.path.join(current_dir, 'new.xlsx')
    
    work_book = load_workbook(work_path)
    sheet = work_book.worksheets[0]

    result_book = load_workbook(result_path)
    result_sheet = result_book.worksheets[0]
    result_rows = result_sheet.rows
    count = 1
    
    tmp_name = os.walk(cv_dir)
    for root, sub_dir, files_list in tmp_name:
        for file in files_list:
            if file[-4:] == 'docx':
                
                file = os.path.join(root,file)

                # the root is in format of /blah/blah/CVs/10007
                # and cv_id will be '10007'
                cv_id =  root.rsplit("/",1)[1]
                added_cv_id = str(int(cv_id) + 20000)

                # TODO: add exception handler and log file support
                document = opendocx(file)
                unparsed_text = getdocumenttext(document)
                parsed_text = ''
                for c in unparsed_text:
                    parsed_text += c.encode("utf-8")
                    
                parsed_cv_text = clean_parse(parsed_text)
                
                        
                #string_len = len(string_text)
                cv_len = len(parsed_cv_text)
                #print "string length %d" % string_len
                #print "cv length %d" % cv_len
                author_row = sheet.rows
                
                #print len(author_row)
                for i in range(len(author_row)):
                    wos_id = str(author_row[i][6].value)
                    if wos_id == added_cv_id:
                        wos_string = str(author_row[i][7].value)
                        ld = levenshtein(parsed_cv_text, wos_string)
                        print "author %s, cv %s" % (str(author_row[i][6].value), cv_id)
                        print ld
                        
                        result_sheet.cell(row = count, column = 0).value = cv_id
                        result_sheet.cell(row = count, column = 1).value = wos_id
                        result_sheet.cell(row = count, column = 2).value = 'cv-title'
                        wos_len = len(wos_string)
                        prob = (ld-(cv_len-wos_len))/float(wos_len)
                        result_sheet.cell(row = count, column = 3).value = prob
                        result_sheet.cell(row = count, column = 4).value = parsed_cv_text
                        result_sheet.cell(row = count, column = 5).value = wos_string
                        count += 1
                        
                        updated_result = ExcelWriter(workbook = result_book)
                        updated_result.save(filename = 'new.xlsx')
                        #exit(0)

    #result_book.save()
    #work_book.save()
                        
                        
'''
                for row in sheet.range('H2:H100'):
                    for cell in row:
                        string_text = str(cell.value)
                        
                        #if cv_id 
                
                        ld = levenshtein(parsed_cv_text, string_text)
                        print "ld length %d" % ld
                        print (ld-(cv_len-string_len))/float(string_len)
                        exit(0)
'''


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit(0)



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
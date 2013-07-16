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

def fuzzy_substring(needle, haystack):
    """
    Calculates the fuzzy match of needle in haystack,
    using a modified version of the Levenshtein distance
    algorithm.
    The function is modified from the levenshtein function
    in the bktree module by Adam Hupp
    http://ginstrom.com/scribbles/2007/12/01/fuzzy-substring-matching
    -with-levenshtein-distance-in-python/
    """
    m, n = len(needle), len(haystack)

    # base cases
    if m == 1:
        return not needle in haystack
        if not n:
            return m

    row1 = [0] * (n+1)
    for i in range(0,m):
        row2 = [i+1]
        for j in range(0,n):
            cost = ( needle[i] != haystack[j] )

            row2.append( min(row1[j+1]+1, # deletion
                             row2[j]+1, #insertion
                             row1[j]+cost) #substitution
            )
        row1 = row2
        return min(row1)

def clean_parse(s):
    s = s.replace(',',' ')
    s = s.replace(':',' ')
    s = s.replace('(',' ')
    s = s.replace(')',' ')
    s = s.replace(';',' ')
    s = s.replace('.',' ')
    s = s.replace('-',' ')
    return s




def main():
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
    
    tmp_name = os.walk(cv_dir)
    for root, sub_dir, files_list in tmp_name:
        for file in files_list:
            if file[-4:] == 'docx':
                
                file = os.path.join(root,file)

                # the root is in format of /blah/blah/CVs/10007
                # and cv_id will be '10007'
                cv_id =  root.rsplit("/",1)[1]
                cv_id = str(int(cv_id) + 20000)

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
                    #print str(author_row[i][6].value)
                    if str(author_row[i][6].value) == cv_id:
                        print "author %s, cv %s" % (str(author_row[i][6].value), cv_id)
                    
                #print (author_row[7883])[7].value
                    #for author_cell in author_row:
                     #   author_id = str(author.cell)
                        
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
    main()



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
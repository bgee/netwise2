import time
import xml.etree.ElementTree as ET
import MySQLdb
import sys

class AddressClass: # i've to store Authors & Addresses before calling SQL because i've to build links between them.
    def __init__(self):
        self.full_address=''
        self.org=''
        self.sub_org=''
        self.city=''
        self.state=''
        self.country=''
        self.address_id = None

    def fillfromXML(self, element):
        self.full_address=get_tag_text(element.find("./rs_address"))
        self.org=get_tag_text(element.find("./rs_organization"))
        self.sub_org=get_subtag_text(element.find("./rs_suborganizations"),"./rs_suborganization","; ")
        self.city=get_tag_text(element.find("./rs_city"))
        self.state=get_tag_text(element.find("./rs_state"))
        self.country=get_tag_text(element.find("./rs_country"))

    def sqlQ(self):
        return 'INSERT INTO address (full_address, org, sub_org, city, state, country) VALUES ("{0}", "{1}", "{2}", "{3}", "{4}", "{5}");'.format( \
            self.full_address, self.org, self.sub_org, self.city, self.state, self.country)

class AuthorClass: # both functions: init() & fillfromXML() needed to fill up the structure!
    def __init__(self, wos_index, wos_key):
        self.wos_key=wos_key
        self.wos_index=wos_index
        self.lastname=''
        self.firstname=''
        self.fullname=''
        self.AUaddress=[]

    def fillfromXML(self, element):
        self.lastname=get_tag_text(element.find("./AuLastName"))
        self.firstname=get_tag_text(element.find("./AuFirstName"))
        self.fullname=get_tag_text(element.find("./AuCollectiveName"))
        for authrecaddr in element.findall("./address"):
            self.AUaddress.append((int_empty_to_zero(get_tag_attr(authrecaddr,"number"))-1,get_tag_text(authrecaddr)))
 
    def sqlQ(self):
        return 'INSERT INTO AUTHOR (wos_key, wos_index, lastname, firstname, fullname) VALUES ("{0}", "{1}", "{2}", "{3}", "{4}");'.format( \
            self.wos_key, self.wos_index, self.lastname, self.firstname, self.fullname)

# these functions get text from ET elements & do some basic cleaning of symbols that screw up SQL: \ " * and empty integers
def clean_string(strg): return '' if strg is None else strg.replace('\\','\\\\').replace('"','\\"').strip()
def int_empty_to_zero(strg): return 0 if strg=='' else int(strg)
def get_tag_text(element): return '' if element is None else clean_string(element.text)
def get_tag_attr(element, attr): return '' if element is None else clean_string(element.get(attr))
def get_subtag_text(element, subtag, divisor):
    if element is None: return ''
    subtagText=[]
    for subelement in element.findall(subtag):
        subtagText.append(get_tag_text(subelement))
        subtagText.append(divisor)
    if subtagText: subtagText.pop()
    return ''.join(subtagText)


def insert_article(db, REC):

    print "=========================== START RECORD ==========================="
#    ET.dump(REC)

    AllAddresses=[]
    for addrrec in REC.findall("./item/research_addrs/research"):
        curraddr=AddressClass()
        curraddr.fillfromXML(addrrec)
        sqlQ_address=curraddr.sqlQ()
        print "SQL ADDRESS:", sqlQ_address
#        try: c.execute(sqlQ_address)
#        except: return False, sqlQ_address
#        curraddr.address_id=c.lastrowid # this will be used for relations with ARTICLEs & AUTHORs
        curraddr.address_id=6666
        ARTICLE_article_id=9999
        AllAddresses.append(curraddr)

        sqlQ_article2address='INSERT INTO article2address (article_id, address_id) VALUES ({0}, {1});'.format(ARTICLE_article_id, curraddr.address_id)
        print "SQL ARTICLE 2 ADDRESS:", sqlQ_article2address
#        try: c.execute(sqlQ_article2address)
#        except: return False, sqlQ_article2address

#    for getaddr in AllAddresses:
#        print getaddr.full_address, "||", getaddr.org, "||",  getaddr.sub_org, "||",  getaddr.city, "||",  getaddr.state, "||",  getaddr.country        
#    print AllAddresses[0].full_address, "||", AllAddresses[0].org, "||",  AllAddresses[0].sub_org, "||",  AllAddresses[0].city, "||",  AllAddresses[0].state, "||",  AllAddresses[0].country

    AllAuthors=[]
    AllAuthors.append(AuthorClass(get_tag_text(REC.find("./item/authors/primaryauthor")),''))
    for authrec in REC.findall("./item/authors/author"):
        AllAuthors.append(AuthorClass(get_tag_text(authrec), get_tag_attr(authrec,"key")))
        
    authcnt=0
    for authrec in REC.findall("./item/authors/fullauthorname"):
        AllAuthors[authcnt].fillfromXML(authrec)
        authcnt+=1

    for getauth in AllAuthors:
        sqlQ_author=getauth.sqlQ()
        print "SQL AUTHOR:", sqlQ_author
#        try: c.execute(sqlQ_author)
#        except: return False, sqlQ_author
#        getauth.author_id=c.lastrowid # this will be used for relations with ARTICLEs & ADDRESSes
        getauth.author_id=5555

        sqlQ_article2author='INSERT INTO article2author (article_id, author_id) VALUES ({0}, {1});'.format(ARTICLE_article_id, getauth.author_id)
        print "SQL ARTICLE 2 AUTHOR:", sqlQ_article2author
#        try: c.execute(sqlQ_article2author)
#        except: return False, sqlQ_article2author

        for arec, afull in getauth.AUaddress:
            if AllAddresses[arec].full_address != afull: return False, 'ADDRESS/AUTHOR MISMATCH. AUTHOR ADDRESS: "{0}", ADDRESS ADDRESS: "{1}"'.format(AllAddresses[arec].full_address, afull)
            sqlQ_author2address= 'INSERT INTO author2address (address_id, author_id) VALUES ({0}, {1});'.format(AllAddresses[arec].address_id, getauth.author_id)
            print "SQL AUTHOR 2 ADDRESS:", sqlQ_author2address
#            try: c.execute(sqlQ_author2address)
#            except: return False, sqlQ_author2address

#        print getauth.index, "||", getauth.key, "||", getauth.last, "||",getauth.first, "||", getauth.fullname, "||",getauth.AUaddress

#    ET.dump(REC.find("./item/keywords"))
#    ARTICLE_keywords=get_subtag_text(REC.find("./item/keywords"),"keyword","; ")
#    print "KW", ARTICLE_keywords
#    ET.dump(REC.find("./item/keywords_plus"))
#    ARTICLE_keywordsplus=get_subtag_text(REC.find("./item/keywords_plus"),"keyword","; ")
#    print "KWP", ARTICLE_keywordsplus
    return True, ''

#commit only if the whole record is inserted successfully. Otherwise save the XML record to a file & go to the next record.
    c=db.cursor()

# start fetching from the XML record the values of the fields.
    JOURNAL_title=get_tag_text(REC.find("./item/source_title"))
    JOURNAL_abbrev=get_tag_text(REC.find("./item/source_abbrev"))
#construct the SQL statement from the fetched values
    sqlQ_journal='INSERT INTO journal (title, abbrev) VALUES ("{0}", "{1}");'.format(JOURNAL_title, JOURNAL_abbrev)

#    print "SQL JOURNAL:", sqlQ_journal
#    JOURNAL_journal_id=9999
    try: c.execute(sqlQ_journal)
    except: return False, sqlQ_journal
    JOURNAL_journal_id=c.lastrowid # this will be used in ARTICLE
#    JOURNAL_journal_id=nw2db.insert_id() 
   
    ARTICLE_recid = get_tag_attr(REC,"recid")
    ARTICLE_ut=get_tag_text(REC.find("./item/ut"))
    ARTICLE_journal_id=JOURNAL_journal_id
    ARTICLE_title=get_tag_text(REC.find("./item/item_title"))
    ARTICLE_times_cited = int_empty_to_zero(get_tag_attr(REC,"timescited"))
    ARTICLE_year= int_empty_to_zero(get_tag_attr(REC.find("./item/bib_issue"),"year"))
    ARTICLE_doctype=get_tag_text(REC.find("./item/doctype"))
    ARTICLE_primary_author=get_tag_text(REC.find("./item/authors/primaryauthor"))
    ARTICLE_keywords=get_subtag_text(REC.find("./item/keywords"),"./keyword","; ")
    ARTICLE_keywordsplus=get_subtag_text(REC.find("./item/keywords_plus"),"./keyword","; ")
    ARTICLE_abstract=get_subtag_text(REC.find("./item/abstract"),"./p"," ")
    sqlQ_article='INSERT INTO article (recid, ut, journal_id, title, times_cited, year, doctype, primary_author, keywords, keywordsplus, abstract) \
        VALUES ("{0}", "{1}", {2}, "{3}", {4}, {5}, "{6}", "{7}", "{8}", "{9}", "{10}");'.format(ARTICLE_recid, ARTICLE_ut, ARTICLE_journal_id, \
            ARTICLE_title, ARTICLE_times_cited, ARTICLE_year, ARTICLE_doctype, ARTICLE_primary_author, ARTICLE_keywords, ARTICLE_keywordsplus, ARTICLE_abstract)

#    print "SQL ARTICLE:", sqlQ_article
#    ARTICLE_article_id=8888
    try: c.execute(sqlQ_article)
    except: return False, sqlQ_article
    ARTICLE_article_id=c.lastrowid # this will be used for relations with ADDRESSes, CITEs, AUTHORs

#    CITE_cite_id=7777
    for citerec in REC.findall("./cite"):
        CITE_rec_id=get_tag_text(citerec.find("./RECID"))
        CITE_journal=get_tag_text(citerec.find("./J2"))
        CITE_year=int_empty_to_zero(get_tag_text(citerec.find("./PY")))
        CITE_author=get_tag_text(citerec.find("./AU"))
        sqlQ_cite='INSERT INTO cite (rec_id, isWos, journal, year, author) VALUES ("{0}", {1}, "{2}", {3}, "{4}");'.format( \
            CITE_rec_id, 0, CITE_journal, CITE_year, CITE_author)
#        print "SQL CITE:", sqlQ_cite
#        CITE_cite_id+=1
        try: c.execute(sqlQ_cite)
        except: return False, sqlQ_cite
        CITE_cite_id=c.lastrowid # this will be used for relations with ARTICLEs

        sqlQ_article2cite='INSERT INTO article2cite (article_id, cite_id) VALUES ({0}, {1});'.format(ARTICLE_article_id, CITE_cite_id)
#        print "SQL CITE 2 ARTICLE:", sqlQ_article2cite
        try: c.execute(sqlQ_article2cite)
        except: return False, sqlQ_article2cite



    db.commit()
    return True, ''


def main():
    tt=time.time()

#    tr=int(sys.argv[1]) # script receives tr value as parameter, and uses it to open the designated import data file. 
#    print'STARTING IMPORT: {0}'.format(tr)
    tr=5

#    nw2db=MySQLdb.connect(host='localhost', named_pipe=1, user='nw2admin', passwd='netwise2root', db='dbkbe')
#    nw2db=MySQLdb.connect(host='130.207.70.141', port=3306, user='nw2admin', passwd='netwise2root', db='dbkbe')
#    nw2db=MySQLdb.connect(host='127.0.0.1', port=3306, user='nw2admin', passwd='netwise2root', db='dbkbe')
    nw2db=0 # to test the parsing only w/o DB operations

    currentRec=1
    record = []    # http://www.skymind.com/~ocrow/python_string/  method 4. faster string concatenation

    with open('C:\\TR_DATA\\TR source data\\TR_{0}00k.xml'.format(tr),'r') as f:        
#    with open('C:\\TR_DATA\\TR source data\\bad_sql_recs_{0}00k_IN.xml'.format(tr),'r') as f:        

        for line in f:
            record.append(line)
            if not '</REC>' in line: continue

            try: REC = ET.XML(''.join(record)) # try the XML parser. if fails, go to the next record.
            except:
                print 'IMPORT: {0}  || BAD XML RECORD: {1} '.format(tr, currentRec)
            else:
                sqlsuccess, sqlstr = insert_article(nw2db, REC) # try the SQL inserts, if fails, save the XML record
                if not sqlsuccess:
                    nw2db.rollback()
                    with open('C:\\TR_DATA\\TR source data\\bad_sql_recs_{0}00k.xml'.format(tr),'a') as bad: bad.write(''.join(record))
                    print 'IMPORT: {0}  || BAD SQL: {1} '.format(tr, currentRec)
                    print sqlstr
                
            record = []
            currentRec+=1
            if currentRec>8: break # stop after the first 1000 records            

#    nw2db.close()
    print time.time() - tt
    raw_input('IMPORT {0} FINISHED ---->'.format(tr)) # wait for the keystroke

if __name__ == "__main__":
    main()

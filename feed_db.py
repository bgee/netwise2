import time
import xml.etree.ElementTree as ET
import MySQLdb

def get_tag_text(element): return '' if element is None else element.text.replace('\\','\\\\').replace('"','\\"')
def get_tag_attr(element,attr): return '' if element is None else element.get(attr).replace('\\','\\\\').replace('"','\\"')


def insert_article(db, xml):
    ARTICLE_recid = get_tag_attr(xml,"recid")
    ARTICLE_ut=get_tag_text(xml.find("./item/ut"))
    ARTICLE_journal_id=0
    ARTICLE_title=get_tag_text(xml.find("./item/item_title"))
    ARTICLE_times_cited = get_tag_attr(xml,"timescited")
    ARTICLE_year=get_tag_attr(xml.find("./item/bib_issue"),"year")
    ARTICLE_doctype=get_tag_text(xml.find("./item/doctype"))
    ARTICLE_primary_author=get_tag_text(xml.find("./item/authors/primaryauthor"))
    ARTICLE_abstract=get_tag_text(xml.find("./item/abstract/p"))
    
    sqlQ='INSERT INTO article (recid, ut, journal_id, title, times_cited, year, doctype, primary_author, abstract)  VALUES ("{0}", "{1}", {2}, "{3}", {4}, {5}, "{6}", "{7}", "{8}");'.format(ARTICLE_recid, ARTICLE_ut, ARTICLE_journal_id, ARTICLE_title, ARTICLE_times_cited, ARTICLE_year, ARTICLE_doctype, ARTICLE_primary_author, ARTICLE_abstract)                                                                                                
    
    c = db.cursor()
    try:
        c.execute(sqlQ)
    except:
        db.rollback()
        print "BAD SQL:", currentRec
        print sqlQ
        with open('C:\\TR_DATA\\TR source data\\bad_sql_recs_'+str(tr)+'00k.xml','a') as bad: bad.write(''.join(record))
    else:
        ARTICLE_article_id=db.insert_id()
        db.commit()

def main():
    tt=time.time()

    tr=5
    currentRec=1    
    record = []    # http://www.skymind.com/~ocrow/python_string/  method 4

    nw2db=MySQLdb.connect(host='localhost', named_pipe=1, user='nw2admin', passwd='netwise2root', db='dbkbe')
    #nw2db=MySQLdb.connect(host='127.0.0.1', port=3306, user='nw2admin', passwd='netwise2root', db='dbkbe')
                          
    with open('C:\TR_DATA\TR source data\TR_'+str(tr)+'00k.xml','r') as f:        
        
        for line in f:
            record.append(line)
            if not '</REC>' in line:
                continue

            try:
                REC = ET.XML(''.join(record))
            except:
                print "BAD RECORD: ", currentRec
                record = []
                currentRec+=1
                continue
            insert_article(nw2db, REC)
            record = []
            currentRec+=1

    nw2db.close()
    print time.time() - tt
    raw_input('---->')

if __name__ == "__main__":
    main()

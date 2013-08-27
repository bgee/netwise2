import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
def process_record(record):
    #print record
    #exit(0)
    #root = ET.fromstring(record)
    #print root.i_ckey
    '''for child in root:
        for grandchild in child:
            print grandchild.tag, grandchild.attrib'''
    root = BeautifulSoup(record)
    print root.i_ckey.string
    exit(0)

def main():
    with open('tree.xml') as f:
        
        next(f)
        record = ''
        for line in f:
            if '</REC>' in line:
                process_record(record+line)
                record = ''
            else:
                record = record+line



if __name__ == "__main__":
    main()
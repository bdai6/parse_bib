#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Receives a Bibtex file and produces the markdown files for academic-hugo theme

@author: Petros Aristidou
@contact: p.aristidou@ieee.org
@date: 19-10-2017
@version: alpha
"""

import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
import os, sys, getopt, re

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# remove all decorative expression in a string
def supetrim(string):
    return string.replace("\\" , "").replace("{" , "").replace("}" , "").replace("\n"," ")


def month_string_to_number(string):
    m = {
        'jan':1,
        'feb':2,
        'mar':3,
        'apr':4,
        'may':5,
        'jun':6,
        'jul':7,
        'aug':8,
        'sep':9,
        'oct':10,
        'nov':11,
        'dec':12
        }
    s = string.strip()[:3].lower()

    try:
        out = m[s]
        return out
    except:
        raise ValueError('Not a month')
        
        
# remove empty elements from a string
def removeEmptyString(inStr):
    while("" in inStr):
        inStr.remove("") 
        

# convert bib entry ID to firstAuthor-year-journal-otherInfo format
def formatID(inStr):
    # if the format is already correct in bibtex
    if '-' in inStr:
        return inStr
    #for example, str1 = 'meza2012:report:nvm
    elif ':' in inStr:
        return inStr.replace(':', "-")
    else:
        # e.g., 'li2018iscaCnnDnn'
        # before the year
        a = re.split('[^a-zA-Z]', inStr)
        # year
        b = re.split('[a-zA-Z]', inStr)
        removeEmptyString(a)
        removeEmptyString(b)
        # journal name
        c = re.split('[A-Z][a-zA-Z]*', a[1])
        removeEmptyString(c)
        # other info
        d = re.findall('[A-Z][a-zA-Z]*', a[1])
        outStr = '-'.join([a[0]] + b + c + d)
        return outStr.lower()


def main(argv):
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:", ["ifile="])
    except getopt.GetoptError:
        print('parse_bib.py -i <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('parse_bib.py -i <inputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
    return inputfile


if __name__ == "__main__":
    inputfile = main(sys.argv[1:])

    try:
        with open(inputfile, encoding="utf8") as bibtex_file:
            bibtex_str = bibtex_file.read()
    except EnvironmentError:  # parent of IOError, OSError *and* WindowsError where available
        print('File '+inputfile+' not found or some other error...')

    # It takes the type of the bibtex entry and maps to a corresponding category of the academic theme
    # Publication type.
    # Legend:
    # 0 = Uncategorized
    # 1 = Conference paper
    # 2 = Journal article
    # 3 = Preprint / Working Paper
    # 4 = Report
    # 5 = Book
    # 6 = Book section
    # 7 = Thesis
    # 8 = Patent
    pubtype_dict = {
        'Uncategorized': '"0"',
        'misc': '"0"',
        'inproceedings': '"1"',
        'conference': '"1"',
        'article': '"2"',
        'submitted': '"3"',
        'preprint': '"3"',
        'techreport': '"4"',
        'book': '"5"',
        'incollection': '"6"',
        'phdthesis': '"7"',
        'mastersthesis': '"7"',
        'patent': '"8"',
    }
    
    bib_database = bibtexparser.loads(bibtex_str)
    for entry in bib_database.entries:
        dirName = formatID(entry['ID'])
#        filedir = 'content/en/publication/'+entry['ID'] 
        filedir = 'publication/' + dirName
        if not os.path.exists(filedir):
            os.mkdir(filedir)
#        filenm = 'content/en/publication/'+entry['ID']+'/index.md'
        filenm = 'publication/'+ dirName + '/index.md'
        
        # If the same publication exists, then skip the creation. I customize the .md files later, so I don't want them overwritten. Only new publications are created.
        #if os.path.isfile(filenm):
        #    print("publication " + dirName + " already exists. Skipping...")
        #    pass
        #else:
        with open(filenm, 'w', encoding='utf8') as the_file:
            the_file.write('---\n')
            
            # Treating the title of the publication
            the_file.write('title: "'+supetrim(entry['title'])+'"\n')
            print('Parsing ' + dirName)

            # Treating the authors
            if 'author' in entry:
                authors = entry['author'].split(' and ')
                the_file.write('authors: [')
                authors_str = ''
                for author in authors:
                    author_strip = supetrim(author)
                    author_split = author_strip.split(',')
                    # two naming conventions in bibtex: "LastName, FirstName" or "FirstName LastName"
                    ## 1st case: "LastName, FirstName"
                    if len(author_split)==2:
                        author_strip = author_split[1].strip() + ' ' +author_split[0].strip()
                    # comment out as we just need to print the full name
                    #author_split = author_strip.split(' ')
                    #author_strip = author_split[0][0]+'. '+' '.join(map(str, author_split[1:]))
                    authors_str = authors_str+ '"'+author_strip+'",'
                the_file.write(authors_str[:-1]+']\n')
            
            # Date
            ## just use the date if it's already there and is in yyyy-mm-dd format
            if 'date' in entry:
                if len(entry['date']) == 10:
                    the_file.write('date: ' + entry['date'] + '\n')
                else:
                    the_file.write('date: ' + entry['date'] + '-01\n')
            elif 'year' in entry:
                date = entry['year']
                if 'month' in entry:
                    if RepresentsInt(entry['month']):
                        month = entry['month']
                    else:
                        month = str(month_string_to_number(entry['month']))
                    date = date+'-'+ month.zfill(2)
                else:
                    date = date+'-01'
                the_file.write('date: '+date+'-01\n')

            # DOI
            if 'doi' in entry:
                the_file.write('doi: "'+supetrim(entry['doi'])+'"\n')
                        
            # Treating the publication type
            if 'ENTRYTYPE' in entry:
                if 'booktitle' in entry and ('Seminar' in supetrim(entry['booktitle'])):
                    the_file.write('publication_types: ['+pubtype_dict['conference']+']\n')
                elif 'booktitle' in entry and ('Workshop' in supetrim(entry['booktitle'])):
                    the_file.write('publication_types: ['+pubtype_dict['conference']+']\n')
                elif 'note' in entry and ('review' in supetrim(entry['note'])):
                    the_file.write('publication_types: ['+pubtype_dict['submitted']+']\n')
                elif 'note' in entry and ('Conditional' in supetrim(entry['note'])):
                    the_file.write('publication_types: ['+pubtype_dict['submitted']+']\n')
                else:
                    the_file.write('publication_types: ['+pubtype_dict[entry['ENTRYTYPE']]+']\n')
            
            # Treating the publication journal, conference, etc.
            if 'booktitle' in entry:
                the_file.write('publication: "_'+supetrim(entry['booktitle'])+'_"\n')
                ## including short name for conference proceedings
                if 'series' in entry:
                    the_file.write('publication: "_' + supetrim(entry['booktitle']) + ', ser. ' + supetrim(entry['series']) + '_"\n')
                    print('publication: "_' + supetrim(entry['booktitle']) + ', ser. ' + supetrim(entry['series']) + '_"\n')
            elif 'journal' in entry:
                the_file.write('publication: "_'+supetrim(entry['journal'])+'_"\n')
            elif 'school' in entry:
                the_file.write('publication: "_'+supetrim(entry['school'])+'_"\n')
            elif 'institution' in entry:
                the_file.write('publication: "_'+supetrim(entry['institution'])+'_"\n')
                
            ## for articles, it should display title, _journal_, **volumne**, (number), page_start-page_end
            
            ## for proceedings, it should display title, _booktitle_, ser.series, location, month, year.
                
            # I never put the short version. In the future I will use a dictionary like the authors to set the acronyms of important conferences and journals
            the_file.write('publication_short: ""\n')
            
            # Add the abstract if it's available in the bibtex
            if 'abstract' in entry:
                the_file.write('abstract: "'+supetrim(entry['abstract'])+'"\n')
            
            # Some features are disabled. I activate them later
            the_file.write('summary: ""\n')
            
            # Treating the keywords/tags
            if 'keywords' in entry:
                # keywords are separated by ',' instead of ';'
                the_keywords = entry['keywords'].split(',')
                the_file.write('tags: [')
                keyword_str = ''
                for keyword in the_keywords:
                    keyword_strip = supetrim(keyword)
                    keyword_str = keyword_str+ '"'+keyword_strip.lower()+'",'
                the_file.write(keyword_str[:-1]+']\n')
            else:
                the_file.write('tags: []\n')

            the_file.write('categories: []\n')
            
            if 'featured' in entry:
                the_file.write('featured: true\n\n')
            else:
                the_file.write('featured: false\n\n')

            # I add urls to the pdf and the DOI
            # disabled for now
            #the_file.write('url_pdf: "/publication/'+entry['ID']+'/manuscript.pdf"\n')
            the_file.write('url_pdf:\n')
            the_file.write('url_code:\nurl_dataset:\nurl_poster:\nurl_project:\nurl_slides:\nurl_source:\nurl_video:\n\n')
            
            # Default parameters that can be later customized
            the_file.write('image:\n')
            the_file.write('  caption: ""\n')
            the_file.write('  focal_point: ""\n')
            the_file.write('  preview_only: false\n\n')

            the_file.write('projects: []\n\n')
            the_file.write('slides: ""\n')
            
            # I keep in my bibtex file a parameter called award for publications that received an award (e.g., best paper, etc.)
            if 'award' in entry:
                the_file.write('award: "true"\n')
            
            # I put the individual .bib entry to a file with the same name as the .md to create the CITE option
            db = BibDatabase()
            db.entries =[entry]
            writer = BibTexWriter()
            with open('publication/' + dirName + '/cite.bib', 'w', encoding='utf8') as bibfile:
                bibfile.write(writer.write(db))

            the_file.write('---\n\n')
            
            # Any notes are copied to the main document
            if 'note' in entry:
                strTemp = supetrim(entry['note'])
                the_file.write(strTemp + "\n")

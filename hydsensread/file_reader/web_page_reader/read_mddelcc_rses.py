# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 14:29:29 2017
@author: jnsebgosselin
"""

# Standard library imports :

import re
import urllib
import urllib.parse as urlparse
from urllib.request import urlopen

from bs4 import BeautifulSoup, CData


# =============================================================================
# Utility functions

def getFile_from_url(url, name):
    # These operations  are required if non_ASCII char are presents in the url
    url = urllib.parse.urlsplit(url)
    url = list(url)
    url[2] = urllib.parse.quote(url[2])
    url = urllib.parse.urlunsplit(url)


def findUnique(pattern, string):
    result = re.findall(pattern, string)
    if len(result) > 0:
        return result[0].strip()
    else:
        return None

# =============================================================================
# fonctions to grab the database from the MDDELCC website


def getUrl_xml():  # Get the name of the last xml data table.
    mpjs = 'http://www.mddelcc.gouv.qc.ca/eau/piezo/carte_google/markers-piezo.js'

    f = urlopen(mpjs)
    reader = f.read().decode('utf-8', 'replace')

    txt = "MYMAP.placePuits('"
    n = len("MYMAP.placePuits('")
    indx0 = reader.find(txt) + n
    indx1 = reader.find("');", indx0)

    url = 'http://www.mddelcc.gouv.qc.ca/eau/piezo/%s' % reader[indx0:indx1]

    return url


def read_xml_datatable(url):
    # Read the xml datafile and return a database with the well info
    xml = urlopen(url)
    soup = BeautifulSoup(xml, 'html.parser')
    places = soup.find_all('placemark')

    db = {}
    for place in places:
        print('-'*78)
        desc = place.find('description')
        name = place.find('name').text
        for cd in desc.findAll(text=True):
            if isinstance(cd, CData):

                pid = findUnique('Piézomètre =(.*?)<br/>', cd)
                db[pid] = {}
                db[pid]['ID'] = pid
                db[pid]['Name'] = name
                db[pid]['Longitude'] = findUnique('Longitude =(.*?)<br/>', cd)
                db[pid]['Latitude'] = findUnique('Latitude =(.*?)<br/>', cd)
                db[pid]['Nappe'] = findUnique('Nappe =(.*?)<br/>', cd)
                db[pid]['Influenced'] = findUnique('Influencé =(.*?)<br/>', cd)
                db[pid]['Last'] = findUnique(
                        'Dernière lecture =(.*?)<br/>', cd)

                s = '<br/><a href="(.*?)">Données'
                db['url data'] = findUnique(s, cd)
                s = 'Données</a><br/><a href="(.*?)">Schéma'
                db['url drilllog'] = findUnique(s, cd)
                s = 'Schéma</a><br/><a href="(.*?)">Graphique'
                db['url graph'] = findUnique(s, cd)

                print(name, pid, db[pid]['Latitude'], db[pid]['Longitude'],
                      db[pid]['Nappe'], db[pid]['Influenced'])
                print(db['url data'])
                print(db['url drilllog'])
                print(db['url graph'])

    return db


if __name__ == "__main__":
    import pprint
    url_xml = getUrl_xml()
    print(url_xml)
    db = read_xml_datatable(url_xml)
    pprint.pprint(db)


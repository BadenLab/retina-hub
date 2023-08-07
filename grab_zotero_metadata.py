"""
Small script to load necessary libraries and match google scholar entries to Web of Science entries using WOS api
"""
import requests
import pandas as pd
from pyzotero import zotero
import io
import os
#import json
#import time





sheet_url = "https://docs.google.com/spreadsheets/d/15jE_Hc_otR_OvAkRy_aseGhCaO7c29M8DKyNuso6dyU/export#gid=693684877"
garticles = pd.read_excel(sheet_url,header=0)



# Step 2: Connect to Zotero

with open("zotero_api","r") as fid:
    api_key = fid.readline()

library_id = "4584648"
library_type = "group"
#api_key = "your_zotero_api_key"
zot = zotero.Zotero(library_id, library_type, api_key)
zotero_group_items = zot.top(limit=500) # adjust limit as per your needs

# Extract DOIs from the zotero group
zotero_dois = [item['data'].get('DOI', None) for item in zotero_group_items]

g_doi_column = 'Identifier (DOI, ISBN, PMID, arXiv ID). If unknown, please query CrossRef: https://www.crossref.org/guestquery'
# Step 3: Find the DOIs in the Google Sheet not in the Zotero group
google_sheet_dois = garticles[g_doi_column].tolist()

dois_to_add = list(set(google_sheet_dois) - set(zotero_dois))

items_to_add = garticles.loc[garticles[g_doi_column].isin(dois_to_add)]

# Step 4: Add these papers to Zotero subgroups

collections = {
  "animals":{
    "amphibian":"I5YWZIRR",
    "bird":"ZRC54PQF",
    "cell culture":"KMUTY94V",
    "organoid":"BHNIC5FW",
    "fish: any other":"V46CQ3NS",
    "fish: zebrafish":"22IG9MCX",
    "fish: other teleost":"BB7H8KCR",
    "mammals: mouse":"JWRUTIIE",
    "mammals: non-placental":"Z4IN47WJ",
    "mammals: other placental":"MMU8BX4C",
    "mammals: other rodent":"8A9R3YVS",
    "mammals: human" : "5NKZQ2X4",
    "mammals: non-human primate":"HJ7UFULD",
    "other":"WDSXVYN6",
    "reptile":"W4T7HAGP",
  },

  "pub":{
    "book chapter":"IL925QCT",
    "dispatch or similar":"PQQDDZX4",
    "methods article (peer reviewed)":"2JQYH89M",
    "other":"4QEYI2KS",
    "preprint":"UAYZHHPY",
    "research article (peer reviewed)":"N3H5YAW3",
    "resource/database":"EJ2U2JHB",
    "review (peer reviewed)":"UF9V5CB6",
  },
  "area":{
    "computation":"QVN2AP8C",
    "development":"7CALX6AJ",
    "function":"ICYG3YV6",
    "injury/disease/regeneration":"NI8DPUXS",
    "molecular":"B9M3K8VL",
    "other":"ZWVM2ZIS",
    "structure":"R5ZD6ZLM",
    "tool development: biological":"WVKZJ7M5",
    "tool development: hardware":"IFSBYJPB",
    "tool development: software":"48T6FHZ2",

  },
  "cell":{
    "amacrine":"2ECXQ9WE",
    "bipolar":"78A6KXVR",
    "cortex and related":"BLSPC9W3",
    "glia":"B9QIZAVV",
    "horizontal":"M6CLZYGV",
    "other":"UZD6C2J9",
    "photoreceptors":"66QHAKSP",
    "retinal ganglion":"8QY5WMJH",
    "superior colliculus/tectum":"J7U6BRBG",
    "thalamus and related":"A8XHEV8F",
   }
  }

#dois = articles.iloc[:,3]





##to run zotero translator, one needs to have docker installed and run it so (if one is using command line):
#docker pull zotero/translation-server
#docker run -d -p 1969:1969 --rm --name translation-server zotero/translation-server

#KPVJRAE9:14:Animal model;I2DXCS7M:11:Publication type;NC2HRG88:12:Main Areas;BXSDS9PK:13:Cell types

url = "http://127.0.0.1:1969/search"  # zotero translator server running locally
#url = "https://zotero.retina-hub.org:1969/search"
headers = {"content-type": "text/plain", "Accept-Charset": "UTF-8"}
# r = requests.post(url=url, data=dois[0], headers=headers)


# now add entries to the zotero collection, add the type of OA to tags





for idx in items_to_add.index:
    if str(items_to_add.loc[idx][g_doi_column])!="nan":
        print(idx)
        r = requests.post(url=url, data=items_to_add.loc[idx][g_doi_column], headers=headers)
        temp = r.json()
         
        r.close()
        
        #temp[0]["tags"].append(articles["oa_status"][idx])
        
        result = zot.create_items(temp)
        print(result)
        entry_key = result["successful"]["0"]["key"]

        #animal species
        species = items_to_add.loc[idx]["Species / tissue"]
        species = species.split(",")
        for animal in species:
            animal = animal.lower().strip()
                
        
            if animal=="amphibian":
                zot.addto_collection(collections["animals"]["amphibian"],zot.item(entry_key))    
            if animal=="bird":
                zot.addto_collection(collections["animals"]["bird"],zot.item(entry_key))    
            if animal=="cell culture":
                zot.addto_collection(collections["animals"]["cell culture"],zot.item(entry_key))    
            if animal=="organoid":
                zot.addto_collection(collections["animals"]["organoid"],zot.item(entry_key))    
            if animal=="fish: any other":
                zot.addto_collection(collections["animals"]["fish: any other"],zot.item(entry_key))    
            if animal=="fish: zebrafish":
                zot.addto_collection(collections["animals"]["fish: zebrafish"],zot.item(entry_key))    
            if animal=="fish: other teleost":
                zot.addto_collection(collections["animals"]["fish: other teleost"],zot.item(entry_key))    
            if animal=="mammals: mouse":
                zot.addto_collection(collections["animals"]["mammals: mouse"],zot.item(entry_key))
            if animal=="mammals: non-placental":
                zot.addto_collection(collections["animals"]["mammals: non-placental"],zot.item(entry_key))
            if animal=="mammals: other placental":
                zot.addto_collection(collections["animals"]["mammals: other placental"],zot.item(entry_key))
            if animal=="mammals: other rodent":
                zot.addto_collection(collections["animals"]["mammals: other rodent"],zot.item(entry_key))
            if animal=="mammals: human":
                zot.addto_collection(collections["animals"]["mammals: human"],zot.item(entry_key))
            if animal=="mammals: non-human primate":
                zot.addto_collection(collections["animals"]["mammals: non-human primate"],zot.item(entry_key))
            if animal=="other":
                zot.addto_collection(collections["animals"]["other"],zot.item(entry_key))
            if animal=="reptiles":
                zot.addto_collection(collections["animals"]["reptile"],zot.item(entry_key))




            
            if animal!="amphibian" and \
               animal!="bird"and \
               animal!="cell culture"and \
               animal!="organoid" and\
               animal!="fish: any other" and\
               animal!="fish: zebrafish" and\
               animal!="fish: other teleost" and\
               animal!="mammals: mouse" and\
               animal!="mammals: non-placental" and\
               animal!="mammals: other placental" and\
               animal!="mammals: other rodent" and\
               animal!="mammals: human" and\
               animal!="mammals: non-human primate" and\
               animal!="reptile":
                print(animal)
                zot.addto_collection(collections["animals"]["other"],zot.item(entry_key))                

        #publication type
        pub_type = items_to_add.loc[idx]["Type"]
        pub_type = pub_type.split(",")
        for publication in pub_type:
            publication = publication.lower().strip()
                
            if publication=="book chapter":
                zot.addto_collection(collections["pub"]["book chapter"],zot.item(entry_key))    
            if publication=="dispatch or similar":
                zot.addto_collection(collections["pub"]["dispatch or similar"],zot.item(entry_key))          
            if publication=="methods article (peer reviewed)":
                zot.addto_collection(collections["pub"]["methods article (peer reviewed)"],zot.item(entry_key))          
            if publication=="other":
                zot.addto_collection(collections["pub"]["other"],zot.item(entry_key))    
            if publication=="preprint":
                zot.addto_collection(collections["pub"]["preprint"],zot.item(entry_key))    
            if publication=="research article (peer reviewed)":
                zot.addto_collection(collections["pub"]["research article (peer reviewed)"],zot.item(entry_key))   
            if publication=="resource/database":
                zot.addto_collection(collections["pub"]["resource/database"],zot.item(entry_key))    
            if publication=="review (peer reviewed)":
                zot.addto_collection(collections["pub"]["review (peer reviewed)"],zot.item(entry_key))    

            if publication!="book chapter" and\
               publication!="dispatch or similar" and\
               publication!="methods article (peer reviewed)" and\
               publication!="other" and\
               publication!="preprint" and\
               publication!="research article (peer reviewed)" and\
               publication!="resource/database" and\
               publication!="review (peer reviewed)" :
                print(publication)
                zot.addto_collection(collections["pub"]["other"],zot.item(entry_key))    
     #main areas
        main_area = items_to_add.loc[idx]["Subject areas"]
        main_area = main_area.split(",")
        for area in main_area :
            area = area.lower().strip()
            if area=="computation":
                zot.addto_collection(collections["area"]["computation"],zot.item(entry_key))       
            if area=="development":
                zot.addto_collection(collections["area"]["development"],zot.item(entry_key))       
            if area=="function":
                zot.addto_collection(collections["area"]["function"],zot.item(entry_key))
            if area=="injury/disease/regeneration":
                zot.addto_collection(collections["area"]["injury/disease/regeneration"],zot.item(entry_key))       
            if area=="molecular":
                zot.addto_collection(collections["area"]["molecular"],zot.item(entry_key))       
            if area=="structure":
                zot.addto_collection(collections["area"]["structure"],zot.item(entry_key))       
            if area=="tool development: biological":
                zot.addto_collection(collections["area"]["tool development: biological"],zot.item(entry_key))       
            if area=="tool development: hardware":
                zot.addto_collection(collections["area"]["tool development: hardware"],zot.item(entry_key))       
            if area=="tool development: software":
                zot.addto_collection(collections["area"]["tool development: software"],zot.item(entry_key))                       
            if area != "computation" and \
                area!= "development" and \
                area!="function" and\
                area!="injury/disease/regeneration" and\
                area!="molecular" and\
                area!="structure" and\
                area!="tool development: biological" and\
                area!="tool development: hardware" and\
                area!="tool development: software":
                print(area)
                zot.addto_collection(collections["area"]["other"],zot.item(entry_key))       

        #celltype
        cell_type = items_to_add.loc[idx]["Cell types"]
        cell_type = cell_type.split(",")
        for cell in cell_type :
            cell = cell.lower().strip()
            if cell=="amacrine cells":
                zot.addto_collection(collections["cell"]["Amacrine cells"],zot.item(entry_key))       
            if cell=="bipolar cells":
                zot.addto_collection(collections["cell"]["Bipolar cells"],zot.item(entry_key))       
            if cell=="cortex and related":
                zot.addto_collection(collections["cell"]["Cortex and related"],zot.item(entry_key))       
            if cell=="horizontal cells":
                zot.addto_collection(collections["cell"]["Horizontal cells"],zot.item(entry_key))       
            if cell=="photoreceptors":
                zot.addto_collection(collections["cell"]["Photoreceptors"],zot.item(entry_key))       
            if cell=="ganglion cells":
                zot.addto_collection(collections["cell"]["Retinal ganglion"],zot.item(entry_key))       
            if cell=="superior colliculus/tectum and related":
                zot.addto_collection(collections["cell"]["Superior colliculus/tectum"],zot.item(entry_key))       
            if cell=="thalamus and related":
                zot.addto_collection(collections["cell"]["Thalamus and related"],zot.item(entry_key))       

            if cell!="amacrine cells" and \
                cell!="bipolar cells" and \
                cell!="cortex and related" and\
                cell!="horizontal cells" and\
                cell!="photoreceptors" and\
                cell !="ganglion cells" and\
                cell!="superior colliculus/tectum and related" and\
                cell!="thalamus and related" :
                print(cell)
                zot.addto_collection(collections["cell"]["other"],zot.item(entry_key))       
                


#with open(dataPath + "zotMeta.json", "w") as fid:
#    json.dump(allMeta, fid)




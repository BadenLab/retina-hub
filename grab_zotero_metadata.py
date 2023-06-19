"""
Small script to load necessary libraries and match google scholar entries to Web of Science entries using WOS api
"""
import requests
import pandas as pd
from pyzotero import zotero
#import json
#import time




#sheet_id = "14EgPuHwmltEjWeFZfwygVKYwSlvYkG5yCv6IXquz2Os"
#sheet_name = "Form Responses 1"
#url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"


#sheet_url = "https://docs.google.com/spreadsheets/d/14EgPuHwmltEjWeFZfwygVKYwSlvYkG5yCv6IXquz2Os/edit#gid=1702410538"
sheet_url = "https://docs.google.com/spreadsheets/d/15jE_Hc_otR_OvAkRy_aseGhCaO7c29M8DKyNuso6dyU/edit?resourcekey#gid=693684877"
url_1 = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')

# Convert data to pandas DataFrame
garticles = pd.read_csv(url_1)

# Step 2: Connect to Zotero

with open("zotero_api","r") as fid:
    api_key = fid.readline()

library_id = "4584648"
library_type = "group"
#api_key = "your_zotero_api_key"
zot = zotero.Zotero(library_id, library_type, api_key)
zotero_group_items = zot.top(limit=100) # adjust limit as per your needs

# Extract DOIs from the zotero group
zotero_dois = [item['data'].get('DOI', None) for item in zotero_group_items]

g_doi_column = 'Publication Identifier (DOI, ISBN, PMID, arXiv ID). If you do not know any of these for the entry, please use crossref search engine https://www.crossref.org/guestquery - use the subfield "search on article title")'
# Step 3: Find the DOIs in the Google Sheet not in the Zotero group
google_sheet_dois = garticles[g_doi_column].tolist()

dois_to_add = list(set(google_sheet_dois) - set(zotero_dois))

items_to_add = garticles.loc[garticles[g_doi_column].isin(dois_to_add)]

# Step 4: Add these papers to Zotero subgroups

collections = {
  "animals":{
    "amphibians":"I5YWZIRR",
  "frog":"FKN3BCFK",
  "human":"6B6UBDAK",
  "mouse":"K93FPB4B",
  "non-human primate":"U39PBZ7C",
  "other":"WDSXVYN6",
  "rat":"T4AYDE66",
  "zebrafish":"33DJT8BK",
  "shark":"Z4IN47WJ"
  },
  "pub":{
  "book":"IL925QCT",
  "other":"WACYJQPH",
  "peer reviewed":"N3H5YAW3",
  "preprint":"UAYZHHPY",
  "review":"UF9V5CB6",
  },
  "area":{
  "computational":"QVN2AP8C",
  "function":"ICYG3YV6",
  "injury/disease":"NI8DPUXS",
  "inner retina":"J5IMW5BP",
  "molecular":"DUB5BNPW",
  "organoid":"GBXAVJMW",
  "other":"ZWVM2ZIS",
  "outer retina":"D8SDAZI7",
  "structure":"R5ZD6ZLM",
  },
  "cell":{
  "amacrine":"2ECXQ9WE",
  "bipolar":"78A6KXVR",
  "cones":"66QHAKSP",
  "horizontal":"M6CLZYGV",
  "other":"UZD6C2J9",
  "retinal ganglion":"8QY5WMJH",
  "rods":"4WMPKKHJ"
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
index=0
#allMeta = list()



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
        species = items_to_add.loc[idx]["Species (select all that apply)"]
        species = species.split(",")
        for animal in species:
            animal = animal.lower().strip()
                
        
            if animal=="frog":
                zot.addto_collection(collections["animals"]["frog"],zot.item(entry_key))    
            if animal=="human":
                zot.addto_collection(collections["animals"]["human"],zot.item(entry_key))    
            if animal=="mouse":
                zot.addto_collection(collections["animals"]["mouse"],zot.item(entry_key))    
            if animal=="non-human primate":
                zot.addto_collection(collections["animals"]["non-human primate"],zot.item(entry_key))    

            if animal=="rat":
                zot.addto_collection(collections["animals"]["rat"],zot.item(entry_key))    
            if animal=="zebrafish":
                zot.addto_collection(collections["animals"]["zebrafish"],zot.item(entry_key))
            if animal=="shark":
                zot.addto_collection(collections["animals"]["shark"],zot.item(entry_key))
            if animal!="frog" and \
               animal!="non-human primate"and \
               animal!="rat"and \
               animal!="zebrafish" and\
               animal!="human" and\
                 animal!="chicken" and\
                animal!="shark" and\
               animal!="mouse":
                print(animal)
                zot.addto_collection(collections["animals"]["other"],zot.item(entry_key))                

        #publication type
        pub_type = items_to_add.loc[idx]["Type"]
        pub_type = pub_type.split(",")
        for publication in pub_type:
            publication = publication.lower().strip()
                
            if publication=="peer reviewed":
                zot.addto_collection(collections["pub"]["peer reviewed"],zot.item(entry_key))    
            if publication=="book":
                zot.addto_collection(collections["pub"]["book"],zot.item(entry_key))          
            if publication=="preprint":
                zot.addto_collection(collections["pub"]["preprint"],zot.item(entry_key))          
            if publication=="review":
                zot.addto_collection(collections["pub"]["review"],zot.item(entry_key))    
            if publication!="book" and\
               publication!="peer reviewed" and\
               publication!="preprint" and\
               publication!="review":
                print(publication)
                zot.addto_collection(collections["pub"]["other"],zot.item(entry_key))    
     #main areas
        main_area = items_to_add.loc[idx]["Main areas (please select all that apply)"]
        main_area = main_area.split(",")
        for area in main_area :
            area = area.lower().strip()
            if area=="computational":
                zot.addto_collection(collections["area"]["computational"],zot.item(entry_key))       
            if area=="function":
                zot.addto_collection(collections["area"]["function"],zot.item(entry_key))
            if area=="injury/disease":
                zot.addto_collection(collections["area"]["injury/disease"],zot.item(entry_key))       
            if area=="inner retina":
                zot.addto_collection(collections["area"]["inner retina"],zot.item(entry_key))       
            if area=="molecular":
                zot.addto_collection(collections["area"]["molecular"],zot.item(entry_key))       
            if area=="organoid":
                zot.addto_collection(collections["area"]["organoid"],zot.item(entry_key))       
            #elif area=="other":
            #    zot.addto_collection(collections["area"]["other"],zot.item(entry_key))       
            if area=="outer retina":
                zot.addto_collection(collections["area"]["outer retina"],zot.item(entry_key))       
            if area=="structure":
                zot.addto_collection(collections["area"]["structure"],zot.item(entry_key))       
            if area != "structure" and \
                area!= "outer retina" and \
                area!="organoid" and\
                area!="molecular" and\
                area!="inner retina" and\
                area!="injury/disease" and\
                area!="function" and\
                area!="computational":
                print(area)
                zot.addto_collection(collections["area"]["other"],zot.item(entry_key))       

        #celltype
        cell_type = items_to_add.loc[idx]["cell types (select all that apply)"]
        cell_type = cell_type.split(",")
        for cell in cell_type :
            cell = cell.lower().strip()
            if cell=="amacrine cells":
                zot.addto_collection(collections["cell"]["amacrine"],zot.item(entry_key))       
            if cell=="bipolar cells":
                zot.addto_collection(collections["cell"]["bipolar"],zot.item(entry_key))       
            if cell=="cones":
                zot.addto_collection(collections["cell"]["cones"],zot.item(entry_key))       
            if cell=="horizontal cells":
                zot.addto_collection(collections["cell"]["horizontal"],zot.item(entry_key))       
            #if cell=="other":
            #    zot.addto_collection(collections["cell"]["other"],zot.item(entry_key))       
            if cell=="retinal ganglion cells":
                zot.addto_collection(collections["cell"]["retinal ganglion"],zot.item(entry_key))       
            if cell=="rods":
                zot.addto_collection(collections["cell"]["rods"],zot.item(entry_key))       
            if cell!="rods" and cell!="cones" and \
                cell!="horizontal cells" and\
                cell!="bipolar cells" and\
                cell!="amacrine cells" and\
                cell !="retinal ganglion cells":
                print(cell)
                zot.addto_collection(collections["cell"]["other"],zot.item(entry_key))       
                


#with open(dataPath + "zotMeta.json", "w") as fid:
#    json.dump(allMeta, fid)


"""
with open(dataPath + "zotMeta.json", "r") as fid:
    allMeta = json.load(fid)
 
 #print(data)

with open("zotero_api","r") as fid:
    key = fid.readline()

zot = zotero.Zotero(library_id=4584648,library_type='group', api_key=key)

index=0
for item in allMeta:
    if item !="None":
        index=index+1
        zot.create_items(item)
        #time.sleep(0.1)
        print(index)
"""
# Import olika libraryes som behövs i projecktet.
import requests
import tkinter as tk
from tkinter import ttk, StringVar
import json

#'Jag försokte att skriva namnet för stationen som ska tåget gå emot, men programet krashar hela tiden när jag gör det, så jag skrev bara nycklen.'


# API-nyckel på Trafiklab.se.
# En dictionary - Lista som innehåller alla nykelar coh platser för alla stationer i värmland.
stations_dict = {'Karlstad':'Ks', 'Arvika':'Ar', "Bäckebron":"Bäb", "Charlottenberg":"Cg", "Edane": "En", "Fagerås":"Fgå", "Frykåsen":"Frå", "Filipstad":"Fid", "Grums": "Gms", "Högboda":"Hbd", "Kil": "Kil", "Kolsnäs": "Kns", "Välsviken":"Kvä", "Kristinehamn": "Khn", "Lysvik":"Lyv", "Nässundet": "Nd", "Nykroppa": "Nka", "Oleby": "Ol", "Rottneros":"Rts" }

# Min API nyckel.
API_KEY = 'aa916ca49ce741d5bc78df1302631bfd'

# Huvud metoden som är grunden för hela programmet som hämtar informationerna som jag har bestämmt att de ska finnas i Textruta.
def getDepartures():
    with open('mydata.json', 'w') as f:
      #Hittar index från stations namn i Stations_Dict och skriver in den i mydata.json.
      json.dump(list(stations_dict.values()).index(stations_dict[stationer.get()]), f)

    """
    Hämtar data från Trafikverket med ett POST-anrop
    """
    request = f"""<REQUEST>
<LOGIN authenticationkey="{API_KEY}" />
<QUERY objecttype="TrainAnnouncement" schemaversion="1.3" orderby="AdvertisedTimeAtLocation">
<FILTER>
<AND>
<EQ name="ActivityType" value="Avgang" />
<EQ name="LocationSignature" value="{stations_dict[stationer.get()]}" />
<OR>
<AND>
<GT name="AdvertisedTimeAtLocation" value="$dateadd(07:00:00)" />
<LT name="AdvertisedTimeAtLocation" value="$dateadd(12:00:00)" />
</AND>
</OR>
</AND>
</FILTER>
<INCLUDE>LocationSignature</INCLUDE>
<INCLUDE>AdvertisedTrainIdent</INCLUDE>
<INCLUDE>AdvertisedTimeAtLocation</INCLUDE>
<INCLUDE>TrackAtLocation</INCLUDE>
<INCLUDE>ToLocation</INCLUDE>
<INCLUDE>AdvertisedLocationName</INCLUDE>

</QUERY>
</REQUEST>"""

    # Här sker själva anropet.
    url = 'https://api.trafikinfo.trafikverket.se/v1.3/data.json'
    response = requests.post(url, data = request, headers = {'Content-Type': 'text/xml'}, )

    # Formatera svaret från servern som ett json-objekt.
    response_json = json.loads(response.text)
    departures = response_json["RESPONSE"]['RESULT'][0]['TrainAnnouncement']
    
    # Töm svarsrutan.
    stationer_text.delete(1.0,"end")

    # Delen för hur kan man se informationen.
    for dep in departures:
        stationer_text.insert(1., '\n--------------\n\n')
        tillstationenKey = dep['ToLocation'][0]['LocationName']
        stationer_text.insert(1., tillstationenKey)
        stationer_text.insert(1., '\n---------------\n')

        Spår ="Spår: " + dep['TrackAtLocation']
        stationer_text.insert(1., Spår)
        stationer_text.insert(1., '\n----------------\n')

        tågnummer ="Tågnummer: " + dep['AdvertisedTrainIdent']
        stationer_text.insert(1., tågnummer)
        stationer_text.insert(1., '\n----------------\n')

        datum = "Datum: " + dep['AdvertisedTimeAtLocation']
        stationer_text.insert(1., datum)
        stationer_text.insert(1., '\n----------------------------------------------------\n\n\n')
          
#----------------------

# Det grafiska gränssnittet för programet.
root = tk.Tk()
canvas = tk.Canvas(root,height=700, width=1000)
canvas.configure(bg='#6D214F')
canvas.pack()

# Knapp delen.
button=tk.Button(root, text='Klicka här', command= getDepartures)
button.place(width=200, height=75, relx=0.6, rely=0.72)
button.configure( fg='#25CCF7',bg='#6D214F', font= 2.2, cursor='clock')


# läser datan från mydata.json och använder indexet som current value efter att vi gör det till int.
f = open ('mydata.json', "r") 
data = int(json.loads(f.read()))
# Combobox med stationer. Läser in alla "uppslagsord" från stations_dict.
stationer = ttk.Combobox(canvas, state='readonly')
stationer['values'] = list(stations_dict.keys())
stationer.current(data)
stationer.place(relx=0, rely=0, width=450, height=70)

# Textruta delen.
stationer_text = tk.Text(canvas)
stationer_text.place(relx=0.0005, rely=0.1, relwidth=0.9989, relheight=1)
stationer_text.configure(bg='#6D214F', fg='#0fbcf9', font =2.2, cursor= 'star') 

root.mainloop()
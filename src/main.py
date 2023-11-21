import re
import urllib.request
from pandas import DataFrame


def crawl_stats(regex, list, asInt):
    stat = re.findall(regex, http)
    if stat:
        if asInt:
            list.append(int(stat[0]))
        else:
            list.append(stat[0].replace('&#039;', "'"))
    else:
        if asInt:
            list.append(0)
        else:
            list.append('')


print('Parsing Wishlist...')
wishlist = open("AtlasLoot.lua", "r")
ids = re.findall(r'(\d+)(?=\s*,\s*--\s*\[2)', wishlist.read())

outID = []
outName = []
outSlot = []
outType = []
outTier = []
outArmor = []
outStr = []
outAgi = []
outStam = []
outInt = []
outSpirit = []
outCrit = []
outHaste = []
outMastery = []
outDodge = []
outParry = []
outHit = []
outExpertise = []
outSP=[]
outWep = []
outSockets = []
outSocketBonus = []
outSocketBonusRAW = []

index = -1
print("Starting Crawl...")
for id in ids:
    index += 1

    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers = {'User-Agent': user_agent, }
    request = urllib.request.Request("https://mop-shoot.tauri.hu/?item="+ id, None, headers)
    #request = urllib.request.Request("https://mop-twinhead.twinstar.cz/?item="+ id, None, headers)
    page = urllib.request.urlopen(request)
    pageBytes = page.read()
    http = pageBytes.decode("utf8")
    page.close()

    if "Plans:" in http:
        id = re.findall(r'creates:\[(\d+)\s*,', http)[0]
        page = urllib.request.urlopen("https://mop-shoot.tauri.hu/?item=" + id)
        pageBytes = page.read()
        http = pageBytes.decode("utf8")
        page.close()

    print("CRAWLING: ", id)
    outID.append(int(id))
    outWep.append(0)
    outSP.append(0)

    crawl_stats(r'<h1>(.*?) - Item', outName, False)
    crawl_stats(r'<table width=\"100%\"><tr><td>(.*?)</td>', outSlot, False)
    crawl_stats(r'</td><th>(.*?)</th>', outType, False)

    if "Tier" in http:
        outTier.append(1)
    else:
        outTier.append(0)

    crawl_stats(r'</table>(\d+)\s* Armor', outArmor, True)
    crawl_stats(r'>\+(\d+)\s* Strength', outStr, True)
    crawl_stats(r'>\+(\d+)\s* Agility', outAgi, True)
    crawl_stats(r'>\+(\d+)\s* Stamina', outStam, True)
    crawl_stats(r'>\+(\d+)\s* Intellect', outInt, True)
    crawl_stats(r'>\+(\d+)\s* Spirit', outSpirit, True)
    crawl_stats(r'>\+(\d+)\s* Crit', outCrit, True)
    crawl_stats(r'>\+(\d+)\s* Haste', outHaste, True)
    crawl_stats(r'>\+(\d+)\s* Mastery', outMastery, True)
    crawl_stats(r'>\+(\d+)\s* Dodge', outDodge, True)
    crawl_stats(r'>\+(\d+)\s* Parry', outParry, True)
    crawl_stats(r'>\+(\d+)\s* Hit', outHit, True)
    crawl_stats(r'>\+(\d+)\s* Expertise', outExpertise, True)
    crawl_stats(r'Socket Bonus: \+(.*?)<', outSocketBonus, False)
    if outSocketBonus[index]:
        outSocketBonusRAW.append(int(re.findall(r'\d+', outSocketBonus[index])[0]))
    else:
        outSocketBonusRAW.append(0)

    redSockets = http.count("Red Socket")
    yellowSockets = http.count("Yellow Socket")
    blueSockets = http.count("Blue Socket")
    itemSockets = ''
    for socket in range(redSockets):
        itemSockets += 'R'
    for socket in range(yellowSockets):
        itemSockets += 'Y'
    for socket in range(blueSockets):
        itemSockets += 'B'
    outSockets.append(itemSockets)

if index >= 0:
    df = DataFrame({'ID': outID, 'NAME': outName, 'SLOT': outSlot, 'TYPE': outType, 'ARMOR': outArmor,
                    'STR': outStr, 'AGI': outAgi, 'STAM': outStam, 'INT': outInt, 'SPIRIT': outSpirit,
                    'CRIT': outCrit, 'HASTE': outHaste, 'MASTERY': outMastery, 'DODGE': outDodge, 'PARRY': outParry,
                    'HIT': outHit, 'EXP': outExpertise, 'SP': outSP, 'WEP': outWep, 'TIER': outTier,
                    'SOCKETS': outSockets, 'BONUS': outSocketBonus, 'RAW BONUS': outSocketBonusRAW})

    fileName = input("Write file name...")
    df.to_excel(fileName + '.xlsx', index=False)
    print("SUCCESS")
else:
    print("FAILED")

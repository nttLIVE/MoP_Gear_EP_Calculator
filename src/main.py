import re
import urllib.request
from pandas import DataFrame


def crawl_stats(regex, list):
    stat = re.findall(regex, http)
    if stat:
        list.append(stat[0].replace('&#039;', "'"))
    else:
        list.append('')


def crawl_stats_int(regex, list):
    stat = re.findall(regex, http)
    if stat:
        list.append(int(stat[0]))
    else:
        list.append(0)


def crawl_stats_float(regex, list):
    stat = re.findall(regex, http)
    if stat:
        list.append(float(stat[0]))
    else:
        list.append(float(0))


print('Parsing WishList')
wishList = open("AtlasLoot.lua", "r")
wishListText = wishList.read()
wishListTexts = re.findall(r'\s*{\s*{\s*{\s*0, -- \[1][\s\S]+?\["name"] = [\s\S]+?,', wishListText)
wishListNames = re.findall(r'\["name"] = "([\s\S]+?)",', wishListText)

if len(wishListTexts) > 0:
    print("WishLists Found: ")
    wishListNameCounter = 0
    wishListNamePrint = ''
    for wishListName in wishListNames:
        wishListNamePrint += wishListName + "(" + str(wishListNameCounter) + ") "
        wishListNameCounter += 1

    print(wishListNamePrint)
    print("Select all WishLists to be parsed by entering their respective numbers separated with spaces... ")
    wishListInput = input()
    selectedWishLists = list(map(int, set(re.findall(r'\d+', wishListInput))))

    for selectedWishList in selectedWishLists:
        if selectedWishList >= len(wishListTexts):
            continue

        ids = re.findall(r'(\d+)(?=\s*,\s*--\s*\[2)', wishListTexts[selectedWishList])

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
        outSP = []
        outWep = []
        outSockets = []
        outSocketBonus = []
        outSocketBonusRAW = []

        index = -1
        print("Starting Crawl")
        for id in ids:
            index += 1

            user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
            headers = {'User-Agent': user_agent, }
            request = urllib.request.Request("https://mop-shoot.tauri.hu/?item=" + id, None, headers)
            # request = urllib.request.Request("https://mop-twinhead.twinstar.cz/?item="+ id, None, headers)
            page = urllib.request.urlopen(request)
            pageBytes = page.read()
            http = pageBytes.decode("utf8")
            page.close()

            if "Plans:" in http or "Pattern:" in http:
                id = re.findall(r'creates:\[(\d+)\s*,', http)[0]
                page = urllib.request.urlopen("https://mop-shoot.tauri.hu/?item=" + id)
                pageBytes = page.read()
                http = pageBytes.decode("utf8")
                page.close()

            print("CRAWLING: ", id)
            outID.append(int(id))

            crawl_stats(r'<h1>(.*?) - Item', outName)
            crawl_stats(r'<table width=\"100%\"><tr><td>(.*?)</td>', outSlot)
            crawl_stats(r'</td><th>(.*?)</th>', outType)

            if "Tier" in http:
                outTier.append(1)
            else:
                outTier.append(0)

            crawl_stats_float(r'([0-9]*[.]?[0-9]+) damage per second', outWep)
            crawl_stats_int(r'>\+(\d+)\s* Spell Power', outSP)

            crawl_stats_int(r'</table>(\d+)\s* Armor', outArmor)
            crawl_stats_int(r'>\+(\d+)\s* Strength', outStr)
            crawl_stats_int(r'>\+(\d+)\s* Agility', outAgi)
            crawl_stats_int(r'>\+(\d+)\s* Stamina', outStam)
            crawl_stats_int(r'>\+(\d+)\s* Intellect', outInt)
            crawl_stats_int(r'>\+(\d+)\s* Spirit', outSpirit)
            crawl_stats_int(r'>\+(\d+)\s* Crit', outCrit)
            crawl_stats_int(r'>\+(\d+)\s* Haste', outHaste)
            crawl_stats_int(r'>\+(\d+)\s* Mastery', outMastery)
            crawl_stats_int(r'>\+(\d+)\s* Dodge', outDodge)
            crawl_stats_int(r'>\+(\d+)\s* Parry', outParry)
            crawl_stats_int(r'>\+(\d+)\s* Hit', outHit)
            crawl_stats_int(r'>\+(\d+)\s* Expertise', outExpertise)
            crawl_stats(r'Socket Bonus: \+(.*?)<', outSocketBonus)
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
                            'CRIT': outCrit, 'HASTE': outHaste, 'MASTERY': outMastery, 'DODGE': outDodge,
                            'PARRY': outParry,
                            'HIT': outHit, 'EXP': outExpertise, 'SP': outSP, 'WEP': outWep, 'TIER': outTier,
                            'SOCKETS': outSockets, 'BONUS': outSocketBonus, 'RAW BONUS': outSocketBonusRAW})

            print("SUCCESS")

            df.to_excel(wishListNames[selectedWishList] + '.xlsx', sheet_name=wishListNames[selectedWishList],
                        index=False)
        else:
            print("FAILED")

    print("Press Enter to close")
    input()
else:
    print("No WishLists detected")
    print("Press Enter to close")
    input()
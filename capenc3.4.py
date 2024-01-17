# Please excuse this code for being such a mess... I am so tired...

# Oh, Hey! You found a way to look at code you're not supposed to see!
# Can you tell us how you did that, so we can make sure that it doesn't happen again?
# Thanks!

# Written By Anastasia M, Maintained by Anastasia M, Skylar G.
# Base code Originated by Anastasia M. with help of Stack Exchange, Stack Overflow, and Google.

# Please Note, I don't have any of the Licensing stuff in here, as I don't need more people on my ass.

## ADMIN CONFIGURABLE SETTINGS FOR EASE OF ACCESS...
IPAWSpin = ""  # INSERT PIN HERE, NOT PROVIDED
Version = "3.4.6-bldL4"
UserAgent = "MSNGTXTRS_CAPDEC-3.4.6"
DevAccessKey = "yLy2QgApUomsc0DmUlfUvJc4IkFwr1poTiUGsR3SIjmIZnxUyFC7CuOEK52iGGDB2OpSiddtBZESYyeSlWW23."
DevModeAccnt = {
    "nickname": "Developer",
    "uid": "HAH-LOL-420_69",
    "access": True,
    "encoder": True,
    "ipaws": True,
    "naad": True,
    "nws": True,
    "legacy": True,
}

# Standard Library
import xml.etree.ElementTree as ET
from argparse import ArgumentParser
from base64 import b64decode
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from json import dump, load
from os import _exit as OSExit
from os import path, remove, system
from platform import system as OSType
from threading import Thread
from time import mktime, sleep

# Third-Party
from ansimarkup import ansiprint as print
from EAS2Text.EAS2Text import EAS2Text
from EASGen.EASGen import EASGen
from pydub import AudioSegment, effects
from pydub.playback import play as pdplay
from requests import get
from requests.exceptions import ConnectionError, Timeout

# First-Party
import Extras

oldAlert = []
alerts = []
currentAlert = []
currentAlert2 = []
currentID = []
currentID2 = []
num = 0
PollingState = False
OldAlertListNWS = []
OldAlertListCAP = []
logAlert = []
logAlert2 = []
ATTNAudioData = ""
ATTNAudioData2 = ""
EOMAudioData = ""
EOMAudioData2 = ""
NWSHold = False
NWSHold2 = False
IPAWSHold = False
UAheader = {"user-agent": UserAgent}

NWSFilter = [
    ["*", ""],
    ["NOAA ", "Noah"],
    ["PRECAUTIONARY/PREPAREDNESS ACTIONS... ", ""],
    ["mph ", "miles per hour "],
    ["kts ", "Knots "],
    ["/", "or"],
    ["*AT", "at"],
    ["...", ", "],
    ["..", ", "],
    ["-", "or"],
    ["precip ", "precipitation"],
    ["Mar ", "March"],
    ["Feb ", "February"],
    ["Jan ", "January"],
    ["Dec ", "December"],
    ["Nov ", "November"],
    ["Oct ", "October"],
    ["Sep ", "September"],
    ["Aug ", "August"],
    ["Jul ", "July"],
    ["Jun ", "June"],
    ["May ", "May"],
    ["Apr ", "April"],
    ["NM ", "nautical miles"],
    ["MST/", "MST"],
    ["MDT/", "MDT"],
    ["PST/", "PST"],
    ["PDT/", "PDT"],
    ["EST/", "EST"],
    ["EDT/", "EDT"],
    ["CST/", "CST"],
    ["CDT/", "CDT"],
    ["AKST/", "AKST"],
    [" PDT ", " Pacific Daylight Time "],
    [" MDT ", " Mountain Daylight Time "],
    [" MST ", " Mountain Standard Time "],
    [" PST ", " Pacific Standard Time "],
    [" CDT ", " Central Daylight Time "],
    [" CST ", " Central Standard Time "],
    [" EDT ", " Eastern Daylight Time "],
    [" EST ", " Eastern Standard Time "],
    [" AKST", " Alaskan Standard Time "],
    [" WPC ", " Weather Prediction Center "],
    ["/1 ", "or 1"],
    ["/2 ", "or 2"],
    ["/3 ", "or 3"],
    ["/4 ", "or 4"],
    ["/5 ", "or 5 "],
    ["/6 ", "or 6"],
    ["/7 ", "or 7"],
    ["/8 ", "or 8"],
    ["/9 ", "or 9"],
    ["/10 ", "or 10"],
    ["/11 ", "or 11"],
    ["/12 ", "or 12"],
    ["am ", "AM "],
    ["pm ", "PM "],
    ["1am ", "1 AM "],
    ["2am ", "2 AM "],
    ["3am ", "3 AM "],
    ["4am ", "4 AM "],
    ["5am ", "5 AM "],
    ["6am ", "6 AM "],
    ["7am ", "7 AM "],
    ["8am ", "8 AM "],
    ["9am ", "9 AM "],
    ["10am ", "10 AM "],
    ["11am ", "11 AM "],
    ["12am ", "12 AM "],
    ["1pm ", "1 PM "],
    ["2pm ", "2 PM "],
    ["3pm ", "3 PM "],
    ["4pm ", "4 PM "],
    ["5pm ", "5 PM "],
    ["6pm ", "6 PM "],
    ["7pm ", "7 PM "],
    ["8pm ", "8 PM "],
    ["9pm ", "9 PM "],
    ["10pm ", "10 PM "],
    ["01 ", "O 1"],
    ["02 ", "O 2"],
    ["03 ", "O 3"],
    ["04 ", "O 4"],
    ["05 ", "O 5"],
    ["06 ", "O 6"],
    ["07 ", "O 7"],
    ["08 ", "O 8"],
    ["09 ", "O 9"],
    ["= ", ""],
    ["\n", " "],
]

CAPFilter = [
    [" EAS ", " E A S "],
    [".", ". "],
    ["mph", "miles per hour"],
    [" E.A.S. ", " Emergency Alert System "],
    [" E.A.S ", " Emergency Alert System "],
    [":00", ""],
    [":01 ", " O 1 "],
    [":02 ", " O 2 "],
    [":03 ", " O 3 "],
    [":04 ", " O 4 "],
    [":05 ", " O 5 "],
    [":06 ", " O 6 "],
    [":07 ", " O 7 "],
    [":08 ", " O 8 "],
    [":09 ", " O 9 "],
    [":", " "],
    [" PM ", " P M "],
    [" AM ", " A M "],
    [" PM. ", " P M. "],
    [" AM. ", " A M. "],
    ["\n", " "],
    ["*", ""],
]

StateFilter = [
    [" AL; ", " Alabama; "],
    [" AK; ", " Alaska; "],
    [" AZ; ", " Arizona; "],
    [" AR; ", " Arkansas; "],
    [" CA; ", " California; "],
    [" CO; ", " Colorado; "],
    [" CT; ", " Connecticut; "],
    [" DE; ", " Delaware; "],
    [" FL; ", " Florida; "],
    [" GA; ", " Georgia; "],
    [" HI; ", " Hawaii; "],
    [" ID; ", " Idaho; "],
    [" IL; ", " Illinois; "],
    [" IN; ", " Indiana; "],
    [" IA; ", " Iowa; "],
    [" KS; ", " Kansas; "],
    [" KY; ", " Kentucky; "],
    [" LA; ", " Louisiana; "],
    [" ME; ", " Maine; "],
    [" MD; ", " Maryland; "],
    [" MA; ", " Massachusetts; "],
    [" MI; ", " Michigan; "],
    [" MN; ", " Minnesota; "],
    [" MS; ", " Mississippi; "],
    [" MO; ", " Missouri; "],
    [" MT; ", " Montana; "],
    [" NE; ", " Nebraska; "],
    [" NV; ", " Nevada; "],
    [" NH; ", " New Hampshire; "],
    [" NJ; ", " New Jersey; "],
    [" NM; ", " New Mexico; "],
    [" NY; ", " New York; "],
    [" NC; ", " North Carolina; "],
    [" ND; ", " North Dakota; "],
    [" OH; ", " Ohio; "],
    [" OK; ", " Oklahoma; "],
    [" OR; ", " Oregon; "],
    [" PA; ", " Pennsylvania; "],
    [" RI; ", " Rhode Island; "],
    [" SC; ", " South Carolina; "],
    [" SD; ", " South Dakota; "],
    [" TN; ", " Tennessee; "],
    [" TX; ", " Texas; "],
    [" UT; ", " Utah; "],
    [" VT; ", " Vermont; "],
    [" VA; ", " Virginia; "],
    [" WA; ", " Washington; "],
    [" WV; ", " West Virginia; "],
    [" WI; ", " Wisconsin; "],
    [" WY; ", " Wyoming; "],
    [" AS; ", " American Samoa; "],
    [" GM; ", " Guam; "],
    [" MP; ", " Northern Mariana Islands; "],
    [" PR; ", " Puerto Rico; "],
    [" VI; ", " U.S. Virgin Islands; "],
    [" UM; ", " U.S. Minor Outlying Islands; "],
]


def cls():
    if OSType() == "Windows":
        system("cls")
    elif OSType() == "Linux":
        system("clear")


# Authentication shit
def apiUIDExists():
    global accnt
    accnt = {
        "nickname": "Removed Licensing",
        "uid": "Because I can.",
        "access": True,
        "encoder": True,
        "ipaws": True,
        "naad": True,
        "nws": True,
        "legacy": True,
    }


def logToDiscord():
    print(f"[<g>LOGGER</g>] Service Started.")
    while True:
        if test == "tdl.":
            testLog = True
        else:
            testLog = False
        sleep(0.5)
        try:
            (
                orgText,
                message,
                instruction,
                header,
                ident,
                audio,
                url,
                status,
                filter,
            ) = logAlert.pop(0)
            Extras.log(
                str(orgText),
                str(message),
                str(instruction),
                str(header).replace("\xab", ""),
                str(ident),
                str(audio),
                "Output/EAS_" + ident + ".wav",
                str(url.split("://")[1].split("/")[0]),
                status,
                filter,
                Version,
                testLog,
            )
        except IndexError:
            pass
        except Exception as e:
            print(f"[<r>LOGGER</r>] Log Error: {str(e)}")


def _ts_parse(ts):
    """Parse alert timestamp, return UTC datetime object to maintain Python 2 compatibility."""
    dt = datetime.strptime(ts[:19], "%Y-%m-%dT%H:%M:%S")
    if ts[19] == "+":
        dt -= timedelta(hours=int(ts[20:22]), minutes=int(ts[23:]))
    elif ts[19] == "-":
        dt += timedelta(hours=int(ts[20:22]), minutes=int(ts[23:]))
    return dt.replace(tzinfo=None)


def dumpCap(status, identifier, header, url):
    try:
        ##return None #Use for debugging. This shit is annoying to deal with.
        alerts["cap"].append(
            [
                status,
                identifier,
                str(header),
                str(url.split("://")[1].split("/")[0]),
            ]
        )
        with open("Static/capAlerts.json", "w") as f:
            dump(alerts, f, indent=4)
            f.close()
        if debug:
            print(f"[<e>DEV</e>] Dumped CAP log.")
        return
    except:
        print(
            f"[<r>RUN</r>] <w,r>FATAL ERROR: Cannot Dump Alert Log. This is a Non-Recoverable Error.</w,r>\n[<r>RUN</r>] <w,r>Program will now EXIT.</w,r>"
        )
        remove("Static/capAlerts.json")
        with open("Static/capAlerts.json", "w") as f:
            f.write('{"cap": []}')
            f.close()
        OSExit(1)


def getIPAWS():
    global OldAlertListCAP
    global IPAWSHold
    global num
    if path.exists("pin.txt"):
        with open("pin.txt", "r") as f:
            pin = f.read()
        if debug:
            print(f"[<e>DEV</e>] Using external IPAWS pin.")
    else:
        pin = IPAWSpin
        if debug:
            print(f"[<e>DEV</e>] Using internal IPAWS pin.")
    try:
        resp = []
        alerts = []
        ipaws = get(
            f"https://{test}apps.fema.gov/IPAWSOPEN_EAS_SERVICE/rest/feed?pin="
            + pin,
            headers=UAheader,
            timeout=5,
        )
        if ipaws.status_code == 403:
            if IPAWSHold != True:
                print(
                    f"[<r>IPAWS</r>] <b>*** Pin is Invalid. <r>Not</r> Polling. ***</b>"
                )
                IPAWSHold = True
            return None
        elif ipaws.status_code == 200:
            if IPAWSHold == True:
                print(
                    f"[<g>IPAWS</g>] <b>*** Connected <g>Successfully</g>. Polling. ***</b>"
                )
                IPAWSHold = False
            ipfeed = ET.fromstring(ipaws.content)
            for feed in ipfeed:
                if str(feed.tag).endswith("entry"):
                    for entry in feed:
                        if str(entry.tag).endswith("id"):
                            alerts.append(str(entry.text))
            for alert in alerts:
                if alert in OldAlertListCAP:
                    pass
                else:
                    OldAlertListCAP.append(alert)
                    resp.append(
                        get(alert + "?pin=" + pin, headers=UAheader, timeout=5)
                    )
            for i in OldAlertListCAP:
                if i in alerts:
                    pass
                else:
                    if debug:
                        print(
                            f"[<e>IPAWS</e>] Removing old alert {i} from internal buffer..."
                        )
                    OldAlertListCAP.pop(OldAlertListCAP.index(i))
        else:
            return None
        if isinstance(resp, list):
            for alrt in resp:
                if alrt.status_code == 200:
                    resp = str(alrt.content.decode("utf-8"))
                    parseCap(
                        f"https://{test}apps.fema.gov/IPAWSOPEN_EAS_SERVICE/rest/update",
                        resp,
                        False,
                        True,
                    )
                elif alrt.status_code == 403:
                    print(
                        f"[<d><r>IPAWS</r></d>] <d>Alert has Expired. Ignoring.</d>"
                    )
                else:
                    num = num + 1
                    print(
                        f"[<d><r>IPAWS</r></d>] <d>Alert Fetch Failed. (<r>{str(alrt.status_code)}</r>)</d> ({str(num)})"
                    )
            return None
        else:
            if resp.status_code == 200:
                resp = str(resp.content.decode("utf-8"))
                parseCap(
                    f"https://{test}apps.fema.gov/IPAWSOPEN_EAS_SERVICE/rest/update",
                    resp,
                    False,
                    True,
                )
            elif resp.status_code == 403:
                print(
                    f"[<d><r>IPAWS</r></d>] <d>Alert has Expired. Ignoring.<d>"
                )
            else:
                num = num + 1
                print(
                    f"[<d><r>IPAWS</r></d>] <d>Alert Fetch Failed. (<r>{str(resp.status_code)}</r>)</d> ({str(num)})"
                )
            return None
    except ConnectionError:
        num = num + 1
        print(f"[<d><r>IPAWS</r></d>] <d>Alert Fetch Failed.</d> ({str(num)})")
    except Timeout:
        num = num + 1
        print(
            f"[<d><r>IPAWS</r></d>] <d>Server is slow to respond. Please check your network connection.</d> ({str(num)})"
        )
    except Exception as e:
        print(f"[<r>IPAWS</r>] <v>FATAL ERROR: {str(e)}</v>")


def getCap(url1):
    global NWSHold
    global NWSHold2
    global num
    NWS = False
    global OldAlertListNWS
    try:
        ALERT_URL = str(url1.split("://")[1].split("/")[0])
        if "api.weather.gov" in url1:
            if accnt["nws"] == True:
                if NWSHold2:
                    print("[<g>NWS</g>] NWS Polling has been enabled.")
                NWSHold2 = False
                if "?zone=" in url1 or "&zone=" in url1:
                    NWSHold = False
                    resp = []
                    NWSAlerts = []
                    alerts = get(url1, headers=UAheader, timeout=5).json()[
                        "features"
                    ]
                    try:
                        currentIdents = []
                        for feature in alerts:
                            NWSAlerts.append(feature["id"])
                        for alert in NWSAlerts:
                            if debug:
                                print(f"[<e>DEV</e>] NWS Alert {alert}")
                            currentIdents.append(
                                alert.split("://")[1].split("/")[-1]
                            )
                            resp.append(
                                get(
                                    alert,
                                    headers={
                                        "accept": "application/cap+xml",
                                        "user-agent": UserAgent,
                                    },
                                    timeout=5,
                                )
                            )
                        for i in OldAlertListNWS:
                            if i in currentIdents:
                                pass
                            else:
                                if debug:
                                    print(
                                        f"[<e>NWS</e>] Removing old alert {i} from internal buffer..."
                                    )
                                OldAlertListNWS.pop(OldAlertListNWS.index(i))
                        NWS = True
                    except IndexError:
                        return None
                else:
                    if NWSHold != True:
                        print(
                            f'[<d><r>NWS</r></d>] <d>National NWS CAP has been disabled. Use the "Zone" Tag. Ignored.<d>'
                        )
                    NWSHold = True
            else:
                if not NWSHold2:
                    print(
                        "[<yellow>NWS</yellow>] NWS Polling has been disabled on your instance, or you do not have an NWS License. Except I removed licensing. So..."
                    )
                    NWSHold2 = True
                resp = []
        else:
            resp = ""
            resp = get(url1, headers=UAheader, timeout=5)
        printCAP = "CAP" if not NWS else "NWS"
        if isinstance(resp, list):
            for alrt in resp:
                if alrt.status_code == 200:
                    resp = str(alrt.content.decode("utf-8"))
                    parseCap(url1, resp, NWS, False)
                elif (
                    alrt.status_code == 404 and "api.weather.gov" in ALERT_URL
                ):
                    if debug:
                        print(
                            f"[<e>DEV</e>] NWS Alert failed for URL {alrt.url}"
                        )
                else:
                    num = num + 1
                    if debug:
                        print(
                            f"[<e>DEV</e>] NWS Alert failed for URL {alrt.url}"
                        )
                    print(
                        f"[<d><r>{printCAP}</r></d>] <d>Alert Fetch Failed on server <i>{ALERT_URL}</i>. (<r>{str(alrt.status_code)}</r>)</d> ({str(num)})"
                    )
            return None
        else:
            if resp.status_code == 200:
                resp = str(resp.content.decode("utf-8"))
                parseCap(url1, resp, NWS, False)
            elif resp.status_code == 404 and "api.weather.gov" in ALERT_URL:
                if debug:
                    print(f"[<e>DEV</e>] NWS Alert failed for URL {resp.url}")
            else:
                num = num + 1
                if debug:
                    print(f"[<e>DEV</e>] NWS Alert failed for URL {resp.url}")
                print(
                    f"[<d><r>{printCAP}</r></d>] <d>Alert Fetch Failed on server <i>{ALERT_URL}</i>. (<r>{str(resp.status_code)}</r>)</d> ({str(num)})"
                )
            return None
    except ConnectionError:
        num = num + 1
        print(
            f"[<d><r>CAP</r></d>] <d>Alert Fetch Failed on server <i>{ALERT_URL}</i>.</d> ({str(num)})"
        )
    except Timeout:
        num = num + 1
        print(
            f"[<d><r>CAP</r></d>] <d>Server <i>{ALERT_URL}</i> is slow to respond. Please check your network connection.</d> ({str(num)})"
        )
    except Exception as e:
        print(f"[<r>CAP</r>] <v>FATAL ERROR: {str(e)}</v>")


def parseCap(url1, resp, NWS, IPAWS):
    global oldAlert
    global OldAlertListNWS
    global alerts
    eventCode = ""
    sameCodes = []
    startTime = ""
    endTime = ""
    details = ""
    instructions = ""
    Audio = None
    dRef = None
    OrgCode = None
    identifier = ""
    thing1234 = False
    hours = 0
    minutes = 0
    global beep
    ALERT_URL = str(url1.split("://")[1].split("/")[0])
    printCAP = (
        "CAP" if not NWS and not IPAWS else "NWS" if not IPAWS else "IPAWS"
    )
    with open("Static/filterFile.json", "r") as f:
        wList = load(f)["setFilters"]
        f.close()
    try:
        element = ET.fromstring(resp)
        for child in element:
            try:
                child.tag = child.tag.split("}")[1]
            except:
                pass
            if child.tag == "identifier":
                identifier = str(child.text)
                if debug and debugThread:
                    print(f"[<e>DEV</e>] Identifer is {identifier}.")
                if NWS:
                    if identifier in OldAlertListNWS:
                        return None
                    else:
                        OldAlertListNWS.append(identifier)
                else:
                    if oldAlert[URL.index(url1)] == identifier:
                        return None
                    oldAlert[URL.index(url1)] = identifier
            elif child.tag == "sent":
                startTime = str(child.text)
            elif child.tag == "msgType":
                if str(child.text) == "Cancel":
                    print(
                        f"[<d><r>{printCAP}</r></d>] <d>Alert is a Cancellation. Ignoring. ({ALERT_URL})</d>"
                    )
                    return None
            elif child.tag == "status":
                status = str(child.text)
                for stat in Config["Status"]:
                    if status == stat:
                        thing1234 = True
            elif child.text == None or child.text.strip(" ").startswith("\n"):
                if (
                    child.tag == "info"
                    and child[0].text.lower() == str(Config["Lang"]).lower()
                ):
                    for item in child:
                        try:
                            item.tag = item.tag.split("}")[1]
                        except:
                            pass
                        if item.tag == "description":
                            details = item.text
                        elif item.tag == "instruction":
                            instructions = item.text
                        elif item.tag == "expires":
                            endTime = item.text
                        elif item.tag == "parameter":
                            if item[0].text == "EAS-ORG":
                                OrgCode = item[1].text
                        elif item.tag == "resource":
                            for i in item:
                                if i.tag.split("}")[1] == "derefUri":
                                    dRef = i.text
                                elif i.tag.split("}")[1] == "uri":
                                    Audio = i.text
                                else:
                                    pass
                        try:
                            if item.text == None or item.text.strip(
                                " "
                            ).startswith("\n"):
                                for thing in item:
                                    try:
                                        thing.tag = thing.tag.split("}")[1]
                                    except:
                                        pass
                                    if item.tag == "eventCode":
                                        if thing.tag == "value":
                                            eventCode = str(thing.text).strip()
                                            # Let's give the NWS a big thanks for this code block!
                                            if eventCode.startswith("FA"):
                                                eventCode = (
                                                    "FL" + eventCode[-1]
                                                )
                                            elif eventCode.startswith("TOW"):
                                                eventCode = "TOR"
                                            elif eventCode.startswith("SVW"):
                                                eventCode = "SVR"
                                            # Sometimes, You just wanna... Hurt someone, ya know?
                                    elif thing.tag == "geocode":
                                        num = 0
                                        for i in thing:
                                            num = num + 1
                                            if i.text == "SAME":
                                                if (
                                                    thing[num].text
                                                    in sameCodes
                                                ):
                                                    pass
                                                else:
                                                    sameCodes.append(
                                                        thing[num].text
                                                    )
                        except:
                            sameCodes = []
                elif (
                    child.tag == "info"
                    and child[0].text.lower() != str(Config["Lang"]).lower()
                ):
                    print(
                        f"[<d><r>{printCAP}</r></d>] <d>Language is not supported. ({ALERT_URL})</d>"
                    )
        startTime = _ts_parse(startTime)
        endTime = _ts_parse(endTime)
        currentTime = datetime.utcnow()
        JJJHHMM = (
            str(startTime.strftime("%j")).zfill(3)
            + str(startTime.hour).zfill(2)
            + str(startTime.minute).zfill(2)
        )
        num1 = mktime(startTime.timetuple())
        num2 = mktime(endTime.timetuple())
        num3 = int(num2 - num1)
        minutes = int(num3 / 60)
        while minutes >= 60:
            minutes = minutes - 60
            hours = hours + 1
        if hours <= 0:
            if minutes <= 15:
                minutes = 15
            elif minutes > 15 and minutes <= 30:
                minutes = 30
            elif minutes > 30 and minutes <= 45:
                minutes = 45
            else:
                minutes = 0
                hours = 1
        else:
            if minutes <= 30 and minutes > 0:
                minutes = 30
            elif minutes > 30:
                minutes = 0
                hours = hours + 1
        TTTT = str(hours).zfill(2) + str(minutes).zfill(2)
        preamble = ""
        if "tdl.apps.fema.gov" in url1:
            cs = "IPAWSTDL"
            if OrgCode == "None" or OrgCode == None:
                OrgCode = "EAS"
        elif "apps.fema.gov" in url1:
            cs = "IPAWSCAP"
            if OrgCode == "None" or OrgCode == None:
                OrgCode = "CIV"
        elif "api.weather.gov" in url1:
            cs = "NOAA/CAP"
            if OrgCode == "None" or OrgCode == None:
                OrgCode = "WXR"
        else:
            if OrgCode == "None" or OrgCode == None:
                OrgCode = Config["ENCOrg"]
                print(
                    f"[<d><e>{printCAP}</e></d>] <d>No ORG Code provided, using Default. ({ALERT_URL})</d>"
                )
            cs = str(Config["ENCCall"])[:8].ljust(8, " ")
        if len(sameCodes) <= 32:
            pass
        else:
            sameCodes = sameCodes[:31]
            print(
                f"[<d><e>{printCAP}</e></d>] <d>Headers truncated from {len(sameCodes)} to 31. ({ALERT_URL})</d>"
            )
        beep = f'ZCZC-{str(OrgCode)}-{str(eventCode)}-{"-".join(sameCodes)}+{str(TTTT)}-{str(JJJHHMM)}-{cs}-'
        EASProtocol = preamble + beep
        TextData = str(details)
        InstData = str(instructions)
        with open("Static/capAlerts.json", "r") as f:
            alerts = load(f)
            f.close()
        if [status, identifier, str(beep), ALERT_URL] in alerts["cap"]:
            print(
                f"[<d><r>{printCAP}</r></d>] <d>Alert Already Processed. Ignoring. ({ALERT_URL})</d>"
            )
            return None
        elif [status, not identifier, str(beep), ALERT_URL] in alerts["cap"]:
            print(
                f"[<d><r>{printCAP}</r></d>] <d>Possible Duplicate Alert Detected. Ignoring. ({ALERT_URL})</d>"
            )
            dumpCap(status, identifier, beep, url1)
            with open(
                f'CAP_Alerts/{identifier.replace(" ", "_").replace("/", "_").replace(":", "_")}.xml',
                "wb",
            ) as f:
                ET.ElementTree(element).write(f, encoding="utf-8")
            return None
        elif [status, identifier, str(beep), not ALERT_URL] in alerts["cap"]:
            print(
                f"[<d><r>{printCAP}</r></d>] <d>Duplicate Alerts Detected. Ignoring. ({ALERT_URL})</d>"
            )
            if not [status, identifier, str(beep), ALERT_URL] in alerts["cap"]:
                dumpCap(status, identifier, beep, url1)
                with open(
                    f'CAP_Alerts/{identifier.replace(" ", "_").replace("/", "_").replace(":", "_")}.xml',
                    "wb",
                ) as f:
                    ET.ElementTree(element).write(f, encoding="utf-8")
            return None
        elif [not status, identifier, str(beep), ALERT_URL] in alerts["cap"]:
            print(
                f"[<b><g>{printCAP}</g></b>] <b>New Alert Update Recieved, Checking...</b> <d>({ALERT_URL})</d>"
            )
            pass
        elif eventCode in [None, "None", "none"]:
            print(
                f"[<d><r>{printCAP}</r></d>] <d>No Event Code Provided in Alert. Ignoring. ({ALERT_URL})</d>"
            )
            dumpCap(status, identifier, beep, url1)
            with open(
                f'CAP_Alerts/{identifier.replace(" ", "_").replace("/", "_").replace(":", "_")}.xml',
                "wb",
            ) as f:
                ET.ElementTree(element).write(f, encoding="utf-8")
            return None
        elif sameCodes in [None, "None", "none", ["None"], []]:
            print(
                f"[<d><r>{printCAP}</r></d>] <d>No SAME Codes Provided in Alert. Ignoring. ({ALERT_URL})</d>"
            )
            dumpCap(status, identifier, beep, url1)
            return None
        elif thing1234 != True:
            print(
                f"[<d><r>{printCAP}</r></d>] <d>Alert Status Not to be Relayed. Ignoring. ({ALERT_URL})</d>"
            )
            dumpCap(status, identifier, beep, url1)
            with open(
                f'CAP_Alerts/{identifier.replace(" ", "_").replace("/", "_").replace(":", "_")}.xml',
                "wb",
            ) as f:
                ET.ElementTree(element).write(f, encoding="utf-8")
            return None
        elif currentTime > endTime:
            try:
                if Config["IgnoreExpired"]:
                    print(
                        f"[<d><r>{printCAP}</r></d>] <d>Sending EXPIRED ALERTS Enabled. (Bad Idea!) ({ALERT_URL})</d>'"
                    )
                    send = True
                else:
                    send = False
            except KeyError:
                send = False
            if not send:
                print(
                    f"[<d><r>{printCAP}</r></d>] <d>Recieved Alert has Expired. Ignoring. ({ALERT_URL})</d>"
                )
                dumpCap(status, identifier, beep, url1)
                with open(
                    f'CAP_Alerts/{identifier.replace(" ", "_").replace("/", "_").replace(":", "_")}.xml',
                    "wb",
                ) as f:
                    ET.ElementTree(element).write(f, encoding="utf-8")
                return None
        if Config["BlockUnknownEventCodes"]:
            try:
                if eventCode in Extras.stats["EVENTS"]:
                    pass
                else:
                    print(
                        f"[<d><r>{printCAP}</r></d>] <d>Blocking unknown event code '{eventCode}'. ({ALERT_URL})</d>"
                    )
                    dumpCap(status, identifier, beep, url1)
                    logAlert.append(
                        [
                            EAS2Text(EASProtocol).EASText,
                            TextData,
                            InstData,
                            EASProtocol,
                            identifier,
                            None,
                            url1,
                            "Logged",
                            f"Unknown EAS Code - ALERT IGNORED",
                        ]
                    )
                    return None
            except:
                print(
                    f"[<d><r>{printCAP}</r></d>] <d>Blocking unknown event code '{eventCode}'. ({ALERT_URL})</d>"
                )
                dumpCap(status, identifier, beep, url1)
                logAlert.append(
                    [
                        EAS2Text(EASProtocol).EASText,
                        TextData,
                        InstData,
                        EASProtocol,
                        identifier,
                        None,
                        url1,
                        "Logged",
                        f"Unknown EAS Code - ALERT IGNORED",
                    ]
                )
                return None
        print(
            f"[<b><g>{printCAP}</g></b>] <b>New Valid Alert! Sending.</b> <d>({ALERT_URL})</d>"
        )
        dumpCap(status, identifier, beep, url1)
        with open(
            f'CAP_Alerts/{identifier.replace(" ", "_").replace("/", "_").replace(":", "_")}.xml',
            "wb",
        ) as f:
            ET.ElementTree(element).write(f, encoding="utf-8")
        AudioStat = "This Alert is using TTS-Generate Audio Locally."
        if Audio != None:
            AudioStat = "This Alert is using URL Provided Audio."
        elif dRef != None:
            AudioStat = "This Alert is using Base64 Provided Audio"
        print(
            f"[<b><g>{printCAP}</g></b>] New Alert Data: \n[<b><g>{printCAP}</g></b>]  -  {str(EASProtocol)}  {identifier}\n[<b><g>{printCAP}</g></b>]  -  {AudioStat}"
        )
        for i in range(len(wList)):
            if (
                (
                    (OrgCode in wList[i]["Originators"])
                    or ("*" in wList[i]["Originators"])
                )
                and (
                    (eventCode in wList[i]["EventCodes"])
                    or ("*" in wList[i]["EventCodes"])
                )
                and (
                    (
                        True
                        in [
                            (code in wList[i]["SameCodes"])
                            for code in sameCodes
                        ]
                    )
                    or (
                        True
                        in [
                            ("*" in wList[i]["SameCodes"])
                            for code in sameCodes
                        ]
                    )
                )
            ):
                print(
                    f'[<e>FILTERS</e>] MATCHED FILTER: {str(wList[i]["Name"])}'
                )
                resp, act = wList[i]["Action"].split(":")
                print(f"[<e>FILTERS</e>] Filter Action: {resp}")
                if resp.lower() == "relay":
                    if act.lower() == "forced":
                        print(
                            f"\n[<v>FILTERS</v>]  <v>*** ALERT - ALERT - ALERT ***\n[<e>FILTERS</e>]  *** INCOMING ALERT IS OF EXTREME IMPORTANCE! ***</v>\n\n"
                        )
                        print(
                            f"[<b><g>{printCAP}</g></b>] <b>*** Alert Valid. Sending. ***</b>"
                        )
                        currentAlert.append(
                            [
                                str(EASProtocol),
                                TextData,
                                InstData,
                                Audio,
                                dRef,
                                identifier,
                                NWS,
                                url1,
                                str(wList[i]["Name"]),
                            ]
                        )
                        return None
                    elif act.lower() == "now":
                        print(f"[<e>FILTERS</e>] Sending Alert NOW.")
                        print(
                            f"[<b><g>{printCAP}</g></b>] <b>*** Alert Valid. Sending. ***</b>"
                        )
                        currentAlert.append(
                            [
                                str(EASProtocol),
                                TextData,
                                InstData,
                                Audio,
                                dRef,
                                identifier,
                                NWS,
                                url1,
                                str(wList[i]["Name"]),
                            ]
                        )
                        return None
                    else:
                        try:
                            timeout = int(act)
                            if timeout > 3600:
                                timeout == 3600
                            print(
                                f"[<e>FILTERS</e>] Filter Timing out for {timeout} seconds."
                            )
                            print(
                                f"[<b><g>{printCAP}</g></b>] <b>*** Alert Valid. ***</b>"
                            )
                            print(
                                f"[<e>FILTERS</e>] Sending Alert in {str(timeout)} seconds."
                            )
                            sleep(timeout)
                            print(
                                f"[<b><g>{printCAP}</g></b>] <b>*** Sending Timed-Out Alert. ***</b>"
                            )
                            currentAlert.append(
                                [
                                    str(EASProtocol),
                                    TextData,
                                    InstData,
                                    Audio,
                                    dRef,
                                    identifier,
                                    NWS,
                                    url1,
                                    str(wList[i]["Name"]),
                                ]
                            )
                            return None
                        except ValueError:
                            print(
                                f"[<e>FILTERS</e>] Option is invalid. Treating as Ignore."
                            )
                            print(f"[<e>FILTERS</e>] Ignoring Alert.")
                            if Config["LOGEnbl"] == True:
                                logAlert.append(
                                    [
                                        EAS2Text(EASProtocol).EASText,
                                        TextData,
                                        InstData,
                                        EASProtocol,
                                        identifier,
                                        Audio,
                                        url1,
                                        "Logged",
                                        f'{str(wList[i]["Name"])} - ALERT IGNORED',
                                    ]
                                )
                            return None
                elif resp.lower() == "ignore":
                    print(f"[<e>FILTERS</e>] <d>Ignoring Alert.</d>")
                    if Config["LOGEnbl"] == True:
                        logAlert.append(
                            [
                                EAS2Text(EASProtocol).EASText,
                                TextData,
                                InstData,
                                EASProtocol,
                                identifier,
                                Audio,
                                url1,
                                "Logged",
                                f'{str(wList[i]["Name"])} - ALERT IGNORED',
                            ]
                        )
                    return None
                else:
                    print(
                        f"[<e>FILTERS</e>] <d>Invalid Action Type. Ignoring.</d>"
                    )
                    print(f"[<e>FILTERS</e>] <d>Ignoring Alert.</d>")
                    if Config["LOGEnbl"] == True:
                        logAlert.append(
                            [
                                EAS2Text(EASProtocol).EASText,
                                TextData,
                                InstData,
                                EASProtocol,
                                identifier,
                                Audio,
                                url1,
                                "Logged",
                                f'{str(wList[i]["Name"])} - ALERT IGNORED',
                            ]
                        )
                    return None
    except ET.ParseError as e:
        print(f"[<r>CAP</r>] Parse Error: {str(e)}")
        pass
    except Exception as e:
        print(f"[<r>CAP</r>] <v>FATAL ERROR: {str(e)}</v>")


def TTSGen(voice, message, ident):
    print(f"[AUDIO] Using Text To Speech Engine")
    print(f"[AUDIO] Generating TTS Message")
    if voice.lower() == "flite":
        print(f"[AUDIO] Using F-Lite KAL16 TTS Voice.")
        system(
            f'flite -voice kal16 -t "{str(message)}" -o "Output/TTS_{ident}.wav"'
        )
    elif voice.lower() == "pico":
        print(f"[AUDIO] Using PICO TTS Voice.")
        system(
            f'pico2wave --wave="Output/TTS_{ident}.wav" "{str(message).lower()}"'
        )
    elif voice.lower() == "espeak":
        print(f"[AUDIO] Using E-Speak EN-US TTS Voice.")
        system(
            f'espeak -s 150 -v EN-US -w "Output/TTS_{ident}.wav" "{str(message)}"'
        )
    else:
        print(f"[AUDIO] Using Default TTS Voice.")
        system(
            f'espeak -s 150 -v EN-US  -w "Output/TTS_{ident}.wav" "{str(message)}"'
        )
    print(f"[AUDIO] Done Generating Text To Speech")
    return


def audio():
    """Audio Thread"""
    global currentID2
    global logAlert2
    global ATTNAudioData
    global ATTNAudioData2
    global EOMAudioData
    global EOMAudioData2
    print(f"[<g>AUDIO</g>] Service Started.")
    try:
        while True:
            sleep(0.25)
            try:
                if currentAlert[0]:
                    if debug:
                        print(
                            f"[<e>DEV</e>] Alert Audio Buffer: {str(currentAlert)}."
                        )
                    print(f"[AUDIO] <i>Audio Generation Subsystem Start</i>")
                    try:
                        (
                            message,
                            messageFromIn,
                            InstData,
                            AudioLink,
                            dRef,
                            ident,
                            NWS,
                            url1,
                            filter,
                        ) = currentAlert.pop(0)
                        msgaudio = AudioSegment.empty()
                        ident = (
                            ident.replace(" ", "_")
                            .replace("/", "_")
                            .replace(":", "_")
                        )
                        messageFrom = (
                            f"{messageFromIn} {InstData}".replace('"', "")
                            .replace("'", "")
                            .replace("\n", " ")
                            .strip()
                            .lower()
                        )
                        orgText = EAS2Text(message).EASText
                        voice = str(Config["ENCTTS"])
                        freq = int(Config["ENCFREQ"])
                        print(
                            f"[<fg #FFA500>AUDIO</fg #FFA500>] <i>Generating Alert...</i>"
                        )

                        if (
                            "-RWT-" in message.upper()
                            and Config["ENCRWTAUD"] == False
                        ):
                            msgaudio = AudioSegment.silent(duration=100)
                            ATTN = False
                        else:
                            ATTN = True
                            ttshead = orgText
                            for item in StateFilter:
                                ttshead = str(
                                    ttshead.upper().replace(
                                        str(item[0].upper()),
                                        str(item[1].upper()),
                                    )
                                )
                            for item in CAPFilter:
                                ttshead = str(
                                    ttshead.lower().replace(
                                        str(item[0].lower()),
                                        str(item[1].lower()),
                                    )
                                )
                                messageFrom = str(
                                    messageFrom.replace(
                                        str(item[0].lower()),
                                        str(item[1].lower()),
                                    )
                                )
                            if NWS == True:
                                for item in NWSFilter:
                                    messageFrom = str(
                                        messageFrom.replace(
                                            str(item[0].lower()),
                                            str(item[1].lower()),
                                        )
                                    )
                            messageFrom = str(ttshead + messageFrom).upper()
                            try:
                                print(
                                    f"[<e>AUDIO</e>] CAP Text: <i>{str(messageFrom)}</i>"
                                )
                                if AudioLink == None:
                                    if dRef == None:
                                        TTSGen(voice, messageFrom, ident)
                                    else:
                                        print(
                                            f"[<e>AUDIO</e>] Using Base64 Encoded Audio"
                                        )
                                        print(
                                            f"[<fg #FFA500>AUDIO</fg #FFA500>] <i>Decoding Audio File</i>"
                                        )
                                        with open(
                                            f"Output/TTS_{ident}.mp3", "wb"
                                        ) as f:
                                            f.write(b64decode(dRef))
                                        AudioSegment.from_mp3(
                                            f"Output/TTS_{ident}.mp3"
                                        ).export(
                                            f"Output/TTS_{ident}.wav",
                                            format="wav",
                                        )
                                        print(
                                            f"[<g>AUDIO</g>] Done Decoding Audio File"
                                        )
                                else:
                                    print(
                                        f"[<e>AUDIO</e>] Using CAP Provided Audio"
                                    )
                                    print(
                                        f"[<fg #FFA500>AUDIO</fg #FFA500>] <i>Downloading...</i>"
                                    )
                                    if debug:
                                        print(
                                            f"[<e>DEV</e>] Polling Audio Link {AudioLink.strip()}."
                                        )
                                    response = get(
                                        AudioLink.strip(),
                                        headers=UAheader,
                                        timeout=5,
                                    )
                                    if debug:
                                        print(
                                            f"[<e>DEV</e>] Response {str(response.status_code)}."
                                        )
                                    if response.status_code == 200:
                                        with open(
                                            f"Output/TTS_{ident}.mp3", "wb"
                                        ) as f:
                                            f.write(response.content)
                                        AudioSegment.from_mp3(
                                            f"Output/TTS_{ident}.mp3"
                                        ).export(
                                            f"Output/TTS_{ident}.wav",
                                            format="wav",
                                        )
                                        remove(f"Output/TTS_{ident}.mp3")
                                        print(
                                            f"[<g>AUDIO</g>] Audio Downloaded Successfully."
                                        )
                                    else:
                                        print(
                                            f"[<r>AUDIO</r>] Audio Download Failed: {str(response.status_code)}"
                                        )
                                        TTSGen(voice, messageFrom, ident)
                            except Exception as e:
                                TTSGen(voice, messageFrom, ident)
                            msgaudio = effects.normalize(
                                AudioSegment.from_wav(
                                    f"Output/TTS_{ident}.wav"
                                )
                                .set_frame_rate(freq)
                                .set_channels(1)
                                .set_sample_width(2),
                                -3,
                            )
                            if msgaudio.duration_seconds > 120:
                                msgaudio = msgaudio[: 120 * 1000]
                            remove(f"Output/TTS_{ident}.wav")

                        if Config["ENCNWS"] == True or NWS == True:
                            print(
                                f"[<fg #FFA500>AUDIO</fg #FFA500>] <i>Generating Alert...</i>"
                            )
                            Alert = EASGen.genEAS(
                                header=message,
                                attentionTone=ATTN,
                                audio=msgaudio,
                                mode="NWS",
                                sampleRate=freq,
                            )
                            print(f"[<g>AUDIO</g>] Alert Generation Done.")
                        else:
                            print(
                                f"[<fg #FFA500>AUDIO</fg #FFA500>] <i>Generating Alert...</i>"
                            )
                            Alert = EASGen.genEAS(
                                header=message,
                                attentionTone=ATTN,
                                audio=msgaudio,
                                mode="SAGE",
                                sampleRate=freq,
                            )
                            print(f"[<g>AUDIO</g>] Alert Generation Done.")

                        print(f"[<e>AUDIO</e>] <i>Finishing Audio</i>")
                        Alert.export(f"Output/EAS_{ident}.wav", format="wav")
                        # Hopefully patching the Memory Leak here
                        Alert = None
                        msgaudio = None
                        dRef = None
                        print(
                            f"[<g>AUDIO</g>] <i>Audio Generation Completed</i>"
                        )
                        logAlert2.append(
                            [
                                orgText,
                                messageFromIn,
                                InstData,
                                message,
                                ident,
                                AudioLink,
                                url1,
                                "Relayed",
                                filter,
                            ]
                        )
                        currentID.append(ident)
                    except Exception as e:
                        print(f"[<r>AUDIO</r>] Exception: {str(e)}")
            except IndexError:
                pass
            except Exception as e:
                print(f"[<r>AUDIO</r>] Exception: {str(e)}")
    except Exception as e:
        print(f"[<r>AUDIO</r>] <v>FATAL ERROR: {str(e)}</v>")


def playWAV():
    global currentID
    global logAlert
    try:
        if Config["ExportEnable"]:
            print(f"[<g>EXPORTER</g>] Service Started.")
            try:
                while True:
                    sleep(0.25)
                    try:
                        if currentID[0]:
                            print(
                                f"[EXPORTER] <i>Audio Exporter Subsystem Start</i>"
                            )
                            if Config["LOGEnbl"] == True:
                                logAlert.append(logAlert2[0])
                                fucc = logAlert2[0][3]
                                del logAlert2[0]
                            wav_file = AudioSegment.from_file(
                                f"Output/EAS_{currentID[0]}.wav", format="wav"
                            )
                            print(
                                f"[<e>EXPORTER</e>] <d><i>Audio Length is {str(round(wav_file.duration_seconds, 2))} Seconds.</i></d>"
                            )
                            print(
                                f"[<fg #FFA500>EXPORTER</fg #FFA500>] <b>*** Exporting Audio. ***</b>"
                            )
                            try:
                                folder = Config["ExportFolder"]
                                alertPath = f'{folder}{"" if folder.endswith("/") else "/"}EAS_{currentID[0]}.wav'
                                wav_file.export(alertPath)
                                print(
                                    f"[<e>EXPORTER</e>] <d>Audio File Exported: {alertPath}</d>"
                                )
                                if Config["ExportToENDEC"] == True:
                                    ENDECfolder = Config["ENDECOverrideFolder"]
                                    alertPathmp3 = f'{ENDECfolder}{"" if folder.endswith("/") else "/"}ENDEC_{currentID[0]}.mp3'
                                    wav_file.export(
                                        alertPathmp3,
                                        format="mp3",
                                        tags={
                                            "artist": "capdec",
                                            "comments": fucc,
                                        },
                                    )
                                    print(
                                        f"[<e>EXPORTER</e>] <d>Audio File Exported to ENDEC for Playout</d>"
                                    )
                                beep = None
                            except KeyError:
                                print(
                                    f"[<r>EXPORTER</r>] <b>Failed to export audio.</b>"
                                )
                            print(f"[<g>EXPORTER</g>] Done Exporting Audio.")
                            encoder = str(Config["ENCWait"])
                            filelength = len(wav_file) / 1000
                            wav_file = None
                            print(
                                f"[<e>AUDIO</e>] <d>Audio File Saved: Output/EAS_{currentID[0]}.wav</d>"
                            )
                            del currentID[0]
                            if currentID != []:
                                if len(currentID) == 1:
                                    plural = ""
                                else:
                                    plural = "s"
                                print(
                                    f"[<e>EXPORTER</e>] <i><b>{str(len(currentID))}</b> New Alert{plural} Ready after Timeout.</i>"
                                )
                            if encoder.lower() == "sage":
                                print(
                                    f"[<fg #FFA500>EXPORTER</fg #FFA500>] Sleeping for <b>30</b> Seconds."
                                )
                                sleep(30)
                            elif encoder.lower() == "none":
                                print(
                                    f"[<fg #FFA500>EXPORTER</fg #FFA500>] Sleeping for <b>0</b> Seconds."
                                )
                            else:
                                print(
                                    f"[<fg #FFA500>EXPORTER</fg #FFA500>] Sleeping for <b>{str(int(filelength)+30)}</b> Seconds."
                                )
                                sleep(int(filelength) + 30)
                            print(
                                f"[<g>EXPORTER</g>] Done Sleeping. Alert Forwarding Active."
                            )
                            sleep(0.75)
                    except IndexError:
                        pass
                    except Exception as e:
                        print(f"[<r>EXPORTER</r>] Exception: {str(e)}")
            except Exception as e:
                print(f"[<r>EXPORTER</r>] <v>FATAL ERROR: {str(e)}</v>")
        else:
            print(f"[<g>PLAYER</g>] Service Started.")
            try:
                while True:
                    sleep(0.25)
                    try:
                        if currentID[0]:
                            print(
                                f"[PLAYER] <i>Audio Playback Subsystem Start</i>"
                            )
                            if Config["LOGEnbl"] == True:
                                logAlert.append(logAlert2[0])
                                del logAlert2[0]
                            wav_file = AudioSegment.from_file(
                                f"Output/EAS_{currentID[0]}.wav", format="wav"
                            )
                            print(
                                f"[<e>PLAYER</e>] <d><i>Audio Length is {str(round(wav_file.duration_seconds, 2))} Seconds.</i></d>"
                            )
                            print(
                                f"[<fg #FFA500>PLAYER</fg #FFA500>] <b>*** Playing Audio. ***</b>"
                            )
                            pdplay(wav_file + int(Config["AudioLevels"]))
                            print(f"[<g>PLAYER</g>] Done Playing Audio.")
                            encoder = str(Config["ENCWait"])
                            filelength = len(wav_file) / 1000
                            wav_file = None
                            print(
                                f"[<e>AUDIO</e>] <d>Audio File Saved: Output/EAS_{currentID[0]}.wav</d>"
                            )
                            del currentID[0]
                            if currentID != []:
                                if len(currentID) == 1:
                                    plural = ""
                                else:
                                    plural = "s"
                                print(
                                    f"[<e>PLAYER</e>] <i><b>{str(len(currentID))}</b> New Alert{plural} Ready after Timeout.</i>"
                                )
                            if encoder.lower() == "sage":
                                print(
                                    f"[<fg #FFA500>PLAYER</fg #FFA500>] Sleeping for <b>30</b> Seconds."
                                )
                                sleep(30)
                            elif encoder.lower() == "none":
                                print(
                                    f"[<fg #FFA500>PLAYER</fg #FFA500>] Sleeping for <b>0</b> Seconds."
                                )
                            else:
                                print(
                                    f"[<fg #FFA500>PLAYER</fg #FFA500>] Sleeping for <b>{str(int(filelength)+30)}</b> Seconds."
                                )
                                sleep(int(filelength) + 30)
                            print(
                                f"[<g>PLAYER</g>] Done Sleeping. Alert Forwarding Active."
                            )
                            sleep(0.75)
                    except IndexError:
                        pass
                    except Exception as e:
                        print(f"[<r>PLAYER</r>] Exception: {str(e)}")
            except Exception as e:
                print(f"[<r>PLAYER</r>] <v>FATAL ERROR: {str(e)}</v>")
    except Exception as e:
        print(f"[<r>PLAYER</r>] <v>FATAL ERROR: {str(e)}</v>")


def getIPAWSTest():
    print(f"[<g>IPAWS</g>] Service Started")
    IPAWSHold = False
    pollTime = 15
    sleep(3)
    while True:
        try:
            if Config["IPAWS"] == True and accnt["ipaws"] == True:
                if IPAWSHold:
                    print("[<g>IPAWS</g>] IPAWS Polling has been enabled.")
                    IPAWSHold = False
                getIPAWS()
                sleep(pollTime)
            elif Config["IPAWS"] == False and accnt["ipaws"] == True:
                if not IPAWSHold:
                    print(
                        f"[<yellow>IPAWS</yellow>] IPAWS Polling Disabled, Please check config."
                    )
                    IPAWSHold = True
                sleep(10)
            else:
                if not IPAWSHold:
                    print(
                        "[<yellow>IPAWS</yellow>] IPAWS Polling has been disabled on your instance, or you do not have an IPAWS License. Except I removed licensing. So..."
                    )
                    IPAWSHold = True
                sleep(10)
        except KeyboardInterrupt:
            return


def FetchCap(url, wait):
    if "apps.fema.gov" in url:
        return
    if "api.weather.gov" in url:
        logText = "NWS"
    else:
        logText = "CAP"
    print(
        f"[<g>{logText}</g>] Service Started. <d>({str(url.split('://')[1].split('/')[0])})</d>"
    )
    sleep(5)
    while True:
        try:
            getCap(url)
            if wait >= 1:
                sleep(wait)
            else:
                sleep(1)
        except KeyboardInterrupt:
            return


def devTest():
    print(f"[<g>DEBUG</g>] Service Started.")
    while not online:
        sleep(1)
    while True:
        try:
            print(f"[<e>DEBUG</e>] OLDALERT:\n[<e>DEV</e>] {oldAlert}")
            print(
                f"[<e>DEBUG</e>] OLDALERTLISTCAP:\n[<e>DEV</e>] {OldAlertListCAP}"
            )
            print(
                f"[<e>DEBUG</e>] OLDALERTLISTNWS:\n[<e>DEV</e>] {OldAlertListNWS}"
            )
            sleep(5)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    system("rm Output/TTS*.wav")
    parser = ArgumentParser(description="capenc3.4.py")
    parser.add_argument(
        "-u", "--update", help="Updates CAPDEC software.", action="store_true"
    )
    args = parser.parse_args()
    online = False
    with open("Static/config.json", "r") as f:
        Config = load(f)
        f.close()
    dev = False
    debug = False
    debugThread = False
    test = ""
    try:
        if Config["IPAWS_TEST"] == True:
            test = "tdl."
    except:
        pass
    try:
        if Config["Developer_Access_Confirmed"] == DevAccessKey:
            dev = True
    except:
        pass
    try:
        if Config["Debug"] == 1:
            debug = True
        elif Config["Debug"] == 2:
            debug = True
            debugThread = True
    except:
        pass
    cls()
    print(f"\n[<e>BOOT</e>] <d>=====</d> <i>CAPDEC BOOTING</i> <d>=====</d>")
    print(f"[<e>BOOT</e>] Version {Version}")
    print(f"[<e>BOOT</e>] Copyright 2024 MissingTextures Soft.")
    print(
        f"[<r>BOOT</r>] <y><b>Config not for Production.</b></y>"
    ) if test != "" else print(
        "", end=""
    )  ## Doing this to make the thing run
    print(
        f"[<r>BOOT</r>] <y><b>Developer Mode Enabled. No Authentication.</b></y>\n[<r>BOOT</r>] <y><b>DO NOT PUSH THIS CONFIG FILE UNDER PRODUCTION!</b></y>"
    ) if dev else print(
        "", end=""
    )  ## Doing this to make the thing run
    print(
        f"[<e>BOOT</e>] <e><b>Debug Level 1 Enabled</b></e>"
    ) if debug and not debugThread else print(
        f"[<e>BOOT</e>] <e><b>Debug Level 2 Enabled</b></e>"
    ) if debug and debugThread else print(
        "", end=""
    )  ## Doing this to make the thing run
    print(f"[<e>BOOT</e>] <d>==========================</d>\n")

    try:
        if Config["ClearOldAlerts"]:
            print(f"[<y>BOOT</y>] Clearing Old Alerts...", end="\r")
            with open("Static/capAlerts.json", "w") as f:
                f.write('{"cap": []}')
                f.close()
            oof = system("rm Output/*.wav")
            oof = system("rm CAP_Alerts/*.xml")
            print(f"[<g>BOOT</g>] Old Alerts Cleared.              \n")
    except KeyError:
        pass

    # print(f"[<y>UPDATE</y>] Checking for updates...", end="\r")
    # try:
    #     updatecheck = get(CDNUpdateLink, headers=UAheader, timeout=5)
    #     if updatecheck.text != Version:
    #         print(
    #             f"[<y>UPDATE</y>] Update to {updatecheck.text} is now available!"
    #         )
    #         if args.update == True:
    #             print("[<y>UPDATE</y>] Updating...")
    #             system(f"wget {CDNUpdaterLink} -O updater.sh")
    #             system("chmod +x updater.sh")
    #             system(f"./updater.sh {updatecheck.text}")
    #             SYSExit()
    #         else:
    #             print(
    #                 f"[<y>UPDATE</y>] To update, add -u to capdec executeable"
    #             )
    #             sleep(1)
    #     else:
    #         print(f"[<g>UPDATE</g>] CAPDEC up to date!")
    #         sleep(1)
    # except Timeout:
    #     print(f"[<r>UPDATE</r>] <d>Timeout in update. Skipping.</d>")
    # except ConnectionError:
    #     print(f"[<r>UPDATE</r>] <d>Failed to get updates.</d>")

    print(f"\n[<e>RUN</e>] <d>=====</d> <i>SERVER STARTUP</i> <d>=====</d>")
    if str(Config["PollTime"]).lower() == "fast":
        polltime = 15
    elif str(Config["PollTime"]).lower() == "slow":
        polltime = 30
    elif Extras.isInt(Config["PollTime"]):
        polltime = Config["PollTime"]
    else:
        polltime = 15
    if polltime < 5:
        print(
            f"[<r>BOOT</r>] <y><b>Polltime is not allowed lower than 5 seconds.</b></y>"
        )
        polltime = 5
    if debug:
        print(f"[<e>DEV</e>] Polltime is set to {str(polltime)} seconds.")
    try:
        if not dev:
            verifyThread = Thread(target=apiUIDExists)
            verifyThread.daemon = True
            verifyThread.start()
            while True:
                try:
                    if accnt["access"] == True:
                        print(f"[<g>AUTH</g>] Successfully Authenticated!")
                        break
                except:
                    sleep(0.1)
        else:
            print(f"[<r>AUTH</r>] <r><b>AUTHENTICATION DISABLED!</b></r>")
            accnt = DevModeAccnt
            with open("Static/capAlerts.json", "w") as f:
                f.write('{"cap": []}')
                f.close()
            print("[<e>DEV</e>] Alerts JSON file emptied.")
            sleep(0.1)
        if debugThread:
            devThread = Thread(target=devTest)
            devThread.daemon = True
            devThread.start()
            sleep(0.1)
        IPAWSThread = Thread(target=getIPAWSTest)
        audioThread = Thread(target=audio)
        playThread = Thread(target=playWAV)
        loggerThread = Thread(target=logToDiscord)
        IPAWSThread.daemon = True
        audioThread.daemon = True
        playThread.daemon = True
        loggerThread.daemon = True
        IPAWSThread.start()
        sleep(0.1)
        audioThread.start()
        sleep(0.1)
        playThread.start()
        sleep(0.1)
        if Config["LOGEnbl"] == True:
            loggerThread.start()
            sleep(0.1)
        oldAlert = [None]
        URL = [
            f"https://{test}apps.fema.gov/IPAWSOPEN_EAS_SERVICE/rest/update"
        ]
        for i in range(len(Config["URLs"])):
            if not "api.weather.gov" in str(Config["URLs"][i]):
                URL.append(str(Config["URLs"][i]))
                oldAlert.append(None)
        if Config["NWS"]:
            URL.append(
                f"https://api.weather.gov/alerts/active?severity=Extreme,Severe&zone={','.join(Config['NWSLocations'])}"
            )
            oldAlert.append(None)
        with ThreadPoolExecutor(max_workers=len(URL)) as executor:
            for i in URL:
                executor.submit(FetchCap, i, polltime)
                sleep(0.1)
            online = True
            print(
                f"\n[<e>RUN</e>] <d>=====</d> <i>CAPDEC: <g>ONLINE</g></i> <d>=====</d>"
            )
    except Exception as e:
        print(f"[<r>RUN</r>] <v>FATAL ERROR ON MAIN THREAD: {str(e)}</v>")

# CAP-Decoder Thingy.

Please note, this software is written HORRIBLY and shouldn't be used for any circumstances ever.

Don't blame me when it doesn't work, I stopped working on it 2 years ago, and everyone else 3 years.

## Initial Setup:
Installing Dependancies
```
sudo apt update
sudo apt install -y python3 python3-pip flite espeak libttspico-utils git
pip3 install pydub requests pytz soundfile discord-webhook owoify futures
```
After installing Dependancies, run
```
git clone https://github.com/A-c0rN/CAPDEC.git 
```
Then you should be able to CD into Static/ and edit config.json.
```
{
    "Status": Alert Status Tags. Read CAP API Documentation.
    "URLs": URLs to poll CAP from.
    "PollTime": Time to wait in-between CAP Polls. Set to "Fast" for 5 seconds, and "Slow" for 30. IPAWS is locked at a 15 second poll by FEMA recommendations.
    "IPAWS": true for IPAWS polling, false to disable it. Requires IPAWS license.
    "Lang": Language to use for the CAP Alert.
    "ENCOrg": Encoder Originator Code. Set to EAS by default.
    "ENCWait": If you are feeding audio into an EAS ENDEC, Put the Brand name here. E.G. SAGE, TFT, TRILITHIC
    "ENCCall": The CALLSIGN for Non-IPAWSCAP and Non-NOAACAP Servers. Cannot be longer than 8 characters.
    "ENCTTS": The Text-To-Speech server to use. Can be set to Flite, ESpeak, or Pico.
    "ENCNWS": Emulate NWS headers. For reliability, Keep false.
    "ENCRWTAUD": Enable Audio to be sent with Required Weekly Tests. Set False.
    "ENCFREQ": Encoder Bitrate. Do not change unless you know what you're doing.
    "AudioLevels": Sets the output levels. Set to 0.
    "LOGEnbl": Enable Alert Logging to Discord. Set to true. Requires Logging License.
    "LOGAud": Log Alert Audio to Discord. Requires Logging Enabled and Logging License.
    "LOGIcon": Logger Icon URL. Requires Logging Enabled and Logging License.
    "WebHooks": Discord Webhooks to log to. Feel Free to add multiple. Requires Logging Enabled and Logging License.
}

```
An example Config file should be like so:
```
{
    "Status": [
        "Actual"
    ], 
    "URLs": [
        "CAPSERVER1", 
        "CAPSERVER2",
        "CAPSERVER3"
    ],
    "PollTime": "Fast",
    "IPAWS": true,
    "Lang": "en-US",
    "ENCOrg": "EAS",
    "AudioLevels": 0,
    "ENCWait": "None",
    "ENCCall": "WACN/OOF",
    "ENCTTS": "flite",
    "ENCNWS": false,
    "ENCRWTAUD": false,
    "ENCFREQ": 24000,
    "LOGEnbl": true,
    "LOGAud": true,
    "LOGIcon": "https://LoggerIconGoesHere.com/Logger.png",
    "WebHooks": [
        "DISCORDWEBHOOKURL"
    ]
}
```
Save, and you should now be good to go!
You can run the CAPDEC by typing
```
python3 capenc3.4.py
```
or
```
./capenc3.4
```
If you're running the compiled binary.

## Features:
- [x] Poll several CAP servers at once, Including IPAWSCAP (With Key) and NWSCAP
- [x] Thread for each individual CAP server
- [x] JSON files for easy access to Alert Logs, as well as setup.
- [x] Changeable Encoder-Specific Audio Delays.
- [x] Multi-Threaded Core, Allows Polling, Audio gen, and Playback at once
- [x] Duplicate Alert Detection, and Prediction.
- [x] Alert Update support.
- [x] Adaptable Callsign Support.\*
- [x] Alert Status Check (Allows Disreguard of Low-Level Alerts)
- [x] Changeable EAS Originator Code
- [x] TTS Systems Built in, use up to 3 different voices.
- [x] Automatic Alert Description based on the SAME Headers
- [x] Customized Headers, designed to sound like old CRS Headers from the NWS. (Only if Specified)
- [x] Discord Alert Logging
- [x] Alert filtering and Verification
- [x] WAV, MP3, and Base64 Encoded Audio Support
- [x] CAP XML and Alert Audio File Logging
## Working on:
- [ ] Web Interface
## To Be Added:
- [ ] Raw EAS Decoding (Full ENDEC support) [See ASMARA](https://github.com/A-c0rN/ASMARA)

\*Callsigns default to "IPAWSCAP" and "NOAA/CAP" for the FEMA and NWS Servers, respectively.


## Known Bugs:
2. There is a bug that causes large text messages to fail to send to Discord Correctly.
5. The Timestamps for alert generation can be somewhat crazy, the reason for this has to be with the conversion from UTC to Localtime.

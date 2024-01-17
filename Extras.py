# -*- coding: utf-8 -*-

# Standard Library
import json
import time
from datetime import datetime as DT

# Third-Party
from ansimarkup import ansiprint as print
from discord_webhook import DiscordEmbed, DiscordWebhook

with open("Static/config.json", "r") as f:
    data = json.load(f)
with open("Static/EASData.json", "r") as f:
    stats = json.load(f)


def isInt(number):
    try:
        int(number)
    except ValueError:
        return False
    else:
        return True


def getTZ():
    tzone = str(time.timezone / 3600.0)
    locTime = time.localtime().tm_isdst
    TMZ = "UTC"
    if tzone == "4.0":
        TMZ = "AST"
        if locTime > 0 == True:
            TMZ = "ADT"
    elif tzone == "5.0":
        TMZ = "EST"
        if locTime > 0 == True:
            TMZ = "EDT"
    elif tzone == "6.0":
        TMZ = "CST"
        if locTime > 0 == True:
            TMZ = "CDT"
    elif tzone == "7.0":
        TMZ = "MST"
        if locTime > 0 == True:
            TMZ = "MDT"
    elif tzone == "8.0":
        TMZ = "PST"
        if locTime > 0 == True:
            TMZ = "PDT"
    return TMZ


def log(
    title,
    message,
    instruction,
    header,
    identifier,
    audio,
    AudioFile,
    server,
    status,
    filter,
    version,
    testLog,
):
    relayTime = DT.now().strftime("%m/%d/%Y at %H:%M:%S ") + getTZ()
    station = str(data["ENCCall"])
    icon = str(data["LOGIcon"])
    AudioLog = data["LOGAud"]
    try:
        lines = str(stats["EVENTS"][header.split("-")[2]])
    except:
        lines = f"an Unknown Event ({header.split('-')[2]})"
    try:
        if lines.startswith("an "):
            lines = (
                f"{str(stats['ORGS2'][header.split('-')[1]])} - {lines[3:]}"
            )
        else:
            lines = (
                f"{str(stats['ORGS2'][header.split('-')[1]])} - {lines[2:]}"
            )
    except:
        if lines.startswith("an "):
            lines = (
                f"Unknown Originator ({header.split('-')[1]}) - {lines[3:]}"
            )
        else:
            lines = (
                f"Unknown Originator ({header.split('-')[1]}) - {lines[2:]}"
            )
    if testLog and "apps.fema.gov" in server:
        lines = lines + " (IPAWS Test Server)"
        server = "IPAWS Test/Development Server"
    elif "apps.fema.gov" in server:
        server = "IPAWS Live Server"
    elif "api.weather.gov" in server:
        server = "NWS CAP Server"
    for webhook in data["WebHooks"]:
        webhooks = DiscordWebhook(url=webhook, rate_limit_retry=True)
        embed = DiscordEmbed(
            title=lines, description=status + " " + relayTime, color=0xFFA500
        )
        embed.set_author(name=station + " - CAP System Logs", icon_url=icon)
        embed.set_footer(
            text="CAP Decoder "
            + version
            + " | © 2024 MissingTextures Software"
        )
        embed.add_embed_field(name="Server:", value=server, inline=False)
        embed.add_embed_field(
            name="Matched Filter:", value=filter, inline=False
        )
        embed.add_embed_field(name="EAS Text Data:", value=title, inline=False)
        if len(message) < 700 and len(message) > 1:
            embed.add_embed_field(
                name="Alert Description:", value=message, inline=False
            )
        elif len(message) == 0:
            pass
        else:
            embed.add_embed_field(
                name="Alert Description:",
                value="Alert text too long to be sent over Discord.",
                inline=False,
            )
        if len(instruction) < 700 and len(instruction) > 1:
            embed.add_embed_field(
                name="Alert Instructions:", value=instruction, inline=False
            )
        elif len(instruction) == 0:
            pass
        else:
            embed.add_embed_field(
                name="Alert Instructions:",
                value="Alert Instructions too long to be sent over Discord.",
                inline=False,
            )
        if audio != "" and audio != None and audio != "None":
            embed.add_embed_field(
                name="CAP Audio Link:", value=audio, inline=False
            )
        embed.add_embed_field(
            name="CAP Message Identifier:", value=identifier, inline=False
        )
        embed.add_embed_field(
            name="EAS Protocol Data:", value=header.upper(), inline=False
        )
        webhooks.add_embed(embed)
        try:
            webhooks.execute()
            print(
                "[<g>LOGGER</g>] <b><g>Successfully</g></b> Posted Log to Webhook!"
            )
            if AudioLog == True and " - ALERT IGNORED" not in filter:
                webhooks = DiscordWebhook(url=webhook, rate_limit_retry=True)
                with open(AudioFile, "rb") as f:
                    webhooks.add_file(file=f.read(), filename=AudioFile)
                    f.close()
                try:
                    webhooks.execute()
                    print(
                        "[<g>LOGGER</g>] <b><g>Successfully</g></b> Posted Audio to Webhook!"
                    )
                except:
                    print(
                        "[<r>LOGGER</r>] <b><r>Failed</r></b> to send Audio to Discord, Check your connection, or webhooks."
                    )
        except:
            print(
                "[<r>LOGGER</r>] <b><r>Failed</r></b> to send Log to Discord, Check your connection, or webhooks."
            )
    return

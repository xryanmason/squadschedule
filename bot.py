# Squad Schedule
# Started on 20180509

# Imports
from __future__ import print_function
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import time
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime
from datetime import timedelta

# Setup the Calendar API
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'

PATH = "C:\\Users\olivi\OneDrive\Documents\Squad Schedule\squadschedule\\"

# Setup Discord Client and Prefix
Client = discord.Client()
bot = commands.Bot(command_prefix="#")


# Test Command
@bot.event
async def on_message(message):
    # invert this if (need to figure out how to close out of a coroutine)
    if message.author.id != bot.user.id:

        if message.content.upper().startswith('#ADDME'):
            user = message.author
            username = user.name
            newCredentialsFile = username + "_credentials.json"
            store = file.Storage(PATH + newCredentialsFile)
            creds = store.get()

            if creds:
                await bot.send_message(message.channel, "It looks like you've already been added to Squad Schedule.")

            else:
                flow = client.flow_from_clientsecrets(
                    'C:\\Users\olivi\OneDrive\Documents\Squad Schedule\squadschedule\SquadSchedule_client_secret.json',
                    SCOPES)
                creds = tools.run_flow(flow, store)

            # need to remove the service ititialization
            service = build('calendar', 'v3', http=creds.authorize(Http()))

        elif message.content.upper().startswith('#CHECKDAY'):

            arrParam = message.content.upper().split(':')
            username = arrParam[1]
            newCredentialsFile = username + "_credentials.json"
            store = file.Storage(PATH + newCredentialsFile)

            creds = store.get()

            if not creds or creds.invalid:
                await bot.send_message(message.channel,
                                       "Wow! \nOops! \nSorry! \nLooks like " + username + " hasn't been added to Squad Schedule.")
            else:
                service = build('calendar', 'v3', http=creds.authorize(Http()))
                # Call the Calendar API
                twentyFourHours = datetime.datetime.utcnow() + timedelta(days=1)
                twentyFourHours = twentyFourHours.isoformat() + 'Z'  # 'Z' indicates UTC time
                now = datetime.datetime.utcnow().isoformat() + 'Z'
                await bot.send_message(message.channel, "Let me check " + username + "'s calendar...")
                events_result = service.events().list(calendarId='primary', timeMin=now, timeMax=twentyFourHours, singleEvents=True,
                                                      orderBy='startTime').execute()
                events = events_result.get('items', [])
                # Output
                if not events:
                    await bot.send_message(message.channel, "Uh-oh... " + username + " might be lookin' for some GGs.")
                else:
                    await bot.send_message(message.channel, "Here's a look at " + username + "'s schedule for the next 24 hours:")
                    for event in events:
                        # start = event['start'].get('dateTime', event['start'].get('date'))
                        await bot.send_message(message.channel, "'" + event['summary']
                                               + "' scheduled for "
                                               + str(event['start'].get('dateTime')))

        elif message.content.upper().startswith('#CHECKWEEK'):
            arrParam = message.content.upper().split(':')
            username = arrParam[1]
            newCredentialsFile = username + "_credentials.json"
            store = file.Storage(PATH + newCredentialsFile)

            creds = store.get()

            if not creds or creds.invalid:
                await bot.send_message(message.channel,
                                       "Wow! \nOops! \nSorry! \nLooks like " + username + " hasn't been added to Squad Schedule.")
            else:
                service = build('calendar', 'v3', http=creds.authorize(Http()))
                # Call the Calendar API
                oneWeek = datetime.datetime.now() + timedelta(days=7)
                oneWeek = oneWeek.isoformat() + 'Z'  # 'Z' indicates UTC time
                now = datetime.datetime.utcnow().isoformat() + 'Z'
                await bot.send_message(message.channel, "Let me check " + username + "'s calendar...")
                events_result = service.events().list(calendarId='primary', timeMin=now, timeMax=oneWeek, singleEvents=True,
                                                      orderBy='startTime').execute()
                events = events_result.get('items', [])
                # Output
                if not events:
                    await bot.send_message(message.channel, "Uh-oh... " + username + " might be lookin' for some GGs.")
                else:
                    await bot.send_message(message.channel, "Here's a look at " + username + "'s schedule for the next week:")
                    for event in events:
                        # start = event['start'].get('dateTime', event['start'].get('date'))
                        await bot.send_message(message.channel, "'" + event['summary']
                                               + "' scheduled for "
                                               + str(event['start'].get('dateTime')))

        elif message.content.upper().startswith('#HELP'):
            await bot.send_message(message.channel, "Welcome to Squad Schedule! If you're trying to get some GGs scheduled, you've come to the right "
                  + "place. Below is the list of available commands along with a brief description and applicable "
                  + "parameters to use the commands."
                  + "\n\nHELP: Lists all of the available commands, their parameters, and a brief description. Parameters"
                  + ": none"
                  + "\n\nADDME: Adds the user to Squad Schedule so the bot can do its thang and facilitate some GGs. "
                  + "Parameters: none"
                  + "\n\nCHECKDAY: Checks the calendar of the specified user to view their schedule for the next 24 hours. "
                  + "Parameters: username of the person whose schedule you'd like to check. Example: #CHECKDAY:username"
                  + "\n\nCHECKWEEK: Works like the CHECKDAY command only it checks their schedule for the next week.")




bot.run("NDQzODg2NDQwMzA1MzkzNjg2.Dd01YA.0HlyDjH-lWHmwKuT48EU2kkrQyM")

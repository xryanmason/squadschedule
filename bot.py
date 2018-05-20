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

# Setup the Calendar API
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
store = file.Storage('C:\\Users\Ryan\Desktop\Squad Schedule\credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('C:\\Users\Ryan\Desktop\Squad Schedule\client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))

# Setup Discord Client and Prefix
Client = discord.Client()
bot = commands.Bot(command_prefix="#")

# Test Command
@bot.event
async def on_message(message):
    #Checks if the message is from the bot AND if the user said #schedule
    if message.author.id != bot.user.id and message.content.upper().startswith('#SCHEDULE'):
        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        await bot.send_message(message.channel, "Let me check the squad's schedule...")
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=1, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
    # Output
        if not events:
            await bot.send_message(message.channel, "No upcoming events found.")
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            await bot.send_message(message.channel, 'Ryan has "'
                                   + event['summary']
                                   + '" scheduled at '
                                   + (event['start'].get('dateTime', event['start'].get('date'))
                                   + ' but can probably get some ggs after. Would you like me to send him an invite?'))
# await bot.send_message(message.channel, (start, event['summary']))
# One little ID boi
bot.run("NDQzODg2NDQwMzA1MzkzNjg2.Dd01YA.0HlyDjH-lWHmwKuT48EU2kkrQyM")

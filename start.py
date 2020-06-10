#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
import json
from telethon import TelegramClient, events, sync
from telethon.extensions import html
from dotenv import load_dotenv


load_dotenv()
tags = os.getenv('TAGS').split('|')


def bot_send(text):
    requests.post(
        'https://api.telegram.org/bot' + os.getenv('BOT_API_TOKEN') + '/sendMessage',
        data={
            'chat_id': '@' + os.getenv('FINAL_CHAT_USERNAME'),
            'text': text,
            'disable_web_page_preview': True,
            'parse_mode': 'HTML'
        }
    )


telegram = TelegramClient('sessions/anonymous', os.getenv('TELEGRAM_API_KEY'), os.getenv('TELEGRAM_API_HASH'))


@telegram.on(events.NewMessage())
async def handler(event):
    print('new message')

    if event.message.reply_to_msg_id:
        print('has reply_to_msg_id')
        return

    if not hasattr(event.message.to_id, 'channel_id'):
        print('no channel_id')
        return

    chat = await telegram.get_entity(event.chat)

    if not hasattr(chat, 'username'):
        print('no username')
        return

    tag_found = False
    message_lower = event.message.message.lower()

    for tag in tags:
        if message_lower.find(tag) != -1:
            tag_found = True

    if not tag_found:
        print ('tags not found')
        return

    print('New message from @' + str(chat.username) + ' | ID: ' + str(chat.id))

    source_message = html.unparse(event.message.message, event.message.entities)
    source_link = '<a href="https://t.me/' + str(chat.username) + '/' + str(event.message.id) + \
                  '">@' + str(chat.username) + '</a>' if chat.username else chat.name
    bottom_message = 'Source: ' + source_link
    send_message = source_message + '\n\n' + bottom_message

    bot_send(send_message)


print('Connection...')
telegram.start()
print('Connection established!')
print('Listening to incoming messages...')
telegram.run_until_disconnected()

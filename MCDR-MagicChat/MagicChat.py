# -*- coding: utf-8 -*-
# v1.4.0

import re
import json

detect = False
player = ""
message = ""


def on_info(server, info):
    global detect
    global player
    global message
    if info.is_player == 1 and '%i' in info.content:
        detect = True
        player = info.player
        message = info.content
        server.execute('data get entity {} SelectedItem'.format(info.player))
    elif info.is_player == 0 and re.fullmatch(r'.* has the following entity data: .*', info.content) and detect == True:
        detect = False
        item = data_convert(info.content)
        item_name = item_name_translate(item)
        if message == '%i':
            server.execute('/tellraw @a [{"text":"[","color":"gray"},{"text":"MagicChat","color":"green"},{"text":"] ","color":"gray"},{"text":"<' + player +
                           '> ","color":"white"},{"text":"[","color":"gold"},{"translate":"item.minecraft.' + item_name + '","hoverEvent":{"action":"show_item","value":' + item + '},"color":"gold"},{"text":"]","color":"gold"}]')
        elif message.startswith('%i'):
            server.execute('/tellraw @a [{"text":"[","color":"gray"},{"text":"MagicChat","color":"green"},{"text":"] ","color":"gray"},{"text":"<' + player +
                           '> ","color":"white"},{"text":"[","color":"gold"},{"translate":"item.minecraft.' + item_name + '","hoverEvent":{"action":"show_item","value":' + item + '},"color":"gold"},{"text":"]","color":"gold"},{"text":"' + message.replace('%i', '') + '"}]')
        elif message.endswith('%i'):
            server.execute('/tellraw @a [{"text":"[","color":"gray"},{"text":"MagicChat","color":"green"},{"text":"] ","color":"gray"},{"text":"<' + player +
                           '> ","color":"white"},{"text":"' + message.replace('%i', '') + '"},{"text":"[","color":"gold"},{"translate":"item.minecraft.' + item_name + '","hoverEvent":{"action":"show_item","value":' + item + '},"color":"gold"},{"text":"]","color":"gold"}]')
        else:
            message = message.split('%i')
            if len(message) == 2:
                server.execute('/tellraw @a [{"text":"[","color":"gray"},{"text":"MagicChat","color":"green"},{"text":"] ","color":"gray"},{"text":"<' + player + '> ","color":"white"},{"text":"' +
                            message[0] + '"},{"text":"[","color":"gold"},{"translate":"item.minecraft.' + item_name + '","hoverEvent":{"action":"show_item","value":' + item + '},"color":"gold"},{"text":"]","color":"gold"},{"text":"' + message[1] + '"}]')


def item_name_translate(item_data):
    item_name = item_data.split(',')[0]
    item_name = re.findall(r"\\\"id\\\": \\\"(.+?)\\\"", item_name)[0]
    return item_name


def data_convert(item):
    item = re.sub(r'^.* has the following entity data: ', '', item)
    item = item.replace('minecraft:', '')
    item = re.sub(r'(?<=\d)[a-zA-Z](?=\D)', '', item)
    item = re.sub(r'([a-zA-Z.]+)(?=:)', '"\g<1>"', item)
    item = json.dumps(item)
    return item

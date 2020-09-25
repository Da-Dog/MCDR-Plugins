# -*- coding: utf-8 -*-
import logging
import os

Death_Msg = ""


def init_logger():
    if not os.path.exists('plugins/DeathPos'):
        os.mkdir("plugins/DeathPos")
    global logger, fileHandler
    logger = logging.getLogger('DPL')
    logger.setLevel(logging.INFO)
    fileHandler = logging.FileHandler('plugins/DeathPos/DPMessage.log', encoding='utf-8')
    fileHandler.setLevel(logging.INFO)
    fileHandler.setFormatter(
        logging.Formatter('[%(asctime)s] %(message)s',
                          datefmt='%Y-%m-%d %H:%M:%S')
    )
    logger.addHandler(fileHandler)


def on_death_message(server, message):
    global Death_Msg
    player = message.split(' ')[0]
    reason = message.split(" ", 1)[1]
    try:
        PlayerInfoAPI = server.get_plugin_instance('PlayerInfoAPI')
        pos = PlayerInfoAPI.getPlayerInfo(server, player, path='Pos')
        x = int(pos[0])
        y = int(pos[1])
        z = int(pos[2])
        dim = PlayerInfoAPI.getPlayerInfo(server, player, path='Dimension')
        dim_tran = {
            0: '§a主世界',
            -1: '§c地狱',
            1: '§6末地',
            'minecraft:overworld': '§a主世界',
            'minecraft:the_nether': '§c地狱',
            'minecraft:the_end': '§6末地'
        }

        server.say("§7[§1Death Position§f/§bINFO§7] §b玩家 §e" + player + " §b因 §e" + reason + " §b死亡 " + "死亡地点 {} §e{}§f, §e{}§f, §e{}".format(dim_tran[dim], x, y, z))
        Death_Msg = "§7[§1Death Position§f/§bHISTORY§7] §b玩家 §e" + player + " §b因 §e" + reason + " §b死亡 " + "死亡地点 {} §e{}§f, §e{}§f, §e{}".format(dim_tran[dim], x, y, z)
        if "a" in dim_tran[dim]:
            dimension = dim_tran[dim].replace('§a', '')
        elif "c" in dim_tran[dim]:
            dimension = dim_tran[dim].replace('§c', '')
        elif "6" in dim_tran[dim]:
            dimension = dim_tran[dim].replace('§6', '')
        logger.info("[Death Position/HISTORY] 玩家 '" + player + "' 因 '" + reason + "' 死亡 " + "死亡地点 '{} {}, {}, {}'".format(dimension, x, y, z))
    except:
        server.say("§7[§1Death Position§f/§bINFO§7] 无法识别玩家死亡信息")


def on_info(server, info):
    global Death_Msg
    if info.is_player == 1:
        if info.content.startswith('!!dp'):
            if Death_Msg != "":
                server.tell(info.player, Death_Msg)
            else:
                server.tell(info.player, "§7[§1Death Position§f/§cWARN§7] §b未找到玩家死亡信息")


def on_load(server, old):
    server.add_help_message('!!dp', '查看上一玩家死亡地点')
    init_logger()


def on_unload(server):
    logger.removeHandler(fileHandler)

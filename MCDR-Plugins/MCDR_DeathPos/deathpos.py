# -*- coding: utf-8 -*-
Death_Msg = ""


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

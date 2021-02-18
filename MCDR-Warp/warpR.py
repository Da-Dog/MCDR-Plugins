# coding=utf-8
import json
import time

plugin_ver = 'v0.2.0'


help_msg = '''------ §aMCDR 坐标点插件帮助信息 §f------
§b!!warp help §f- §c显示帮助消息
§b!!warp add [名称] [可选: True设为私密坐标点] §f- §c添加当前位置为坐标点
§b!!warp update [名称] §f- §c更新坐标点位置为当前位置
§b!!warp list §f- §c显示所有坐标点
§b!!warp search [名称] §f- §c搜索包含此名称的坐标点
§b!!warp del [名称] §f- §c删除包含此名称的坐标点
-----------------{}----------------'''.format(plugin_ver)

json_filename = "./plugins/warp/warp_list.json"

# 可开启坐标点传送
enable_warp_teleport = False

warp_list = {
    
}

dim_tran = {
    0: '§a主世界',
    -1: '§c地狱',
    1: '§6末地',
    'minecraft:overworld': '§a主世界',
    'minecraft:the_nether': '§c地狱',
    'minecraft:the_end': '§6末地'
}

tp_tran = {
    0: 'minecraft:overworld',
    -1: 'minecraft:the_nether',
    1: 'minecraft:overworld',
    'minecraft:overworld': 'minecraft:overworld',
    'minecraft:the_nether': 'minecraft:the_nether',
    'minecraft:the_end': 'minecraft:the_end'
}


def on_info(server, info):
    if info.is_player == 1:
        if info.content.startswith('!!warp'):
            args = info.content.split(' ')
            if len(args) == 1:
                if enable_warp_teleport == True:
                    for line in help_msg.splitlines():
                        server.tell(info.player, line)
                    server.tell(info.player, "§b!!warp tp [名称] §f- §c传送至坐标点")
                else:
                    for line in help_msg.splitlines():
                        server.tell(info.player, line)
            elif args[1] == 'help':
                if enable_warp_teleport == True:
                    for line in help_msg.splitlines():
                        server.tell(info.player, line)
                    server.tell(info.player, "§b!!warp tp [名称] §f- §c传送至坐标点")
                else:
                    for line in help_msg.splitlines():
                        server.tell(info.player, line)
            elif args[1] == 'add':
                warp_add(args, server, info)
                saveJson()
            elif args[1] == 'update':
                warp_update(args, server, info)
                saveJson()
            elif args[1] == 'list':
                warp_print(server, info)
            elif args[1] == 'search':
                warp_search(args, server, info)
            elif args[1] == 'del':
                warp_delete(args, server, info)
                saveJson()
            elif args[1] == 'tp':
                warp_teleport(server, info, args)
            else:
                server.tell(info.player, "§7[§1WARP§f/§cWARN§7] §c参数错误，请输入!!warp help 查看帮助信息")


def warp_teleport(server, info, args):
    if enable_warp_teleport == True:
        if args[2] in warp_list:
            if len(warp_list[args[2]]) == 5:
                if info.player == warp_list[args[2]][4]:
                    server.tell(info.player, "§7[§1WARP§f/§aINFO§7] §b将在3秒后传送至坐标点 {}".format(args[2]))
                    dim = warp_list[args[2]][0]
                    x = warp_list[args[2]][1]
                    y = warp_list[args[2]][2]
                    z = warp_list[args[2]][3]
                    time.sleep(3)
                    server.execute('execute in {} run tp {} {} {} {}'.format(tp_tran[dim], info.player, x, y, z))
                else:
                    server.tell(info.player, "§7[§1WARP§f/§cWARN§7] §c坐标点为私密，非创建人无法传送")
            else:
                server.tell(info.player, "§7[§1WARP§f/§aINFO§7] §b将在3秒后传送至坐标点 {}".format(args[2]))
                dim = warp_list[args[2]][0]
                x = warp_list[args[2]][1]
                y = warp_list[args[2]][2]
                z = warp_list[args[2]][3]
                time.sleep(3)
                server.execute('execute in {} run tp {} {} {} {}'.format(tp_tran[dim], info.player, x, y, z))
        else:
            server.tell(info.player, "§7[§1WARP§f/§cWARN§7] §c坐标点不存在")
    else:
        server.tell(info.player, "§7[§1WARP§f/§cWARN§7] §c服务器未开启坐标点传送")


# 删除坐标点
def warp_delete(args, server, info):
    if len(args) == 3:
        if args[2] in warp_list:
            if len(warp_list[args[2]]) == 5:
                    if warp_list[args[2]][4] == info.player:
                        del warp_list[args[2]]
                        server.tell(info.player, "§7[§1WARP§f/§aINFO§7] §b成功删除坐标点 §e{}".format(args[2]))
                    else:
                        server.tell(info.player, "§7[§1WARP§f/§cWARN§7] §c私密坐标点，只有创建人可以操作")
            else:
                del warp_list[args[2]]
                server.tell(info.player, "§7[§1WARP§f/§aINFO§7] §b成功删除坐标点 §e{}".format(args[2]))
        else:
            server.tell(info.player, "§7[§1WARP§f/§cWARN§7] §c未找到坐标名，请检查拼写")
    else:
        server.tell(info.player, "§7[§1WARP§f/§cWARN§7] §c参数错误，请输入您要删除的坐标名")

# 搜索坐标点
def warp_search(args, server, info):
    i = 0
    if len(args) == 3:
        server.tell(info.player, "§7[§1WARP§f/§aSEARCH§7] §b含有关键词 §e{} 的坐标有: ".format(args[2]))
        for key in warp_list.keys():
            if args[2] in key:
                i = 1
                if len(warp_list[key]) == 5:
                    if warp_list[key][4] == info.player:
                        server.tell(info.player, "§7[§1WARP§f/§aSEARCH§7] §b私密坐标点: §e{} §b坐标: §r{} §e{}§b, §e{}§b, §e{}".format(key, dim_tran[warp_list[key][0]], warp_list[key][1], warp_list[key][2], warp_list[key][3]))
                elif len(warp_list[key]) == 4:
                    server.tell(info.player, "§7[§1WARP§f/§aSEARCH§7] §b坐标点: §e{} §b坐标: §r{} §e{}§b, §e{}§b, §e{}".format(key, dim_tran[warp_list[key][0]], warp_list[key][1], warp_list[key][2], warp_list[key][3]))
        if i == 1:
            i = 0
        else:
            server.tell(info.player, "§7[§1WARP§f/§aINFO§7] §b呀，啥都没有")
    else:
        server.tell(info.player, "§7[§1WARP§f/§cWARN§7] §c参数错误，请输入需要查找的坐标名")


# 打印坐标点
def warp_print(server, info):
    server.tell(info.player, "§7[§1WARP§f/§aLIST§7] §b坐标点列表")
    for key, values in warp_list.items():
        dim = values[0]
        x = values[1]
        y = values[2]
        z = values[3]
        try:
            if len(values) == 5:
                player = values[4]
                if player == info.player:
                    server.tell(info.player, "§7[§1WARP§f/§aLIST§7] §b私密坐标点: §e{} §b坐标: §r{} §e{}, {}, {}".format(key, dim_tran[dim], x, y, z))
        finally:
            if len(values) == 4:
                server.tell(info.player, "§7[§1WARP§f/§aLIST§7] §b公共坐标点: §e{} §b坐标: §r{} §e{}, {}, {}".format(key, dim_tran[dim], x, y, z))


# 更新坐标点
def warp_update(args, server, info):
    if len(args) == 3:
        if args[2] in warp_list:
            if len(warp_list[args[2]]) == 5:
                if warp_list[args[2]][4] == info.player:
                    PlayerInfoAPI = server.get_plugin_instance('PlayerInfoAPI')
                    pos = PlayerInfoAPI.getPlayerInfo(server, info.player, path='Pos')
                    x = int(pos[0])
                    y = int(pos[1])
                    z = int(pos[2])
                    dim = PlayerInfoAPI.getPlayerInfo(server, info.player, path='Dimension')
                    warp_list[args[2]] = [dim, x, y, z, info.player]
                    server.tell(info.player, "§7[§1WARP§f/§bINFO§7] §b已成功更新坐标点 §e{}".format(args[2]))
                else:
                    server.tell(info.player, "§7[§1WARP§f/§cWARN§7] §c私密坐标点，只有创建人可以操作")
            else:
                PlayerInfoAPI = server.get_plugin_instance('PlayerInfoAPI')
                pos = PlayerInfoAPI.getPlayerInfo(server, info.player, path='Pos')
                x = int(pos[0])
                y = int(pos[1])
                z = int(pos[2])
                dim = PlayerInfoAPI.getPlayerInfo(server, info.player, path='Dimension')
                warp_list[args[2]] = [dim, x, y, z]
                server.tell(info.player, "§7[§1WARP§f/§bINFO§7] §b已成功更新坐标点 §e{}".format(args[2]))
        else:
            server.tell(info.player, "§7[§1WARP§f/§cWARN§7] §c坐标点不存在，请检查拼写")
    else:
        server.tell(info.player, "§7[§1WARP§f/§cWARN§7] §c参数错误，请输入需要更新的坐标点名称")


# 添加坐标点
def warp_add(args, server, info):
    if len(args) == 3:
        if args[2] in warp_list:
            server.tell(info.player, "§7[§1WARP§f/§cWARN§7] §c坐标点已存在")
        else:
            PlayerInfoAPI = server.get_plugin_instance('PlayerInfoAPI')
            pos = PlayerInfoAPI.getPlayerInfo(server, info.player, path='Pos')
            x = int(pos[0])
            y = int(pos[1])
            z = int(pos[2])
            dim = PlayerInfoAPI.getPlayerInfo(server, info.player, path='Dimension')
            warp_list[args[2]] = [dim, x, y, z]
            server.tell(info.player, "§7[§1WARP§f/§bINFO§7] §b已成功添加坐标点 §e{}".format(args[2]))
    elif len(args) == 4:
        if args[2] in warp_list:
            server.tell(info.player, "§7[§1WARP§f/§cWARN§7] §c坐标点已存在")
        else:
            if args[3] == 'True':
                PlayerInfoAPI = server.get_plugin_instance('PlayerInfoAPI')
                pos = PlayerInfoAPI.getPlayerInfo(server, info.player, path='Pos')
                x = int(pos[0])
                y = int(pos[1])
                z = int(pos[2])
                dim = PlayerInfoAPI.getPlayerInfo(server, info.player, path='Dimension')
                warp_list[args[2]] = [dim, x, y, z, info.player]
                server.tell(info.player, "§7[§1WARP§f/§bINFO§7] §b已成功添加私密坐标点 §e{}".format(args[2]))
            else:
                server.tell(info.player, "§7[§1WARP§f/§cWARN§7] §c只能为True私密坐标点或留空公共坐标点")
    else:
        server.tell(info.player, "§7[§1WARP§f/§cWARN§7] §c参数错误，请创建坐标点的名称")


def on_load(server, old):
    global warp_list
    server.register_help_message('!!warp', '坐标点插件帮助')
    try:
        with open(json_filename) as f:
            warp_list = json.load(f, encoding='utf8')
    except:
        saveJson()


def on_unload(server):
    saveJson()

#保存字典至JSON
def saveJson():
    with open(json_filename, 'a+') as f:
        json.dump(warp_list, f, indent=4)

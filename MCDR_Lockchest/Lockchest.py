# coding=utf-8
import random
import json
import os
import re

var = 1.2

help_msg = '''------ §aMCR 箱子锁插件帮助信息 §f------
§b!!lc help §f- §c显示帮助消息
§b!!lc lock §f- §c锁定脚下的箱子
§b!!lc unlock §f- §c把钥匙放在副手解锁脚下的箱子
--------------------------------'''

no_input = '''------ §a温馨提示 §f------
§c未知指令 请输入 §b!!lc help 获取帮助
--------------------------------'''

chest_locked = '''------ §a温馨提示 §f------
§c此箱子已锁定，请把钥匙放在副手
§c输入§b!!lc unlock §c 解锁箱子后才能重新上锁
--------------------------------'''

locked = '''------ §a箱子已锁定 §f------
§c箱子已加密，请手持钥匙打开
§c箱子对应钥匙已放至副手
§c输入§b!!lc unlock §c 解锁箱子
--------------------------------'''

unlocked = '''------ §a箱子已解锁 §f------
§c箱子已解锁，钥匙已收回
§c输入§b!!lc lock §c 重新锁定箱子
--------------------------------'''

keyNotMatch = '''------ §a温馨提示 §f------
§c钥匙与箱子不匹配
§c请尝试其它钥匙
--------------------------------'''

chestNotLock = '''------ §a温馨提示 §f------
§c箱子未锁定
§c输入§b!!lc lock §c 锁定箱子
--------------------------------'''

noKeyOnOffhand = '''------ §a温馨提示 §f------
§c请先将您要解锁箱子的钥匙放在副手
§c输入§b!!lc unlock §c 解锁
--------------------------------'''

itemInOffhand = '''------ §a温馨提示 §f------
§c副手有物品，无法将钥匙递给你哦
§c请先将副手清空后重试
--------------------------------'''

notOnChest = '''------ §a温馨提示 §f------
§c未检测到脚下有箱子
§c请站在需要锁定的箱子上
--------------------------------'''

json_filename = "./plugins/Lockchest/key.json"

on_chest = False
on_chest_unlock = False

keys = {
    'Keys': [],
    'Pos': []
}


def on_info(server, info):
    global on_chest
    global on_chest_unlock
    c = str(info.content)
    PlayerInfoAPI = server.get_plugin_instance('PlayerInfoAPI')
    if info.is_player == 1:
        if info.content.startswith('!!lc'):
            args = info.content.split(' ')
            if len(args) == 1:
                for line in help_msg.splitlines():
                    server.tell(info.player, line)
            elif args[1] == 'help':
                for line in help_msg.splitlines():
                    server.tell(info.player, line)
            elif args[1] == 'lock':
                server.execute('execute at ' + info.player + 
                                ' run data get block ~ ~ ~')
                result = PlayerInfoAPI.getPlayerInfo(
                    server, info.player, path='Pos')
                x = int(result[0])
                y = int(result[1])
                z = int(result[2])
                lock_chest(server, info, x, y, z)
            elif args[1] == 'unlock':
                offhandItem = PlayerInfoAPI.getPlayerInfo(
                    server, info.player, 'Inventory[{Slot:-106b}]')
                if offhandItem is not None:
                    r = str(offhandItem).split(",")[3]
                    result = str(r).split(":")[4].replace("}", "").replace(
                        '"', "").replace("'", "").replace(" ", "")
                    pos = PlayerInfoAPI.getPlayerInfo(
                        server, info.player, path='Pos')
                    x = int(pos[0])
                    y = int(pos[1])
                    z = int(pos[2])
                    pos = str(x) + ', ' + str(y) + ', ' + str(z)
                    if pos in keys['Pos']:
                        p = keys['Pos'].index(pos)
                        k = keys['Keys'].index(result)
                        if p == k:
                            del keys['Pos'][p]
                            del keys['Keys'][k]
                            server.execute(
                                'replaceitem entity ' + info.player + ' weapon.offhand minecraft:air')
                            server.execute(
                                'execute at ' + info.player + ' run data merge block ~ ~ ~ {Lock:""}')
                            for line in unlocked.splitlines():
                                server.tell(info.player, line)
                        else:
                            for line in keyNotMatch.splitlines():
                                server.tell(info.player, line)
                    else:
                        for line in chestNotLock.splitlines():
                                server.tell(info.player, line)
                else:
                    for line in noKeyOnOffhand.splitlines():
                                server.tell(info.player, line)
            else:
                for line in no_input.splitlines():
                    server.tell(info.player, line)
    if re.findall('(?<=has the following block data: )\S+',info.content):
        if "minecraft:chest" in info.content:
            on_chest = True
            if "Lock:" in info.content:
                on_chest_unlock = False
            else:
                on_chest_unlock = True


def on_load(server, old):
    global keys
    server.add_help_message('!!lc', '箱子锁系统帮助')
    try:
        with open(json_filename) as f:
            keys = json.load(f, encoding='utf8')
    except:
        saveJson()


def if_offhanditem(server, info):
    PlayerInfoAPI = server.get_plugin_instance('PlayerInfoAPI')
    offhandItem = PlayerInfoAPI.getPlayerInfo(
        server, info.player, 'Inventory[{Slot:-106b}]')
    if offhandItem is None:
        return True
    else:
        return False


def get_pwd():
    seed = "1234567890"
    pw = []
    for i in range(8):
        pw.append(random.choice(seed))
    pwd = ''.join(pw)
    return pwd


def lock_chest(server, info, x, y, z):
    global on_chest
    global on_chest_unlock
    global keys
    Keys = keys['Keys']
    pwd = get_pwd()
    pos = str(x) + ', ' + str(y) + ', ' + str(z)
    # 判断玩家脚下方块是否为箱子
    if on_chest:
        server.tell(info.player, "正在上锁，请不要移动...")
        # 判断副手是否有物品
        if if_offhanditem(server, info):
            # 判断密码重复
            if pwd in Keys:
                lock_chest(server, info, x, y, z)
            else:
                # 判断箱子是否已上锁
                if on_chest_unlock:
                    keys['Keys'].append(pwd)
                    keys['Pos'].append(pos)
                    server.execute(
                        'execute at ' + info.player + ' run data merge block ~ ~ ~ {Lock:"' + pwd + '"}')
                    server.execute(
                        "replaceitem entity " + info.player + " weapon.offhand minecraft:tripwire_hook{display:{Name:'" + '{"text":"' + pwd + '"}' + "'}}")
                    for line in locked.splitlines():
                        server.tell(info.player, line)
                    on_chest_unlock = False
                    on_chest = False
                else: 
                    for line in chest_locked.splitlines():
                        server.tell(info.player, line)
        else:
            for line in itemInOffhand.splitlines():
                server.tell(info.player, line)
    else:
        for line in notOnChest.splitlines():
            server.tell(info.player, line)

def on_unload(server):
    saveJson()


def saveJson():
    if not os.path.exists('./plugins/Lockchest'):
        os.makedirs('./plugins/Lockchest')
    with open(json_filename, 'w') as f:
        json.dump(keys, f, indent=4)

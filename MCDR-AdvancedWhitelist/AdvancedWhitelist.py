# -*- coding: utf-8 -*-
# v0.1.7
import ruamel.yaml as yaml
import requests
import os
import re
import json

Ver = 'v0.1.7'

help_msg = '''-------- §aAdvancedWhitelist 高级白名单插件 §r--------
§b!!aw help §f- §c显示帮助消息
§b!!aw switch §f- §c开关白名单
§b!!aw sip §f- §c开关IP白名单
§b!!aw add [ID] §f- §c添加白名单
§b!!aw remove [ID] §f- §c删除白名单
§b!!aw addip [IP] §f- §c添加IP白名单
§b!!aw removeip [IP] §f- §c删除IP白名单
§b!!aw iplist §f- §cIP白名单列表
§b!!aw list §f- §c白名单列表
§b!!aw update §f- §c插件升级
§b!!aw reload §f- §c插件重载
-------- §bCurrent Version: §e{} §r--------
'''.format(Ver)

config = {
    'Whitelist_status': 'Off',
    'ip_whitelist_status': 'Off',
    'Whitelist_player': [],
    'Whitelist_IP': [],
    'Kick_reason': '§c此服务器已开启白名单，请联系管理员加入白名单',
    'admin': []
}


permission = {}


def on_player_joined(server, player):
    if config['Whitelist_status'] == 'On':
        if player not in config['Whitelist_player']:
            server.execute('kick {} {}'.format(player, '§7[§3AdvancedWhitelist§7] '+ config['Kick_reason']))
            server.say('§7[§3AW§f/§aINFO§7] 玩家因不在白名单被踢出游戏')


def command(server, info, args):
    # 帮助信息
    if len(args) == 1:
        for line in help_msg.splitlines():
            server.reply(info, line)
    elif args[1] == 'help':
        for line in help_msg.splitlines():
            server.reply(info, line)
    # ID白名单开关
    elif args[1] == 'switch':
        awswitch(server, info)
    # IP白名单开关
    elif args[1] == 'sip':
        awipswitch(server, info)
    # 添加白名单玩家
    elif args[1] == 'add':
        if len(args) == 3:
            if args[2] in config['Whitelist_player']:
                    server.reply(info, "§7[§3AW§f/§cWARN§7] §b玩家已存在白名单")
            else:
                config['Whitelist_player'].append(args[2])
                server.reply(info, "§7[§3AW§f/§aINFO§7] §b玩家 §e{} §b已加入白名单".format(args[2]))
                save_config()
        else:
            server.reply(info, "§7[§3AW§f/§cWARN§7] §b参数错误，请输入需要加入白名单的玩家")
    # 移除白名单玩家
    elif args[1] == 'remove':
        if len(args) == 3:
            if args[2] in config['Whitelist_player']:
                config['Whitelist_player'].remove(args[2])
                server.reply(info, "§7[§3AW§f/§aINFO§7] §b玩家 §e{} §b已从白名单移除".format(args[2]))
                save_config()
            else:
                server.reply(info, "§7[§3AW§f/§cWARN§7] §b此玩家不在白名单")
        else:
            server.reply(info, "§7[§3AW§f/§cWARN§7] §b参数错误，请输入需要移除白名单的玩家")
    # 增加白名单IP
    elif args[1] == 'addip':
        if len(args) == 3:
            ip_check = len(args[2].split('.'))
            if ip_check == 4:
                if args[2] in config['Whitelist_IP']:
                    server.reply(info, "§7[§3AW§f/§cWARN§7] §bIP已存在白名单")
                else:
                    config['Whitelist_IP'].append(args[2])
                    server.reply(info, "§7[§3AW§f/§aINFO§7] §bIP §e{} §b已加入白名单".format(args[2]))
                    save_config()
            else:
                server.reply(info, "§7[§3AW§f/§cWARN§7] §bIP格式错误")
        else:
            server.reply(info, "§7[§3AW§f/§cWARN§7] §b参数错误，请输入需要加入白名单的IP")
    # 移除白名单IP
    elif args[1] == 'removeip':
        if len(args) == 3:
            if args[2] in config['Whitelist_IP']:
                config['Whitelist_IP'].remove(args[2])
                server.reply(info, "§7[§3AW§f/§aINFO§7] §bIP §e{} §b已从白名单移除".format(args[2]))
                save_config()
            else:
                server.reply(info, "§7[§3AW§f/§cWARN§7] §b此IP不在白名单")
        else:
            server.reply(info, "§7[§3AW§f/§cWARN§7] §b参数错误，请输入需要移除白名单的IP")
    # ID白名单列表
    elif args[1] == 'list':
        format_list = json.dumps(config['Whitelist_player'])
        server.reply(info, "§7[§3AW§f/§aINFO§7] §b白名单玩家列表: ")
        server.reply(info, format_list)
    # IP白名单列表
    elif args[1] == 'iplist':
        format_list = json.dumps(config['Whitelist_IP'])
        server.reply(info, "§7[§3AW§f/§aINFO§7] §bIP白名单列表: ")
        server.reply(info, format_list)
    # 重载刷新配置文件
    elif args[1] == 'reload':
        server.load_plugin('AdvancedWhitelist.py')
        server.reply(info, "§7[§3AW§f/§aINFO§7] §b重载完成")
    # 插件升级
    elif args[1] == 'update':
        return_code = update()
        if return_code == True:
            server.reply(info, "§7[§3AW§f/§aINFO§7] §b更新成功，插件正在重载...")
            server.refresh_changed_plugins()
        else:
            server.reply(info, "§7[§3AW§f/§cWARN§7] §b更新失败")
    else:
        server.reply(info, "§7[§3AW§f/§cWARN§7] §b参数错误，请输入 §e!!aw help §b查看帮助信息")


def on_info(server, info):
    global config
    if config['ip_whitelist_status'] == 'On' and 'logged in with entity id' in info.content:
        player = info.content.split('[')[0]
        # 匹配玩家IP
        try:
            ip = re.findall(r"/(.+?):", info.content)[0]
        except IndexError:
            ip = re.findall(r"(.*)\[([^\[\]]*)\](.*)", info.content)[0][1]
        if ip not in config['Whitelist_IP'] and ip != 'local':
            server.execute('kick {} {}'.format(player, '§7[§3AdvancedWhitelist§7] '+ config['Kick_reason']))
            server.say('§7[§3AW§f/§aINFO§7] 玩家因不在白名单被踢出游戏')
            for i in config['admin']:
                server.execute('execute at ' + i + ' run tellraw ' + i + ' ["",{"text":"[","color":"gray"},{"text":"AW","color":"dark_aqua"},{"text":"/","color":"white"},{"text":"INFO","color":"green"},{"text":"] IP: ","color":"gray"},{"text":"' + ip + '","color":"gray","clickEvent":{"action":"run_command","value":"!!aw addip ' + ip + r'"},"hoverEvent":{"action":"show_text","contents":"§e\u70b9\u51fb\u4f7f\u6b64ip\u52a0\u5165\u767d\u540d\u5355"}}]')
    if info.content.startswith('!!aw'):
        args = info.content.split(' ')
        if info.is_player == 1:
            if server.get_permission_level(info.player) >= 3:
                command(server, info, args)
            else:
                server.reply(info, "§7[§3AW§f/§cWARN§7] §b权限不足")
        else:
            command(server, info, args)


def awipswitch(server, info):
    global config
    status = config['ip_whitelist_status']
    if status == 'Off':
        config['ip_whitelist_status'] = 'On'
        server.reply(info, "§7[§3AW§f/§aINFO§7] §b服务器IP白名单已开启，IP不在白名单将无法进入游戏")
    else:
        config['ip_whitelist_status'] = 'Off'
        server.reply(info, "§7[§3AW§f/§aINFO§7] §b服务器IP白名单已关闭，所有玩家均可进入游戏")


def awswitch(server, info):
    global config
    status = config['Whitelist_status']
    if status == 'Off':
        config['Whitelist_status'] = 'On'
        server.reply(info, "§7[§3AW§f/§aINFO§7] §b服务器白名单已开启，玩家不在白名单将无法进入游戏")
    else:
        config['Whitelist_status'] = 'Off'
        server.reply(info, "§7[§3AW§f/§aINFO§7] §b服务器白名单已关闭，所有玩家均可进入游戏")


def on_load(server, old):
    if not os.path.exists('./config/AdvancedWhitelist.yml'):
        save_config()
    read_config()


def read_config():
    global config
    with open('./config/AdvancedWhitelist.yml') as file:
        config = yaml.load(file, Loader=yaml.Loader)


def save_config():
    with open('./config/AdvancedWhitelist.yml', 'w') as file:
        save = yaml.dump(config, file)


def update():
    file = requests.get('https://raw.githubusercontent.com/Da-Dog/MCDR-AdvancedWhitelist/master/AdvancedWhitelist.py')
    if file.status_code == 200:
        with open('./plugins/AdvancedWhitelist.py', "wb") as update:
            update.write(file.content)
            return True
    else:
        return False

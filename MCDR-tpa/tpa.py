# -*- coding:utf-8 -*-
# v0.1.0
from mcdreforged.api.rtext import *
from time import sleep

request_list = {}
player_list = []

help_msg = '''------ §aMCDR TPA传送插件帮助信息 §f------
§b!!tpa §f- §c显示帮助消息
§b!!tpa <player> §f- §c发送传送请求
§b!!tpaccept §f- §c同意传送请求
§b!!tpdeny §f- §c拒绝传送请求
--------------------------------'''


def on_user_info(server, info):
    if info.content == '!!tpaccept':
        if info.player in request_list.values():
            tp_player = list (request_list.keys()) [list (request_list.values()).index (info.player)]
            server.tell(info.player, "§7[§3TPA§f/§aINFO§7] §b对方正在传送")
            server.tell(tp_player, "§7[§3TPA§f/§aINFO§7] §b对方已接受传送请求，将在3秒后传送，请不要移动")
            sleep(3)
            del request_list[tp_player]
            server.execute('tp {} {}'.format(tp_player, info.player))
        else:
            server.tell(info.player, "§7[§3TPA§f/§cWARN§7] §c无传送请求等待处理")
    elif info.content.startswith('!!tpa'):
        args = info.content.split(' ')
        if len(args) == 1:
            for line in help_msg.splitlines():
                server.tell(info.player, line)
        elif len(args) == 2:
            tp_request(server, info, args)
        else:
            server.tell(info.player, "§7[§3TPA§f/§cWARN§7] §c参数错误，请输入 §e!!tpa §c查看帮助")
    elif info.content == '!!tpcancel':
        if info.player in request_list.keys():
            another_player = request_list[info.player]
            server.tell(another_player, "§7[§3TPA§f/§aINFO§7] §b对方已取消传送请求")
            server.tell(info.player, "§7[§3TPA§f/§aINFO§7] §b传送请求已取消")
            del request_list[info.player]
        else:
            server.tell(info.player, "§7[§3TPA§f/§cWARN§7] §c无传送请求等待处理")
    elif info.content == '!!tpdeny':
        if info.player in request_list.values():
            tp_player = list (request_list.keys()) [list (request_list.values()).index (info.player)]
            server.tell(info.player, "§7[§3TPA§f/§aINFO§7] §b已拒绝传送请求")
            server.tell(tp_player, "§7[§3TPA§f/§aINFO§7] §b对方已拒绝传送请求")
            del request_list[tp_player]
        else:
            server.tell(info.player, "§7[§3TPA§f/§cWARN§7] §c无传送请求等待处理")


def tp_request(server, info, args):
    if args[1] in player_list:
        if args[1] == info.player:
            server.tell(info.player, "§7[§3TPA§f/§cWARN§7] §c请不要原地TP")
        else:
            if args[1] in request_list.values():
                server.tell(info.player, "§7[§3TPA§f/§cWARN§7] §c请稍等, 玩家正在处理另一传送请求")
            else:
                if info.player in request_list.keys():
                    server.tell(info.player, "§7[§3TPA§f/§cWARN§7] §c上一传送请求尚未处理完成")
                else:
                    server.tell(info.player, RTextList(
                        RText(' --------------------------------------\n'),
                        RText('§b传送请求已发送至玩家 §e{}\n'.format(args[1])),
                        RText('[取消传送请求]\n', color=RColor.gold).h('§b点击取消传送请求').c(RAction.run_command, '!!tpcancel'),
                        RText('--------------------------------------')
                    ))
                    request_list[info.player] = args[1]
                    server.tell(args[1], RTextList(
                        RText(' --------------------------------------\n'),
                        RText('§b   玩家 §e{} §b想传送到你身边\n\n'.format(info.player)),
                        RText('      [同意]          ', color=RColor.green).h('§b点击同意传送请求').c(RAction.run_command, '!!tpaccept'),
                        RText('[拒绝]\n', color=RColor.red).h('§b点击拒绝传送请求').c(RAction.run_command, '!!tpdeny'),
                        RText('--------------------------------------')
                    ))
    else:
        server.tell(info.player, "§7[§3TPA§f/§cWARN§7] §c玩家不在线")

def on_player_joined(server, player, Info):
    player_list.append(player)

def on_player_left(server, player):
    if player in player_list:
        player_list.remove(player)
    if player in request_list.keys():
        tell_player = request_list[player]
        server.tell(tell_player, "§7[§3TPA§f/§aINFO§7] §b玩家 §e{} §b已退出, 传送请求自动取消".format(player))
        del request_list[player]
    if player in request_list.values():
        tell_player = list (request_list.keys()) [list (request_list.values()).index (player)]
        server.tell(tell_player, "§7[§3TPA§f/§aINFO§7] §b玩家 §e{} §b已退出, 传送请求自动取消".format(player))
        del request_list[tell_player]

def on_load(server, old_module):
    server.register_help_message('!!tpa', '传送插件帮助信息')
    if old_module is not None:
        player_list = old_module.player_list

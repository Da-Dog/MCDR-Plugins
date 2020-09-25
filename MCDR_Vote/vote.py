# coding=utf-8
import json
import time

help_msg = '''------ §aMCDR 投票插件帮助信息 §f------
§b!!vote help §f- §c显示帮助消息
§b!!vote list §f- §c显示所有进行中的投票
§b!!vote add (事件名称) §e[True: 结果只对自己开放(可选)] §f- §c添加新的投票项目
§b!!vote remove (项目ID) §f- §c移除投票项目
§b!!vote result (项目ID) §f- §c查看投票项目结果
§b!!vote agree (项目ID) §f- §c赞成
§b!!vote disagree (项目ID) §f- §c反对
--------------------------------'''

json_filename = "./plugins/vote/vote_event.json"

event_list = {
    
}


def on_info(server, info):
    if info.is_player == 1:
        if info.content.startswith('!!vote'):
            args = info.content.split(' ')
            if len(args) == 1:
                for line in help_msg.splitlines():
                    server.tell(info.player, line)
            elif args[1] == 'help':
                for line in help_msg.splitlines():
                    server.tell(info.player, line)
            elif args[1] == 'list':
                server.tell(info.player, "§7[§1VOTE§f/§aLIST§7] §b进行中的投票列表")
                for key in event_list.keys():
                    server.tell(info.player, "§7[§1VOTE§f/§aLIST§7] §bID: §e{}".format(key))
            elif args[1] == 'add':
                add_event(args, server, info)
            elif args[1] == 'remove':
                remove_event(args, server, info)
            elif args[1] == 'result':
                result(args, server, info)
            elif args[1] == 'agree':
                agree_vote(args, server, info)
            elif args[1] == 'disagree':
                disagree_vote(args, server, info)
            else:
                server.tell(info.player, "§7[§1VOTE§f/§cWARN§7] §c参数错误，请输入!!vote help 查看帮助信息")


#反对投票
def disagree_vote(args, server, info):
    if len(args) == 3:  
        if args[2] in event_list:
            if info.player in event_list[args[2]][3]:
                server.tell(info.player, "§7[§1VOTE§f/§cWARN§7] §c您不能为自己的项目投票哦")
            elif info.player in event_list[args[2]]:
                server.tell(info.player, "§7[§1VOTE§f/§cWARN§7] §c您已为此项目投票，不能重复投票哦")
            else:
                event_list[args[2]][1] = event_list[args[2]][1] + 1
                event_list[args[2]].append(info.player)
                server.tell(info.player, "§7[§1VOTE§f/§aINFO§7] §b您已成功为此项目投票")
        else:
            server.tell(info.player, "§7[§1VOTE§f/§cWARN§7] §c参数错误，请求ID不存在")
    else:
        server.tell(info.player, "§7[§1VOTE§f/§cWARN§7] §c参数错误，请输入赞成的项目的ID")


# 赞成投票
def agree_vote(args, server, info):
    if len(args) == 3:  
        if args[2] in event_list:
            if info.player in event_list[args[2]][3]:
                server.tell(info.player, "§7[§1VOTE§f/§cWARN§7] §c您不能为自己的项目投票哦")
            elif info.player in event_list[args[2]]:
                server.tell(info.player, "§7[§1VOTE§f/§cWARN§7] §c您已为此项目投票，不能重复投票哦")
            else:
                event_list[args[2]][0] = event_list[args[2]][0] + 1
                event_list[args[2]].append(info.player)
                server.tell(info.player, "§7[§1VOTE§f/§aINFO§7] §b您已成功为此项目投票")
        else:
            server.tell(info.player, "§7[§1VOTE§f/§cWARN§7] §c参数错误，请求ID不存在")
    else:
        server.tell(info.player, "§7[§1VOTE§f/§cWARN§7] §c参数错误，请输入赞成的项目的ID")


# 显示结果
def result(args, server, info):
    if len(args) == 3:
        if args[2] in event_list:
            if event_list[args[2]][2] == True:
                if event_list[args[2]][3] == info.player:
                    server.tell(info.player, "§7[§1VOTE§f/§aRESULT§7] §b项目 §e{} §b截止到目前为止的票数为：".format(args[2]))
                    server.tell(info.player, "§7[§1VOTE§f/§aRESULT§7] §b赞成: §e{} 票".format(event_list[args[2]][0]))
                    server.tell(info.player, "§7[§1VOTE§f/§aRESULT§7] §b反对: §e{} 票".format(event_list[args[2]][1]))
                    server.tell(info.player, "§7[§1VOTE§f/§aINFO§7] §b可以输入!!vote remove 移除此项目")
                else:
                    server.tell(info.player, "§7[§1VOTE§f/§cWARN§7] §c非常抱歉，项目创建者禁止他人查看结果")
            else:
                server.tell(info.player, "§7[§1VOTE§f/§aRESULT§7] §b项目 §e{} §b截止到目前为止的票数为：".format(args[2]))
                server.tell(info.player, "§7[§1VOTE§f/§aRESULT§7] §b赞成: §e{} 票".format(event_list[args[2]][0]))
                server.tell(info.player, "§7[§1VOTE§f/§aRESULT§7] §b反对: §e{} 票".format(event_list[args[2]][1]))
                server.tell(info.player, "§7[§1VOTE§f/§aINFO§7] §b可以输入!!vote remove 移除此项目")
        else:
            server.tell(info.player, "§7[§1VOTE§f/§cWARN§7] §c参数错误，请求ID不存在")
    else:
        server.tell(info.player, "§7[§1VOTE§f/§cWARN§7] §c参数错误，请输入需要查看项目的ID")


# 移除投票项目
def remove_event(args, server, info):
    if len(args) == 3:
        if args[2] in event_list:
            if info.player == event_list[args[2]][3]:
                del event_list[args[2]]
                server.tell(info.player, "§7[§1VOTE§f/§bINFO§7] §b已成功移除项目 §e{}".format(args[2]))
            else:
                server.tell(info.player, "§7[§1VOTE§f/§cWARN§7] §c只有项目创建人可以删除项目")
        else:
            server.tell(info.player, "§7[§1VOTE§f/§cWARN§7] §c参数错误，请求ID不存在")
    else:
        server.tell(info.player, "§7[§1VOTE§f/§cWARN§7] §c参数错误，请输入需要删除项目的ID")


# 添加投票项目 
def add_event(args, server, info):
    if len(args) == 3:
        if args[2] in event_list:
            server.tell(info.player, "§7[§1VOTE§f/§cWARN§7] §c项目名称已存在")
        else:
            event_list['{}'.format(args[2])] = [0, 0, False, info.player]
            server.tell(info.player, "§7[§1VOTE§f/§bINFO§7] §b已成功添加项目 §e{}".format(args[2]))
    elif len(args) == 4:
        if args[3] == 'True':
            if args[2] in event_list:
                server.tell(info.player, "§7[§1VOTE§f/§cWARN§7] §c项目名称已存在")
            else:
                event_list['{}'.format(args[2])] = [0, 0, True, info.player]
                server.tell(info.player, "§7[§1VOTE§f/§bINFO§7] §b已成功添加项目 §e{} §b投票结果将对外隐藏".format(args[2]))
        else:
            server.tell(info.player, "§7[§1VOTE§f/§cWARN§7] §c参数错误，只能为True对外隐藏或对外开放")
    else:
        server.tell(info.player, "§7[§1VOTE§f/§cWARN§7] §c参数错误，请输入创建项目的名称")


# 玩家加入提醒
def on_player_joined(server, player):
    i = 0
    if event_list:
        for item in event_list:
            if player not in event_list[item] and i == 0:
                i = 1
                time.sleep(0.5)
                server.tell(player, "§7[§1VOTE§f/§bINFO§7] §b又有了新的投票项目哦，快去看看吧!")
                server.tell(player, "§7[§1VOTE§f/§bINFO§7] §b输入!!vote list 查看所有投票项目")


def on_load(server, old):
    global event_list
    server.add_help_message('!!vote', '投票系统帮助')
    try:
        with open(json_filename) as f:
            event_list = json.load(f, encoding='utf8')
    except:
        saveJson()


def on_unload(server):
    saveJson()

#保存字典至JSON
def saveJson():
    with open(json_filename, 'w') as f:
        json.dump(event_list, f, indent=4)
            

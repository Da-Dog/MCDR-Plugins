# coding=utf-8
import time
import json
import random
# 可以以_作为空格
# 游戏中可以使用&加颜色代码改变公告颜色，默认颜色为天蓝色
# 颜色代码表
# 0	黑色
# 1	深蓝色
# 2	深绿色
# 3	湖蓝色
# 4	深红色
# 5	紫色
# 6	金色
# 7	灰色
# 8	深灰色
# 9	蓝色
# a	绿色
# b	天蓝色
# c	红色
# d	粉红色
# e	黄色
# f	白色
# k	随机字符
# l	粗体
# m	删除线
# n	下划线
# o	斜体

help_msg = '''------ §aMCDR 定时公告帮助信息 §f------
§b!!ann help §f- §c显示帮助消息
§b!!ann start §f- §c停止公告
§b!!ann stop §f- §c开启公告
§b!!ann status §f- §c公告系统状态
§b!!ann timer [秒] §f- §c公告发送间隔
§b!!ann add [内容] §f- §c添加公告
§b!!ann del [编号] §f- §c删除公告
§b!!ann list §f- §c公告列表
--------------------------------'''

# 配置文件位置
json_filename = "config/ann_list.json"

# 公告前缀
Prefix = "[§e温馨提示§f] "

# 公告列表，上次服务器离线时状态
ann_list = {
    'List': [],
    'Last_Status': [False],
    'timer': [30]
}

# 玩家加入提示，默认打开
on_player_join = True


def on_load(server, old):
    global ann_list
    server.add_help_message('!!ann', '定时公告帮助')
    try:
        with open(json_filename) as f:
            ann_list = json.load(f, encoding='utf8')
    except:
        saveJson()
    if ann_list['Last_Status'][0]:
        ann_start(server)
    else:
        ann_list['Last_Status'][0] = False


# 玩家加入提示
def on_player_joined(server, player):
    if on_player_join:
        server.say("[§e温馨提示§f] §b玩家 §e{} §b加入游戏".format(player))
        server.execute('execute at @a run playsound minecraft:entity.arrow.hit_player player @a')


def on_info(server, info):
    global ann_list
    if info.is_player == 1:
        if info.content.startswith('!!ann'):
            args = info.content.split(' ')
            if server.get_permission_level(info) == 3:
                if len(args) == 1:
                    for line in help_msg.splitlines():
                        server.tell(info.player, line)
                elif args[1] == 'help':
                    for line in help_msg.splitlines():
                        server.tell(info.player, line)
                elif args[1] == 'start':
                    server.tell(info.player, "§7[§1ANN§f/§bINFO§7] §b公告系统已开启发送间隔为 §e{} §b秒/次".format(ann_list['timer']))
                    ann_list['Last_Status'][0] = True
                    ann_start(server)
                elif args[1] == 'stop':
                    if ann_list['Last_Status'][0]:
                        server.tell(info.player, "§7[§1ANN§f/§bINFO§7] §b公告系统已暂停")
                        ann_list['Last_Status'][0] = False
                    else:
                        server.tell(info.player, "§7[§1ANN§f/§cWARN§7] §b系统未开启")
                elif args[1] == 'status':
                    if ann_list['Last_Status'][0]:
                        server.tell(info.player, "§7[§1ANN§f/§bINFO§7] §b公告系统已开启, 循环间隔为 §e{} §b秒/次".format(ann_list['timer'][0]))
                    else:
                        server.tell(info.player, "§7[§1ANN§f/§bINFO§7] §b系统未开启")
                elif args[1] == 'timer':
                    if len(args) == 3:
                        num = int(args[2])
                        if isinstance(num, int):
                            ann_list['timer'][0] = args[2]
                            server.tell(info.player, "§7[§1ANN§f/§bINFO§7] §b公告发送间隔已切换为 §e{} §b秒/次".format(ann_list['timer']).replace("'", ""))
                        else:
                            server.tell(info.player, "§7[§1ANN§f/§cWARN§7] §b参数无效，请输入整数")
                    else:
                        server.tell(info.player, "§7[§1ANN§f/§cWARN§7] §b参数无效，请输入公告发送间隔")
                elif args[1] == 'add':
                    if len(args) == 3:
                        content = args[2].replace("&", "§")
                        content = content.replace("_", " ")
                        ann_list['List'].append(content)
                        server.tell(info.player, "§7[§1ANN§f/§bINFO§7] §b成功添加公告 §e" + content)
                    else:
                        server.tell(info.player, "§7[§1ANN§f/§cWARN§7] §b参数无效，请输入需要添加的公告文本")
                elif args[1] == 'del':
                    if len(args) == 3:
                        args_len = len(ann_list['List'])
                        num = int(args[2])
                        if isinstance(num, int):
                            if args_len < args[2]:
                                server.tell(info.player, "§7[§1ANN§f/§cWARN§7] §b参数无效，无法找到指定公告")
                            else:
                                ann_list['List'].pop(args[2])
                                server.tell(info.player, "§7[§1ANN§f/§cINFO§7] §b成功移除编号为 {} 的公告".format(args[2]))
                        else:
                            server.tell(info.player, "§7[§1ANN§f/§cWARN§7] §b参数无效，请输入需要移除的公告对应的编号")
                    else:
                        server.tell(info.player, "§7[§1ANN§f/§cWARN§7] §b参数无效，请输入需要移除的公告对应的编号")
                elif args[1] == 'list':
                    server.tell(info.player, "§7[§1ANN§f/§aLIST§7] 公告文本列表")
                    server.tell(info.player, "§f| §a编号 §f| §c文本 §f|")
                    for num, string in enumerate(ann_list['List'], 1):
                        server.tell(info.player, "§f|  §b{}  §f| §e{} §f|".format(num, string))
                else:
                    server.tell(info.player, "§7[§1ANN§f/§cWARN§7] §b参数无效，请输入 §e!!ann help §b查看帮助")
            else:
                server.tell(info.player, "§7[§1ANN§f/§cWARN§7] §b权限不足，无法执行操作")


def on_unload(server):
    saveJson()


def on_load(server, old):
    server.add_help_message('!!ann', '定时公告插件帮助')
    

def saveJson():
    with open(json_filename, 'w') as f:
        json.dump(ann_list, f, indent=4)


# 公告发布
def ann_start(server):
    i = 0
    while ann_list['Last_Status'][0]:
        delay = ann_list['timer'][0]
        if i < delay:
            time.sleep(1)
            i = i + 1
        else:
            ann = random.choice(ann_list['List'])
            server.say(Prefix + "§b" + ann)
            i = 0

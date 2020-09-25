# -*- coding: utf-8 -*-
# v0.1.8
from decimal import Decimal
import random
import numpy as np
import time

# AI胜率，最高20意味着AI百分百获胜
AI_win_rate = 15

# 返还率，玩家下注 * 返还率 = 玩家胜利得到的钱
return_rate = 2

help_msg = '''------ §aMCDR 21点娱乐插件帮助信息 §f------
§b!!blackjack help §f- §c显示帮助消息
§b!!blackjack play [钱] §f- §c开始游玩
------ §aMCDR 21点娱乐插件游戏规则 §f------
§b当输入 §e!!blackjack play [钱] §b时， 游戏将会开始，
§b电脑和玩家将会获得两张牌，决定要牌或跳过
§b最后牌点数加起来，点数多的一方获胜，如一方点数超过21，则判定
§b对方获胜
--------------------------------'''

vault = ""

poker_name = ['♦10', '♦2', '♦3', '♦4', '♦5', '♦6', '♦7', '♦8', '♦9', '♦A', '♦J', '♦K', '♦Q',
 '♣10', '♣2', '♣3', '♣4', '♣5', '♣6', '♣7', '♣8', '♣9', '♣A', '♣J', '♣K', '♣Q',
 '♥10', '♥2', '♥3', '♥4', '♥5', '♥6', '♥7', '♥8', '♥9', '♥A', '♥J', '♥K', '♥Q',
 '♠10', '♠2', '♠3', '♠4', '♠5', '♠6', '♠7', '♠8', '♠9', '♠A', '♠J', '♠K', '♠Q']
poker_value = {'♣A':1,'♥A':1,'♠A':1,'♦A':1,'♦10': 10, '♦2': 2, '♦3': 3, '♦4': 4, '♦5': 5, '♦6': 6, '♦7': 7, '♦8': 8, '♦9': 9,  '♦J': 10, '♦K': 10, '♦Q': 10,
 '♣10': 10, '♣2': 2, '♣3': 3, '♣4': 4, '♣5': 5, '♣6': 6, '♣7': 7, '♣8': 8, '♣9': 9,  '♣J': 10, '♣K': 10, '♣Q': 10,
 '♥10': 10, '♥2': 2, '♥3': 3, '♥4': 4, '♥5': 5, '♥6': 6, '♥7': 7, '♥8': 8, '♥9': 9,  '♥J': 10, '♥K': 10, '♥Q': 10,
 '♠10': 10, '♠2': 2, '♠3': 3, '♠4': 4, '♠5': 5, '♠6': 6, '♠7': 7, '♠8': 8, '♠9': 9,  '♠J': 10, '♠K': 10, '♠Q': 10}
poker_database = []
status = 'idle'
player = ""
hit_stand = None


def on_user_info(server, info):
    global hit_stand
    global status
    global player
    global vault
    if info.content.startswith('!!blackjack'):
        args = info.content.split(' ')
        if len(args) == 1:
            for line in help_msg.splitlines():
                server.tell(info.player, line)
        elif args[1] == 'help':
            for line in help_msg.splitlines():
                server.tell(info.player, line)
        elif args[1] == 'play':
            if len(args) == 3:
                if Decimal(args[2]) > 0:
                    if status == 'idle':
                        player = info.player
                        play_result = start_play(server, info, args)
                        if play_result == 1:
                            win = Decimal(args[2]) * return_rate
                            vault.give(info.player, Decimal(win))
                            status = 'idle'
                            server.tell(info.player, "§7[§3BLOCKJACK§f/§aINFO§7] §b你赢了, 获得了 §e{}§b, 目前账户余额 §e{}§b!".format(win, vault.check(info.player)))
                            server.logger.info("Player Win")
                        elif play_result == -1:
                            status = 'idle'
                            server.tell(info.player, "§7[§3BLOCKJACK§f/§aINFO§7] §b你输了，目前账户余额 §e{}§b!".format(vault.check(info.player)))
                            server.logger.info("Player Lose")
                        elif play_result == 0:
                            vault.give(info.player, Decimal(args[2]))
                            status = 'idle'
                            server.tell(info.player, "§7[§3BLOCKJACK§f/§aINFO§7] §b平局，下注金额已返还，目前账户余额 §e{}§b!".format(vault.check(info.player)))
                            server.logger.info("Player Draw")
                        elif play_result == None:
                            return
                        else:
                            server.tell(info.player, "§7[§3BLOCKJACK§f/§cERROR§7] §b判断系统错误，请联系管理员 code: " + str(play_result))
                            server.logger.info('money: {}, error code: {}, player: {}'.format(args[2], str(play_result), info.player))
                    else:
                        server.tell(info.player, "§7[§3BLOCKJACK§f/§cWARN§7] §b游戏进行中，请等待上局游戏结束后开始")
                else:
                    server.tell(info.player, "§7[§3BLOCKJACK§f/§cWARN§7] §b参数错误! 请不要输入小于等于0的下注金额")
            else:
                server.tell(info.player, "§7[§3BLOCKJACK§f/§cWARN§7] §b参数错误! 请输入下注金额")
        elif args[1] == 'add':
            if status == 'busy':
                if info.player == player:
                    hit_stand = True
        elif args[1] == 'skip':
            if status == 'busy':
                if info.player == player:
                    hit_stand = False
        else:
            server.tell(info.player, "§7[§3BLOCKJACK§f/§cWARN§7] §b参数错误! 请输入 §e!!blackjack help §b查看帮助")


def Judgement(your_score,pc_score):
    if your_score > 21 and pc_score > 21:
        return 0
    elif your_score > 21 and pc_score <= 21:
        return -1
    elif your_score <= 21 and pc_score > 21:
        return 1
    elif your_score <= 21 and pc_score <= 21:
        if your_score < pc_score:
            return -1
        elif your_score > pc_score:
            return 1
        else:
            return 0


def start_play(server, info, args):
    global vault
    global poker_database
    global status
    global hit_stand
    AI_win_lost = AI_decision()
    if Decimal(args[2]) <= vault.check(info.player):
        server.logger.info(Decimal(args[2]))
        remain = vault.take(info.player, Decimal(args[2]))
        server.logger.info('take money return code: ' + str(remain))
        server.tell(info.player, "§7[§3BLOCKJACK§f/§aINFO§7] §b已从账户扣取: §e{}§b, 目前账户余额为: §e{}".format(args[2], vault.check(info.player)))
        server.tell(info.player, "§7[§3BLOCKJACK§f/§aINFO§7] §b开始游戏!")
        server.tell(info.player, "§7[§3BLOCKJACK§f/§aINFO§7] §b发牌中")
        time.sleep(0.15)
        server.tell(info.player, "§7[§3BLOCKJACK§f/§aINFO§7] §b发牌中.")
        time.sleep(0.15)
        server.tell(info.player, "§7[§3BLOCKJACK§f/§aINFO§7] §b发牌中..")
        time.sleep(0.15)
        server.tell(info.player, "§7[§3BLOCKJACK§f/§aINFO§7] §b发牌中...")
        time.sleep(0.15)
        status = 'busy'
        poker_database = poker_name * 1
        random.shuffle(poker_database)
        player = []
        computer = []
        you_get = givecard_start()  
        pc_get = givecard_start()
        server.tell(info.player, "§7[§3BLOCKJACK§f/§aINFO§7] §b你的牌: §e{} {}".format(you_get[0], you_get[1]))
        server.tell(info.player, "§7[§3BLOCKJACK§f/§aINFO§7] §b电脑的牌: §e{} ?".format(pc_get[0]))
        player.extend(you_get)
        computer.extend(pc_get)
        score = np.array([Score_Count(player),Score_Count(computer)])
        while score[0] <= 21:
            hit_stand = None
            Get_New_Poker = New_Card(server, info)
            if Get_New_Poker != False:
                if Get_New_Poker != None:
                    player.append(Get_New_Poker)
                    server.tell(info.player, "§7[§3BLOCKJACK§f/§aINFO§7] §b您目前拥有的牌: §e{}".format(player))
                    score[0] = Score_Count(player)
                    if score[0] > 21:
                        server.tell(info.player, "§7[§3BLOCKJACK§f/§aINFO§7] §b超过21点，爆牌!")
                        server.tell(info.player, "§7[§3BLOCKJACK§f/§aINFO§7] §b电脑的牌 §e{}".format(computer))
                        return Judgement(score[0],score[1])
                    else:
                        continue
                else:
                    Get_New_Poker = poker_database.pop(0)
            else:
                if AI_win_lost == False:
                    while score[1] < score[0]:
                        PC_Ask_Poker = poker_database.pop(0)
                        computer.append(PC_Ask_Poker)
                        pc_score = Score_Count(computer)
                        score[1] = pc_score
                        server.tell(info.player, "§7[§3BLOCKJACK§f/§aINFO§7] §b最后电脑的牌 §e{}".format(computer))
                        return Judgement(score[0],score[1])
                        break
                else:
                    pc_score = Score_Count(computer)
                    score[1] = pc_score
                    server.tell(info.player, "§7[§3BLOCKJACK§f/§aINFO§7] §b最后电脑的牌 §e{}".format(computer))
                    return Judgement(score[0],score[1])
                    break
    else:
        server.tell(info.player, "§7[§3BLOCKJACK§f/§cWARN§7] §b您的账户余额不足!")  


def AI_decision():
    rate = random.randint(AI_win_rate, 20)
    if rate < 20:
        return True
    else:
        return False


def New_Card(server, info): 
    global poker_database
    global hit_stand
    server.tell(info.player, "§7[§3BLOCKJACK§f/§aINFO§7] §b是否继续要牌, 是: §e!!blackjack add§b, 否: §e!!blackjack skip")
    while hit_stand == None:
        time.sleep(0.1)
        if hit_stand == True:
            hit_stand = None
            return poker_database.pop(0)
        elif hit_stand == False:
            hit_stand = None
            return False
        else: pass

def givecard_start():
    global poker_database
    pop = [poker_database.pop(0), poker_database.pop(0)]
    return pop


def on_load(server, old):
    global vault
    vault = server.get_plugin_instance('vault')


def Score_Count(hand_poker):
    Ace = {'♣A','♥A','♠A','♦A'}
    Score = 0
    Have_Ace = False
    for k in hand_poker:
        Score += poker_value[k]
    for i in hand_poker:
        if i in Ace:
            Have_Ace = True
            break
        else: continue
    if Have_Ace == True:
        if Score + 10 <= 21:
            Score = Score + 10
    return Score

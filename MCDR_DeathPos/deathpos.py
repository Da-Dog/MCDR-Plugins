# -*- coding: utf-8 -*-
import json as js
import re
import csv
import os
from imp import load_source
PlayerInfoAPI = load_source('PlayerInfoAPI','./plugins/PlayerInfoAPI.py')
path='./config/Waypoints.csv'   # 路径点保存位置
permission_check=True   # 权限校验开关True/False
prefix_short='!!wp'
prefix='!!waypoints'
name=[]
x=[]
y=[]
z=[]
dimension=[]
complicated=False
help_msg='''
======== §bWaypoints §r========
§6欢迎使用由@GamerNoTitle开发的路径点插件！
§6你可以在Github搜索MCDR-Waypoints找到本项目！
本插件中§d!!wp§r与§d!!waypoints§r效果相同，两者可以互相替换
§b!!wp§r显示本帮助信息
§b!!wp list§r显示路径点列表
§b!!wp search <content>§r搜索含有指定内容名字的路径点
§b!!wp show <content>§r显示名字为指定内容的导航点信息
§b!!wp dim <dim>§r显示在主世界/地狱/末地的所有导航点（分别对应dim：0,-1,1，默认为当前维度）
§b!!wp add <name> (x) (y) (z) (Dimension) §r添加名为<name>的路径点（x,y,z指定坐标，Dimension为维度，0是主世界，-1是地狱，1是末地，非必须）
§b!!wp del <name>§r删除名为<name>的路径点（需要MCDR.helper以上权限）
§b!!wp reload§r重载路径点列表
'''
def refresh_list():
    global name,x,y,z,dimension,complicated
    database=csv.reader(path)
    name=[]
    x=[]
    y=[]
    z=[]
    dimension=[]
    file=open(path,'r',encoding='gbk')
    database=csv.reader(file)
    for i in database:
        name.append(i[0])
        x.append(i[1])
        y.append(i[2])
        z.append(i[3])
        dimension.append(i[4])
    complicated==False

def change_dim(dim):
    dimlist={
        "minecraft:overworld": 0,
        "minecraft:the_nether": -1,
        "minecraft:end": 1
    }
    try:
        changed_dim=dimlist[str(dim)]
    except:
        changed_dim=0
    return changed_dim

def create_csv(path):
    with open(path,"w+",newline='',encoding="gbk") as file:
        file.close()

def append_csv(path,data):
    with open(path,"a+",newline='',encoding="gbk") as file:
        csv_file = csv.writer(file)
        data=[data]
        csv_file.writerows(data)

def add(server,info,message):
    if len(message) == 2:
        server.reply(info, '§b[Waypoints]§4你必须输入路径点的名字！',encoding=None)
    elif len(message) == 3:
        pos,Dimension=get_pos(server,info)
        try:
            Dimension=int(Dimension)
        except:
            Dimension=change_dim(Dimension)
        x=int(list(pos)[0])
        y=int(list(pos)[1])
        z=int(list(pos)[2])
        data=[str(message[2]),str(x),str(y),str(z),str(Dimension)]
        append_csv(path,data)
        refresh_list()
        server.reply(info, '§b[Waypoints]§r导航点[name: {}, x: {}, y: {}, z: {}, dim: {}]已添加！'.format(message[2],x,y,z,Dimension),encoding=None)
    elif len(message) == 6:
        x=message[3]
        y=message[4]
        z=message[5]
        pos,Dimension=get_pos(server,info)
        try:
            Dimension=int(Dimension)
        except:
            Dimension=change_dim(Dimension)
        data=[message[2],x,y,z,Dimension]
        append_csv(path,data)
        refresh_list()
        server.reply(info, '§b[Waypoints]§r导航点[name: {}, x: {}, y: {}, z: {}, dim: {}]已添加！'.format(message[2],x,y,z,Dimension),encoding=None)
    elif len(message) == 7:
        x=message[3]
        y=message[4]
        z=message[5]
        try:
            Dimension=int(message[6])
            if Dimension>1 or Dimension<-1:
                server.reply(info,'§b[Waypoints]§4你必须输入介于-1到1之间的整数！',encoding=None)
            else:
                data=[message[2],x,y,z,Dimension]
                append_csv(path,data)
                refresh_list()
                server.reply(info, '§b[Waypoints]§r导航点[name: {}, x: {}, y: {}, z: {}, dim: {}]已添加！'.format(message[2],x,y,z,Dimension),encoding=None)
        except:
            server.reply(info,'§b[Waypoints]§4你必须输入整数！',encoding=None)
    else:
        server.reply(info, '§b[Waypoints]§4输入格式不正确！',encoding=None)    

def is_duplicated(point):
    i=0
    for i in range(len(name)):
        if point==name[i]:
            global complicated
            complicated=True

def delete(server,info,point):
    point_pos=None
    for i in range(0,len(name)):
        if point == name[i]:
            point_pos=i
    if point_pos == None:
        server.reply(info, '§b[Waypoints]§4未找到名为§d{}§4的路径点！'.format(point),encoding=None)
    else:
        for i in range(point_pos,len(name)):
            try:
                name[i] = name[i+1]
                x[i] = x[i+1]
                y[i] = y[i+1]
                z[i] = z[i+1]
                dimension[i] = dimension[i+1]
            except:
                None
        del(name[len(name)-1])
        del(x[len(x)-1])
        del(y[len(y)-1])
        del(z[len(z)-1])
        del(dimension[len(dimension)-1])
        os.remove(path)
        create_csv(path)
        for i in range(0,len(name)):
            data=[name[i],x[i],y[i],z[i],dimension[i]]
            append_csv(path,data)
        refresh_list()
        server.reply(info, '§b[Waypoints]§r名为§d{}§r的导航点已经删除！'.format(point),encoding=None)


def showdetail(server,info,point):
    is_exist=False
    for i in range(0,len(name)):
        if point == name[i]:
            is_exist=True
            detail='[name: {}, x: {}, y: {}, z: {}, dim: {}]'.format(point,x[i],y[i],z[i],dimension[i],encoding=None)
    if is_exist:
        server.reply(info, '§b[Waypoints]§r导航点§d{}§r的信息：{}'.format(point,detail),encoding=None)
        is_exist=False
    else:
        server.reply(info, '§b[Waypoints]§4未查询到名为§d{}§4的导航点的相关信息！'.format(point),encoding=None)

def showlist(server,info):
    if len(name) == 0:
        server.reply(info, '§b[Waypoints]§6导航点列表还是空荡荡的哦~',encoding=None)
    else:
        pointlist=''
        for i in range(0,len(name)):
            if i==len(name):
                pointlist=pointlist+name[i]
            else:
                pointlist=pointlist+name[i]+', '
        server.reply(info, '§b[Waypoints]§r数据库中有以下导航点： {}'.format(pointlist),encoding=None)
        server.reply(info, '§b[Waypoints]§r你可以使用§b!!wp show <name> §r来展示导航点的相关信息',encoding=None)

def search(server,info,point,dim):
    result=[]
    if dim == 'all':
        for i in range(0,len(name)):
            if str(point) in str(name[i]):
                result.append(name[i])
        if result == []:
            server.reply(info, '§b[Waypoints]§4暂时没有含有§d{}§4关键词的路径点哦~'.format(point),encoding=None)
        else:
            server.reply(info, '§b[Waypoints]§r含有关键词§d{}§r的路径点有§6{}'.format(point,result),encoding=None)
            server.reply(info, '§b[Waypoints]§r你可以使用§b!!wp show <name> §r来展示导航点的相关信息',encoding=None)
    elif int(dim) == 1 or int(dim) == -1 or int(dim) == 0:
        for i in range(0,len(name)):
            if str(point) in str(name[i]) and int(dimension[i]) == str(dim):
                result.append(name[i])
        if result == []:
            server.reply(info, '§b[Waypoints]§4暂时没有含有§d{}§4关键词的路径点哦~'.format(point),encoding=None)
        else:
            server.reply(info, '§b[Waypoints]§r含有关键词§d{}§r的路径点有§6{}'.format(point,result),encoding=None)
            server.reply(info, '§b[Waypoints]§r你可以使用§b!!wp show <name> §r来展示导航点的相关信息',encoding=None)
    else:
        server.reply(info, '§b[Waypoints]§4维度输入错误！请输入§b!!wp§r获取使用方法！',encoding=None)

def dimshow(server,info,dim):
    if int(dim) == 0:
        dimension_name = '§a主世界'
    if int(dim) == 1:
        dimension_name = '§5末地'
    if int(dim) == -1:
        dimension_name = '§c地狱'
    result=[]
    for i in range(0,len(name)):
        if int(dimension[i]) == dim:
            result.append(name[i])
    server.reply(info, '§b[Waypoints]§r在维度{}§r里共有导航点§d{}§r个，列表如下：{}'.format(dimension_name,len(result),result),encoding=None)

def on_load(server, old_module):
    refresh_list()
    server.add_help_message('!!wp', '§b获取Waypoints插件使用方法')

def get_pos(server,info):
    PlayerInfoAPI = server.get_plugin_instance('PlayerInfoAPI')
    pos=PlayerInfoAPI.getPlayerInfo(server, info.player, 'Pos')
    dim=PlayerInfoAPI.getPlayerInfo(server, info.player, 'Dimension')
    return pos,dim

def on_server_startup(server):
    if os.path.exists(path):
        refresh_list()
    else:
        create_csv(path)


def on_info(server,info):
    if info.content == '!!create':
        create_csv(path)
    if prefix in info.content or prefix_short in info.content:
        message=info.content.split()
        if info.content == prefix or info.content == prefix_short:
            server.reply(info, help_msg,encoding=None)
        elif message[0] == prefix or message[0] == prefix_short:
            if message[1] == 'add':
                global complicated
                is_duplicated(message[2])
                if complicated==True:
                    server.reply(info, '§b[Waypoints]§4名为{}的路径点已存在！'.format(message[2]),encoding=None)
                    refresh_list()
                    complicated=False
                else:
                    add(server,info,message)
            if message[1] == 'del':
                if permission_check:
                    if(server.get_permission_level(info)>2):
                        if len(message) == 2:
                            server.reply(info, '§b[Waypoints]§4你必须输入要删除的路径点名字！',encoding=None)
                        elif len(message) == 3:
                            delete(server,info,message[2])
                        else:
                            server.reply(info, '§b[Waypoints]§4输入格式不正确！',encoding=None)
                    else:
                        server.reply(info, '§b[Waypoints]§4权限不足！',encoding=None)
                else:
                    if len(message) == 2:
                        server.reply(info, '§b[Waypoints]§4你必须输入要删除的路径点名字！',encoding=None)
                    elif len(message) == 3:
                        delete(server,info,message[2])
                    else:
                        server.reply(info, '§b[Waypoints]§4输入格式不正确！',encoding=None)

            if message[1] == 'reload':
                try:
                    refresh_list()
                    server.say('§b[Waypoints]§a由玩家§d{}§a发起的Waypoints重载成功'.format(info.player),encoding=None)
                except Exception as e:
                    server.say('§b[Waypoints]§4由玩家§d{}§4发起的Waypoints重载失败：{}'.format(info.player,e),encoding=None)

            if message[1] == 'list':
                showlist(server,info)

            if message[1] == 'search':
                if len(message) == 2:
                    server.reply(info, '§b[Waypoints]§4请在命令后输入查询的导航点关键词！',encoding=None)
                elif len(message) == 3:
                    PlayerInfoAPI = server.get_plugin_instance('PlayerInfoAPI')
                    nbt=PlayerInfoAPI.getPlayerInfo(server, info.player)
                    search(server,info,message[2],nbt['Dimension'])
                elif len(message) == 4:
                    search(server,info,message[2],message[3])
                else:
                    server.reply(info, '§b[Waypoints]§4输入格式不正确！',encoding=None)
            
            if message[1] == 'show':
                if len(message) == 2:
                    server.reply(info, '§b[Waypoints]§4请在命令后输入展示的导航点名称！',encoding=None)
                elif len(message) == 3:
                    showdetail(server,info,message[2])
                else:
                    server.reply(info, '§b[Waypoints]§4输入格式不正确！',encoding=None)

            if message[1] == 'dim':
                if len(message) == 2:
                    PlayerInfoAPI = server.get_plugin_instance('PlayerInfoAPI')
                    nbt=PlayerInfoAPI.getPlayerInfo(server, info.player)
                    dimshow(server,info,nbt['Dimension'])
                if len(message) == 3:
                    dim=int(message[2])
                    if dim == 1 or dim == 0 or dim == -1:
                        dimshow(server,info,dim)
                    else:
                        server.reply(info, '§b[Waypoints]§4维度输入错误！请输入§b!!wp§4获取使用信息！',encoding=None)


# -*- coding: utf-8 -*-
import os
import urllib
import filecmp
import shutil
import json
import time

version_check_path = './plugins/AutoUpdate/Current_Version.json'
empty_list = {}


# Change this to release if using release version of minecraft
update_version = 'snapshot'
# update_version = 'release'


def on_info(server, info):
    if info.content == '!!checkupdate':
        check_update(server)


def on_server_startup(server):
    check_update(server)


def check_update(server):
    urllib.request.urlretrieve('https://launchermeta.mojang.com/mc/game/version_manifest.json', 'versions_new.json')
    if not os.path.exists(version_check_path):
        os.mkdir('./plugins/AutoUpdate')
        with open(version_check_path, 'w') as f:
            json.dump(empty_list, f, indent=4)
        server.stop()
        server_update(server)
        os.remove(r'./server/server.jar')
        os.rename(r'./server/server_New.jar', r'./server/server.jar')
        time.sleep(3)
        server.start()
        if os.path.exists('versions_new.json'):
            os.remove('versions_new.json')
    elif not filecmp.cmp('versions_new.json', version_check_path):
        if update_version == 'snapshot':
            server.stop()
            server_update(server)
            os.remove(r'./server/server.jar')
            os.rename(r'./server/server_New.jar', r'./server/server.jar')
            time.sleep(3)
            server.start()
            if os.path.exists('versions_new.json'):
                os.remove('versions_new.json')
        else:
            with open(version_check_path) as Version1:
                version1 = json.load(Version1)
            with open('versions_new.json') as Version2:
                version2 = json.load(Version2)
            if version1["latest"][update_version] == version2["latest"][update_version]:
                os.remove('versions_new.json')
                server.logger.info('[AutoUpdate] Update Check Success, No New Version Exists')
            else:
                server.stop()
                server_update(server)
                os.remove(r'./server/server.jar')
                os.rename(r'./server/server_New.jar', r'./server/server.jar')
                time.sleep(3)
                server.start()
                if os.path.exists('versions_new.json'):
                    os.remove('versions_new.json')
    else:
        os.remove('versions_new.json')
        server.logger.info('[AutoUpdate] Update Check Success, No New Version Exists')


def server_update(server):
    shutil.copy2('versions_new.json', version_check_path)
    with open(version_check_path) as versions_file:
            versions = json.load(versions_file)
    version = versions["latest"][update_version]
    server.logger.info('[AutoUpdate] Current Version is {}, Updating...'.format(version))
    version_json = ''
    with open(version_check_path) as versions_file:
        versions = json.load(versions_file)

    for version_entry in versions["versions"]:
        if version_entry["id"] == version and version_entry["type"] == update_version:
            version_json = version_entry["url"]
            break

    if version_json is not '':
        urllib.request.urlretrieve(version_json, 'server.json')
        with open('server.json') as version_file:
            version_json_file = json.load(version_file)
            server_url = version_json_file["downloads"]["server"]["url"]
    urllib.request.urlretrieve(server_url, 'server/server_New.jar')
    os.remove('server.json')

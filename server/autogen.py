# -*- coding: utf-8 -*-
import os
import pyshark
from server import UPLOAD_FOLDER
import simplejson as json
from time import localtime, strftime
import re

__author__ = 'PCPC'


class RegexTree:
    def __init__(self, name, value=''):
        self.name = name
        self.value = value
        self.childrens = []

    def __repr__(self, level=0):
        ret = "\t" * level + repr(self.name + '#' + self.value) + "\n"
        for child in self.childrens:
            ret += child.__repr__(level + 1)
        return ret

    def convert2json(self, root=None):
        if self.value is None or self.value == '':
            infoname = None
            pattern = r"%s.:(.*?)" % self.name
            regex = []
            root.append({"infoname": infoname, "pattern": pattern, "regex": regex})
            for child in self.childrens:
                child.convert2json(regex)
        else:
            infoname, pattern = self.value.split('~', 1)
            regex = None
            root.append({"infoname": infoname, "pattern": pattern, "regex": regex})


class ModeRegTree(RegexTree):
    def __init__(self, name, value='', mode='default'):
        super(name, value)
        self.mode = mode

    def __repr__(self, level=0):
        ret = "\t" * level + repr(self.name + '#' + self.value + '#' + self.mode) + "\n"
        for child in self.childrens:
            ret += child.__repr__(level + 1)
        return ret


def gen_config_1_json(pcapfile, frame_ids, businesss_type='LBS', name=''):
    cap = pyshark.FileCapture(os.path.join(UPLOAD_FOLDER, pcapfile))
    data_list = []
    for id in frame_ids:
        package = cap[id - 1]
        # 过滤非http层
        if not hasattr(package, 'http'):
            continue
        # 分为req和response
        if hasattr(package.http, 'request'):
            # TODO 以后要增加TXL
            mid_data = extract_mid_data(package, businesss_type, name)
        else:
            if hasattr(package.http, 'request_in'):
                req_id = int(package.http.request_in)
            else:
                req_id = int(package.http.prev_request_in)
            mid_data = extract_mid_data(cap[req_id - 1], businesss_type, name)

        data_list.append(mid_data)

    # import json
    # return json.dumps(data_list)
    return data_list


def extract_mid_data(package, businesss_type='LBS', name=''):
    mid_data = dict(TYPE=businesss_type)
    mid_data['HOST'] = package.http.host
    mid_data['URL'] = package.http.request_uri
    mid_data['METHOD'] = package.http.request_method
    mid_data['NAME'] = name
    return mid_data


def read_pair(path):
    # 将所有的中间pair按时间顺序排序
    # 这样相邻两个pair为一个请求对
    pairs = [os.path.join(path, x) for x in os.listdir(path) if os.path.isfile(os.path.join('.', path, x))]
    pairs.sort(cmp=lambda x, y: cmp(os.path.getctime(x), os.path.getctime(y)), reverse=True)
    # 每个frame分为4个部分request_head,request_body,response_head,response_body
    frame_list = list()
    p = re.compile(r'\n')
    for i in range(0, len(pairs), 2):
        # print(pairs[i],pairs[i+1])
        frame = dict()
        with open(pairs[i], 'rU') as f:
            req = f.read().split('\n\n', 1)
            frame['req_h'] = req[0]
            if len(req) > 1:
                frame['req_b'] = req[1]
            else:
                frame['req_b'] = ''
        with open(pairs[i + 1], 'rU') as f:
            res = f.read().split('\n\n', 1)
            frame['res_h'] = res[0]
            if len(res) > 1:
                frame['res_b'] = res[1]
            else:
                frame['res_b'] = ''
        for k in frame.keys():
            frame[k] = p.sub(r'<br>', frame[k])
        frame_list.append(frame)
    return frame_list


def get_interface(business):
    with open('server/conf/interface.json') as f:
        xx_interface = json.load(f)
        return xx_interface[business]


# 将一条叶子节点到root的路径合并到树中
def mergeTree(total_tree, single_root):
    if total_tree is None:
        return [single_root]
    # 先判sigle_root 有没有可能是total_tree中的一个树
    same_root = None
    for tree in total_tree:
        if tree.name == single_root.name:
            same_root = tree
    if same_root is None:
        total_tree.append(single_root)
        return total_tree
    # pt比p大一层
    if single_root.childrens is not None:
        p = single_root.childrens
    else:
        return
    pt = same_root
    # 每层节点对比
    while p is not None or pt is not None:
        i = 0
        for node in pt.childrens:
            if p.name == node.name:
                break
            i += 1
        if i >= len(pt.childrens):
            pt.childrens.append(p)
            return total_tree
        p = p.childrens[0]
        pt = pt.childrens[i]
    if pt is None and p is not None:
        pt.childrens.append(p)
    return total_tree


def parse_locations(locs):
    # 遍历location中的response。。requestBody
    loc_tree = []
    for loc in locs:
        # 遍历每一个infoname
        total_tree = None
        for info in locs[loc]:
            traces = info['value'].split('~')
            # 对每一个infoname的value 建立一个单孩子的树p
            p = None
            for trace in traces:
                node = RegexTree(trace)
                if p:
                    p.childrens.append(node)
                    p = p.childrens[0]
                else:
                    root = node
                    p = root

            p.value = info['infoname'] + '~' + info['regex']
            total_tree = mergeTree(total_tree, root)
        loc_tree.append((total_tree, loc))
    return loc_tree


def pack_senddata(reg_trees, infos, **kw):
    pack = {"time": strftime("%Y-%m-%d %H:%M:%S", localtime()), 'info': [], 'locations': {}}
    pack.update(kw)
    # 添加inof信息
    for info in infos:
        pack['info'].append(info)
    # 添加regx信息
    pack['locations'] = {}
    # 遍历locations
    for tree in reg_trees:
        regs = tree[0]
        name = tree[1]
        pack['locations'][name] = []
        for reg in regs:
            tmp = []
            reg.convert2json(tmp)
            pack['locations'][name] += tmp
    return json.dumps(pack)


import copy


def make_pack_to_txl(pack):
    for lockey, locval in pack['locations'].iteritems():
        for_each = locval
        pack['locations'][lockey] = {'info_split': '', 'contact_split': '', 'for_each': [], 'for_joint': []}
        # 在origin中找是否是特殊的mode
        for reg in for_each:
            if reg['infoname'] == 'contact_split':
                pack['locations'][lockey]['contact_split'] = reg['pattern']
            elif reg['infoname'] == 'info_split':
                pack['locations'][lockey]['info_split'] = reg['pattern']
            elif '~' in reg['pattern']:
                reg_copy = copy.deepcopy(reg)
                sp = reg['pattern'].split('~')
                reg_copy['pattern'] = sp[0]
                reg_copy['replace'] = {'pattern': sp[1], 'replaceValue': sp[2]}
                pack['locations'][lockey]['for_joint'].append(reg_copy)
            else:
                pack['locations'][lockey]['for_each'].append(dict(reg))
    return pack

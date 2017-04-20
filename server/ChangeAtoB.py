# -*- coding: utf-8 -*-
import os


def OperateJson(data, wirter):  # 解析json数据
    # 将字符串转换为dict
    dicts = eval(data);
    # print(dicts['NAME']);
    # dict的长度
    # print(len(dicts));

    resultStr = '<!--android GET Current Position-->\n';
    resultStr += ' <FILTER METHOD="' + dicts['METHOD'] + '" URL="' + dicts['URL'].split('?', 1)[0] + '" HOST="' + \
                 dicts['HOST'];
    if dicts['TYPE'] == 'LBS':
        resultStr += '" MSG_TYPE="' + dicts['TYPE'] + '_CURRENT_POSITION" ENCODING="HTML">';
    else:
        resultStr += '" MSG_TYPE="AddressBook" ENCODING="HTML">';
    resultStr += ' </FILTER>\n';

    # print(resultStr);
    wirter.write(resultStr);


def gen_1_xml(data):
    with open(os.path.join('.', "server/cfg/yj_hp_in.conf"), 'w') as writefile:
        arr = [];  # 借助中间变量数组arr，将字典转换为字符串，然后去重
        # 添加标题
        resultStr = ''
        # dict遍历,在遍历字典数组的时候,进行字符串拼接
        for index in range(len(data)):
            arr.append(str(data[index]));
        # print(eval((list(set(arr)))[0])['NAME']);
        resultStr += '<SITE ID="20100" NAME="' + eval((list(set(arr)))[0])['NAME'] + '" DOMAIN="' + \
                     eval((list(set(arr)))[0])['HOST'] + '" TYPE="' + eval((list(set(arr)))[0])['TYPE'] + '">\n'
        writefile.write(resultStr)
        resultStr = ''
        for index in range(len((list(set(arr))))):
            OperateJson((list(set(arr)))[index], writefile);
            # print((list(set(arr)))[index]);
        resultStr += '</SITE>\n'
        writefile.write(resultStr)

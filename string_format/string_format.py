"""
Android字符串整理工具

使用方法：将相关语言values文件放入source_file_path下，添加相关语言处理方法handlerLangString
例如：
    values
    values-en
    values-zh-rCN

    使用：
        handlerString()
        handlerLangString("values-en")
        handlerLangString("values-zh-rCN")
"""

import xml.etree.ElementTree as ET
import os
from xml.etree.ElementTree import Element

source_file_path = "file/"
target_file_path = "target/"


def read_xml(res):
    dict_result = {}
    tree = ET.parse(res)
    resources = tree.getroot()
    for string in resources:
        dict_result[string.attrib['name']] = string.text
    return dict_result


def __indent(elem, level=0):
    i = "\n" + level * "\t"
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "\t"
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            __indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def output_xml(res, dict_data):
    resources = ET.Element('resources')
    tree = ET.ElementTree(resources)
    for key in dict_data.keys():
        string = Element("string", {'name': key})
        string.text = dict_data[key]
        resources.append(string)
    __indent(resources)

    if not os.path.exists(target_file_path):
        os.mkdir(target_file_path)
    tree.write(target_file_path + res, encoding='utf-8', xml_declaration=True)


# 检验是否含有中文字符
def is_contains_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False


# 整理默认string下的字符
def handlerString():
    dict_head = {}
    dict_tail = {}

    dict_result = read_xml(source_file_path + "values/strings.xml")
    for key in dict_result.keys():
        if is_contains_chinese(dict_result[key]):
            dict_tail[key] = dict_result[key]
        else:
            dict_head[key] = dict_result[key]

    dict_head.update(dict_tail)

    output_xml("strings.xml", dict_head)


# 整理默认string下的字符
def handlerLangString(lang):
    dict_head = {}
    dict_tail = {}

    dict_strings = read_xml(target_file_path + "strings.xml")
    dict_strings_en = read_xml(source_file_path + lang + "/strings.xml")

    for key in dict_strings.keys():
        if key in dict_strings_en.keys():
            dict_head[key] = dict_strings_en[key]
        else:
            dict_tail[key] = "untranslated"

    dict_head.update(dict_tail)
    output_xml("string" + lang + ".xml", dict_head)


# 整理默认string下的字符
def handlerZhString():
    dict_head = {}
    dict_tail = {}

    dict_strings = read_xml("strings.xml")
    dict_strings_en = read_xml("file/values-zh-rCN/strings.xml")

    for key in dict_strings.keys():
        if key in dict_strings_en.keys():
            dict_head[key] = dict_strings_en[key]
        else:
            dict_tail[key] = "untranslated"

    dict_head.update(dict_tail)
    output_xml("string_zh.xml", dict_head)
    print(dict_head)


handlerString()
handlerLangString("values-en")
handlerLangString("values-zh-rCN")
handlerLangString("values-ko")

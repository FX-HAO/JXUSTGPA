#!/usr/bin/env python

"""
# 程序:将字符串中的中文转化为指定的unicode编码
# 版本1.0
# 作者:HFX
# 日期:GMT 7:36:352014年 4月 20日 (星期日)
# 语言:Python 3.3
# 操作:调用codeparse函数，输入需要转换的字符串，指定转换的编码，默认为utf-8
# 功能:返回转码后的字符串
# 提示:暂时只支持utf-8,gbk,gb2312,big5编码
"""

import urllib.parse
import re

def codeparse(string,encode='utf8'):
    'default code is utf8,please specific type of code'
    collection=re.findall('[\u4e00-\u9fa5]+',string)
    for element in collection:
        string=re.sub('%s' % element,
	       urllib.parse.quote(element,encoding=encode),string)
    return string

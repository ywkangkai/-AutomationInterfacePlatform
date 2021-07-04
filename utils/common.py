# -*- coding: utf-8 -*-

import locale


def datetime_fmt():
    locale.setlocale(locale.LC_CTYPE, 'chinese')
    return '%Y年%m月%d日 %H:%M:%S'

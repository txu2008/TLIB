# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/8 12:49
# @Author  : Tao.Xu
# @Email   : tao.xu2008@outlook.com

"""
Some own/observed great lib/ideas,common useful python libs.
"""

import sys
from tlib import version

if sys.version_info < (2, 6):
    raise ImportError('tlib needs to be run on python 2.6 and above.')

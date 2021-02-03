# -*- coding:utf-8 -*-
# -----------------------------------
# @Time   : 2021/2/3  9:23
# @Author : HaoWu
# @File   : OutPixel.py
# ------------------------------------

import sys
import os
from glob import glob
from PIL import Image

sys.path.append('C:\ProgramData\Anaconda3\envs\wh\python.exe') # 本程序使用在本机创建的'wh'虚拟环境
source_dir = "F:\SUP_1_train\SUP_1_20201224"  # 原始文件
filenames = glob('{}/*'.format(source_dir))

# 遍历文件夹下所有文件并保存在OutPixel.txt文件中
for filename in filenames:
    with Image.open(filename)as im:
        width,height = im.size
        f = open("F:\code\输出目标文件夹下图片信息\OutPixel.txt", "a+")
        print('图片名:',filename, '图片宽:',width, '图片高:',height,
              '图片大小：',os.path.getsize(filename), file=f)
        f.close




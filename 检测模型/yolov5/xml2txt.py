import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
 
sets = []
# classes = ["五星红旗","中国共产党党旗","八一军旗","美国国旗","英国国旗","法国国旗","日本国旗","朝鲜国旗","大韩民国国旗","俄罗斯国旗","西班牙国旗","奥运会会旗","联合国旗帜","欧盟旗帜","菲律宾共和国国旗","印度国旗","巴西国旗","越南国旗","老挝国旗","柬埔寨国旗","缅甸国旗","泰国国旗","马来西亚国旗","新加坡国旗","阿富汗国旗","伊拉克国旗","伊朗国旗","叙利亚国旗","约旦国旗","黎巴嫩国旗","以色列国旗","巴勒斯坦国旗","沙特阿拉伯国旗","瑞典国旗","澳大利亚国旗","加拿大国旗","白俄罗斯国旗","北约旗帜","东南亚国家联盟旗帜","世界贸易会旗"]  ##修改为自己的类别
classes = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","25","27","28","29","30","31","32","33","34","35","36","37","38","29","40"]
#原样保留。size为图片大小
# 将ROI的坐标转换为yolo需要的坐标
# size是图片的w和h
# box里保存的是ROI的坐标（x，y的最大值和最小值）
# 返回值为ROI中心点相对于图片大小的比例坐标，和ROI的w、h相对于图片大小的比例
def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)
 
def convert_annotation(image_add):
    #image_add进来的是带地址的.jpg
    # print(image_add)
    image_add = image_add.split(".")[0]
    # image_add = os.path.split(image_add)[1]        #截取文件名带后缀
    # image_add = image_add[0:image_add.find('.',1)] #删除后缀，现在只有文件名没有后缀
    #现在传进来的只有图片名没有后缀
   
    in_file = open('../flag/label/' + image_add + '.xml')        #修改为你自己的输入目录
    out_file = open('../flag/new_label/%s.txt'%(image_add), 'w')  #修改为你自己的输出目录
 
    tree=ET.parse(in_file)
    root = tree.getroot()
    print(root)
    
    if root.find('size'):
 
        size = root.find('size')
        w = int(size.find('width').text)    #偶尔xml标记出错，width或height设置为0了
        h = int(size.find('height').text)   #需要标记出来，便于单独处理
        if w==0:
            print("出错！ width或height为0:  "+image_add)
            # os.remove("G:/set/"+image_add+".jpg")
            # os.remove("G:/set/"+image_add+".xml")
            # return
        #在一个XML中每个Object的迭代
        for obj in root.iter('object'):
            #iter()方法可以递归遍历元素/树的所有子元素
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
            #如果训练标签中的品种不在程序预定品种，或者difficult = 1，跳过此object
            if cls not in classes or int(difficult)==1:
                continue
            #cls_id 只等于1
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            #b是每个Object中，一个bndbox上下左右像素的元组
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
            bb = convert((w,h), b)
            print(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
            out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
    else:
        print("出错！xml缺少size:  "+image_add)      #偶尔xml缺少size，需要标记出来，便于单独处理
        # os.remove("G:/set/"+image_add+".jpg")
        # os.remove("G:/set/"+image_add+".xml")
 
 
filenames = os.listdir('/u01/isi/maxq/political/flag/label/')
for image_add in filenames:
    if image_add == '.DS_Store':
        continue
    convert_annotation(image_add)
 
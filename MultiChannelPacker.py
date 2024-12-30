from PIL import Image as PILImage
import easygui
import winreg
import os

#获取源图片数量
def GetSourcePicCount():
    PicCount = input('请输入源图片数量(1-4)：')
    #判断输入是否为数字
    if not PicCount.isdigit():
        print('输入错误，请重新输入')
        return GetSourcePicCount()
    
    PicCount = int(PicCount)
    if PicCount < 1 or PicCount > 4:
        print('输入错误，请重新输入')
        return GetSourcePicCount()
    return PicCount

#获取目标图片通道数
def GetTargetPicChannelCount():
    Channel = input('请输入目标图片通道数(3:RGB 4:RGBA)：')
    if Channel != "3" and Channel != "4":
        print('输入错误，请重新输入')
        return GetTargetPicChannelCount()
    Channel = int(Channel)
    return Channel

#判断源图片数量是否大于目标图片通道数
def CheckSourcePicCount():
    SourcePicCount = GetSourcePicCount()
    TargetPicChannelCount = GetTargetPicChannelCount()
    if SourcePicCount > TargetPicChannelCount:
        print('源图片数量大于目标图片通道数，请重新输入')
        return CheckSourcePicCount()
    return SourcePicCount,TargetPicChannelCount

#获取源图片通道顺序
def GetChannelOrder(SourcePicCount,TargetPicChannelCount):
    ChannelOrder = []
    SourcePicTag = []
    print('请输入源图片通道顺序(RGBA01),0是纯黑，1是纯白，可以是一个或多个通道，选中的通道会依次填入输出的图片，比如R/GR/A0GR')
    for i in range(SourcePicCount):
        J = i + 1
        ChannelOrder.append(input('请输入第%d张图片需要使用的通道：'%J))
        SourcePicTag.append(input('请输入第%d张图片的关键字(如_D/_N/_M)：'%J))


    #获取ChannelOrder列表中通道的数量
    char_count = 0
    for i in ChannelOrder:
        char_count += len(i)
    if char_count != TargetPicChannelCount:
        print('通道数量不匹配，请重新输入')
        return GetChannelOrder(SourcePicCount,TargetPicChannelCount)
    #提示目标图片通道顺序，用得是第几张图片的哪个通道
    k = 0
    l = 0
    channel = ['R','G','B','A']
    for i in ChannelOrder:
        k += 1
        for j in i:
            if j.lower() == 'r':
                print('使用第%d张图片的R通道作为目标图片的%s通道'%(k,channel[l]))
            elif j.lower() == 'g':
                print('使用第%d张图片的G通道作为目标图片的%s通道'%(k,channel[l]))
            elif j.lower() == 'b':
                print('使用第%d张图片的B通道作为目标图片的%s通道'%(k,channel[l]))
            elif j.lower() == 'a':
                print('使用第%d张图片的A通道作为目标图片的%s通道'%(k,channel[l]))
            elif j == '0':
                print('使用纯白作为目标图片的%s通道'%(channel[l]))
            elif j == '1':
                print('使用纯黑通道作为目标图片的%s通道'%(channel[l]))
            l += 1
    return ChannelOrder,SourcePicTag

#获取桌面路径
def desktop_path():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    path = winreg.QueryValueEx(key, "Desktop")[0]
    return path

#获取源图片路径
def GetSourcePicPath():
    msg = ''
    title = '选择源图片目录'
    default = desktop_path()
    SourcePicPath = easygui.diropenbox(msg = msg,title = title ,default = default)
    return SourcePicPath

#遍历源图片路径，获取命名包含关键字的图片
def GetSourcePicList(SourcePicPath,SourcePicTag):
    SourcePicList = []
    for root,dirs,files in os.walk(SourcePicPath):
        for file in files:
            if file.find(SourcePicTag) != -1:
                SourcePicList.append(os.path.join(root,file))
    return SourcePicList

#根据关键字和基础命名匹配一组图片
def MatchSourcePic(SourcePicPath,SourcePicTagList):
    MatchPicList = []
    SourcePicTag= SourcePicTagList[0]
    # print(SourcePicTag)
    LastIndex = SourcePicPath.rfind(SourcePicTag)
    BaseName = SourcePicPath[:LastIndex]
    ExtensionName = SourcePicPath[LastIndex:].split(SourcePicTag)[-1]
    # print(ExtensionName)
    for i in range(len(SourcePicTagList)):
            #拼合图片名
        MatchName = BaseName + SourcePicTagList[i] + ExtensionName
        print(MatchName)
        #检测MatchName是否存在
        if os.path.exists(MatchName):
            # print(MatchName)
            MatchPicList.append(MatchName)
        else:
            print('图片不存在：' + MatchName)
            print('请检查源图片路径是否正确')
            #按任意键退出
            os.system('pause')
            exit()




    return MatchPicList
            

#根据通道顺序合成图片
def GetTargetPic(ChannelOrder,SourcePicList,SourcePicPath,SourcePicTag):
    TargetPicChannel = []
    #判断通道数量和源图片数量是否匹配
    if len(ChannelOrder) == len(SourcePicList):
        for j in range(len(ChannelOrder)):
            Image = PILImage.open(SourcePicList[j])
            for k in ChannelOrder[j]:
                if k.lower() == 'r':
                    TargetPicChannel.append(Image.split()[0])
                elif k.lower() == 'g':
                    TargetPicChannel.append(Image.split()[1])
                elif k.lower() == 'b':
                    TargetPicChannel.append(Image.split()[2])
                elif k.lower() == 'a':
                    if len(Image.split()) == 4:
                        TargetPicChannel.append(Image.split()[3])
                    else:
                        #如果图片没有A通道，创建一个全白的A通道
                        TargetPicChannel.append(Image.split()[0].point(lambda i: 255))
                elif k == '0':
                    TargetPicChannel.append(Image.split()[0].point(lambda i: 0))
                elif k == '1':
                    TargetPicChannel.append(Image.split()[0].point(lambda i: 255))
    
    #合成图片
    ChannelCount = 0
    for i in ChannelOrder:
        for j in i:
            ChannelCount += 1
    if ChannelCount == 3:
        TargetPic = PILImage.merge('RGB',TargetPicChannel)
    elif ChannelCount == 4:
        TargetPic = PILImage.merge('RGBA',TargetPicChannel)
    
    #获取源图片路径，将图片保存在output目录下
    TargetPicPath = SourcePicPath + '\\Output\\'
    if not os.path.exists(TargetPicPath):
        os.makedirs(TargetPicPath)
    last_index = SourcePicList[0].split('\\')[-1].rfind(SourcePicTag[0])
    ImageBaseName = SourcePicList[0].split('\\')[-1][:last_index]

    TargetPicPathFull = TargetPicPath + ImageBaseName+ '.tga'

    print('输出图片：' + TargetPicPathFull)
    TargetPic.save(TargetPicPathFull)




            

if __name__ == '__main__':
    print('-------------------------------------------------')
    print('MultiChannelPacker v0.1 Beta')
    print('\n')
    print('本软件免费开源，禁止商业用途')
    print('使用方法及后续更新请访问作者主页：')
    print('https://github.com/BreakPointOo/MultiChannelPacker')
    print('-------------------------------------------------')
    SourcePicCount,TargetPicChannelCount = CheckSourcePicCount()
    ChannelOrder,SourcePicTag = GetChannelOrder(SourcePicCount,TargetPicChannelCount)
    SourcePicPath = GetSourcePicPath()
    SourcePicList = GetSourcePicList(SourcePicPath,SourcePicTag[0])

    for i in SourcePicList:

        MatchPicList = MatchSourcePic(i,SourcePicTag)
        GetTargetPic(ChannelOrder,MatchPicList,SourcePicPath,SourcePicTag)

    os.system('pause')
    
    


    

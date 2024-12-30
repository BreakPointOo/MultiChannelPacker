from PIL import Image as PILImage
import easygui
import winreg
import os

# Get the number of source images
def GetSourcePicCount():
    PicCount = input('Please enter the number of source images (1-4): ')
    # Check if the input is a digit
    if not PicCount.isdigit():
        print('Input error, please re-enter')
        return GetSourcePicCount()
    
    PicCount = int(PicCount)
    if PicCount < 1 or PicCount > 4:
        print('Input error, please re-enter')
        return GetSourcePicCount()
    return PicCount

# Get the number of channels for the target image
def GetTargetPicChannelCount():
    Channel = input('Please enter the number of channels for the target image (3:RGB 4:RGBA): ')
    if Channel != "3" and Channel != "4":
        print('Input error, please re-enter')
        return GetTargetPicChannelCount()
    Channel = int(Channel)
    return Channel

# Check if the number of source images is greater than the number of target image channels
def CheckSourcePicCount():
    SourcePicCount = GetSourcePicCount()
    TargetPicChannelCount = GetTargetPicChannelCount()
    if SourcePicCount > TargetPicChannelCount:
        print('The number of source images is greater than the number of target image channels, please re-enter')
        return CheckSourcePicCount()
    return SourcePicCount, TargetPicChannelCount

# Get the channel order of the source images
def GetChannelOrder(SourcePicCount, TargetPicChannelCount):
    ChannelOrder = []
    SourcePicTag = []
    print('Please enter the channel order of the source images (RGBA01), 0 is pure black, 1 is pure white, it can be one or more channels, the selected channels will be filled into the output image in sequence, such as R/GR/A0GR')
    for i in range(SourcePicCount):
        J = i + 1
        ChannelOrder.append(input('Please enter the channels to be used for the %dth image: ' % J))
        SourcePicTag.append(input('Please enter the keyword for the %dth image (such as _D/_N/_M): ' % J))

    # Get the number of channels in the ChannelOrder list
    char_count = 0
    for i in ChannelOrder:
        char_count += len(i)
    if char_count != TargetPicChannelCount:
        print('The number of channels does not match, please re-enter')
        return GetChannelOrder(SourcePicCount, TargetPicChannelCount)
    # Prompt the channel order of the target image, which is the nth image's which channel
    k = 0
    l = 0
    channel = ['R', 'G', 'B', 'A']
    for i in ChannelOrder:
        k += 1
        for j in i:
            if j.lower() == 'r':
                print('Using the R channel of the %dth image as the %s channel of the target image' % (k, channel[l]))
            elif j.lower() == 'g':
                print('Using the G channel of the %dth image as the %s channel of the target image' % (k, channel[l]))
            elif j.lower() == 'b':
                print('Using the B channel of the %dth image as the %s channel of the target image' % (k, channel[l]))
            elif j.lower() == 'a':
                print('Using the A channel of the %dth image as the %s channel of the target image' % (k, channel[l]))
            elif j == '0':
                print('Using pure white as the %s channel of the target image' % channel[l])
            elif j == '1':
                print('Using pure black as the %s channel of the target image' % channel[l])
            l += 1
    return ChannelOrder, SourcePicTag

# Get the desktop path
def desktop_path():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    path = winreg.QueryValueEx(key, "Desktop")[0]
    return path

# Get the path of the source images
def GetSourcePicPath():
    msg = ''
    title = 'Select the directory of source images'
    default = desktop_path()
    SourcePicPath = easygui.diropenbox(msg=msg, title=title, default=default)
    return SourcePicPath

# Traverse the source image path and get the images whose names contain the keyword
def GetSourcePicList(SourcePicPath, SourcePicTag):
    SourcePicList = []
    for root, dirs, files in os.walk(SourcePicPath):
        for file in files:
            if file.find(SourcePicTag) != -1:
                SourcePicList.append(os.path.join(root, file))
    return SourcePicList

# Match a set of images according to the keyword and base naming
def MatchSourcePic(SourcePicPath, SourcePicTagList):
    MatchPicList = []
    SourcePicTag = SourcePicTagList[0]
    LastIndex = SourcePicPath.rfind(SourcePicTag)
    BaseName = SourcePicPath[:LastIndex]
    ExtensionName = SourcePicPath[LastIndex:].split(SourcePicTag)[-1]
    for i in range(len(SourcePicTagList)):
        # Combine the image name
        MatchName = BaseName + SourcePicTagList[i] + ExtensionName
        print(MatchName)
        # Check if MatchName exists
        if os.path.exists(MatchName):
            # print(MatchName)
            MatchPicList.append(MatchName)
        else:
            print('Image does not exist: ' + MatchName)
            print('Please check if the source image path is correct')
            # Press any key to exit
            os.system('pause')
            exit()


# Composite images according to the channel order
def GetTargetPic(ChannelOrder, SourcePicList, SourcePicPath, SourcePicTag):
    TargetPicChannel = []
    # Check if the number of channels and the number of source images match
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
                        # If the image does not have an A channel, create a fully white A channel
                        TargetPicChannel.append(Image.split()[0].point(lambda i: 255))
                elif k == '0':
                    TargetPicChannel.append(Image.split()[0].point(lambda i: 0))
                elif k == '1':
                    TargetPicChannel.append(Image.split()[0].point(lambda i: 255))

    # Composite images
    ChannelCount = 0
    for i in ChannelOrder:
        for j in i:
            ChannelCount += 1
    if ChannelCount == 3:
        TargetPic = PILImage.merge('RGB', TargetPicChannel)
    elif ChannelCount == 4:
        TargetPic = PILImage.merge('RGBA', TargetPicChannel)

    # Get the source image path and save the image in the output directory
    TargetPicPath = SourcePicPath + '\\Output\\'
    if not os.path.exists(TargetPicPath):
        os.makedirs(TargetPicPath)
    last_index = SourcePicList[0].split('\\')[-1].rfind(SourcePicTag[0])
    ImageBaseName = SourcePicList[0].split('\\')[-1][:last_index]
    TargetPicPathFull = TargetPicPath + ImageBaseName + '.tga'

    print('Output image: ' + TargetPicPathFull)
    TargetPic.save(TargetPicPathFull)

if __name__ == '__main__':
    print('-------------------------------------------------')
    print('MultiChannelPacker v0.1 Beta')
    print('\n')
    print('This software is free and open source, commercial use is prohibited')
    print('For usage and future updates, please visit the author\'s homepage:')
    print('https://github.com/BreakPointOo/MultiChannelPacker')
    print('-------------------------------------------------')
    SourcePicCount, TargetPicChannelCount = CheckSourcePicCount()
    ChannelOrder, SourcePicTag = GetChannelOrder(SourcePicCount, TargetPicChannelCount)
    SourcePicPath = GetSourcePicPath()
    SourcePicList = GetSourcePicList(SourcePicPath, SourcePicTag[0])

    for i in SourcePicList:
        MatchPicList = MatchSourcePic(i, SourcePicTag)
        GetTargetPic(ChannelOrder, MatchPicList, SourcePicPath, SourcePicTag)

    os.system('pause')

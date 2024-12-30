from PIL import Image as PILImage
import easygui
import winreg
import os
import requests
from bs4 import BeautifulSoup
from packaging import version

# Check for updates
def CheckUpdate(Version):
    print('\n')
    print('Checking for updates...')
    print('\n')
    current_version = Version
    try:
        # Set request timeout (in seconds)
        response = requests.get(f'https://github.com/BreakPointOo/MultiChannelPacker/releases', timeout=5)
        response.raise_for_status()  # Raise an exception if the request fails
    except requests.exceptions.RequestException as e:
        print('Failed to get version information')
        print('\n')
        return

    html_content = response.text

    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all version tags
    version_tags = soup.find_all('a', {'class': 'Link--primary'})
    # print('Version information:')
    # for tag in version_tags:
    #         print(tag.text.strip())

    # Parse out the latest version number
    latest_version = None
    for tag in version_tags:
        if 'v' in tag.text and not 'preview' in tag.text.lower():  # Ignore preview versions
            latest_version = tag.text.strip()
            # print(f'Latest version: {latest_version}')
            break
    # Compare the current version and the latest version
    if latest_version and version.parse(latest_version) > version.parse(current_version):

        print('-------------------------------------------------')
        print(f'New version found: {latest_version}, it is recommended to upgrade')
        print('-------------------------------------------------')
        print('\n')
    else:

        print('-------------------------------------------------')
        print('The current version is the latest')
        print('-------------------------------------------------')
        print('\n')


# Get the number of source images
def GetSourcePicCount():
    PicCount = input('Please enter the number of source images (1-4): ')
    # Check if the input is a digit
    if not PicCount.isdigit():
        print('Input error, please re-enter')
        return GetSource珀Count()
    
    PicCount = int(PicCount)
    if PicCount < 1 or PicCount > 4:
        print('Input error, please re-enter')
        return GetSourcePicCount()
    return PicCount

# Get the number of target image channels
def GetTargetPicChannelCount():
    Channel = input('Please enter the number of target image channels (3:RGB 4:RGBA): ')
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
    return SourcePicCount,TargetPicChannelCount

# Get the channel order of source images
def GetChannelOrder(SourcePicCount,TargetPicChannelCount):
    ChannelOrder = []
    SourcePicTag = []
    print('Please enter the channel order of source images (RGBA01), 0 is pure black, 1 is pure white, it can be one or more channels, the selected channels will be filled in the output image in turn, such as R/GR/A0GR')
    for i in range(SourcePicCount):
        J = i + 1
        ChannelOrder.append(input('Please enter the channels to be used for the %dth image: '%J))
        SourcePicTag.append(input('Please enter the keyword for the %dth image (such as _D/_N/_M): '%J))


    # Get the number of channels in the ChannelOrder list
    char_count = 0
    for i in ChannelOrder:
        char_count += len(i)
    if char_count != TargetPicChannelCount:
        print('The number of channels does not match, please re-enter')
        return GetChannelOrder(SourcePicCount,TargetPicChannelCount)
    # Prompt the target image channel order, which is the channel of which image
    k = 0
    l = 0
    channel = ['R','G','B','A']
    for i in ChannelOrder:
        k += 1
        for j in i:
            if j.lower() == 'r':
                print('Use the R channel of the %dth image as the %s channel of the target image'%(k,channel[l]))
            elif j.lower() == 'g':
                print('Use the G channel of the %dth image as the %s channel of the target image'%(k,channel[l]))
            elif j.lower() == 'b':
                print('Use the B channel of the %dth image as the %s channel of the target image'%(k,channel[l]))
            elif j.lower() == 'a':
                print('Use the A channel of the %dth image as the %s channel of the target image'%(k,channel[l]))
            elif j == '0':
                print('Use pure white as the %s channel of the target image'%(channel[l]))
            elif j == '1':
                print('Use pure black as the %s channel of the target image'%(channel[l]))
            l += 1
    return ChannelOrder,SourcePicTag

# Get the desktop path
def desktop_path():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    path = winreg.QueryValueEx(key, "Desktop")[0]
    return path

# Get the source image path
def GetSourcePicPath():
    msg = ''
    title = 'Select Source Image Directory'
    default = desktop_path()
    SourcePicPath = easygui.diropenbox(msg = msg,title = title ,default = default)
    return SourcePicPath

# Traverse the source image path and get images with naming containing keywords
def GetSourcePicList(SourcePicPath,SourcePicTag):
    SourcePicList = []
    for root,dirs,files in os.walk(SourcePicPath):
        for file in files:
            if file.find(SourcePicTag) != -1:
                SourcePicList.append(os.path.join(root,file))
    return SourcePicList

# Match a set of images based on keywords and basic naming
def MatchSourcePic(SourcePicPath,SourcePicTagList,SourcePicCount):
    MatchPicList = []
    ALLMatchPicList = []
    SourcePicTag= SourcePicTagList[0]
    # print(SourcePicTag)
    LastIndex = Source珀ath.rfind(SourcePicTag)
    BaseName = SourcePicPath[:LastIndex]
    ExtensionName = SourcePicPath[LastIndex:].split(SourcePicTag)[-1]
    # print(ExtensionName)
    for i in range(len(SourcePicTagList)):
            # Combine image names
        MatchName = BaseName + SourcePicTagList[i] + ExtensionName
        # print(MatchName)
        # Check if MatchName exists
        if os.path.exists(MatchName):
            MatchPicList.append(MatchName)
    if len(MatchPicList) == SourcePicCount:
        for i in MatchPicList:
            ALLMatchPicList.append(i)
    # Determine if matching is successful
    if len(ALLMatchPicList) == SourcePicCount:
        return ALLMatchPicList
    else:
        return None

# Combine images according to the channel order
def GetTargetPic(ChannelOrder,SourcePicList,SourcePicPath,SourcePicTag):
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
    
    # Combine images
    ChannelCount = 0
    for i in ChannelOrder:
        for j in i:
            ChannelCount += 1
    if ChannelCount == 3:
        TargetPic = PILImage.merge('RGB',TargetPicChannel)
    elif ChannelCount == 4:
        TargetPic = PILImage.merge('RGBA',TargetPicChannel)
    
    # Get the source image path and save the image in the output directory
    TargetPicPath = SourcePicPath + '\\Output\\'
    if not os.path.exists(TargetPicPath):
        os.makedirs(TargetPicPath)
    last_index = SourcePicList[0].split('\\')[-1].rfind(SourcePicTag[0])
    ImageBaseName = SourcePicList[0].split('\\')[-1][:last_index]

    TargetPicPathFull = TargetPicPath + ImageBaseName+ '.tga'

    print('Output image: ' + TargetPicPathFull)
    TargetPic.save(TargetPicPathFull)


if __name__ == '__main__':
    Version = 'v1.1'
    print('-------------------------------------------------')
    print('MultiChannelPacker '+Version)
    print('\n')
    print('This software is free and open source, commercial use is prohibited')
    print('For usage and subsequent updates, please visit the author\'s homepage:')
    print('https://github.com/BreakPointOo/MultiChannelPacker')
    print('-------------------------------------------------')
    CheckUpdate(Version)
    SourcePicCount,TargetPicChannelCount = CheckSourcePicCount()
    ChannelOrder,SourcePicTag = GetChannelOrder(SourcePicCount,TargetPicChannelCount)
    SourcePicPath = GetSourcePicPath()
    SourcePicList = GetSourcePicList(SourcePicPath,SourcePicTag[0])

    for i in SourcePicList:

        MatchPicList = MatchSourcePic(i,SourcePicTag,SourcePicCount)
        if MatchPicList != None:
            GetTargetPic(ChannelOrder,MatchPicList,SourcePicPath,SourcePicTag)

        

    os.system('pause')
    

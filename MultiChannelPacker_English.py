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
    # Parse out the latest version number
    latest_version = None
    for tag in version_tags:
        if 'v' in tag.text and not 'preview' in tag.text.lower():  # Ignore preview versions
            latest_version = tag.text.strip()
            break
    # Compare current version and latest version
    if latest_version and version.parse(latest_version) > version.parse(current_version):
        print('-------------------------------------------------')
        print(f'New version found: {latest_version}, upgrade recommended')
        print('-------------------------------------------------')
        print('\n')
    else:
        print('-------------------------------------------------')
        print('Current version is the latest')
        print('-------------------------------------------------')
        print('\n')


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

# Get the number of target image channels
def GetTargetPicChannelCount():
    Channel = input('Please enter the number of target image channels (3:RGB 4:RGBA): ')
    if Channel != "3" and Channel != "4":
        print('Input error, please re-enter')
        return GetTargetPicChannelCount()
    Channel = int(Channel)
    return Channel

# Input custom naming
def GetCustomName():
    CustomName = input('Please enter a custom suffix for the generated image, such as _N/01, press Enter to skip this step: ')
    if CustomName != '':
        return CustomName
    else:
        return None


# Check if the number of source images is greater than the number of target image channels
def CheckSourcePicCount():
    SourcePicCount = GetSourcePicCount()
    TargetPicChannelCount = GetTargetPicChannelCount()
    if SourcePicCount > TargetPicChannelCount:
        print('Number of source images is greater than the number of target image channels, please re-enter')
        return CheckSourcePicCount()
    return SourcePicCount, TargetPicChannelCount

# Get the channel order of source images
def GetChannelOrder(SourcePicCount, TargetPicChannelCount):
    ChannelOrder = []
    SourcePicTag = []
    print('Please enter the channel order of source images (RGBA01), 0 is pure black, 1 is pure white, it can be one or more channels, selected channels will be filled into the output image in order, such as R/GR/A0GR')
    for i in range(SourcePicCount):
        J = i + 1
        ChannelOrder.append(input('Please enter the channels to be used for the %dth image: ' % J))
        SourcePicTag.append(input('Please enter the keyword for the %dth image (such as _D/_N/_M): ' % J))

    # Get the number of channels in the ChannelOrder list
    char_count = 0
    for i in ChannelOrder:
        char_count += len(i)
    if char_count != TargetPicChannelCount:
        print('Channel count does not match, please re-enter')
        return GetChannelOrder(SourcePicCount, TargetPicChannelCount)
    # Prompt the target image channel order, which is the nth image's which channel
    k = 0
    l = 0
    channel = ['R', 'G', 'B', 'A']
    for i in ChannelOrder:
        k += 1
        for j in i:
            if j.lower() == 'r':
                print('Use the R channel of the %dth image as the %s channel of the target image' % (k, channel[l]))
            elif j.lower() == 'g':
                print('Use the G channel of the %dth image as the %s channel of the target image' % (k, channel[l]))
            elif j.lower() == 'b':
                print('Use the B channel of the %dth image as the %s channel of the target image' % (k, channel[l]))
            elif j.lower() == 'a':
                print('Use the A channel of the %dth image as the %s channel of the target image' % (k, channel[l]))
            elif j == '0':
                print('Use pure white as the %s channel of the target image' % (channel[l]))
            elif j == '1':
                print('Use pure black channel as the %s channel of the target image' % (channel[l]))
            l += 1
    return ChannelOrder, SourcePicTag

# Get desktop path
def desktop_path():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    path = winreg.QueryValueEx(key, "Desktop")[0]
    return path

# Get source image path
def GetSourcePicPath():
    msg = ''
    title = 'Select source image directory'
    default = desktop_path()
    SourcePicPath = easygui.diropenbox(msg=msg, title=title, default=default)
    return SourcePicPath

# Traverse the source image path and get images with names containing keywords
def GetSourcePicList(SourcePicPath, SourcePicTag):
    SourcePicList = []
    for item in os.listdir(SourcePicPath):
        # Concatenate full path
        full_path = os.path.join(SourcePicPath, item)
        # Check if it is a file and contains SourcePicTag
        if os.path.isfile(full_path) and item.find(SourcePicTag) != -1:
            SourcePicList.append(full_path)
    return SourcePicList

def get_image_size(image_path):
    """Get image size"""
    with PILImage.open(image_path) as img:
        return img.size

def is_rgb_image(image_path):
    with PILImage.open(image_path) as img:
        return img.mode == 'RGB'

# Match a set of images based on keywords and base naming
def MatchSourcePic(SourcePicPath, SourcePicTagList, SourcePicCount):
    MatchPicList = []
    SourcePicTag = SourcePicTagList[0]
    LastIndex = SourcePicPath.rfind(SourcePicTag)
    BaseName = SourcePicPath[:LastIndex]
    ExtensionName = SourcePicPath[LastIndex:].split(SourcePicTag)[-1]
    for i in range(len(SourcePicTagList)):
        MatchName = BaseName + SourcePicTagList[i] + ExtensionName
        if os.path.exists(MatchName):
            MatchPicList.append(MatchName)
    if len(MatchPicList) == SourcePicCount:
        reference_size = get_image_size(MatchPicList[0])
        for image_path in MatchPicList:
            if not is_rgb_image(image_path):  # Check if the image is in RGB format
                print("Non-RGB image: {}".format(image_path))
                return None
            if get_image_size(image_path) != reference_size:
                # If there is an inconsistent image size, clear the list and return None
                print("Image size mismatch: {}".format(image_path))
                return None
        return MatchPicList
    else:
        return None

# Combine images according to channel order
def GetTargetPic(ChannelOrder, SourcePicList, SourcePicPath, SourcePicTag, CustomName):
    TargetPicChannel = []
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
        TargetPic = PILImage.merge('RGB', TargetPicChannel)
    elif ChannelCount == 4:
        TargetPic = PILImage.merge('RGBA', TargetPicChannel)

    # Get source image path, save the image in the output directory
    TargetPicPath = SourcePicPath + '\\Output\\'
    if not os.path.exists(TargetPicPath):
        os.makedirs(TargetPicPath)
    last_index = SourcePicList[0].split('\\')[-1].rfind(SourcePicTag[0])
    ImageBaseName = SourcePicList[0].split('\\')[-1][:last_index]
    if CustomName != None:
        ImageBaseName = ImageBaseName + CustomName
    TargetPicPathFull = TargetPicPath + ImageBaseName + '.tga'

    print('Output image: ' + TargetPicPathFull)
    TargetPic.save(TargetPicPathFull)


if __name__ == '__main__':
    Version = 'v1.3.0'
    print('-------------------------------------------------')
    print('MultiChannelPacker ' + Version)
    print('\n')
    print('This software is free and open source, commercial use is prohibited')
    print('For usage and future updates, please visit the author\'s homepage:')
    print('https://github.com/BreakPointOo/MultiChannelPacker')
    print('-------------------------------------------------')
    CheckUpdate(Version)
    SourcePicCount, TargetPicChannelCount = CheckSourcePicCount()
    ChannelOrder, SourcePicTag = GetChannelOrder(SourcePicCount, TargetPicChannelCount)

    CustomName = GetCustomName()
    SourcePicPath = GetSourcePicPath()
    SourcePicList = GetSourcePicList(SourcePicPath, SourcePicTag[0])

    for i in SourcePicList:
        MatchPicList = MatchSourcePic(i, SourcePicTag, SourcePicCount)
        if MatchPicList != None:
            GetTargetPic(ChannelOrder, MatchPicList, SourcePicPath, SourcePicTag, CustomName)

    os.system('pause')

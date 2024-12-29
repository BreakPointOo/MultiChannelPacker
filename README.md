# MultiChannelPacker

方便快捷的批量提取多张图片的通道整合成新的图片

A convenient and quick tool for batch extracting channels from multiple images and combining them into a new image.

## 注意事项 Notes

- 源图片必须为RGB/RGBA格式

The source images must be in RGB/RGBA format.

- 在使用多张图片的通道时，图片的命名必须有相关性，除了输入的关键字不同，关键字前的命名必须是相同的，比如Image_*

When using channels from multiple images, the naming of the images must be related. Except for the different keywords, the naming before the keywords must be the same, such as Image_*.

- 目前只能输出tga格式，但是输入的图片可以是其他格式

Currently, only TGA format can be output, but the input images can be in other formats.

- 输入的图片通道顺序会依次填装进新的图片

The channel order of the input images will be sequentially filled into the new image.

## 使用方法 Usage

1.输入源图片的数量和目标图片的通道数，源图片的数量一定是小于等于目标图片的通道数的

Enter the number of source images and the number of channels for the target image. The number of source images must be less than or equal to the number of channels in the target image.

2.依次输入需要使用的通道和关键字。根据关键字寻找匹配的图片，然后根据关键字和通道的顺序将通道提取后依次输入目标图像的RGBA通道。关键字前的命名为基础命名，基础命名相同的图片会被分成一组处理，输出图片时也是按照基础命名输出的。

Enter the channels and keywords to be used one by one. Find matching images according to the keywords, then extract the channels according to the order of the keywords and channels, and sequentially fill them into the RGBA channels of the target image. The naming before the keyword is the base naming, and images with the same base naming will be processed as a group and output according to the base naming when saving the images.

3.在弹窗中选择存放图片的路径，遍历所有的图片后会将批量拼装后的图片输出到存放路径的Output子目录下

Select the path to store the images in the pop-up window. After traversing all the images, the batch-assembled images will be output to the Output subdirectory under the storage path.


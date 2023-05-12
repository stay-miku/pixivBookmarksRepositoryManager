# pixivBookmarksRepositoryManager
一个奇奇怪怪的pixiv收藏本地备份工具

详细说明可见function map.mmd文件

(写的很差，咱自己都不满意)

## 安装
 ```
 pip install pbrm
 ```

## 使用

1.设置备份文件储存路径
```
pbrm set this
```
设置当前路径为备份路径

```
pbrm set C:/pbrm/
```
指定其他路径

2.设置cookie
```
pbrm config cookie <cookie内容>
```

3.更新备份
```
pbrm update
```
会自动备份所有收藏到之前设置的路径中。会自动跳过失效的收藏（如果之前没备份过会存个meta数据，唯一的作用是知道作品pid）

## 一些小功能
1.统计数据
```
pbrm show (unavailable | unavailableSaved | saved) [-o]
```
如:
```
pbrm show unavailable
```
显示所有为备份且失效的收藏

```
pbrm show unavailableSaved -o
```
显示所有已失效但是备份了的收藏，并且只显示数量

2.gif动图保存
首先需要自行配置好ffmpeg

然后：
```
pbrm config ugoira gif
```
之后备份会自动将动图以gif形式保存

3.其他一些小功能
```
pbrm update -f
```
强制更新所有收藏，一般用于之前没用gif保存修改动图保存形式后重新保存一遍，会跳过已失效的收藏

```
pbrm delete <pid>
```
删除备份的一个收藏

其他功能就看pbrm -h了

## 备份格式
（自己看看就知道了）

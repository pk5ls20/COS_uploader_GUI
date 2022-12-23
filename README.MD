## **墙裂推荐使用本GUI版本的`COS_uploader`**
>  本项目为[pk5ls20-COS_uploader](https://github.com/pk5ls20/COS_uploader)的**GUI重构版**，GUI使用Pyqt5重新开发
### 已实现/新增的功能
- [x] 加载/保存参数文件
- [x] 上传单个文件/文件夹
- [x] 上传文件名判重
- [x] 上传进度条
- [x] 状态栏指示
- [x] 日志分级保存
- [x] 异常处理
- [x] 上帝模式(sudo mode)
- [x] 更多在GUI里特有的小细节...
### 使用方法
1. 下载releases里的可执行文件  
2. 输入参数后即可使用（关于参数可参见[pk5ls20/COS_uploader/readme](https://github.com/pk5ls20/COS_uploader#readme)）
>   **上帝模式(sudo mode)**:</br>
>  本模式可以在打开程序时自动加载参数，适合持久使用  
> 在保存参数时密码输入`sudo`即可触发本模式
### 部署方法
`pip install -r requirements.txt`

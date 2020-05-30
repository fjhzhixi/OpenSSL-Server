# OpenSSL-Server

## 项目介绍

本项目为基于`OpenSSL`的安全云盘项目，本项目的核心要点有以下三点：

### https安全连接

1. 安全问题：通过`web`端进行对云盘的访问时，传统的`http`协议极易收到攻击造成数据泄露，例如网络窃听者
2. 解决方法：基于`OpenSSL`构建`ssl`服务器使用`https`建立连接

### 云端文件加密

1. 安全问题：文件如果以明文的方式存储在云端，假如服务商将这些私人文件信息提取并应用于非法目的对造成极大的安全隐患，是对个人隐私的侵犯
2. 解决方法：引入第三方可信任的密钥服务器，使用非对称加密传递对称加密密钥，再对上传文件加密，从而对云盘上的文件实现加密，具体过程如下：
   1. 用户首先向密钥服务器发送自己的`RSA`公钥
   2. 密钥服务器使用该`RSA`公钥加密`ASE`密钥传输给用户
   3. 用户使用自己的`RSA`私钥解密数据得到双方公认的`ASE`密钥
   4. 用户使用`ASE`密钥加密文件之后上传到云盘服务器，这样云盘服务器就无法得知文件具体内容
   5. 当用户需要下载时，向密钥服务器请求`ASE`密钥，同样使用`RSA`非对称加密算法传递

### 云盘功能

本项目基本实现了云盘注册，登录，显示，上传，下载的基本功能要求

## 项目结构介绍

1. `bash`中保存创建本地`sql`数据库的脚本
2. `docs`中为本项目参考文档
3. `keysite`中为第三方信任密钥服务器‘’
4. `resource`中为一些静态资源
5. `rsa`中保存了一组使用`OpenSSL`生成的`RSA`公钥私钥对
6. `Server`中为`SSL`服务器代码
7. `website`中为云盘服务器代码

## 项目运行方法

### 环境要求

1. `Ubuntu 16.04`
2. g++ (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609`
3. `OpenSSL 1.0.2g`
4. `Python 3.5.2`:
   * `Flask 1.1.2`
   * `Flask-Cors 3.0.8`
   * `crypto 1.4.1`

### 运行准备

1. 配置`OpenSSL`库，执行`sudo apt-get install libssl-dev`安装
2. 在`Server`目录下执行`make`产生`MyWebServer`可执行文件
3. 运行`./MyWebServer`，打开浏览器，在地址栏输入`https://localhost:8000`如果浏览器提示此链接不受信任，需要添加例外后再进行访问。添加例外后，可以在firefox中查看添加的认证，位置为preferences -> privacy&security -> view certificates -> servers
4. 在`mysql`中运行`bash`中的脚本文件创建数据库
5. 在`website/core.py`文件的第22行将`password`更换为自己的`mysql`的密码

### 运行

1. 在`Server`目录下运行`./MyWebServer`
2. 在`keysite`目录下运行`python3 core.py`
3. 在`website`目录下运行`python3 core.py`
4. 访问`https://localhost:8000`


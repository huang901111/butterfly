# butterfly

<div align=center><img src="https://github.com/meetbill/butterfly/blob/master/images/butterfly.png" width="350"/></div>

蝴蝶（轻量化 Web 框架）如同蝴蝶一样，此框架小而美

```
    __          __  __            ______
   / /_  __  __/ /_/ /____  _____/ __/ /_  __
  / __ \/ / / / __/ __/ _ \/ ___/ /_/ / / / /
 / /_/ / /_/ / /_/ /_/  __/ /  / __/ / /_/ /
/_.___/\__,_/\__/\__/\___/_/  /_/ /_/\__, /
                                    /____/
```
<!-- vim-markdown-toc GFM -->

* [1 环境](#1-环境)
* [2 特性](#2-特性)
* [3 使用手册](#3-使用手册)
    * [3.1 手册传送门](#31-手册传送门)
    * [3.2 举个栗子](#32-举个栗子)
* [4 版本信息](#4-版本信息)
* [5 参加步骤](#5-参加步骤)

<!-- vim-markdown-toc -->

## 1 环境

env:Python 2.7

## 2 特性

```
# 不带参数
http://IP:PORT/{handlers 下的 package,此处支持多级}/{func_name}

# 带参数
http://IP:PORT/{handlers 下的 package,此处支持多级}/{func_name}?args1=value1

如:
curl -v "http://127.0.0.1:8585/x/ping"                      ===> handlers/x::ping()
curl -v "http://127.0.0.1:8585/x/hello?str_info=meetbill"   ===> handlers/x::hello(str_info=meetbill)
```

> * 根据 handlers package 下 package 目录结构自动加载路由(目前不支持动态路由)
> * 自定义 HTTP header
> * Handler 的参数列表与 HTTP 请求参数保持一致，便于接口开发
> * 自动对 HTTP 请求参数进行参数检查
> * 请求的响应 Header 中包含请求的 reqid(会记录在日志中),便于进行 trace

## 3 使用手册

### 3.1 手册传送门

* [Butterfly 手册](https://github.com/meetbill/butterfly/wiki)
* [Butterfly 示例](https://github.com/meetbill/butterfly-examples)
* [Butterfly 前端](https://github.com/meetbill/butterfly-fe)
* [Butterfly nginx 配置](https://github.com/meetbill/butterfly-nginx)

### 3.2 举个栗子

> 前后端分离 + 单点登录结合
>  * 后端接口认证使用 nginx auth_request 进行验证
>  * [接口认证方案](https://github.com/meetbill/butterfly/wiki/butterfly_cas)模块化，复用性强

```
               +--------------------------------------------------------------------------+
               |                          butterfly-nginx                                 |
               +--------------------------------------------------------------------------+
                       |                     |                                      |
                       V                     V                                      V
               +-------------+    +---------------------+                      +----------+
               |~* /static/  |    |= /auth/verification |                      |/         |
               |= /index.html|    |= /butterfly_401     |                      |          |
               |= /          |    |= /auth/ssologin     |                      |          |
               +-------------+    +---------------------+                      +----------+
                       |                     |                                       |
                       V                     V                                       V
+----------+       +------------+     +--------------+       +----------+     +-----------+
|web browse|       |butterfly-fe|     |butterfly-auth|       |cas-server|     |app-backend|
+----------+       +------------+     +--------------+       +----------+     +-----------+
     |                    |                  |                     |                   |
     +-------route------->|/                 |                     |                   |
     |<-------page--------+/index.html       |                     |                   |
     |                    |                  |                     |                   |
     ==================================================================== not have token
     |                    |                  |                     |                   |
     +--V----------------request api-------------------------------------------------->|
     |  +-sub request-header not have token->|(/auth/verification) |                   |
     |<-code=401,targetURL=../auth/ssologin--+                     |                   |
     |                    |                  |                     |                   |
     +--window.location.herf=directurl------>|(/auth/ssologin)     |                   |
     |<----code=302,Location=cas-server------+                     |                   |
     |                    |                  |                     |                   |
     +-----302 http://cas-server/login  login page --------------->|(/login)           |
     |<-------------code=302,set Cookie TGT=xxx -------------------+                   |
     |                    |                  |                     |                   |
     +-----302 /auth/ssologin?ticket=xxx --->|                     |                   |
     |                    |                  +-------check st----->|(/session/validate)|
     |                    |                  |<-------st vaild-----+                   |
     |<--code=302 set Cookie butterfly_token-+                     |                   |
     |                    |                  |                     |                   |
     +--302 / ----------->|                  |                     |                   |
     |<-------page--------+/index.html       |                     |                   |
     |                    |                  |                     |                   |
     ======================================================================== have token
     |                    |                  |                     |                   |
     +---V----------------request api------------------------------------------------->|
     |   +-sub request-header have token---->|/auth/verification   |                   |
     |<-------------------response-----------------------------------------------------+
```

## 4 版本信息

本项目的各版本信息和变更历史可以在[这里][changelog]查看。

## 5 参加步骤

* 在 GitHub 上 `fork` 到自己的仓库，然后 `clone` 到本地，并设置用户信息。
```
$ git clone https://github.com/meetbill/butterfly.git
$ cd butterfly
$ git config user.name "yourname"
$ git config user.email "your email"
```
* 修改代码后提交，并推送到自己的仓库。
```
$ #do some change on the content
$ git commit -am "Fix issue #1: change helo to hello"
$ git push
```
* 在 GitHub 网站上提交 pull request。
* 定期使用项目仓库内容更新自己仓库内容。
```
$ git remote add upstream https://github.com/meetbill/butterfly.git
$ git fetch upstream
$ git checkout master
$ git rebase upstream/master
$ git push -f origin master
```

[changelog]: CHANGELOG.md

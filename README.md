# butterfly

<div align=center><img src="https://github.com/meetbill/butterfly/blob/master/images/butterfly.png" width="350"/></div>

蝴蝶（轻量化 Web 框架）就像蝴蝶这个名字一样，此框架小而美

```
    __          __  __            ______
   / /_  __  __/ /_/ /____  _____/ __/ /_  __
  / __ \/ / / / __/ __/ _ \/ ___/ /_/ / / / /
 / /_/ / /_/ / /_/ /_/  __/ /  / __/ / /_/ /
/_.___/\__,_/\__/\__/\___/_/  /_/ /_/\__, /
                                    /____/
```
<!-- vim-markdown-toc GFM -->

* [环境](#环境)
* [特性](#特性)
* [使用手册](#使用手册)
* [版本信息](#版本信息)
* [参加步骤](#参加步骤)

<!-- vim-markdown-toc -->

## 环境

env:Python 2.7

## 特性

> * 自动加载路由(目前不支持动态路由)
> * 自定义 HTTP header
> * Handler 的参数列表与 HTTP 请求参数保持一致，便于接口开发
> * 自动对 HTTP 请求参数进行参数检查

## 使用手册

[使用手册](https://github.com/meetbill/butterfly/wiki)

## 版本信息

本项目的各版本信息和变更历史可以在[这里][changelog]查看。

## 参加步骤

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

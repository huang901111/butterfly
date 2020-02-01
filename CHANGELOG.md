Changelog
===
以下记录了项目中所有值得关注的变更内容，其格式基于 [Keep a Changelog]。

本项目版本遵守 [Semantic Versioning] 和 [PEP-440]。

## [1.0.9] - 2020-02-01
### Changed
- 增加通过装饰器自定义 handler 属性
### Removed
- 删除 x 目录下自动设置 handler 属性逻辑

## [1.0.8] - 2020-01-09
### Changed
- 修改访问日志格式，方便统计
### Added
- 增加报表（输出用户访问分布量 / 状态码分布图 / 认证请求路径分布图 / 每天访问量等）

## [1.0.7] - 2019-12-02
### Changed
- 添加 redirect 重定向

## [1.0.6] - 2019-11-15
### Changed
- butterfly 添加 test_handler.py 用于方便测试 handlers 方法输出
- xlib 添加 middleware
- xlib 添加 util [wrapt 1.11.2](https://github.com/GrahamDumpleton/wrapt)
- request 添加 cookie 解析
- request 添加 user 属性

## [1.0.5] - 2019-10-06
### Fixed
- 修正请求静态文件时，日志中不打印静态文件信息以及状态码问题
### Changed
- 日志中添加打印 filename 以及 lineno 列，方便排查问题

## [1.0.4] - 2019-08-09
### Added
- 支持 auth(pyjwt)
- 添加 MySQL pool

## [1.0.3] - 2019-08-03
### Changed
- 支持多级路由，自动加载路由从自动从 moudle 中加载，修改为自动从指定 package 下自动加载
- 路由字典中的 key 由 func_name ，修改为 `/package_name/func_name`

```
请求 PATH_INFO    ==> 路由字典中的 key ==> 实际的函数路径
/ping or /ping/   ==> /ping            ==> handlers/__init__.py::ping
/apidemo/ping     ==> /apidemo/ping    ==> handlers/apidemo/__init__.py::ping
```

## [1.0.2] - 2019-07-24
### Added
- 增加通用 logging 配置
- 请求的响应中包含 butterfly 的版本信息

[Keep a Changelog]: https://keepachangelog.com/zh-CN/1.0.0/
[Semantic Versioning]: https://semver.org/lang/zh-CN/
[PEP-440]: https://www.python.org/dev/peps/pep-0440/
[1.0.2]: https://github.com/meetbill/butterfly/wiki/butterfly_man1.0.2

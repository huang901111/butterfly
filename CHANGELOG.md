Changelog
===
以下记录了项目中所有值得关注的变更内容，其格式基于 [Keep a Changelog]。

本项目版本遵守 [Semantic Versioning] 和 [PEP-440]。

## [1.0.4] - 2019-08-09 
### Added
- 支持 auth(pyjwt)

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

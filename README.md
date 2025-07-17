# hitokoto_plugin

自动在指定时间内获取一言，并发送到设置的群。

## 使用
你可以手动放置本项目至你的 `plugins` 目录下。

当然，也可以使用`git submodule`来添加本项目。

```bash
cd /path/to/ncatbot/
git submodule add https://github.com/Yang-qwq/hitokoto_plugin.git plugins/hitokoto_plugin
```

在NcatBot启动后，请依次在聊天环境下对机器人输入以下命令来配置插件：

```
/cfg Hitokoto.target_groups 114514;1919810  # 目标群组ID，多个用分号隔开
/cfg Hitokoto.time_lists 10:00;14:00;18:00  # 发送时间，多个用分号隔开
```

最后，请执行：

```
/cfg Hitokoto.is_configured true
```

后，重启NcatBot实例。

## 可选参数

### msg_prefix
如果你想在发送的消息前添加一些内容，可以设置 `msg_prefix` 参数。

但请注意，如果你希望输入是换行的，那么无论是前缀还是后缀，都必须以换行符 `\n` 结尾/开头。
```
/cfg Hitokoto.msg_prefix 一言：\n  # 发送的消息前缀
/cfg Hitokoto.msg_suffix   # 发送的消息后缀
```

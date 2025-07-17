# -*- coding: utf-8 -*-
from ncatbot.plugin import BasePlugin, CompatibleEnrollment
from ncatbot.utils.logger import get_log
import time
import requests

bot = CompatibleEnrollment  # 兼容回调函数注册器
_log = get_log("hitokoto_plugin")  # 日志记录器


class Hitokoto(BasePlugin):
    name = "Hitokoto"  # 插件名
    version = "0.0.1"  # 插件版本

    async def _batch_send_hitokoto(self, groups: list[int]) -> None:
        """批量发送消息到指定群组

        :param groups: 群组ID列表
        :return: None
        """
        _log.debug("正在拉取一言内容")
        res = requests.get("https://v1.hitokoto.cn/")
        if res.status_code != 200:
            _log.error("获取一言内容失败，状态码: %s", res.status_code)
            return None
        else:
            hitokoto_data = res.json()
            _message = f"{self.config['msg_prefix']}{hitokoto_data['hitokoto']} - {hitokoto_data['from']}{self.config['msg_suffix']}"

            # 遍历群组并发送消息
            for group in groups:
                await self.api.post_group_msg(group, _message)
                _log.debug("已发送一言到群组: %s", group)
                time.sleep(0.5)  # 防止 发送过快导致的限制
            return None

    async def on_load(self):
        self.register_config("time_lists", description="自动触发发送事件的事件，格式为`HH:MM;HH:MM;...`",
                             allowed_values=["str"], default="06:00;18:00")
        self.register_config("target_groups", description="自动触发发送事件的目标群组，格式为`123456789;987654321;...`",
                             allowed_values=["str"], default="0")
        self.register_config("msg_prefix", description="发送消息的前缀", allowed_values=["str"], default="")
        self.register_config("msg_suffix", description="发送消息的后缀", allowed_values=["str"], default="")
        self.register_config("is_configured", description="是否已配置好插件", allowed_values=["bool"], default=False)

        # 分割`target_groups`配置
        target_groups = self.config["target_groups"].split(";")

        # 分割并遍历`time_lists`配置
        time_lists = self.config["time_lists"].split(";")

        # 注册每个时间下的定时任务
        if self.config["is_configured"]:
            _log.debug("插件已配置，开始注册定时任务")
            for time_str in time_lists:
                self.add_scheduled_task(
                    self._batch_send_hitokoto, "send_hitokoto_cron.%s" % time_lists.index(time_str), time_str,
                    kwargs={"groups": target_groups}
                )
                _log.debug("已注册定时任务: %s", time_str)
        else:
            _log.warning("插件未配置，无法注册定时任务")

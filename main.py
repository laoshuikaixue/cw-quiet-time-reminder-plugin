from datetime import datetime
from .ClassWidgets.base import PluginBase


class Plugin(PluginBase):  # 定义插件类
    def __init__(self, cw_contexts, method):
        super().__init__(cw_contexts, method)  # 调用父类初始化方法

        # 若要引用插件目录的内容，需在目录前添加插件的工作目录：
        self.plugin_dir = self.cw_contexts['PLUGIN_PATH']
        self.notified_times = set()  # 用于记录已经发送通知的时间点

    def update(self, cw_contexts):
        super().update(cw_contexts)  # 获取最新接口
        current_time = datetime.now().strftime('%H:%M')

        if current_time in ['12:00', '18:50'] and current_time not in self.notified_times:
            self.method.send_notification(
                state=4,  # 自定义通知
                title='静班提醒',
                content='静班时间到！'
            )
            self.notified_times.add(current_time)

        # 清除过期通知时间点（防止 set 过大）
        if len(self.notified_times) > 2:
            self.notified_times = {t for t in self.notified_times if t in ['12:00', '18:50']}

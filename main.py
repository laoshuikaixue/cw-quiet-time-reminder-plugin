from datetime import datetime
from .ClassWidgets.base import PluginBase


class Plugin(PluginBase):  # 定义插件类
    def __init__(self, cw_contexts, method):
        super().__init__(cw_contexts, method)  # 调用父类初始化方法

        # 若要引用插件目录的内容，需在目录前添加插件的工作目录：
        self.plugin_dir = self.cw_contexts['PLUGIN_PATH']
        self.notified_times = set()  # 用于记录已经发送通知的时间点
        self.current_date = datetime.now().date()  # 记录当前日期

    def update(self, cw_contexts):
        super().update(cw_contexts)  # 获取最新接口
        now = datetime.now()
        current_time = now.strftime('%H:%M')
        today = now.date()

        # 如果日期变化（即到了第二天），清空已通知的时间点
        if today != self.current_date:
            self.notified_times.clear()
            self.current_date = today  # 更新当前日期

        if current_time in ['12:00', '18:50'] and current_time not in self.notified_times:
            self.method.send_notification(
                state=4,  # 自定义通知
                title='静班提醒',
                content='静班时间到！',
                duration=10000  # 通知持续时间（毫秒）
            )
            self.notified_times.add(current_time)

# KeyMaster

KeyMaster 是一个用 Python 编写的桌面应用程序，用于记录和分析键盘输入。它在后台运行，捕获键盘事件，并提供直观的统计信息。

## 功能

- 后台键盘事件记录
- 自动保存数据到 CSV 文件
- 按日期分类的数据存储
- 实时统计分析
- 可视化数据展示，包括按键频率和每小时分布图表

## 安装

1. 确保您的系统已安装 Python 3.7 或更高版本。

2. 克隆此仓库：
   ```
   git clone https://github.com/guliqianxun/KeyMaster
   cd KeyMaster
   ```

3. 安装所需的依赖：
   ```
   pip install -r requirements.txt
   ```
## 使用方法

1. 运行主程序：
   ```
   python main.py
   ```

2. 程序将在后台开始记录键盘输入。

3. 主窗口提供以下选项：
   - "手动保存"：立即保存当前记录的数据
   - "查看统计"：打开统计窗口，显示数据分析结果
   - "退出"：停止记录并关闭程序

4. 在统计窗口中，您可以查看：
   - 按键频率图表
   - 每小时按键分布图表
   - 总体摘要信息

## 文件结构

```
KeyMaster/
│
├── main.py                 # 主程序入口
├── config.py               # 配置文件
├── requirements.txt        # 依赖列表
│
├── model/
│   ├── key_logger.py       # 键盘记录器
│   ├── data_storage.py     # 数据存储
│   └── stats_analyzer.py   # 统计分析
│
├── view/
│   ├── main_window.py      # 主窗口 UI
│   └── statistics_view.py  # 统计窗口 UI
│
└── controller/
    └── app_controller.py   # 应用控制器
```

## 注意事项

- KeyMaster 会在后台持续记录键盘输入，请确保在不需要时关闭程序。
- 所有数据都保存在本地 CSV 文件中，不会上传到任何服务器。
- 建议定期备份 `key_logs` 文件夹中的数据文件。

## 贡献

欢迎提交问题报告和拉取请求。对于重大更改，请先开issue讨论您想要改变的内容。

## 许可

[MIT](https://choosealicense.com/licenses/mit/)

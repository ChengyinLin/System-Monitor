# System-Monitor
Local computer status monitoring for Windows system

🚀 使用方法
方案：复制到目标电脑运行
1. 将整个 scripts 文件夹复制到目标 Windows 电脑
2. 确保目标电脑有 Python + psutil（conda 或 pip install psutil）
3. 双击 启动系统监控.bat

仪表盘会显示该电脑的真实数据：
1. CPU 实时占用 + 每核心线程
2. 内存总量/已用/百分比
3. NVIDIA GPU（利用率、温度、显存）
4. 所有磁盘容量
5. 网络上传/下载速度
6.CPU/GPU 温度双圆环

📋 目标电脑需要的环境
1. 仅需 Python + psutil + Flask（conda 自带）
2. conda list psutil
3. conda list flask

如果没有，安装命令：
conda install psutil flask 或 pip install psutil flask

🔥 已实现功能

✅ 真实系统数据 — 通过 psutil + nvidia-smi 读取

✅ 自动刷新 — 每2秒更新一次

✅ 多机部署 — 复制到任意 Windows 电脑即可运行

✅ 局域网访问 — 同网络下其他设备可用浏览器打开

<img width="1575" height="706" alt="image" src="https://github.com/user-attachments/assets/3afee877-c953-4a62-9d2a-a94f5f07da66" />

## 项目简介
系统监控仪表盘是一个实时监控电脑硬件状态的Web应用，支持CPU、内存、GPU、磁盘、网络的实时监控，特别优化了Intel独立显卡的识别功能。


<img width="1571" height="707" alt="image" src="https://github.com/user-attachments/assets/b25ade76-45f5-4585-907c-bfbd295cd26c" />


# System Dashboard — 使用说明

🚀 使用方法
在本机运行：

## 快速启动

**方式一：双击运行**
```
双击「启动系统监控.bat」
```

**方式二：命令行**
```
cd scripts
python server.py
```

启动后浏览器自动打开 `http://127.0.0.1:18999`

## 局域网访问

在同一 WiFi/局域网下，其他设备用浏览器访问：
```
http://<电脑IP>:18999
```

如何查看本机 IP：
```powershell
ipconfig
```
找「IPv4 地址」即可，例如 `192.168.1.100`

## 实时数据

- **CPU**：总览 + 每核心线程占用率
- **内存**：总量 / 已用 / 百分比
- **GPU**：NVIDIA（利用率、温度、显存）— 需要 nvidia-smi
- **磁盘**：所有分区容量和使用率
- **网络**：实时上传/下载速度
- **温度**：CPU + GPU 双圆环

## 关闭

在运行的终端窗口按 `Ctrl + C`，然后关闭窗口即可。

## 依赖

仅使用 Python 标准库 + psutil（已在 conda 环境中）：
- `conda run python server.py`
- 或先 `conda activate` 再 `python server.py`



🌐 在其他电脑使用
1. 将所有文件（整个 scripts 文件夹）复制到目标 Windows 电脑
2. 确保目标电脑有 Python + psutil（conda 或 pip install psutil）
3. 双击 启动系统监控.bat

📋 目标电脑需要的环境
1. 仅需 Python + psutil + Flask（conda 自带）
2. conda list psutil   # 确保已安装
3. conda list flask    # 确保已安装

如果没有，安装命令：
1. conda install psutil flask
2. pip install psutil flask

🔥 已实现功能

✅ 真实系统数据 — 通过 psutil + nvidia-smi 读取

✅ 自动刷新 — 每2秒更新一次

✅ 多机部署 — 复制到任意 Windows 电脑即可运行

✅ 局域网访问 — 同网络下其他设备可用浏览器打开

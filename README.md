# System Dashboard — 使用说明

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

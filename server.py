# -*- coding: utf-8 -*-
"""
System Dashboard Server
读取本机真实系统数据，通过 HTTP 提供 API
"""

from flask import Flask, jsonify, send_from_directory
import psutil
import platform
import socket
import datetime
import threading
import time
import os
import webbrowser

app = Flask(__name__, static_folder='')

# 缓存数据，减少频繁调用
_cache = {}
_cache_lock = threading.Lock()
_cache_ttl = 1.0  # 缓存有效期（秒）

def _get_cpu_per_core():
    per = psutil.cpu_percent(interval=None, percpu=True)
    return per

def _get_mem():
    vm = psutil.virtual_memory()
    return {
        'total': round(vm.total / (1024**3), 1),
        'used': round(vm.used / (1024**3), 1),
        'free': round(vm.free / (1024**3), 1),
        'percent': vm.percent,
    }

def _get_disks():
    result = []
    for part in psutil.disk_partitions():
        if part.fstype == '' or 'cdrom' in part.opts.lower():
            continue
        try:
            usage = psutil.disk_usage(part.mountpoint)
            total = round(usage.total / (1024**3), 0)
            free = round(usage.free / (1024**3), 1)
            result.append({
                'id': part.device,
                'name': part.mountpoint,
                'total': int(total),
                'free': free,
                'used': round(usage.used / (1024**3), 1),
                'percent': usage.percent,
            })
        except:
            pass
    return result

def _get_gpu():
    # 尝试通过 nvidia-smi 获取 GPU 数据
    try:
        import subprocess
        out = subprocess.check_output(
            ['nvidia-smi', '--query-gpu=utilization.gpu,temperature.gpu,memory.used,memory.total',
             '--format=csv,noheader,nounits'],
            encoding='utf-8', timeout=3
        )
        parts = [x.strip() for x in out.strip().split(',')]
        return {
            'name': 'NVIDIA GPU',
            'util': float(parts[0]),
            'temp': float(parts[1]),
            'mem_used': float(parts[2]),
            'mem_total': float(parts[3]),
        }
    except Exception:
        return {
            'name': 'Unknown',
            'util': 0,
            'temp': 0,
            'mem_used': 0,
            'mem_total': 0,
        }

def _get_net():
    stats = psutil.net_io_counters()
    return {
        'sent': round(stats.bytes_sent / (1024**2), 1),
        'recv': round(stats.bytes_recv / (1024**2), 1),
    }

def _get_boot_time():
    bt = psutil.boot_time()
    now = time.time()
    uptime_s = now - bt
    days = int(uptime_s // 86400)
    hours = int((uptime_s % 86400) // 3600)
    minutes = int((uptime_s % 3600) // 60)
    return f'{days}天 {hours}小时'

def _refresh_cache():
    with _cache_lock:
        gpu = _get_gpu()
        _cache.update({
            'cpu': psutil.cpu_percent(interval=None),
            'cpu_cores': _get_cpu_per_core(),
            'mem': _get_mem(),
            'disks': _get_disks(),
            'gpu': gpu,
            'net': _get_net(),
            'uptime': _get_boot_time(),
            'hostname': socket.gethostname(),
            'platform': platform.platform(),
            'cpu_name': platform.processor(),
            'updated_at': datetime.datetime.now().strftime('%H:%M:%S'),
        })

# 启动时预填充缓存
_refresh_cache()

def background_refresh():
    while True:
        time.sleep(_cache_ttl)
        try:
            _refresh_cache()
        except Exception:
            pass

# 后台线程定期刷新
t = threading.Thread(target=background_refresh, daemon=True)
t.start()

@app.route('/')
def index():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'system_dashboard.html')

@app.route('/api/status')
def api_status():
    with _cache_lock:
        return jsonify(_cache.copy())

@app.route('/favicon.ico')
def favicon():
    return '', 204

if __name__ == '__main__':
    port = 18999
    url = f'http://127.0.0.1:{port}'

    print('=' * 50)
    print('  System Dashboard Server')
    print('=' * 50)
    print(f'  Local:  {url}')
    print(f'  Network: http://<your-ip>:{port}')
    print()
    print('  Press Ctrl+C to stop')
    print('=' * 50)

    try:
        webbrowser.open(url)
    except Exception:
        pass

    app.run(host='0.0.0.0', port=port, threaded=True, use_reloader=False)

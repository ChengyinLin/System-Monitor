# test API
import psutil
import platform
import socket
print('hostname:', socket.gethostname())
print('platform:', platform.platform())
print('cpu percent:', psutil.cpu_percent(interval=1))
print('cpu cores:', psutil.cpu_count())
mem = psutil.virtual_memory()
print('mem total:', round(mem.total / (1024**3), 1), 'GB')
print('mem used:', round(mem.used / (1024**3), 1), 'GB', round(mem.percent), '%')
disks = []
for part in psutil.disk_partitions():
    if part.fstype == '':
        continue
    try:
        u = psutil.disk_usage(part.mountpoint)
        disks.append({'id': part.device, 'name': part.mountpoint, 'total': round(u.total/(1024**3),0), 'free': round(u.free/(1024**3),1), 'percent': round(u.percent)})
    except:
        pass
for d in disks:
    print('disk:', d)
print('OK - all APIs work!')

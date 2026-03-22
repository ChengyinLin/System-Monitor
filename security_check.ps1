# Windows 安全巡检脚本
# 运行频率：每天早上 8:00

$Report = @()
$Report += "===== Windows 安全巡检报告 ====="
$Report += "时间: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
$Report += ""

# 1. Windows Defender 状态
$Report += "【1. 防病毒软件】"
try {
    $Defender = Get-MpComputerStatus -ErrorAction Stop
    if ($Defender.AntivirusEnabled) {
        $Report += "✅ Windows Defender: 已启用"
    } else {
        $Report += "🔴 Windows Defender: 已关闭 - 请立即启用！"
    }
    if ($Defender.RealTimeProtectionEnabled) {
        $Report += "✅ 实时保护: 已启用"
    } else {
        $Report += "🔴 实时保护: 已关闭 - 请立即启用！"
    }
    $Report += "病毒库更新: $($Defender.AntivirusSignatureLastUpdated)"
} catch {
    $Report += "⚠️ 无法检查 Defender 状态（权限不足）"
}
$Report += ""

# 2. 防火墙状态
$Report += "【2. 防火墙】"
try {
    $Firewall = Get-NetFirewallProfile -ErrorAction Stop
    foreach ($Profile in $Firewall) {
        $Status = if ($Profile.Enabled) { "✅ 已启用" } else { "🔴 已关闭" }
        $Report += "$($Profile.Name): $Status"
    }
} catch {
    $Report += "⚠️ 无法检查防火墙状态（权限不足）"
}
$Report += ""

# 3. 系统更新
$Report += "【3. 系统更新】"
try {
    $UpdateSession = New-Object -ComObject Microsoft.Update.Session
    $UpdateSearcher = $UpdateSession.CreateUpdateSearcher()
    $SearchResult = $UpdateSearcher.Search("IsInstalled=0 and Type='Software'")
    if ($SearchResult.Updates.Count -eq 0) {
        $Report += "✅ 系统已是最新状态"
    } else {
        $Report += "🔴 有 $($SearchResult.Updates.Count) 个更新待安装"
    }
} catch {
    $Report += "⚠️ 无法检查更新状态"
}
$Report += ""

# 4. 可疑进程（高内存占用）
$Report += "【4. 高占用进程 TOP 5】"
$Processes = Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First 5
foreach ($p in $Processes) {
    $Mem = [math]::Round($p.WorkingSet64/1MB, 1)
    $Report += "  $($p.ProcessName): ${Mem} MB"
}
$Report += ""

# 5. 网络连接（可疑连接）
$Report += "【5. 网络连接检查】"
try {
    $Connections = Get-NetTCPConnection -State Established -ErrorAction SilentlyContinue | Select-Object -First 10
    $Report += "当前活跃连接数: $($Connections.Count)"
} catch {
    $Report += "⚠️ 无法检查网络连接"
}
$Report += ""

# 6. 磁盘空间
$Report += "【6. 磁盘空间】"
$Drives = Get-PSDrive -PSProvider FileSystem | Where-Object {$_.Used -ne $null}
foreach ($Drive in $Drives) {
    $Used = [math]::Round($Drive.Used/1GB, 1)
    $Free = [math]::Round($Drive.Free/1GB, 1)
    $Total = $Used + $Free
    $Percent = [math]::Round($Used/$Total*100, 1)
    $Report += "  $($Drive.Name): ${Used}GB / ${Total}GB (已用 ${Percent}%)"
}
$Report += ""

# 7. 安全建议
$Report += "【7. 安全建议】"
$Report += "1. 确保 Windows Defender 已启用"
$Report += "2. 开启防火墙"
$Report += "3. 定期更新系统"
$Report += "4. 不打开未知来源的文件"
$Report += "5. 使用强密码"

$Report += ""
$Report += "===== 巡检完成 ====="

# 输出报告
$Report | ForEach-Object { Write-Host $_ }

# 保存报告
$ReportPath = "$env:USERPROFILE\SecurityReports"
if (-not (Test-Path $ReportPath)) {
    New-Item -ItemType Directory -Path $ReportPath -Force | Out-Null
}
$Report | Out-File -FilePath "$ReportPath\$(Get-Date -Format 'yyyy-MM-dd')_security_report.txt" -Encoding UTF8
Write-Host ""
Write-Host "报告已保存到: $ReportPath\$(Get-Date -Format 'yyyy-MM-dd')_security_report.txt"

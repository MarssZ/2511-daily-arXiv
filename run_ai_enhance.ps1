# AI 增强脚本 - 为论文生成中文摘要
# 使用阿里百炼 API（自动禁用代理）

param(
    [string]$DataFile = "",
    [int]$MaxWorkers = 10
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "arXiv 论文 AI 增强" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# 检查虚拟环境
if (-not (Test-Path ".venv")) {
    Write-Host "❌ 虚拟环境不存在，请先运行 'uv sync'" -ForegroundColor Red
    exit 1
}

# 如果没有指定文件，使用今天的日期
if ($DataFile -eq "") {
    $today = (Get-Date).ToString("yyyy-MM-dd")
    $DataFile = "data/$today.jsonl"
}

# 检查文件是否存在
if (-not (Test-Path $DataFile)) {
    Write-Host "❌ 文件不存在: $DataFile" -ForegroundColor Red
    Write-Host "请先运行爬虫或指定正确的文件路径" -ForegroundColor Yellow
    exit 1
}

# 统计论文数量
$paperCount = (Get-Content $DataFile | Measure-Object -Line).Lines
Write-Host "论文数量: $paperCount 篇"
Write-Host "数据文件: $DataFile"
Write-Host "并发数: $MaxWorkers"
Write-Host ""

# 激活虚拟环境
Write-Host "✓ 激活虚拟环境..." -ForegroundColor Green
.\.venv\Scripts\Activate.ps1

# 加载环境变量
if (Test-Path ".env") {
    Write-Host "✓ 加载配置文件..." -ForegroundColor Green
    Get-Content .env | ForEach-Object {
        if ($_ -match '^([^#][^=]+)=(.+)$') {
            $name = $matches[1].Trim()
            $value = $matches[2].Trim()
            Set-Item -Path "env:$name" -Value $value
        }
    }
}

# 显示配置
Write-Host "✓ API 配置:" -ForegroundColor Green
Write-Host "  模型: $env:MODEL_NAME"
Write-Host "  语言: $env:LANGUAGE"
Write-Host "  Base URL: $env:OPENAI_BASE_URL"
Write-Host ""

# 临时禁用代理（访问阿里百炼无需代理）
Write-Host "✓ 禁用代理（国内API）..." -ForegroundColor Green
$oldHttpProxy = $env:HTTP_PROXY
$oldHttpsProxy = $env:HTTPS_PROXY
$oldAllProxy = $env:ALL_PROXY

$env:HTTP_PROXY = ""
$env:HTTPS_PROXY = ""
$env:ALL_PROXY = ""

# 运行 AI 增强
Write-Host "✓ 开始生成中文摘要..." -ForegroundColor Green
Write-Host ""

cd ai
python enhance.py --data "../$DataFile" --max_workers $MaxWorkers
$exitCode = $LASTEXITCODE
cd ..

# 恢复代理设置
$env:HTTP_PROXY = $oldHttpProxy
$env:HTTPS_PROXY = $oldHttpsProxy
$env:ALL_PROXY = $oldAllProxy

# 检查结果
if ($exitCode -eq 0) {
    $language = $env:LANGUAGE
    if (-not $language) { $language = "Chinese" }

    $outputFile = $DataFile -replace '.jsonl$', "_AI_enhanced_$language.jsonl"

    if (Test-Path $outputFile) {
        $outputCount = (Get-Content $outputFile | Measure-Object -Line).Lines
        $fileSize = (Get-Item $outputFile).Length / 1KB

        Write-Host ""
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host "✅ AI 增强完成！" -ForegroundColor Green
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host "处理论文: $outputCount 篇"
        Write-Host "文件大小: $([math]::Round($fileSize, 2)) KB"
        Write-Host "输出文件: $outputFile"
        Write-Host ""
        Write-Host "💡 下一步: 运行 Markdown 转换" -ForegroundColor Yellow
        Write-Host "   cd to_md"
        Write-Host "   python convert.py --data ../$outputFile"
    } else {
        Write-Host "❌ 输出文件未生成" -ForegroundColor Red
    }
} else {
    Write-Host ""
    Write-Host "❌ AI 增强失败，退出码: $exitCode" -ForegroundColor Red
}

# ==========================================================
>> #  CTF Noise Generator - Windows Sandbox Edition
>> #  "Make the logs scream, but keep it harmless."
>> # ==========================================================
>>
>> param(
>>     [int]$DurationSeconds = 120,
>>     [int]$ThrottleMs = 50
>> )
>>
>> $endTime = (Get-Date).AddSeconds($DurationSeconds)
>>
>> $noiseWords = @(
>>     "panic", "trace", "debug", "fail", "retry", "ghost", "void",
>>     "packet", "echo", "shadow", "glitch", "404", "noise", "error"
>> )
>>
>> function Random-String($len = 12) {
>>     -join ((65..90) + (97..122) | Get-Random -Count $len | ForEach-Object {[char]$_})
>> }
>>
>> function Write-NoiseFile {
>>     $dir = "$env:TEMP\ctf_noise"
>>     New-Item -ItemType Directory -Force -Path $dir | Out-Null
>>
>>     $name = "$(Get-Random -InputObject $noiseWords)_$(Random-String).log"
>>     $path = Join-Path $dir $name
>>
>>     $content = @(
>>         "timestamp=$(Get-Date -Format o)"
>>         "status=unsettled"
>>         "payload=$(Random-String 32)"
>>         "mood=chaotic-neutral"
>>     )
>>
>>     Set-Content -Path $path -Value $content -Force
>> }
>>
>> function Invoke-ProcessNoise {
>>     $cmds = @(
>>         "ipconfig /all",
>>         "whoami",
>>         "tasklist",
>>         "echo CTF_NOISE",
>>         "ping 127.0.0.1 -n 1"
>>     )
>>
>>     Start-Process powershell -ArgumentList "-Command $($cmds | Get-Random)" -WindowStyle Hidden
>> }
>>
>> function Invoke-RegistryNoise {
>>     $base = "HKCU:\Software\CTFNoise"
>>     New-Item -Path $base -Force | Out-Null
>>
>>     $key = "$(Get-Random -InputObject $noiseWords)_$(Random-String 6)"
>>     $value = Random-String 20
>>
>>     New-ItemProperty -Path $base -Name $key -Value $value -Force | Out-Null
>> }
>>
>> function Invoke-EventNoise {
>>     try {
>>         $source = "CTFNoiseSource"
>>         if (-not [System.Diagnostics.EventLog]::SourceExists($source)) {
>>             New-EventLog -LogName Application -Source $source -ErrorAction SilentlyContinue
>>         }
>>
>>         Write-EventLog -LogName Application -Source $source -EntryType Information `
>>             -EventId (Get-Random -Minimum 1000 -Maximum 9999) `
>>             -Message "CTF noise event: $(Random-String 24)"
>>     } catch {
>>         # Sandbox-friendly fallback: just ignore if permissions fail
>>     }
>> }
>>
>> function Invoke-ThreadNoise {
>>     1..5 | ForEach-Object {
>>         Start-Job -ScriptBlock {
>>             1..20 | ForEach-Object {
>>                 [void](Get-Random)
>>                 Start-Sleep -Milliseconds (Get-Random -Minimum 10 -Maximum 50)
>>             }
>>         }
>>     } | Out-Null
>> }
>>
>> Write-Host "Starting CTF noise storm for $DurationSeconds seconds..." -ForegroundColor Cyan
>>
>> while ((Get-Date) -lt $endTime) {
>>
>>     switch (Get-Random -Minimum 1 -Maximum 6) {
>>         1 { Write-NoiseFile }
>>         2 { Invoke-ProcessNoise }
>>         3 { Invoke-RegistryNoise }
>>         4 { Invoke-EventNoise }
>>         5 { Invoke-ThreadNoise }
>>     }
>>
>>     Start-Sleep -Milliseconds $ThrottleMs
>> }
>>
>> Write-Host "Noise storm complete. Your logs are now emotionally unavailable." -ForegroundColor Yellow
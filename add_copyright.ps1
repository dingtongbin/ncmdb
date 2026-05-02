# PowerShell script to add copyright headers to source files

$pythonHeader = @"
# Copyright 2026 dingtongbin
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"@

$jsHeader = @"
/*
 * Copyright 2026 dingtongbin
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

"@

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Adding copyright headers to source files" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Process Python files
Write-Host "`nProcessing Python files..." -ForegroundColor Yellow
$pyFiles = Get-ChildItem -Path ".\ncmdb-server" -Filter "*.py" -Recurse | Where-Object {
    $_.FullName -notmatch 'migrations' -and 
    $_.FullName -notmatch '__pycache__' -and
    $_.FullName -notmatch 'venv'
}

$count = 0
foreach ($file in $pyFiles) {
    $content = Get-Content $file.FullName -Raw -Encoding UTF8
    
    if ($content -notmatch 'Copyright 2026 dingtongbin') {
        $newContent = $pythonHeader + $content
        Set-Content -Path $file.FullName -Value $newContent -Encoding UTF8 -NoNewline
        Write-Host "  Added: $($file.Name)" -ForegroundColor Green
        $count++
    }
}
Write-Host "Python files processed: $count" -ForegroundColor Cyan

# Process JavaScript/Vue files
Write-Host "`nProcessing JavaScript/Vue files..." -ForegroundColor Yellow
$jsFiles = Get-ChildItem -Path ".\ncmdb-view",".\netms-mobile" -Include "*.js","*.vue" -Recurse | Where-Object {
    $_.FullName -notmatch 'node_modules' -and 
    $_.FullName -notmatch 'dist' -and
    $_.FullName -notmatch '\.config\.js'
}

$count = 0
foreach ($file in $jsFiles) {
    $content = Get-Content $file.FullName -Raw -Encoding UTF8
    
    if ($content -notmatch 'Copyright 2026 dingtongbin') {
        $newContent = $jsHeader + $content
        Set-Content -Path $file.FullName -Value $newContent -Encoding UTF8 -NoNewline
        Write-Host "  Added: $($file.Name)" -ForegroundColor Green
        $count++
    }
}
Write-Host "JavaScript/Vue files processed: $count" -ForegroundColor Cyan

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Copyright headers added successfully!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

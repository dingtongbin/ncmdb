#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量为源代码文件添加 Apache 2.0 版权声明
"""
import os
import glob

# Python 文件版权头
PYTHON_HEADER = """# Copyright 2026 dingtongbin
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

"""

# JavaScript/Vue 文件版权头
JS_HEADER = """/*
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

"""

def add_copyright_to_file(file_path, header):
    """为单个文件添加版权声明"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已经有版权声明
        if 'Copyright 2026 dingtongbin' in content:
            print(f"跳过（已有版权）: {file_path}")
            return False
        
        # 在文件开头添加版权声明
        new_content = header + content
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"已添加版权: {file_path}")
        return True
    except Exception as e:
        print(f"错误处理文件 {file_path}: {e}")
        return False

def process_python_files(base_dir):
    """处理所有 Python 文件"""
    pattern = os.path.join(base_dir, '**/*.py')
    files = glob.glob(pattern, recursive=True)
    
    count = 0
    for file_path in files:
        # 跳过迁移文件和虚拟环境
        if 'migrations' in file_path or '__pycache__' in file_path or 'venv' in file_path:
            continue
        
        if add_copyright_to_file(file_path, PYTHON_HEADER):
            count += 1
    
    return count

def process_js_files(base_dir):
    """处理所有 JavaScript 和 Vue 文件"""
    patterns = [
        os.path.join(base_dir, '**/*.js'),
        os.path.join(base_dir, '**/*.vue')
    ]
    
    files = []
    for pattern in patterns:
        files.extend(glob.glob(pattern, recursive=True))
    
    count = 0
    for file_path in files:
        # 跳过 node_modules 和构建目录
        if 'node_modules' in file_path or 'dist' in file_path or '.config.js' in file_path:
            continue
        
        if add_copyright_to_file(file_path, JS_HEADER):
            count += 1
    
    return count

if __name__ == '__main__':
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    print("=" * 60)
    print("开始为源代码添加版权声明")
    print("=" * 60)
    
    # 处理后端 Python 文件
    backend_dir = os.path.join(project_root, 'ncmdb-server')
    if os.path.exists(backend_dir):
        print(f"\n处理后端文件: {backend_dir}")
        py_count = process_python_files(backend_dir)
        print(f"后端 Python 文件处理完成: {py_count} 个文件")
    
    # 处理前端 JS/Vue 文件
    frontend_dir = os.path.join(project_root, 'ncmdb-view')
    if os.path.exists(frontend_dir):
        print(f"\n处理前端文件: {frontend_dir}")
        js_count = process_js_files(frontend_dir)
        print(f"前端 JS/Vue 文件处理完成: {js_count} 个文件")
    
    # 处理移动端文件
    mobile_dir = os.path.join(project_root, 'netms-mobile')
    if os.path.exists(mobile_dir):
        print(f"\n处理移动端文件: {mobile_dir}")
        mobile_count = process_js_files(mobile_dir)
        print(f"移动端 JS/Vue 文件处理完成: {mobile_count} 个文件")
    
    print("\n" + "=" * 60)
    print("版权声明添加完成！")
    print("=" * 60)

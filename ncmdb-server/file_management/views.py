from django.http import FileResponse
from rest_framework.decorators import api_view, permission_classes

from user.permissions import IsNetworkEngineer

# 支持预览的文件扩展名
TEXT_FILE_EXTENSIONS = ['.txt', '.md', '.cfg', '.conf', '.ini', '.log', '.json', '.xml', '.yaml', '.yml', '.py', '.js',
                        '.css', '.html']


@api_view(['GET'])
@permission_classes([IsNetworkEngineer])
def list_directory(request):
    """
    列出指定目录下的所有文件和文件夹
    权限：网络管理员
    """
    relative_path = request.GET.get('path', '')

    # 安全检查
    if '..' in relative_path:
        return JsonResponse({'success': False, 'error': '无效路径'}, status=status.HTTP_400_BAD_REQUEST)

    base_path = os.path.join(settings.MEDIA_ROOT, 'filem')
    target_path = os.path.join(base_path, relative_path.lstrip('/')) if relative_path else base_path

    if not os.path.exists(target_path):
        return JsonResponse({'success': False, 'error': '目录不存在'}, status=status.HTTP_404_NOT_FOUND)

    if not os.path.isdir(target_path):
        return JsonResponse({'success': False, 'error': '路径不是目录'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        items = []
        for item_name in os.listdir(target_path):
            item_path = os.path.join(target_path, item_name)
            stat_info = os.stat(item_path)
            item_type = 'folder' if os.path.isdir(item_path) else 'file'

            items.append(
                {'name': item_name, 'type': item_type, 'size': stat_info.st_size if item_type == 'file' else None,
                    'size_format': format_file_size(stat_info.st_size) if item_type == 'file' else None,
                    'modified_time': datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                    'created_time': datetime.fromtimestamp(stat_info.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
                    'path': os.path.join(relative_path, item_name).replace('\\', '/') if relative_path else item_name,
                    'is_text_file': is_text_file(item_name) if item_type == 'file' else False})

        # 排序：文件夹在前，然后按名称排序
        items.sort(key=lambda x: (x['type'] == 'file', x['name'].lower()))

        return JsonResponse({'success': True, 'data': {'path': relative_path, 'items': items}})
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'读取目录失败：{str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsNetworkEngineer])
def upload_files(request):
    """
    上传文件（支持单/多文件）
    权限：网络管理员
    """
    if not request.FILES:
        return JsonResponse({'success': False, 'error': '未提供文件'}, status=status.HTTP_400_BAD_REQUEST)

    target_path = request.POST.get('path', '')
    overwrite = request.POST.get('overwrite', 'false').lower() == 'true'

    if '..' in target_path:
        return JsonResponse({'success': False, 'error': '无效路径'}, status=status.HTTP_400_BAD_REQUEST)

    base_path = os.path.join(settings.MEDIA_ROOT, 'filem')
    target_dir = os.path.join(base_path, target_path.lstrip('/')) if target_path else base_path

    if not os.path.exists(target_dir):
        return JsonResponse({'success': False, 'error': '目标目录不存在'}, status=status.HTTP_404_NOT_FOUND)

    if not os.path.isdir(target_dir):
        return JsonResponse({'success': False, 'error': '目标路径不是目录'}, status=status.HTTP_400_BAD_REQUEST)

    uploaded_files = []
    errors = []

    for field_name in request.FILES:
        files_list = request.FILES.getlist(field_name)
        for uploaded_file in files_list:
            try:
                file_path = os.path.join(target_dir, uploaded_file.name)

                if os.path.exists(file_path):
                    if not overwrite:
                        errors.append(f'文件 {uploaded_file.name} 已存在')
                        continue
                    else:
                        os.remove(file_path)

                with open(file_path, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)

                stat_info = os.stat(file_path)
                relative_path = os.path.relpath(file_path, base_path).replace('\\', '/')

                uploaded_files.append({'name': uploaded_file.name, 'path': relative_path, 'size': stat_info.st_size,
                    'size_format': format_file_size(stat_info.st_size)})
            except Exception as e:
                errors.append(f'上传文件 {uploaded_file.name} 失败：{str(e)}')

    response_data = {'success': len(uploaded_files) > 0 and len(errors) == 0, 'uploaded_files': uploaded_files,
        'errors': errors if errors else None, 'message': f'成功上传 {len(uploaded_files)} 个文件'}

    return JsonResponse(response_data,
                        status=status.HTTP_201_CREATED if uploaded_files else status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsNetworkEngineer])
def create_folder(request):
    """
    创建文件夹
    权限：网络管理员
    """
    try:
        data = json.loads(request.body)
        parent_path = data.get('path', '')
        folder_name = data.get('name')

        if not folder_name:
            return JsonResponse({'success': False, 'error': '文件夹名称不能为空'}, status=status.HTTP_400_BAD_REQUEST)

        if any(c in folder_name for c in ['/', '\\', '..', ':', '*', '?', '"', '<', '>', '|']):
            return JsonResponse({'success': False, 'error': '文件夹名称包含非法字符'},
                                status=status.HTTP_400_BAD_REQUEST)

        if '..' in parent_path:
            return JsonResponse({'success': False, 'error': '无效路径'}, status=status.HTTP_400_BAD_REQUEST)

        base_path = os.path.join(settings.MEDIA_ROOT, 'filem')
        target_parent_path = os.path.join(base_path, parent_path.lstrip('/')) if parent_path else base_path
        new_folder_path = os.path.join(target_parent_path, folder_name)

        if not os.path.exists(target_parent_path):
            return JsonResponse({'success': False, 'error': '父目录不存在'}, status=status.HTTP_404_NOT_FOUND)

        if not os.path.isdir(target_parent_path):
            return JsonResponse({'success': False, 'error': '父路径不是目录'}, status=status.HTTP_400_BAD_REQUEST)

        if os.path.exists(new_folder_path):
            return JsonResponse({'success': False, 'error': '同名文件或文件夹已存在'},
                                status=status.HTTP_400_BAD_REQUEST)

        os.makedirs(new_folder_path)

        return JsonResponse({'success': True, 'data': {'name': folder_name,
            'path': os.path.join(parent_path, folder_name).replace('\\', '/') if parent_path else folder_name,
            'type': 'folder'}}, status=status.HTTP_201_CREATED)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': '请求数据格式错误'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'创建文件夹失败：{str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsNetworkEngineer])
def rename_item(request):
    """
    重命名文件/文件夹
    权限：网络管理员
    """
    try:
        data = json.loads(request.body)
        current_path = data.get('path')
        new_name = data.get('new_name')

        if not current_path or not new_name:
            return JsonResponse({'success': False, 'error': '路径和新名称都不能为空'},
                                status=status.HTTP_400_BAD_REQUEST)

        if any(c in new_name for c in ['/', '\\', '..', ':', '*', '?', '"', '<', '>', '|']):
            return JsonResponse({'success': False, 'error': '新名称包含非法字符'}, status=status.HTTP_400_BAD_REQUEST)

        if '..' in current_path:
            return JsonResponse({'success': False, 'error': '无效路径'}, status=status.HTTP_400_BAD_REQUEST)

        base_path = os.path.join(settings.MEDIA_ROOT, 'filem')
        full_current_path = os.path.join(base_path, current_path.lstrip('/'))
        parent_dir = os.path.dirname(full_current_path)
        new_path = os.path.join(parent_dir, new_name)

        if not os.path.exists(full_current_path):
            return JsonResponse({'success': False, 'error': '文件/文件夹不存在'}, status=status.HTTP_404_NOT_FOUND)

        if os.path.exists(new_path):
            return JsonResponse({'success': False, 'error': '同名文件或文件夹已存在'},
                                status=status.HTTP_400_BAD_REQUEST)

        os.rename(full_current_path, new_path)

        relative_new_path = os.path.relpath(new_path, base_path).replace('\\', '/')

        return JsonResponse(
            {'success': True, 'data': {'old_path': current_path, 'new_path': relative_new_path, 'new_name': new_name}})
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': '请求数据格式错误'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'重命名失败：{str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsNetworkEngineer])
def delete_item(request):
    """
    删除文件或文件夹
    权限：网络管理员
    """
    try:
        data = json.loads(request.body)
        item_path = data.get('path')

        if not item_path:
            return JsonResponse({'success': False, 'error': '路径不能为空'}, status=status.HTTP_400_BAD_REQUEST)

        if '..' in item_path:
            return JsonResponse({'success': False, 'error': '无效路径'}, status=status.HTTP_400_BAD_REQUEST)

        base_path = os.path.join(settings.MEDIA_ROOT, 'filem')
        full_path = os.path.join(base_path, item_path.lstrip('/'))

        if not os.path.exists(full_path):
            return JsonResponse({'success': False, 'error': '文件/文件夹不存在'}, status=status.HTTP_404_NOT_FOUND)

        if os.path.isdir(full_path):
            shutil.rmtree(full_path)
            item_type = 'folder'
        else:
            os.remove(full_path)
            item_type = 'file'

        return JsonResponse(
            {'success': True, 'message': f'成功删除{item_type}', 'data': {'path': item_path, 'type': item_type}})
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': '请求数据格式错误'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'删除失败：{str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsNetworkEngineer])
def preview_file(request):
    """
    预览文本文件内容
    支持：txt, md, cfg, conf, ini, log, json, xml, yaml, yml, py, js, css, html
    """
    file_path = request.GET.get('path')
    if not file_path:
        return JsonResponse({'success': False, 'error': '文件路径不能为空'}, status=status.HTTP_400_BAD_REQUEST)
    if '..' in file_path:
        return JsonResponse({'success': False, 'error': '无效路径'}, status=status.HTTP_400_BAD_REQUEST)
    base_path = os.path.join(settings.MEDIA_ROOT, 'filem')
    full_file_path = os.path.join(base_path, file_path.lstrip('/'))
    if not os.path.exists(full_file_path):
        return JsonResponse({'success': False, 'error': '文件不存在'}, status=status.HTTP_404_NOT_FOUND)

    if not os.path.isfile(full_file_path):
        return JsonResponse({'success': False, 'error': '指定路径不是文件'}, status=status.HTTP_400_BAD_REQUEST)

    if not is_text_file(file_path):
        return JsonResponse({'success': False, 'error': '不支持预览此文件类型'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        with open(full_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        return JsonResponse(
            {'success': True, 'data': {'path': file_path, 'name': os.path.basename(file_path), 'content': content}})
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'读取文件失败：{str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsNetworkEngineer])
def download_file(request):
    """
    下载文件
    """
    file_path = request.GET.get('path')

    if not file_path:
        return HttpResponseBadRequest('文件路径不能为空')

    if '..' in file_path:
        return HttpResponseBadRequest('无效路径')

    base_path = os.path.join(settings.MEDIA_ROOT, 'filem')
    full_file_path = os.path.join(base_path, file_path.lstrip('/'))

    if not os.path.exists(full_file_path):
        return HttpResponseNotFound('文件不存在')

    if not os.path.isfile(full_file_path):
        return HttpResponseBadRequest('指定路径不是文件')

    try:
        filename = os.path.basename(full_file_path)
        from urllib.parse import quote
        response = FileResponse(open(full_file_path, 'rb'))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = f"attachment; filename*=UTF-8''{quote(filename)}"
        return response

    except Exception as e:
        return JsonResponse({'error': f'下载失败：{str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def format_file_size(size_bytes):
    """格式化文件大小"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"


def is_text_file(filename):
    """判断是否为文本文件"""
    ext = os.path.splitext(filename)[1].lower()
    return ext in TEXT_FILE_EXTENSIONS


import json
import os
import shutil
import base64
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest
from rest_framework import status
from rest_framework.decorators import api_view
from datetime import datetime
from setting import settings
from user.permissions import IsNetworkEngineer


@api_view(['POST'])
@permission_classes([IsNetworkEngineer])
def download_file(request):
    """
    下载文件（POST 方式，安全）
    权限：网络管理员
    返回文件 base64 编码，前端下载
    """
    try:
        data = request.data
        file_path = data.get('path')

        if not file_path:
            return JsonResponse({'success': False, 'error': '文件路径不能为空'}, status=status.HTTP_400_BAD_REQUEST)

        if '..' in file_path:
            return JsonResponse({'success': False, 'error': '无效路径'}, status=status.HTTP_400_BAD_REQUEST)

        base_path = os.path.join(settings.MEDIA_ROOT, 'filem')
        full_file_path = os.path.join(base_path, file_path.lstrip('/'))

        if not os.path.exists(full_file_path):
            return JsonResponse({'success': False, 'error': '文件不存在'}, status=status.HTTP_404_NOT_FOUND)

        if not os.path.isfile(full_file_path):
            return JsonResponse({'success': False, 'error': '指定路径不是文件'}, status=status.HTTP_400_BAD_REQUEST)

        # 读取文件并 base64 编码
        with open(full_file_path, 'rb') as f:
            file_content = base64.b64encode(f.read()).decode('utf-8')

        return JsonResponse({'success': True,
            'data': {'name': os.path.basename(full_file_path), 'content': file_content,
                'type': 'application/octet-stream'}})
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'下载失败：{str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

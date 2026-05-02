<template>
  <div class="file-manager-container">
    <!-- 顶部导航栏 -->
    <el-card class="nav-card" shadow="never">
      <div class="nav-content">
        <div class="breadcrumb-section">
          <el-icon @click="navigateTo('')" class="home-icon"><Folder /></el-icon>
          <span class="current-path">{{ currentPath || '根目录' }}</span>
        </div>
        <el-button
            v-if="currentPath"
            @click="goBack"
            :disabled="!currentPath"
            size="small"
        >
          <el-icon><ArrowLeft /></el-icon>
          返回上级
        </el-button>
      </div>
    </el-card>

    <!-- 操作按钮栏 -->
    <el-card class="toolbar-card" shadow="never">
      <div class="toolbar-content">
        <el-button type="success" @click="showUploadDialog = true">
          <el-icon><Upload /></el-icon>
          上传文件
        </el-button>
        <el-button type="primary" @click="showCreateFolder = true">
          <el-icon><FolderAdd /></el-icon>
          新建文件夹
        </el-button>
      </div>
    </el-card>

    <!-- 文件列表 -->
    <el-card class="file-list-card" shadow="never">
      <el-table
          v-loading="loading"
          :data="fileList"
          style="width: 100%"
          border
          stripe
          @row-dblclick="handleRowDblClick"
      >
        <el-table-column prop="name" label="名称" min-width="300">
          <template #default="{ row }">
            <div class="file-name">
              <el-icon :size="20" :color="row.type === 'folder' ? '#409EFF' : '#909399'">
                <Folder v-if="row.type === 'folder'" />
                <Document v-else />
              </el-icon>
              <span>{{ row.name }}</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="size_format" label="大小" width="120" align="right">
          <template #default="{ row }">
            {{ row.type === 'folder' ? '-' : row.size_format }}
          </template>
        </el-table-column>

        <el-table-column prop="modified_time" label="修改时间" width="180" />

        <el-table-column label="操作" width="280" fixed="right">
          <template #default="{ row }">
            <div class="action-buttons">
              <el-button
                  v-if="row.type === 'folder'"
                  type="primary"
                  size="small"
                  @click="enterFolder(row)"
              >
                进入
              </el-button>

              <el-button
                  v-if="row.is_text_file"
                  type="info"
                  size="small"
                  @click="handlePreview(row)"
              >
                预览
              </el-button>

              <el-button
                  v-if="row.type === 'file'"
                  type="success"
                  size="small"
                  @click="handleDownload(row)"
              >
                下载
              </el-button>

              <el-dropdown trigger="click" @command="handleCommand">
                <el-button size="small">
                  更多<el-icon class="el-icon--right"><ArrowDown /></el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item :command="{ command: 'rename', data: row }">
                      <el-icon><Edit /></el-icon> 重命名
                    </el-dropdown-item>
                    <el-dropdown-item
                        :command="{ command: 'delete', data: row }"
                        style="color: #f56c6c"
                    >
                      <el-icon><Delete /></el-icon> 删除
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </template>
        </el-table-column>
      </el-table>

      <el-empty v-if="!loading && fileList.length === 0" description="暂无文件" />
    </el-card>

    <!-- 上传文件对话框 -->
    <el-dialog
        v-model="showUploadDialog"
        title="上传文件"
        width="500px"
    >
      <el-upload
          ref="uploadRef"
          drag
          :auto-upload="false"
          :on-change="handleFileChange"
          :on-remove="handleFileRemove"
          :file-list="uploadFileList"
          multiple
      >
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          拖拽文件到此处或<em>点击上传</em>
        </div>
      </el-upload>

      <template #footer>
        <el-button @click="showUploadDialog = false">取消</el-button>
        <el-button type="primary" @click="submitUpload" :loading="uploading">
          开始上传
        </el-button>
      </template>
    </el-dialog>

    <!-- 新建文件夹对话框 -->
    <el-dialog
        v-model="showCreateFolder"
        title="新建文件夹"
        width="400px"
    >
      <el-form :model="folderForm" label-width="80px">
        <el-form-item label="文件夹名">
          <el-input v-model="folderForm.name" placeholder="请输入文件夹名称" />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="showCreateFolder = false">取消</el-button>
        <el-button type="primary" @click="submitCreateFolder" :loading="creating">
          确定
        </el-button>
      </template>
    </el-dialog>

    <!-- 重命名对话框 -->
    <el-dialog
        v-model="showRename"
        title="重命名"
        width="400px"
    >
      <el-form :model="renameForm" label-width="80px">
        <el-form-item label="新名称">
          <el-input v-model="renameForm.new_name" placeholder="请输入新名称" />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="showRename = false">取消</el-button>
        <el-button type="primary" @click="submitRename" :loading="renaming">
          确定
        </el-button>
      </template>
    </el-dialog>

    <!-- 文件预览对话框 -->
    <el-dialog
        v-model="showPreview"
        :title="previewData.name"
        width="800px"
    >
      <div class="preview-content">
        <pre>{{ previewData.content }}</pre>
      </div>

      <template #footer>
        <el-button @click="showPreview = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Folder, FolderAdd, Document, Upload, UploadFilled,
  ArrowLeft, ArrowDown, Edit, Delete
} from '@element-plus/icons-vue'
import {
  listDirectory,
  uploadFiles,
  createFolder,
  renameItem,
  deleteItem,
  previewFile as previewFileApi,
  downloadFile as downloadFileApi
} from '../api/file_api.js'

// 当前路径
const currentPath = ref('')
const fileList = ref([])
const loading = ref(false)

// 对话框控制
const showUploadDialog = ref(false)
const showCreateFolder = ref(false)
const showRename = ref(false)
const showPreview = ref(false)

// 上传相关
const uploadRef = ref(null)
const uploadFileList = ref([])
const uploading = ref(false)

// 新建文件夹
const folderForm = reactive({
  name: ''
})
const creating = ref(false)

// 重命名
const renameForm = reactive({
  path: '',
  new_name: ''
})
const renaming = ref(false)

// 预览
const previewData = reactive({
  name: '',
  content: ''
})

// 加载目录
const loadDirectory = async (path = '') => {
  loading.value = true
  try {
    const response = await listDirectory({ path })
    if (response.success) {
      fileList.value = response.data.items
      currentPath.value = response.data.path
    } else {
      ElMessage.error(response.error || '加载失败')
    }
  } catch (error) {
    console.error('加载失败:', error)
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

// 进入文件夹
const enterFolder = (row) => {
  loadDirectory(row.path)
}

// 双击进入
const handleRowDblClick = (row) => {
  if (row.type === 'folder') {
    enterFolder(row)
  }
}

// 返回上级
const goBack = () => {
  if (!currentPath.value) return
  const parts = currentPath.value.split('/')
  parts.pop()
  const parentPath = parts.join('/')
  loadDirectory(parentPath)
}

// 导航到指定路径
const navigateTo = (path) => {
  loadDirectory(path)
}

// 处理文件变化
const handleFileChange = (file) => {
  uploadFileList.value.push(file)
}

const handleFileRemove = (file) => {
  uploadFileList.value = uploadFileList.value.filter(f => f.uid !== file.uid)
}

// 提交上传
const submitUpload = async () => {
  if (uploadFileList.value.length === 0) {
    ElMessage.warning('请选择文件')
    return
  }

  uploading.value = true
  try {
    const formData = new FormData()
    uploadFileList.value.forEach(file => {
      formData.append('files', file.raw)
    })
    formData.append('path', currentPath.value)
    formData.append('overwrite', 'false')

    const response = await uploadFiles(formData)
    if (response.success) {
      ElMessage.success(response.message)
      showUploadDialog.value = false
      uploadFileList.value = []
      await loadDirectory(currentPath.value)
    } else {
      ElMessage.error(response.errors?.[0] || '上传失败')
    }
  } catch (error) {
    console.error('上传失败:', error)
    ElMessage.error('上传失败')
  } finally {
    uploading.value = false
  }
}

// 创建文件夹
const submitCreateFolder = async () => {
  if (!folderForm.name) {
    ElMessage.warning('请输入文件夹名称')
    return
  }

  creating.value = true
  try {
    const response = await createFolder({
      path: currentPath.value,
      name: folderForm.name
    })

    if (response.success) {
      ElMessage.success('创建成功')
      showCreateFolder.value = false
      folderForm.name = ''
      await loadDirectory(currentPath.value)
    } else {
      ElMessage.error(response.error || '创建失败')
    }
  } catch (error) {
    console.error('创建失败:', error)
    ElMessage.error('创建失败')
  } finally {
    creating.value = false
  }
}

// 处理命令
const handleCommand = ({ command, data }) => {
  if (command === 'rename') {
    renameForm.path = data.path
    renameForm.new_name = data.name
    showRename.value = true
  } else if (command === 'delete') {
    confirmDelete(data)
  }
}

// 确认删除
const confirmDelete = async (row) => {
  try {
    await ElMessageBox.confirm(
        `确定要删除"${row.name}"吗？`,
        '删除确认',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
    )

    const response = await deleteItem({ path: row.path })
    if (response.success) {
      ElMessage.success('删除成功')
      await loadDirectory(currentPath.value)
    } else {
      ElMessage.error(response.error || '删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

// 提交重命名
const submitRename = async () => {
  if (!renameForm.new_name) {
    ElMessage.warning('请输入新名称')
    return
  }

  renaming.value = true
  try {
    const response = await renameItem({
      path: renameForm.path,
      new_name: renameForm.new_name
    })

    if (response.success) {
      ElMessage.success('重命名成功')
      showRename.value = false
      await loadDirectory(currentPath.value)
    } else {
      ElMessage.error(response.error || '重命名失败')
    }
  } catch (error) {
    console.error('重命名失败:', error)
    ElMessage.error('重命名失败')
  } finally {
    renaming.value = false
  }
}

// 预览文件
const handlePreview = async (row) => {
  try {
    const response = await previewFileApi({ path: row.path })
    if (response.success) {
      previewData.name = response.data.name
      previewData.content = response.data.content
      showPreview.value = true
    } else {
      ElMessage.error(response.error || '预览失败')
    }
  } catch (error) {
    console.error('预览失败:', error)
    ElMessage.error('预览失败')
  }
}

// 下载文件
const handleDownload = async (row) => {
  try {
    const response = await downloadFileApi({ path: row.path })
    if (response.success) {
      // base64 转 blob 下载
      const binaryString = atob(response.data.content)
      const bytes = new Uint8Array(binaryString.length)
      for (let i = 0; i < binaryString.length; i++) {
        bytes[i] = binaryString.charCodeAt(i)
      }
      const blob = new Blob([bytes], { type: 'application/octet-stream' })
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = response.data.name
      link.click()
      window.URL.revokeObjectURL(url)
      ElMessage.success('下载成功')
    } else {
      ElMessage.error(response.error || '下载失败')
    }
  } catch (error) {
    console.error('下载失败:', error)
    ElMessage.error('下载失败')
  }
}

onMounted(() => {
  loadDirectory()
})
</script>

<style scoped>
.file-manager-container {
  padding: 15px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.nav-card, .toolbar-card, .file-list-card {
  margin-bottom: 15px;
}

.nav-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.breadcrumb-section {
  display: flex;
  align-items: center;
  gap: 10px;
}

.home-icon {
  cursor: pointer;
  font-size: 20px;
  color: #409EFF;
}

.current-path {
  font-size: 14px;
  color: #606266;
}

.toolbar-content {
  display: flex;
  gap: 10px;
}

.file-name {
  display: flex;
  align-items: center;
  gap: 8px;
}

.action-buttons {
  display: flex;
  gap: 5px;
}

.preview-content {
  max-height: 500px;
  overflow: auto;
  background: #f5f7fa;
  padding: 15px;
  border-radius: 4px;
}

.preview-content pre {
  margin: 0;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 13px;
  line-height: 1.6;
  white-space: pre-wrap;
  word-wrap: break-word;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .file-manager-container {
    padding: 10px;
  }

  .nav-content {
    flex-direction: column;
    gap: 10px;
  }

  .toolbar-content {
    flex-wrap: wrap;
  }

  .toolbar-content .el-button {
    flex: 1;
    min-width: 120px;
  }

  :deep(.el-table) {
    font-size: 12px;
  }

  :deep(.el-table .cell) {
    padding: 8px 5px;
  }
}
</style>

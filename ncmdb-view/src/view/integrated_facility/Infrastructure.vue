<script setup>
import {onMounted, reactive, ref} from 'vue'
import {ElMessage, ElMessageBox} from 'element-plus'
import {
  ArrowDown,
  ArrowRight,
  Delete,
  Edit,
  Grid,
  MoreFilled,
  OfficeBuilding,
  Plus,
  Refresh,
  Search
} from '@element-plus/icons-vue'
import {
  createConnection,
  createEquipmentRoom,
  createInfrastructureEquipment,
  createRack,
  deleteConnection,
  deleteEquipmentRoom,
  deleteInfrastructureEquipment,
  deleteRack,
  getConnections,
  getEquipmentRooms,
  getInfrastructureEquipment,
  getInfrastructureEquipmentDetail,
  getRacks,
  updateConnection,
  updateEquipmentRoom,
  updateInfrastructureEquipment,
  updateRack
} from '../../api/infrastructure.js'

// 左侧边栏数据
const equipmentRooms = ref([])
const selectedRoomId = ref(null)
const selectedRackId = ref(null)
const currentRack = ref(null)
const showCreateRoomDialog = ref(false)
const showRenameRoomDialog = ref(false)
const showCreateRackDialog = ref(false)
const showRenameRackDialog = ref(false)
const currentRoomId = ref(null)
const currentRoomName = ref('')
const currentRackId = ref(null)

// 右侧设备数据
const deviceList = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(100)
const total = ref(0)
const searchValue = ref('')
const selectedDevices = ref([])
const allRacks = ref([])

// 表单数据
const roomForm = reactive({
  name: '',
  location: '',
  remarks: ''
})

const rackForm = reactive({
  name: '',
  height: 42,
  width: 600,
  depth: 1000,
  remarks: ''
})

const deviceForm = reactive({
  name: '',
  type: '',
  rack_id: '',
  brand: '',
  model: '',
  serial_number: '',
  device_number: '',
  is_active: true,
  remarks: ''
})

const connectionForm = reactive({
  device_id: null,
  home_interface: '',
  peer_interface: '',
  peer_device: '',
  connection_type: '',
  remarks: ''
})

// 控制变量
const operating = ref(false)
const showCreateDeviceDialogVisible = ref(false)
const isEditDevice = ref(false)
const currentDeviceId = ref(null)
const showDeviceDetailDrawer = ref(false)
const currentDevice = ref(null)
const connectionList = ref([])
const showAddConnection = ref(false)
const isEditConnection = ref(false)
const currentConnectionId = ref(null)

// 加载设备间列表
const loadEquipmentRooms = async () => {
  try {
    const res = await getEquipmentRooms()
    console.log('设备间 API 响应:', res)
    const dataList = res.data?.results || res.data || []
    equipmentRooms.value = Array.isArray(dataList) ? dataList.map(room => ({
      ...room,
      expanded: false,
      racks: [],
      racksLoaded: false
    })) : []
  } catch (error) {
    console.error('加载设备间列表错误:', error)
    ElMessage.error('加载设备间列表失败')
  }
}

// 切换设备间展开/收起
const toggleRoomExpand = async (room) => {
  equipmentRooms.value.forEach(r => {
    if (r.id !== room.id) {
      r.expanded = false
    }
  })

  room.expanded = !room.expanded

  if (room.expanded) {
    try {
      console.log(`加载设备间 ${room.id} 的机柜列表`)
      const res = await getRacks({ equipment_room_id: room.id })
      console.log('机柜 API 响应:', res)

      room.racks = []
      room.racksLoaded = false

      const rackList = res.data?.results || res.data || []
      if (Array.isArray(rackList)) {
        room.racks = rackList
        room.racksLoaded = true
      }
    } catch (error) {
      console.error('加载机柜列表失败:', error)
      ElMessage.error('加载机柜列表失败')
      room.racks = []
      room.racksLoaded = false
    }
  } else {
    room.racks = []
    room.racksLoaded = false
  }
}

// 选择机柜
const selectRack = async (rack, room) => {
  console.log('选择机柜:', rack, '所属设备间:', room)

  equipmentRooms.value.forEach(r => {
    r.racks?.forEach(rk => {
      if (rk.id !== rack.id) {
        // 不主动设置 false
      }
    })
  })

  selectedRackId.value = rack.id
  selectedRoomId.value = room ? room.id : null
  currentRack.value = rack
  currentRackId.value = rack.id

  currentPage.value = 1
  searchValue.value = ''

  console.log('使用机柜 ID 查询设备:', rack.id)

  await loadDevices()
}

// 处理设备间操作
const handleRoomCommand = ({ command, data }) => {
  if (command === 'rename') {
    currentRoomId.value = data.id
    currentRoomName.value = data.name
    roomForm.name = data.name
    roomForm.location = data.location || ''
    roomForm.remarks = data.remarks || ''
    showRenameRoomDialog.value = true
  } else if (command === 'add_rack') {
    currentRoomId.value = data.id
    currentRoomName.value = data.name
    rackForm.name = ''
    rackForm.height = 42
    rackForm.width = 600
    rackForm.depth = 1000
    rackForm.remarks = ''
    showCreateRackDialog.value = true
  } else if (command === 'delete') {
    confirmDeleteRoom(data.id)
  }
}

// 处理机柜操作
const handleRackCommand = ({ command, data }) => {
  if (command === 'rename') {
    currentRackId.value = data.id
    rackForm.name = data.name
    rackForm.height = data.height || 42
    rackForm.width = data.width || 600
    rackForm.depth = data.depth || 1000
    rackForm.remarks = data.remarks || ''
    showRenameRackDialog.value = true
  } else if (command === 'delete') {
    confirmDeleteRack(data.id)
  }
}

// 确认删除设备间
const confirmDeleteRoom = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除此设备间吗？删除后将不可恢复', '删除确认', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await deleteEquipmentRoom(id)
    ElMessage.success('删除成功')
    await loadEquipmentRooms()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 确认删除机柜
const confirmDeleteRack = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除此机柜吗？删除后将不可恢复', '删除确认', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await deleteRack(id)
    ElMessage.success('删除成功')

    if (id === selectedRackId.value) {
      selectedRackId.value = null
      currentRackId.value = null
      currentRack.value = null
      deviceList.value = []
    }

    await loadEquipmentRooms()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 提交创建设备间
const submitCreateRoom = async () => {
  if (!roomForm.name) {
    ElMessage.warning('请输入设备间名称')
    return
  }
  operating.value = true
  try {
    await createEquipmentRoom(roomForm)
    ElMessage.success('创建成功')
    showCreateRoomDialog.value = false
    roomForm.name = ''
    roomForm.location = ''
    roomForm.remarks = ''
    await loadEquipmentRooms()
  } catch (error) {
    ElMessage.error('创建失败')
  } finally {
    operating.value = false
  }
}

// 提交重命名设备间
const submitRenameRoom = async () => {
  if (!roomForm.name) {
    ElMessage.warning('请输入设备间名称')
    return
  }
  operating.value = true
  try {
    await updateEquipmentRoom(currentRoomId.value, roomForm)
    ElMessage.success('更新成功')
    showRenameRoomDialog.value = false
    await loadEquipmentRooms()
  } catch (error) {
    ElMessage.error('更新失败')
  } finally {
    operating.value = false
  }
}

// 提交创建机柜
const submitCreateRack = async () => {
  if (!rackForm.name) {
    ElMessage.warning('请输入机柜名称')
    return
  }
  operating.value = true
  try {
    await createRack({
      ...rackForm,
      equipment_room_id: currentRoomId.value
    })
    ElMessage.success('创建成功')
    showCreateRackDialog.value = false

    const room = equipmentRooms.value.find(r => r.id === currentRoomId.value)
    if (room) {
      room.expanded = false
      room.racks = []
      room.racksLoaded = false
      await toggleRoomExpand(room)
    }

    await loadEquipmentRooms()
  } catch (error) {
    ElMessage.error('创建失败')
  } finally {
    operating.value = false
  }
}

// 提交重命名机柜
const submitRenameRack = async () => {
  if (!rackForm.name) {
    ElMessage.warning('请输入机柜名称')
    return
  }
  operating.value = true
  try {
    await updateRack(currentRackId.value, rackForm)
    ElMessage.success('更新成功')
    showRenameRackDialog.value = false
    await loadEquipmentRooms()
  } catch (error) {
    ElMessage.error('更新失败')
  } finally {
    operating.value = false
  }
}

// 加载设备列表
const loadDevices = async () => {
  if (!selectedRackId.value) {
    console.warn('没有选中的机柜，不加载设备')
    return
  }

  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      search: searchValue.value,
      rack_id: selectedRackId.value
    }

    console.log('查询设备参数:', params)
    const res = await getInfrastructureEquipment(params)
    console.log('设备列表响应:', res)

    deviceList.value = res.data?.results || []
    total.value = res.data?.count || 0
  } catch (error) {
    console.error('加载设备列表失败:', error)
    ElMessage.error('加载设备列表失败')
    deviceList.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

// 加载所有机柜
const loadAllRacks = async () => {
  try {
    const res = await getRacks()
    console.log('所有机柜 API 响应:', res)
    allRacks.value = res.data?.results || res.data || []
  } catch (error) {
    console.error('加载所有机柜失败', error)
    ElMessage.error('加载机柜列表失败')
  }
}

// 搜索处理
const handleSearch = () => {
  currentPage.value = 1
  loadDevices()
}

// 选择变化
const handleSelectionChange = (val) => {
  selectedDevices.value = val
}

// 批量删除设备
const batchDeleteDevices = async () => {
  if (selectedDevices.value.length === 0) {
    ElMessage.warning('请选择要删除的设备')
    return
  }

  try {
    await ElMessageBox.confirm(`确定要删除选中的 ${selectedDevices.value.length} 个设备吗？`, '删除确认', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    const ids = selectedDevices.value.map(item => item.id)
    console.log('批量删除的 IDs:', ids)
    await deleteInfrastructureEquipment.bulkDelete(ids)

    ElMessage.success('删除成功')
    selectedDevices.value = []
    await loadDevices()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('批量删除失败:', error)
      ElMessage.error(error.response?.data?.error || '删除失败')
    }
  }
}

// 显示设备详情
const showDeviceDetail = async (row) => {
  currentDeviceId.value = row.id
  try {
    const res = await getInfrastructureEquipmentDetail(row.id)
    currentDevice.value = res.data || {}
    showDeviceDetailDrawer.value = true
    await loadConnections(row.id)
  } catch (error) {
    console.error('加载设备详情失败:', error)
    ElMessage.error('加载设备详情失败')
  }
}

// 加载连接信息
const loadConnections = async (deviceId) => {
  try {
    console.log('加载连接信息，设备 ID:', deviceId)
    const res = await getConnections({device_id: deviceId})
    console.log('连接信息 API 响应:', res)
    connectionList.value = res.data?.results || res.data || []
    console.log('连接列表数据:', connectionList.value)
  } catch (error) {
    console.error('加载连接信息失败:', error)
    ElMessage.error('加载连接信息失败')
    connectionList.value = []
  }
}
// 编辑当前设备
const editCurrentDevice = () => {
  showDeviceDetailDrawer.value = false
  showEditDevice(currentDevice.value)
}

// 显示编辑设备
const showEditDevice = (row) => {
  isEditDevice.value = true
  currentDeviceId.value = row.id
  deviceForm.name = row.name
  deviceForm.type = row.type
  deviceForm.rack_id = row.rack_id || row.rack
  deviceForm.brand = row.brand
  deviceForm.model = row.model
  deviceForm.serial_number = row.serial_number
  deviceForm.device_number = row.device_number
  deviceForm.is_active = row.is_active
  deviceForm.remarks = row.remarks
  showCreateDeviceDialogVisible.value = true
}

// 删除设备
const deleteDevice = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除此设备吗？', '删除确认', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await deleteInfrastructureEquipment(row.id)
    ElMessage.success('删除成功')
    await loadDevices()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 提交设备
const submitDevice = async () => {
  if (!deviceForm.name || !deviceForm.type || !deviceForm.rack_id) {
    ElMessage.warning('请填写必填项')
    return
  }
  operating.value = true
  try {
    if (isEditDevice.value) {
      await updateInfrastructureEquipment(currentDeviceId.value, deviceForm)
      ElMessage.success('更新成功')
    } else {
      await createInfrastructureEquipment(deviceForm)
      ElMessage.success('创建成功')
    }
    showCreateDeviceDialogVisible.value = false
    deviceForm.name = ''
    deviceForm.type = ''
    deviceForm.rack_id = ''
    deviceForm.brand = ''
    deviceForm.model = ''
    deviceForm.serial_number = ''
    deviceForm.device_number = ''
    deviceForm.is_active = true
    deviceForm.remarks = ''
    await loadDevices()
  } catch (error) {
    ElMessage.error(isEditDevice.value ? '更新失败' : '创建失败')
  } finally {
    operating.value = false
  }
}

// 编辑连线
const editConnection = (row) => {
  isEditConnection.value = true
  currentConnectionId.value = row.id
  connectionForm.device_id = row.device_id
  connectionForm.home_interface = row.home_interface
  connectionForm.peer_interface = row.peer_interface
  connectionForm.peer_device = row.peer_device || ''
  connectionForm.connection_type = row.connection_type
  connectionForm.remarks = row.remarks || ''
  showAddConnection.value = true
}

// 删除连线
const handleDeleteConnection = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除此连线吗？', '删除确认', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await deleteConnection(row.id)
    ElMessage.success('删除成功')
    await loadConnections(currentDeviceId.value)
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 提交连线
const submitConnection = async () => {
  if (!connectionForm.home_interface || !connectionForm.peer_interface) {
    ElMessage.warning('请填写必填项')
    return
  }
  operating.value = true
  try {
    connectionForm.device_id = currentDeviceId.value
    if (isEditConnection.value) {
      await updateConnection(currentConnectionId.value, connectionForm)
      ElMessage.success('更新成功')
    } else {
      await createConnection(connectionForm)
      ElMessage.success('创建成功')
    }
    showAddConnection.value = false
    connectionForm.device_id = null
    connectionForm.home_interface = ''
    connectionForm.peer_interface = ''
    connectionForm.peer_device = ''
    connectionForm.connection_type = ''
    connectionForm.remarks = ''
    await loadConnections(currentDeviceId.value)
  } catch (error) {
    ElMessage.error(isEditConnection.value ? '更新失败' : '创建失败')
  } finally {
    operating.value = false
  }
}

// 获取设备类型标签
const getDeviceTypeTag = (type) => {
  const typeMap = {
    'UPS': 'warning',
    '精密空调': 'success',
    '配电柜': 'danger',
    '蓄电池组': 'info',
    '发电机': 'warning',
    '动环监控': 'success',
    '消防系统': 'danger'
  }
  return typeMap[type] || ''
}

// 新增设备按钮点击
const handleAddDevice = () => {
  if (!selectedRackId.value) {
    ElMessage.warning('请先选择机柜')
    return
  }

  isEditDevice.value = false
  deviceForm.name = ''
  deviceForm.type = ''
  deviceForm.rack_id = selectedRackId.value
  deviceForm.brand = ''
  deviceForm.model = ''
  deviceForm.serial_number = ''
  deviceForm.device_number = ''
  deviceForm.is_active = true
  deviceForm.remarks = ''

  showCreateDeviceDialogVisible.value = true
}

onMounted(() => {
  loadEquipmentRooms()
  loadAllRacks()
})
</script>

<template>
  <div class="infrastructure-container">
    <!-- 左侧边栏 -->
    <div class="sidebar">
      <div class="sidebar-header">
        <span class="sidebar-title">管理</span>
        <div class="header-actions">
          <el-tooltip content="新建设备间" placement="bottom">
            <el-button type="primary" size="small" @click="showCreateRoomDialog = true">
              <el-icon><Plus /></el-icon>
            </el-button>
          </el-tooltip>
          <el-tooltip content="刷新" placement="bottom">
            <el-button size="small" @click="loadEquipmentRooms">
              <el-icon><Refresh /></el-icon>
            </el-button>
          </el-tooltip>
        </div>
      </div>

      <div class="sidebar-content">
        <div
            v-for="room in equipmentRooms"
            :key="room.id"
            class="room-item"
            :class="{ active: selectedRoomId === room.id }"
        >
          <el-tooltip :content="room.location || '无地址'" placement="right">
            <div class="room-header" @click="toggleRoomExpand(room)">
              <el-icon class="expand-icon" :class="{ expanded: room.expanded }">
                <ArrowRight v-if="room.expanded" />
                <ArrowRight v-else />

              </el-icon>
              <el-icon class="room-icon"><OfficeBuilding /></el-icon>
              <span class="room-name">{{ room.name }}</span>
              <span class="room-count">{{ room.rack_count || 0 }}个机柜</span>
              <el-dropdown trigger="click" @command="handleRoomCommand" class="room-actions">
                <el-button size="small" link>
                  <el-icon><MoreFilled /></el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item :command="{ command: 'rename', data: room }">
                      <el-icon><Edit /></el-icon> 重命名
                    </el-dropdown-item>
                    <el-dropdown-item :command="{ command: 'add_rack', data: room }">
                      <el-icon><Plus /></el-icon> 新增机柜
                    </el-dropdown-item>
                    <el-dropdown-item :command="{ command: 'delete', data: room }" style="color: #f56c6c">
                      <el-icon><Delete /></el-icon> 删除
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </el-tooltip>

          <!-- 机柜列表 -->
          <div v-if="room.expanded" class="rack-list">
            <div
                v-for="rack in room.racks"
                :key="rack.id"
                class="rack-item"
                :class="{ active: selectedRackId === rack.id }"
                @click="selectRack(rack, room)"
            >
              <el-icon class="rack-icon"><Grid /></el-icon>
              <span class="rack-name">{{ rack.name }}</span>
              <span class="rack-device-count">{{ rack.device_count || 0 }}台设备</span>
              <el-dropdown trigger="click" @command="handleRackCommand" class="rack-actions">
                <el-button size="small" link>
                  <el-icon><MoreFilled /></el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item :command="{ command: 'rename', data: rack }">
                      <el-icon><Edit /></el-icon> 重命名
                    </el-dropdown-item>
                    <el-dropdown-item :command="{ command: 'delete', data: rack }" style="color: #f56c6c">
                      <el-icon><Delete /></el-icon> 删除
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 右侧主内容区 -->
    <div class="main-content">
      <el-empty v-if="!selectedRackId" description="请选择机柜" />

      <template v-else>
        <!-- 工具栏 -->
        <div class="toolbar">
          <div class="toolbar-left">
            <el-button type="primary" @click="handleAddDevice">
              <el-icon><Plus /></el-icon> 新增设备
            </el-button>
            <el-button v-if="selectedDevices.length > 0" type="danger" @click="batchDeleteDevices">
              <el-icon><Delete /></el-icon> 批量删除
            </el-button>
          </div>
          <div class="toolbar-right">
            <el-input
                v-model="searchValue"
                placeholder="搜索设备名称、型号..."
                clearable
                style="width: 300px"
                @input="handleSearch"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </div>
        </div>

        <!-- 设备表格 -->
        <el-card class="table-card" shadow="never">
          <el-table
              v-loading="loading"
              :data="deviceList"
              style="width: 100%"
              border
              stripe
              @selection-change="handleSelectionChange"
          >
            <el-table-column type="selection" width="55" />
            <el-table-column prop="device_number" label="设备编号" width="120" />
            <el-table-column prop="name" label="设备名称" min-width="150" />
            <el-table-column prop="type" label="设备类型" width="120">
              <template #default="{ row }">
                <el-tag :type="getDeviceTypeTag(row.type)">{{ row.type }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="brand" label="品牌" width="120" />
            <el-table-column prop="model" label="型号" width="150" />
            <el-table-column prop="serial_number" label="序列号" width="150" />
            <el-table-column prop="is_active" label="状态" width="80">
              <template #default="{ row }">
                <el-tag :type="row.is_active ? 'success' : 'danger'">
                  {{ row.is_active ? '启用' : '停用' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="200" fixed="right">
              <template #default="{ row }">
                <el-button size="small" type="primary" link @click="showDeviceDetail(row)">
                  详情
                </el-button>
                <el-button size="small" type="primary" link @click="showEditDevice(row)">
                  编辑
                </el-button>
                <el-button size="small" type="danger" link @click="deleteDevice(row)">
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>


        </el-card>
      </template>
    </div>

    <!-- 新建设备间对话框 -->
    <el-dialog v-model="showCreateRoomDialog" title="新建设备间" width="500px">
      <el-form :model="roomForm" label-width="100px">
        <el-form-item label="设备间名称" required>
          <el-input v-model="roomForm.name" placeholder="请输入设备间名称" />
        </el-form-item>
        <el-form-item label="地址">
          <el-input v-model="roomForm.location" placeholder="请输入地址" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input
              v-model="roomForm.remarks"
              type="textarea"
              :rows="3"
              placeholder="请输入备注"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateRoomDialog = false">取消</el-button>
        <el-button type="primary" @click="submitCreateRoom" :loading="operating">
          确定
        </el-button>
      </template>
    </el-dialog>

    <!-- 重命名设备间对话框 -->
    <el-dialog v-model="showRenameRoomDialog" title="重命名设备间" width="500px">
      <el-form :model="roomForm" label-width="100px">
        <el-form-item label="设备间名称" required>
          <el-input v-model="roomForm.name" placeholder="请输入设备间名称" />
        </el-form-item>
        <el-form-item label="地址">
          <el-input v-model="roomForm.location" placeholder="请输入地址" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input
              v-model="roomForm.remarks"
              type="textarea"
              :rows="3"
              placeholder="请输入备注"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showRenameRoomDialog = false">取消</el-button>
        <el-button type="primary" @click="submitRenameRoom" :loading="operating">
          确定
        </el-button>
      </template>
    </el-dialog>

    <!-- 新建机柜对话框 -->
    <el-dialog v-model="showCreateRackDialog" title="新建机柜" width="500px">
      <el-form :model="rackForm" label-width="100px">
        <el-form-item label="所属设备间">
          <el-input :value="currentRoomName" disabled />
        </el-form-item>
        <el-form-item label="机柜名称" required>
          <el-input v-model="rackForm.name" placeholder="请输入机柜名称" />
        </el-form-item>
        <el-form-item label="高度 (U)" required>
          <el-input-number v-model="rackForm.height" :min="1" :max="100" />
        </el-form-item>
        <el-form-item label="宽度 (mm)">
          <el-input-number v-model="rackForm.width" :min="100" :max="2000" />
        </el-form-item>
        <el-form-item label="深度 (mm)">
          <el-input-number v-model="rackForm.depth" :min="100" :max="2000" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input
              v-model="rackForm.remarks"
              type="textarea"
              :rows="3"
              placeholder="请输入备注"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateRackDialog = false">取消</el-button>
        <el-button type="primary" @click="submitCreateRack" :loading="operating">
          确定
        </el-button>
      </template>
    </el-dialog>

    <!-- 重命名机柜对话框 -->
    <el-dialog v-model="showRenameRackDialog" title="重命名机柜" width="500px">
      <el-form :model="rackForm" label-width="100px">
        <el-form-item label="机柜名称" required>
          <el-input v-model="rackForm.name" placeholder="请输入机柜名称" />
        </el-form-item>
        <el-form-item label="高度 (U)">
          <el-input-number v-model="rackForm.height" :min="1" :max="100" />
        </el-form-item>
        <el-form-item label="宽度 (mm)">
          <el-input-number v-model="rackForm.width" :min="100" :max="2000" />
        </el-form-item>
        <el-form-item label="深度 (mm)">
          <el-input-number v-model="rackForm.depth" :min="100" :max="2000" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input
              v-model="rackForm.remarks"
              type="textarea"
              :rows="3"
              placeholder="请输入备注"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showRenameRackDialog = false">取消</el-button>
        <el-button type="primary" @click="submitRenameRack" :loading="operating">
          确定
        </el-button>
      </template>
    </el-dialog>

    <!-- 新增/编辑设备对话框 -->
    <el-dialog
        v-model="showCreateDeviceDialogVisible"
        :title="isEditDevice ? '编辑设备' : '新增设备'"
        width="600px"
    >
      <el-form :model="deviceForm" label-width="120px">
        <el-form-item label="设备名称" required>
          <el-input v-model="deviceForm.name" placeholder="请输入设备名称" />
        </el-form-item>
        <el-form-item label="设备类型" required>
          <el-select v-model="deviceForm.type" placeholder="请选择设备类型" style="width: 100%">
            <el-option label="UPS" value="UPS" />
            <el-option label="精密空调" value="精密空调" />
            <el-option label="配电柜" value="配电柜" />
            <el-option label="蓄电池组" value="蓄电池组" />
            <el-option label="发电机" value="发电机" />
            <el-option label="动环监控" value="动环监控" />
            <el-option label="消防系统" value="消防系统" />
            <el-option label="其他" value="其他" />
          </el-select>
        </el-form-item>
        <el-form-item label="所属机柜" required>
          <el-input :value="currentRack?.name || ''" disabled placeholder="当前选中的机柜" />
        </el-form-item>
        <el-form-item label="品牌" required>
          <el-input v-model="deviceForm.brand" placeholder="请输入品牌" />
        </el-form-item>
        <el-form-item label="型号" required>
          <el-input v-model="deviceForm.model" placeholder="请输入型号" />
        </el-form-item>
        <el-form-item label="序列号" required>
          <el-input v-model="deviceForm.serial_number" placeholder="请输入序列号" />
        </el-form-item>
        <el-form-item label="设备编号" required>
          <el-input v-model="deviceForm.device_number" placeholder="请输入设备编号" />
        </el-form-item>
        <el-form-item label="是否启用">
          <el-switch v-model="deviceForm.is_active" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input
              v-model="deviceForm.remarks"
              type="textarea"
              :rows="3"
              placeholder="请输入备注"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateDeviceDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitDevice" :loading="operating">
          {{ isEditDevice ? '保存' : '确定' }}
        </el-button>
      </template>
    </el-dialog>

    <!-- 设备详情抽屉 -->
    <el-drawer
        v-model="showDeviceDetailDrawer"
        title="设备详情"
        size="60%"
    >
      <div v-if="currentDevice" class="device-detail">
        <!-- 基本信息 -->
        <el-card class="detail-card" shadow="never">
          <template #header>
            <div class="detail-card-header">
              <span class="card-title">基本信息</span>
              <el-button type="primary" size="small" @click="editCurrentDevice">
                <el-icon><Edit /></el-icon> 编辑
              </el-button>
            </div>
          </template>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="设备编号">{{ currentDevice.device_number }}</el-descriptions-item>
            <el-descriptions-item label="设备名称">{{ currentDevice.name }}</el-descriptions-item>
            <el-descriptions-item label="设备类型">
              <el-tag :type="getDeviceTypeTag(currentDevice.type)">{{ currentDevice.type }}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="所属机柜">{{ currentDevice.rack }}</el-descriptions-item>
            <el-descriptions-item label="品牌">{{ currentDevice.brand }}</el-descriptions-item>
            <el-descriptions-item label="型号">{{ currentDevice.model }}</el-descriptions-item>
            <el-descriptions-item label="序列号">{{ currentDevice.serial_number }}</el-descriptions-item>
            <el-descriptions-item label="状态">
              <el-tag :type="currentDevice.is_active ? 'success' : 'danger'">
                {{ currentDevice.is_active ? '启用' : '停用' }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="备注" :span="2">{{ currentDevice.remarks || '无' }}</el-descriptions-item>
          </el-descriptions>
        </el-card>

        <!-- 连线信息 -->
        <el-card class="detail-card" shadow="never" style="margin-top: 20px">
          <template #header>
            <div class="detail-card-header">
              <span class="card-title">连线信息</span>
              <el-button type="primary" size="small" @click="showAddConnection = true">
                <el-icon><Plus /></el-icon> 新增连线
              </el-button>
            </div>
          </template>
          <el-table :data="connectionList" border stripe>
            <el-table-column prop="home_interface" label="本端接口" min-width="120" />
            <el-table-column prop="peer_interface" label="对端接口" min-width="120" />
            <el-table-column prop="peer_device" label="对端设备" min-width="120" />
            <el-table-column prop="connection_type" label="连接类型" width="120" />
            <el-table-column prop="remarks" label="备注" min-width="150" />
            <el-table-column label="操作" width="150" fixed="right">
              <template #default="{ row }">
                <el-button size="small" type="primary" link @click="editConnection(row)">
                  编辑
                </el-button>
                <el-button size="small" type="danger" link @click="handleDeleteConnection(row)">
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </div>
    </el-drawer>

    <!-- 新增/编辑连线对话框 -->
    <el-dialog
        v-model="showAddConnection"
        :title="isEditConnection ? '编辑连线' : '新增连线'"
        width="500px"
    >
      <el-form :model="connectionForm" label-width="100px">
        <el-form-item label="本端接口" required>
          <el-input v-model="connectionForm.home_interface" placeholder="请输入本端接口" />
        </el-form-item>
        <el-form-item label="对端接口" required>
          <el-input v-model="connectionForm.peer_interface" placeholder="请输入对端接口" />
        </el-form-item>
        <el-form-item label="对端设备" required>
          <el-input v-model="connectionForm.peer_device" placeholder="请输入对端设备名称" />
        </el-form-item>
        <el-form-item label="连接类型">
          <el-select v-model="connectionForm.connection_type" placeholder="请选择连接类型" style="width: 100%">
            <el-option label="网线" value="网线" />
            <el-option label="光纤" value="光纤" />
            <el-option label="电源线" value="电源线" />
            <el-option label="其他" value="其他" />
          </el-select>
        </el-form-item>
        <el-form-item label="备注">
          <el-input
              v-model="connectionForm.remarks"
              type="textarea"
              :rows="3"
              placeholder="请输入备注"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddConnection = false">取消</el-button>
        <el-button type="primary" @click="submitConnection" :loading="operating">
          {{ isEditConnection ? '保存' : '确定' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.infrastructure-container {
  display: flex;
  height: calc(100vh - 120px);
  background-color: #f5f7fa;
}

.sidebar {
  width: 250px;
  background: white;
  border-right: 1px solid #e4e7ed;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 15px;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sidebar-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.header-actions {
  display: flex;
  gap: 5px;
}

.sidebar-content {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
}

.room-item {
  margin-bottom: 5px;
}

.room-header {
  display: flex;
  align-items: center;
  padding: 10px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.room-header:hover {
  background-color: #f5f7fa;
}

.room-item.active > .room-header {
  background-color: #ecf5ff;
}

.expand-icon {
  margin-right: 5px;
  transition: transform 0.3s;
}

.expand-icon.expanded {
  transform: rotate(90deg);
}

.room-icon {
  margin-right: 8px;
  color: #409EFF;
}

.room-name {
  flex: 1;
  font-size: 14px;
  color: #303133;
}

.room-count {
  font-size: 12px;
  color: #909399;
  margin-right: 5px;
}

.room-actions {
  opacity: 0;
  transition: opacity 0.3s;
}

.room-header:hover .room-actions {
  opacity: 1;
}

.rack-list {
  padding-left: 20px;
  margin-top: 5px;
}

.rack-item {
  display: flex;
  align-items: center;
  padding: 8px 10px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
  margin-bottom: 3px;
}

.rack-item:hover {
  background-color: #f5f7fa;
}

.rack-item.active {
  background-color: #ecf5ff;
}

.rack-icon {
  margin-right: 8px;
  color: #67C23A;
}

.rack-name {
  flex: 1;
  font-size: 13px;
  color: #303133;
}

.rack-device-count {
  font-size: 12px;
  color: #909399;
  margin-right: 5px;
}

.rack-actions {
  opacity: 0;
  transition: opacity 0.3s;
}

.rack-item:hover .rack-actions {
  opacity: 1;
}

.main-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.toolbar-left {
  display: flex;
  gap: 10px;
}

.table-card {
  background: white;
}

.pagination-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

.device-detail {
  padding: 10px;
}

.detail-card {
  margin-bottom: 20px;
}

.detail-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
}
</style>

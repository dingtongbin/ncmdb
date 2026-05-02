<script setup>
import {onMounted, reactive, ref} from "vue";
import {Search} from "@element-plus/icons-vue";
import {ElMessage} from "element-plus";
import axios from "axios";
import {isEmpty} from "element-plus/es/utils/index";

const showContainer = ref(false)
const page = ref(1)
const page_size = ref(50)
const search_value = ref('')
const total = ref(0)
const tableLoading = ref(false)
const tableData = ref([])
const showImageList=ref([
])
const tableGetData = ref({})
const containerLoading = ref(true)
const pk = ref('')
// 列表展示项
const tableListItem = ref({})
// 操作的弹出面板控制变量
const showDetailDrawer = ref(false)
const showCreateDrawer = ref(false)
const showUpdateDrawer = ref(false)
// 出入库操作抽屉
const showStockInDrawer = ref(false)
const showStockOutDrawer = ref(false)
// 出入库记录详情抽屉
const showStockRecordDetailDrawer = ref(false)
// 出入库记录列表
const stockRecordList = ref([])
const stockRecordTotal = ref(0)
const stockRecordPage = ref(1)
const stockRecordPageSize = ref(20)
const stockRecordLoading = ref(false)
// 当前选中的物品 ID
const currentItemId = ref(null)
// 当前查看的出入库记录
const currentStockRecord = ref({})
// 出入库表单
const stockInFormData = ref({
  item_id: null,
  operation_type: 'in',
  quantity: 0,
  remarks: ''
})
const stockOutFormData = ref({
  item_id: null,
  operation_type: 'out',
  quantity: 0,
  remarks: ''
})
const stockInFormRef = ref(null)
const stockOutFormRef = ref(null)
// 出入库记录表单验证规则
const stockFormRules = {
  quantity: [
    { required: true, message: '请输入数量', trigger: 'blur' },
    { type: 'number', min: 1, message: '数量必须大于 0', trigger: 'blur' }
  ],
  remarks: [
    { required: false, message: '请输入备注', trigger: 'blur' }
  ]
}


// 删除是弹窗
const showDeleteDialog = ref(false)
const showDeleteDialogList = ref(false)
// 自动匹配表单
const schema = ref({
  pk: "id",
  "fields": [
    {
      "name": "id",
      "label": "序号",
      "type": "text",
      "width":"60px",
      "is_primary_key": true,
      "is_list_item": false,
      "placeholder": "自动生成",
      "readonly": true
    },
    {
      "name": "name",
      "label": "物品名称",
      "type": "text",
      "is_list_item": true,
      "placeholder": "请输入物品名称",
      "rule": [
        {required: true, message: '请输入物品名称', trigger: 'blur'},
        {min: 1, max: 100, message: '物品名称长度应在 1-100 个字符之间', trigger: 'blur'}
      ]
    },
    {
      "name": "item_type",
      "label": "物品类型",
      "type": "select",
      "is_list_item": true,
      "options": [
        {"value": "耗材", "label": "耗材"},
        {"value": "网络设备备件", "label": "网络设备备件"},
        {"value": "维修工具", "label": "维修工具"},
        {"value": "应急救援工具", "label": "应急救援工具"},
        {"value": "其他", "label": "其他"}
      ],
      "placeholder": "请选择物品类型",
      "rule": [
        {required: true, message: '请选择物品类型', trigger: 'blur'}
      ]
    },
    {
      "name": "image",
      "label": "物品图片",
      "type": "image",
      "is_list_item": true,
      "placeholder": "请上传物品图片"
    },
    {
      "name": "location",
      "label": "存放位置",
      "type": "text",
      "is_list_item": true,
      "placeholder": "请输入存放位置",
      "rule": [
        {required: true, message: '请输入存放位置', trigger: 'blur'},
        {min: 1, max: 200, message: '存放位置长度应在 1-200 个字符之间', trigger: 'blur'}
      ]
    },
    {
      "name": "quantity",
      "label": "当前库存",
      "type": "number",
      "is_list_item": true,
      "placeholder": "请输入库存数量",
      "default": 0,
      "rule": [
        {
          type: 'number',
          min: 0,
          message: '库存数量不能为负数',
          trigger: 'blur'
        }
      ]
    },
    {
      "name": "unit",
      "label": "单位",
      "type": "select",
      "is_list_item": true,
      "options": [
        {"value": "个", "label": "个"},
        {"value": "台", "label": "台"},
        {"value": "箱", "label": "箱"},
        {"value": "包", "label": "包"},
        {"value": "件", "label": "件"},
        {"value": "升", "label": "升"},
        {"value": "盒", "label": "盒"},
        {"value": "组", "label": "组"},
        {"value": "公斤/千克", "label": "公斤/千克"},
        {"value": "米", "label": "米"},
        {"value": "其他", "label": "其他"}
      ],
      "placeholder": "请选择单位",
      "rule": [
        {required: true, message: '请选择单位', trigger: 'blur'}
      ]
    },
    {
      "name": "remarks",
      "label": "备注",
      "type": "textarea",
      "is_list_item": true,
      "placeholder": "请输入备注信息"
    },
    {
      "name": "created_at",
      "label": "创建时间",
      "type": "datetime",
      "is_list_item": true,
      "readonly": true
    },
    {
      "name": "updated_at",
      "label": "更新时间",
      "type": "datetime",
      "is_list_item": false,
      "readonly": true
    }
  ],
  API_URL: "http://127.0.0.1:8000/api/inventory/item/",
  STOCK_RECORD_API_URL: "http://127.0.0.1:8000/api/inventory/record/",
  STOCK_OPERATE_API_URL: "http://127.0.0.1:8000/api/inventory/record/item/",
  access_token: localStorage.getItem('access_token'),
})
const request = axios.create({
  timeout: 10000
})
// 请求拦截器 - 自动添加 access_token
request.interceptors.request.use(
    config => {
      // 暂时不启用
      // const userStore = storeSetting()
      // const token = userStore.access_token
      const token = localStorage.getItem('access_token')
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }

      return config
    },
    error => {
      return Promise.reject(error)
    }
)
// 创建表单
const createFormData = ref({})
const createFormRules = ref([])
const createFormRef = ref(null)
// 更新表单
const updateFormData = ref({})
const updateFormRules = ref({})
const updateFormRef = ref(null)
// 删除

// 初始化创建表单数据和规则
const initCreateFormData = (data) => {
  if (data === undefined) {
    return
  }
  let newKV = {}
  for (let i = 0; i < data.length; i++) {
    if (data[i].name !== "id" && data[i].name !== "created_at" && data[i].name !== "updated_at") {
      newKV[data[i].name] = null
    }
  }
  return newKV
}
const initCreateFormRules = (data) => {
  if (data === undefined) {
    return
  }
  let newData = []
  for (let i = 0; i < data.length; i++) {
    if (data[i].name !== "id" && data[i].name !== "created_at" && data[i].name !== "updated_at") {
      newData.push(data[i])
    }
  }
  return newData
}

const setShowImageList=(image)=>{

  const imageList=[]
  imageList.push(String(image))
  showImageList.value=imageList
}

// 初始化更新表单数据和规则
const initUpdateFormData = (data) => {
  if (data === undefined) {
    return
  }
  let newKV = {}
  for (let i = 0; i < data.length; i++) {
    newKV[data[i].name] = ""
  }
  return newKV
}
const initUpdateFormRules = (data) => {
  if (data === undefined) {
    return
  }
  let newData = []
  for (let i = 0; i < data.length; i++) {
    if (data[i].name !== "created_at" && data[i].name !== "updated_at") {
      newData.push(data[i])
    }
  }
  return newData
}

const initTableListItem = (data) => {
  let newData = []
  for (let i = 0; i < data.length; i++) {
    if (data[i].is_list_item === true) {
      newData.push(data[i])
    }
  }
  return newData
}

// api 操作数据函数，异常抛给上层页面操作，request 作为封装的交互工具，对于增删改都没有设置返回值，因为我觉得不是很有必要，如果成功了就不会抛出异常
// 获取列表，参数为模糊搜索、分页和每页数据长度
const formGetList = async (page, page_size) => {
  try {
    const res = await request.get(`${schema.value.API_URL}?search=${search_value.value}&page=${page}&page_size=${page_size}`)
    return res.data
  } catch (e) {
    throw e
  }
}
// 获取单行数据，参数是主键 pk
const formGet = async (pk) => {
  try {
    const res = await request.get(schema.value.API_URL + pk + '/')
    return res.data
  } catch (e) {
    throw e
  }
}
// 创建
const formCreate = async (data) => {
  try {
    const res = await request.post(schema.value.API_URL, data)

  } catch (e) {
    throw e
  }
}
// 局部更新
const formPatch = async (pk, data) => {
  try {
    const res = await request.patch(schema.value.API_URL + pk + '/', data)

  } catch (e) {
    throw e
  }
}
// 删除数据
const fromDelete = async (pk) => {
  try {
    const res = await request.delete(schema.value.API_URL + pk + '/')
  } catch (e) {
    throw e
  }
}
// 处理上传成功事件
const handleUploadSuccess = (response, file, fileList,item) => {
  if (response.status === 'success' && response.file_path) {
    // 精准地将文件路径赋值给对应的字段
    createFormData.value[item] = response.file_path
  }
}
const handleUploadSuccessUpdate = (response, file, fileList,item) => {
  if (response.status === 'success' && response.file_path) {
    // 精准地将文件路径赋值给对应的字段
    updateFormData.value[item] = response.file_path
  }
}
const handleUploadError=(error, file, fileList) =>{
  console.error('上传失败:', error);
  ElMessage.error('文件上传失败');
}
// 删除 id 数组的批量删除
const fromDeleteBulkDelete = async (data) => {
  try {
    const res = await request.post(schema.value.API_URL+'bulk-delete/', {ids: data})
  } catch (e) {
    throw e
  }
}

// 出入库记录相关 API
const getStockRecords = async (item_id, page, page_size) => {
  try {
    const res = await request.get(`${schema.value.STOCK_OPERATE_API_URL}${item_id}/records/?page=${page}&page_size=${page_size}&ordering=-created_at`)
    return res.data
  } catch (e) {
    throw e
  }
}

const getStockRecordDetail = async (id) => {
  try {
    const res = await request.get(schema.value.STOCK_RECORD_API_URL + id + '/')
    return res.data
  } catch (e) {
    throw e
  }
}

const operateStock = async (data) => {
  try {
    const res = await request.post(`${schema.value.STOCK_OPERATE_API_URL}${data.item_id}/operate/`, data)
    return res.data
  } catch (e) {
    throw e
  }
}

// 页面操作数据项目
const tableDataGet = async () => {
  try {
    tableLoading.value = true
    const res = await formGetList(page.value, page_size.value)
    total.value = res.count
    tableData.value = res.results
    tableLoading.value = false
  } catch (e) {
    ElMessage.error(e)
  }

}
const tableGet = async (pk) => {
  try {
    tableGetData.value = await formGet(pk)

  } catch (e) {
    throw e
  }
}

// 出入库记录加载
const loadStockRecords = async (item_id) => {
  try {
    stockRecordLoading.value = true
    const res = await getStockRecords(item_id, stockRecordPage.value, stockRecordPageSize.value)
    stockRecordTotal.value = res.count
    stockRecordList.value = res.results
    console.log(res.results)
    stockRecordLoading.value = false
  } catch (e) {
    ElMessage.error('加载出入库记录失败：' + e)
  }
}

// 页面按钮方法
// 提交创建表单
const createFormSubmit = async () => {
  try {
    // 表单验证
    await createFormRef.value.validate();

    // 验证通过后处理数据
    let newData = Object.fromEntries(
        Object.entries(createFormData.value).filter(([key, value]) => !isEmpty(value))
    );
    const res = await formCreate(newData)
    console.log(res)
    ElMessage.success('添加数据成功')
    showCreateDrawer.value = false
    await tableDataGet()
  } catch (e) {
    console.log(e)
    ElMessage.error('添加数据失败：' + e)
  }
}
// 提交更新函数
const updateFormSubmit = async () => {
  try {
    // 表单验证
    await updateFormRef.value.validate();

    // 验证通过后处理数据
    let newData = Object.fromEntries(
        Object.entries(updateFormData.value).filter(([key, value]) => !isEmpty(value))
    );
    const res = await formPatch(updateRow.value, newData)
    ElMessage.success('更新数据成功')
    showUpdateDrawer.value = false
    await tableDataGet()
  } catch (e) {
    console.log(e)
    ElMessage.error('添加数据失败：' + e)
  }
}
// 删除选中的多个
const tableDeleteHandleCheckbox = async () => {
  showDeleteDialogList.value=true

}
const confirmDeleteList=async()=>{
  try {
    await fromDeleteBulkDelete(selectRow.value)

    ElMessage.success("删除成功")
    await tableDataGet()
    showDeleteDialogList.value=false
  } catch (e) {
    ElMessage.error("删除失败")
  }
}

// 列表详情
const tableDetailHandleClick = async (row) => {
  currentItemId.value = row[pk.value]
  await tableGet(row[pk.value])
  await loadStockRecords(currentItemId.value)
  showDetailDrawer.value = true

}
// 列表项编辑主键标记值
const updateRow = ref(null)
const tableUpdateHandleClick = (row) => {
  try {
    updateRow.value = row[pk.value]
    formGet(row[pk.value]).then(
        (res) => {
          updateFormData.value = res || {}
        }
    )
    showUpdateDrawer.value = true
  } catch (e) {
    ElMessage.error('获取数据失败：' + e)
  }
}
// 列表项删除记录值
const deleteRow = ref(null)
// 列表项删除
const tableDeleteHandleClick = (row) => {
  deleteRow.value = row[pk.value]
  showDeleteDialog.value = true
}
const confirmDelete = async () => {
  try {
    await fromDelete(deleteRow.value)
    showDeleteDialog.value = false
    ElMessage.success("删除成功")
    await tableDataGet()
  } catch (e) {
    ElMessage.error(e)
  }


}
const selectRow = ref(null)
const handleSelectionChange = (val) => {
  selectRow.value = val.map(item => String(item[pk.value] ?? ''));
}

// 出入库操作
const tableStockInHandleClick = async (row) => {
  currentItemId.value = row[pk.value]
  stockInFormData.value = {
    item_id: currentItemId.value,
    operation_type: 'in',
    quantity: 0,
    remarks: ''
  }
  showStockInDrawer.value = true
}

const tableStockOutHandleClick = async (row) => {
  currentItemId.value = row[pk.value]
  stockOutFormData.value = {
    item_id: currentItemId.value,
    operation_type: 'out',
    quantity: 0,
    remarks: ''
  }
  showStockOutDrawer.value = true
}

const stockInFormSubmit = async () => {
  try {
    await stockInFormRef.value.validate()
    await operateStock(stockInFormData.value)
    ElMessage.success('入库成功')
    showStockInDrawer.value = false
    await tableDataGet()
    if (showDetailDrawer.value) {
      await loadStockRecords(currentItemId.value)
    }
  } catch (e) {
    console.log(e)
    ElMessage.error('入库失败：' + e)
  }
}

const stockOutFormSubmit = async () => {
  try {
    await stockOutFormRef.value.validate()
    await operateStock(stockOutFormData.value)
    ElMessage.success('出库成功')
    showStockOutDrawer.value = false
    await tableDataGet()
    if (showDetailDrawer.value) {
      await loadStockRecords(currentItemId.value)
    }
  } catch (e) {
    console.log(e)
    ElMessage.error('出库失败：' + e)
  }
}

// 查看出入库记录详情
const viewStockRecordDetail = async (record) => {
  try {
    currentStockRecord.value = await getStockRecordDetail(record.id)
    showStockRecordDetailDrawer.value = true
  } catch (e) {
    ElMessage.error('加载记录详情失败：' + e)
  }
}

onMounted(async () => {
  await tableDataGet()
  createFormData.value = initCreateFormData(schema.value.fields)
  createFormRules.value = initCreateFormRules(schema.value.fields)
  updateFormData.value = initUpdateFormData(schema.value.fields)
  updateFormRules.value = initUpdateFormRules(schema.value.fields)
  pk.value = schema.value.pk
  console.log(pk.value)
  tableListItem.value = initTableListItem(schema.value.fields)
  containerLoading.value = false
  showContainer.value = true
})

</script>

<template>
  <!--  数据区域-->
  <div
      v-if="showContainer"
      v-loading="containerLoading"
      element-loading-text="Loading..."
  >
    <el-row style="margin-bottom: 1rem;justify-content: space-between">
      <div>
        <el-tooltip
            class="box-item"
            content="点击添加新的数据"
            effect="dark"
            placement="top-start"
        >
          <el-button type="primary" @click="showCreateDrawer=true">添加数据</el-button>
        </el-tooltip>
        <el-tooltip
            class="box-item"
            content="点击删除选中的数据，删除后将不可恢复"
            effect="dark"
            placement="top-start"
        >
          <el-button type="danger"  v-if="selectRow?.length>0" @click="tableDeleteHandleCheckbox">删除选中</el-button>
        </el-tooltip>

      </div>
      <div>
        <el-input v-model="search_value" clearable placeholder="请输入内容" style="width: 300px">
          <template #append>
            <el-tooltip
                class="box-item"
                content="点击搜素"
                effect="dark"
                placement="top-start"
            >
              <el-button :icon="Search" @click="tableDataGet"/>
            </el-tooltip>

          </template>
        </el-input>

      </div>
    </el-row>
    <el-table
        v-loading="tableLoading"
        :border="true"
        :data="tableData"
        height="70vh"
        max-height="70vh"
        stripe
        style="width: 100%;margin-bottom: 1rem"
        @selection-change="handleSelectionChange"
    >

      <el-table-column  type="selection" width="40"/>

      <el-table-column
          v-for="field in tableListItem || []"
          :key="field.name"
          :fixed="field && field.is_primary_key ? 'left' : false"
          :label="field.label"
          :prop="field.name"
          :show-overflow-tooltip="true"
          :width="field.width || '120'"
      >
        <template #default="scope">
          <span v-if="scope.row[field.name]===true">
              <el-tag effect="plain" type="success"> {{ scope.row[field.name] }}</el-tag>
          </span>
          <span v-else-if="scope.row[field.name]===false">
              <el-tag effect="plain" type="danger"> {{ scope.row[field.name] }}</el-tag>
          </span>
          <span v-else-if="String( scope.row[field.name])?.startsWith('http://')">

              <el-image style="width: 100px; height: 100px" :src="scope.row[field.name]" :fit="'cover'" />
          </span>
          <span v-else> {{ scope.row[field.name] }}</span>

        </template>
      </el-table-column>


      <el-table-column fixed="right" label="操作" min-width="200">
        <template #default="scope">
          <el-button link size="small" type="primary" @click="tableDetailHandleClick(scope.row)">详情</el-button>
          <el-button link size="small" type="success" @click="tableStockInHandleClick(scope.row)">入库</el-button>
          <el-button link size="small" type="warning" @click="tableStockOutHandleClick(scope.row)">出库</el-button>
          <el-button link size="small" type="danger" @click="tableDeleteHandleClick(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>


    <el-pagination
        v-model:current-page="page"
        v-model:page-size="page_size"
        :size="'large'"
        :total="total"
        layout="total,  prev, pager, next, jumper"
        @current-change="tableDataGet"
    />
    <!--    详情抽屉-->
    <el-drawer v-if="showDetailDrawer" v-model="showDetailDrawer" :resizable="true" size="50%" title="详细数据">

      <div class="detail-container">
        <div
            v-for="field in schema?.fields || []"
            :key="field.name"
            class="detail-row"
        >
          <div class="detail-label">{{ field.label }}：</div>
          <div class="detail-value">
            <span v-if="String(tableGetData[field.name])?.startsWith('http://')">
              <el-image :previewSrcList="showImageList" style="width: 100px; height: 100px" :src="tableGetData[field.name]" :fit="'cover'" />
            </span>
            <span v-else>
              {{ tableGetData[field.name] || '暂无数据' }}
            </span>
          </div>
        </div>
      </div>

      <!-- 出入库记录区域 -->
      <div class="stock-record-section">
        <h3 style="margin-top: 20px; margin-bottom: 10px;">出入库记录</h3>
        <el-table
            v-loading="stockRecordLoading"
            :data="stockRecordList"
            border
            stripe
            style="width: 100%"
            :height="300"
        >
          <el-table-column prop="operation_type" label="操作类型" width="80">
            <template #default="scope">
              <el-tag :type="scope.row.record_type == 'in' ? 'success' : 'warning'">
                {{ scope.row.record_type == 'in' ? '入库' : '出库' }}


              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="quantity" label="数量" width="80" />
          <el-table-column prop="remarks" label="备注" show-overflow-tooltip />
          <el-table-column prop="operation_time" label="操作时间" width="180" />
          <el-table-column label="操作" width="80" fixed="right">
            <template #default="scope">
              <el-button link size="small" type="primary" @click="viewStockRecordDetail(scope.row)">详情</el-button>
            </template>
          </el-table-column>
        </el-table>
        <el-pagination
            v-model:current-page="stockRecordPage"
            v-model:page-size="stockRecordPageSize"
            :total="stockRecordTotal"
            layout="prev, pager, next"
            @current-change="loadStockRecords(currentItemId)"
            style="margin-top: 10px; justify-content: flex-end"
        />
      </div>
    </el-drawer>


    <!--    创建抽屉-->
    <el-drawer v-if="showCreateDrawer" v-model="showCreateDrawer" :resizable="true" size="50%" title="添加数据">
      <!--      创建表单-->
      <el-form ref="createFormRef" :model="createFormData" :rules="createFormRules" label-width="auto">
        <el-form-item v-for="item in createFormRules" :key="item.name" :label="item.label" :prop="item.name" :rules="item.rule || []">
          <el-input v-if="item.type==='text'" v-model="createFormData[item.name]" :placeholder="item.placeholder"
                    type="text"/>
          <el-input v-else-if="item.type==='textarea'" v-model="createFormData[item.name]" :placeholder="item.placeholder"
                    type="textarea"/>
          <el-input v-else-if="item.type==='number'" v-model.number="createFormData[item.name]" :placeholder="item.placeholder"
                    type="number"/>
          <el-input v-else-if="item.type==='password'" v-model="createFormData[item.name]" :placeholder="item.placeholder"
                    type="password"/>

          <el-upload
              v-else-if="item.type==='image'"
              v-model= "createFormData[item.name]"
              class="upload-demo"
              action="http://127.0.0.1:8000/api/network-engineer/upload/"
              :multiple="false"
              :limit="1"
              @success="(response, file, fileList) => handleUploadSuccess(response, file, fileList, item.name)"
              :on-error="handleUploadError"
          >
            <el-button type="primary">点击上传</el-button>
            <template #tip>
              <div class="el-upload__tip">
                只能选择 jpg 或 png 类型的图片
              </div>
            </template>
          </el-upload>

          <el-select v-else-if="item.type==='select'" v-model="createFormData[item.name]"
                     :placeholder="item.placeholder">
            <el-option v-for="op in item.options" :key="op.value" :label="op.label" :value="op.value"/>
          </el-select>

          <el-date-picker
              v-else-if="item.type==='datetime'"
              v-model="createFormData[item.name]"
              :placeholder="item.placeholder"
              type="datetime"
          />

          <el-date-picker
              v-else-if="item.type==='date'"
              v-model="createFormData[item.name]"
              :placeholder="item.placeholder"
              type="date"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
          />
        </el-form-item>
      </el-form>
      <el-row>
        <el-button type="default" @click="showCreateDrawer = false">取消</el-button>
        <el-button type="primary" @click="createFormSubmit">确认创建</el-button>
      </el-row>
    </el-drawer>


    <!--    更新抽屉-->
    <el-drawer v-if="showUpdateDrawer" v-model="showUpdateDrawer" :resizable="true" size="50%" title="编辑数据">

      <el-form ref="updateFormRef" :model="updateFormData" :rules="updateFormRules" label-width="auto">
        <el-form-item v-for="item in updateFormRules" :key="item.name" :label="item.label" :prop="item.name" :rules="item.rule || []">
          <el-input v-if="item.type==='text'" v-model="updateFormData[item.name]" :placeholder="item.placeholder"
                    type="text"/>
          <el-input v-else-if="item.type==='textarea'" v-model="updateFormData[item.name]" :placeholder="item.placeholder"
                    type="textarea"/>
          <el-input v-else-if="item.type==='number'" v-model.number="updateFormData[item.name]" :placeholder="item.placeholder"
                    type="number"/>
          <el-input v-else-if="item.type==='password'" v-model="updateFormData[item.name]" :placeholder="item.placeholder"
                    type="password"/>
          <el-upload
              v-else-if="item.type==='image'"
              v-model="updateFormData[item.name]"
              class="upload-demo"
              action="http://127.0.0.1:8000/api/network-engineer/upload/"
              :multiple="false"
              @success="(response, file, fileList) => handleUploadSuccessUpdate(response, file, fileList, item.name)"
              :on-error="handleUploadError"
              :limit="1"
          >
            <el-button type="primary">点击上传</el-button>
            <template #tip>
              <div class="el-upload__tip">
                只能选择 jpg 或 png 类型的图片;
                {{updateFormData[item.name] ?' 当前已存储图片 URL：'+ updateFormData[item.name]: ''}}
              </div>

            </template>
          </el-upload>

          <el-select v-else-if="item.type==='select'" v-model="updateFormData[item.name]"
                     :placeholder="item.placeholder">
            <el-option v-for="op in item.options" :key="op.value" :label="op.label" :value="op.value"/>
          </el-select>

          <el-date-picker
              v-else-if="item.type==='datetime'"
              v-model="updateFormData[item.name]"
              :placeholder="item.placeholder"
              type="datetime"
          />

          <el-date-picker
              v-else-if="item.type==='date'"
              v-model="updateFormData[item.name]"
              :placeholder="item.placeholder"
              type="date"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
          />
        </el-form-item>
      </el-form>
      <el-row>
        <el-button type="default" @click="showUpdateDrawer = false">取消</el-button>
        <el-button type="primary" @click="updateFormSubmit">确认更新</el-button>
      </el-row>
    </el-drawer>

    <!-- 入库操作抽屉 -->
    <el-drawer v-model="showStockInDrawer" :resizable="true" size="40%" title="入库操作">
      <el-form ref="stockInFormRef" :model="stockInFormData" :rules="stockFormRules" label-width="auto">
        <el-form-item label="物品 ID" prop="item_id">
          <el-input v-model="stockInFormData.item_id" disabled />
        </el-form-item>
        <el-form-item label="操作类型" prop="operation_type">
          <el-input v-model="stockInFormData.operation_type" disabled />
        </el-form-item>
        <el-form-item label="数量" prop="quantity">
          <el-input-number v-model="stockInFormData.quantity" :min="1" style="width: 100%" />
        </el-form-item>
        <el-form-item label="备注" prop="remarks">
          <el-input v-model="stockInFormData.remarks" type="textarea" :rows="3" placeholder="请输入备注信息（可选）" />
        </el-form-item>
      </el-form>
      <el-row>
        <el-button type="default" @click="showStockInDrawer = false">取消</el-button>
        <el-button type="success" @click="stockInFormSubmit">确认入库</el-button>
      </el-row>
    </el-drawer>

    <!-- 出库操作抽屉 -->
    <el-drawer v-model="showStockOutDrawer" :resizable="true" size="40%" title="出库操作">
      <el-form ref="stockOutFormRef" :model="stockOutFormData" :rules="stockFormRules" label-width="auto">
        <el-form-item label="物品 ID" prop="item_id">
          <el-input v-model="stockOutFormData.item_id" disabled />
        </el-form-item>
        <el-form-item label="操作类型" prop="operation_type">
          <el-input v-model="stockOutFormData.operation_type" disabled />
        </el-form-item>
        <el-form-item label="数量" prop="quantity">
          <el-input-number v-model="stockOutFormData.quantity" :min="1" style="width: 100%" />
        </el-form-item>
        <el-form-item label="备注" prop="remarks">
          <el-input v-model="stockOutFormData.remarks" type="textarea" :rows="3" placeholder="请输入备注信息（可选）" />
        </el-form-item>
      </el-form>
      <el-row>
        <el-button type="default" @click="showStockOutDrawer = false">取消</el-button>
        <el-button type="warning" @click="stockOutFormSubmit">确认出库</el-button>
      </el-row>
    </el-drawer>

    <!-- 出入库记录详情抽屉 -->
    <el-drawer v-model="showStockRecordDetailDrawer" :resizable="true" size="40%" title="出入库记录详情">
      <div class="detail-container">
        <div class="detail-row">
          <div class="detail-label">操作类型：</div>
          <div class="detail-value">
            <el-tag :type="currentStockRecord.operation_type === 'in' ? 'success' : 'warning'">
              {{ currentStockRecord.operation_type === 'in' ? '入库' : '出库' }}
            </el-tag>
          </div>
        </div>
        <div class="detail-row">
          <div class="detail-label">数量：</div>
          <div class="detail-value">{{ currentStockRecord.quantity }}</div>
        </div>
        <div class="detail-row">
          <div class="detail-label">备注：</div>
          <div class="detail-value">{{ currentStockRecord.remarks || '无' }}</div>
        </div>
        <div class="detail-row">
          <div class="detail-label">操作时间：</div>
          <div class="detail-value">{{ currentStockRecord.operation_time }}</div>
        </div>
      </div>
    </el-drawer>

    <!--    删除对话框-->
    <el-dialog
        v-model="showDeleteDialog"
        title="确定要删除本条数据吗？"
        width="500"
    >
      <span>删除后将不可恢复</span>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showDeleteDialog = false">取消</el-button>
          <el-button type="danger" @click="confirmDelete">
            确认删除
          </el-button>
        </div>
      </template>
    </el-dialog>
    <!--    批量删除对话框-->
    <el-dialog
        v-model="showDeleteDialogList"
        title="确定要删除选中的所有数据吗？"
        width="500"
    >
      <span>删除后将不可恢复</span>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showDeleteDialogList = false">取消</el-button>
          <el-button type="danger" @click="confirmDeleteList">
            确认删除
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>
<style scoped>
.detail-container {
  padding: 10px;
}

.detail-row {
  display: flex;
  padding: 12px 0;
  border-bottom: 1px solid #ebeef5;
}

.detail-row:last-child {
  border-bottom: none;
}

.detail-label {
  width: 150px;
  flex-shrink: 0;
  color: #606266;
  font-size: 14px;
  line-height: 24px;
}

.detail-value {
  flex: 1;
  color: #303133;
  font-size: 14px;
  line-height: 24px;
  text-align: right;
  word-break: break-all;
}

.detail-value:deep(span) {
  text-align: right;
}

.detail-value:deep(.el-image) {
  display: inline-block;
}

.stock-record-section {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 2px solid #ebeef5;
}
</style>

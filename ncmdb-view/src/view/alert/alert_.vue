<script setup>
import {onMounted, reactive, ref} from "vue";
import {Search} from "@element-plus/icons-vue";
import {ElMessage} from "element-plus";
import axios from "axios";
const showContainer = ref(false)
const page = ref(1)
const page_size = ref(200)
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
      "placeholder": "请输入该webhook api id",
      rule: [
        {required: true, message: '请输入联系人id', trigger: 'blur'},
      ]
    }, {
      "name": "source",
      "label": "告警来源",
      "type": "text",
      "is_list_item": true,
    }, {
      "name": "severity",
      "label": "告警级别",
      "type": "text",
      "is_list_item": true,
    },{
      "name": "status",
      "label": "告警状态",
      "type": "text",
      "is_list_item": true,
    },{
      "name": "title",
      "label": "告警标题",
      "type": "text",
      "is_list_item": true,
    },{
      "name": "description",
      "label": "告警详情",
      "type": "text",
      "is_list_item": true,
    },{
      "name": "host",
      "label": "主机名",
      "type": "text",
      "is_list_item": true,
    },{
      "name": "ip",
      "label": "IP地址",
      "type": "text",
      "is_list_item": true,
    },{
      "name": "raw_data",
      "label": "原始数据",
      "type": "text",
      "is_list_item": false,
    },{
      "name": "created_at",
      "label": "创建时间",
      "type": "text",
      "is_list_item": true,
    },{
      "name": "confirm_at",
      "label": "确认时间",
      "type": "text",
      "is_list_item": false,
    },
  ],
  API_URL: "http://127.0.0.1:8000/api/alert/alert/",
  access_token: localStorage.getItem('access_token'),
})
const request = axios.create({
  timeout: 10000
})
// 请求拦截器 - 自动添加access_token
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

// 更新表单
const updateFormData = ref({})
const updateFormRules = ref({})
const updateFormRef = ref(null)
// 删除



const initTableListItem = (data) => {
  let newData = []
  for (let i = 0; i < data.length; i++) {
    if (data[i].is_list_item === true) {
      newData.push(data[i])
    }
  }
  return newData
}

// api操作数据函数，异常抛给上层页面操作，request作为封装的交互工具，对于增删改都没有设置返回值，因为我觉得不是很有必要，如果成功了就不会抛出异常
// 获取列表，参数为模糊搜索、分页和每页数据长度
const formGetList = async (page, page_size) => {
  try {
    const res = await request.get(`${schema.value.API_URL}?search=${search_value.value}&page=${page}&page_size=${page_size}`)
    return res.data
  } catch (e) {
    throw e
  }
}
// 获取单行数据，参数是主键pk
const formGet = async (pk) => {
  try {
    const res = await request.get(schema.value.API_URL + pk + '/')
    return res.data
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


// 列表详情
const tableDetailHandleClick = (row) => {
  tableGet(row[pk.value])
  showDetailDrawer.value = true
}
// 列表项编辑主键标记值
const tableUpdateHandleClick = async (row) => {
  try {
    await formPatch(row[pk.value], {status: '已确认'})
    await tableDataGet()
  } catch (e) {
    ElMessage.error('获取数据失败：' + e)
  }
}
// 列表项删除记录值
const selectRow = ref(null)
const handleSelectionChange = (val) => {
  selectRow.value = val.map(item => String(item[pk.value] ?? ''));
}
//
onMounted(async () => {
  await tableDataGet()
  pk.value = schema.value.pk
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


      <el-table-column fixed="right" label="操作" min-width="150">
        <template #default="scope">
          <el-button link size="small" type="primary" @click="tableDetailHandleClick(scope.row)">详情</el-button>
          <template v-if="scope.row?.status==='未确认'">
            <el-button link size="small" type="warning" @click="tableUpdateHandleClick(scope.row)">确认</el-button>

          </template>
          <template v-else>
            <el-button link size="small"  type="success">已确认</el-button>

          </template>


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
            <span v-else-if="field.name === 'raw_data'">
              <pre class="raw-data">{{ tableGetData[field.name] || '暂无数据' }}</pre>
            </span>
            <span v-else>
              {{ tableGetData[field.name] || '暂无数据' }}
            </span>
          </div>
        </div>
      </div>
    </el-drawer>

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

.raw-data {
  white-space: pre-wrap;
  word-break: break-word;
  background-color: #f5f7fa;
  padding: 10px;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 13px;
  max-height: 400px;
  overflow-y: auto;
  text-align: left;
}
</style>

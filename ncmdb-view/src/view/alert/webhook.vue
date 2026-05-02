<script setup>
import {ref} from 'vue'
import GF from "../../components/GF.vue";
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
      "name": "name",
      "label": "名称",
      "type": "text",
      "width":"180px",
      "is_list_item": true,
      "placeholder": "请输入webhook API名称",
      rule: [
        {required: true, message: '请输入webhook API名称', trigger: 'blur'},
      ]
    },{
      "name": "source",
      "label": "告警来源平台",
      "type": "text",
      "is_list_item": true,
      "placeholder": "请输入告警来源平台",
      rule: [
        {required: true, message: '请输入告警来源平台', trigger: 'blur'},
      ]
    },
    {
      "name": "is_active",
      "label": "是否启用",
      "type": "select",
      "is_list_item": true,
      "options": [
        {"value": "true", "label": "启用"},
        {"value": "false", "label": "禁用"},
      ],
      "placeholder": "是否启用",
      rule: [
        {required: true, message: '请选择是否启用', trigger: 'blur'},
      ]
    },
    {
      "name": "remarks",
      "label": "备注",
      "type": "text",
      "width":"180px",
      "is_list_item": true,
      "placeholder": "请输入备注"
    },  {
      "name": "api_token",
      "label": "Api密钥",
      "type": "text",
      "is_list_item": false,
      "readonly": true,
      "placeholder": "api密钥无法更改"
    },
    {
      "name": "updated_at",
      "label": "更新时间",
      "type": "datetime",
      "width":"180px",
      "is_list_item": true,
      "readonly": true
    },
    {
      "name": "created_at",
      "label": "创建时间",
      "type": "datetime",
      "is_list_item": false,
      "readonly": true
    },
  ],
  API_URL: "http://127.0.0.1:8000/api/alert/webhook-crud/",
  access_token: localStorage.getItem('access_token'),
})
</script>

<template>

  <GF :schema="schema"></GF>
</template>

<style scoped>

</style>
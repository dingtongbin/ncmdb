<script setup>
import {ref} from 'vue'
import GF from "../components/GF.vue";
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
      "placeholder": "请输入该联系人id",
      rule: [
        {required: true, message: '请输入联系人id', trigger: 'blur'},
      ]
    }, {
      "name": "name",
      "label": "姓名",
      "type": "text",
      "is_list_item": true,
      "placeholder": "请输入该联系人姓名",
      rule: [
        {required: true, message: '请输入联系人姓名', trigger: 'blur'},
      ]
    },{
      "name": "sex",
      "label": "性别",
      "type": "select",
      "is_list_item": true,
      "options": [
        {"value": "男", "label": "男"},
        {"value": "女", "label": "女"},
      ],
      "placeholder": "请选择该联系人姓名",
      rule: [
        {required: true, message: '请选择联系人姓名', trigger: 'blur'},
      ]
    },
    {
      "name": "phone1",
      "label": "联系电话1",
      "type": "text",
      "is_list_item": true,
      "placeholder": "请输入该联系人的11位联系电话1",
      rule:[
        { required: true, message: '请输入该联系人的11位联系电话1', trigger: 'blur' },
          ]
    }, {
      "name": "phone2",
      "label": "联系电话2",
      "type": "text",
      "is_list_item": true,
      "placeholder": "请输入该联系人的11位联系电话2",
    },
    {
      "name": "email",
      "label": "邮箱",
      "type": "text",
      "is_list_item": true,
      "placeholder": "请输入该联系人邮箱",
    },
    {
      "name": "company",
      "label": "公司",
      "type": "text",
      "is_list_item": true,
      "placeholder": "请输入Zabbix模板名"
    },
    {
      "name": "position",
      "label": "职务",
      "type": "text",
      "is_list_item": true,
      "placeholder": "请输入该联系人职务"
    },
    {
      "name": "address",
      "label": "地址",
      "type": "text",
      "is_list_item": true,
      "placeholder": "请输入该联系人地址"
    },
    {
      "name": "remarks",
      "label": "备注",
      "type": "text",
      "is_list_item": true,
      "placeholder": "请输入备注"
    },
    {
      "name": "updated_at",
      "label": "更新时间",
      "type": "datetime",
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
  API_URL: "http://127.0.0.1:8000/api/contact/crud/",
  access_token: localStorage.getItem('access_token'),
})
</script>

<template>

<GF :schema="schema"></GF>
</template>

<style scoped>

</style>
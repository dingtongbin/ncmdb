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
      "placeholder": "请输入该任务 id",
      rule: [
        {required: true, message: '请输入任务 id', trigger: 'blur'},
      ]
    },
    {
      "name": "task_name",
      "label": "计划任务名称",
      "type": "text",
      "is_list_item": true,
      "placeholder": "请输入计划任务名称",
      rule: [
        {required: true, message: '请输入计划任务名称', trigger: 'blur'},
      ]
    },
    {
      "name": "start_time",
      "label": "开始时间",
      "type": "date",
      "is_list_item": true,
      "placeholder": "请选择开始时间",
      rule: [
        {required: true, message: '请选择开始时间', trigger: 'blur'},
      ]
    },
    {
      "name": "end_time",
      "label": "结束时间",
      "type": "date",
      "is_list_item": true,
      "placeholder": "请选择结束时间",
      rule: [
        {required: true, message: '请选择结束时间', trigger: 'blur'},
      ]
    },
    {
      "name": "publisher",
      "label": "发布人",
      "type": "text",
      "is_list_item": true,
      "placeholder": "请输入发布人",
      rule: [
        {required: true, message: '请输入发布人', trigger: 'blur'},
      ]
    },
    {
      "name": "executor",
      "label": "执行人",
      "type": "text",
      "is_list_item": true,
      "placeholder": "请输入执行人",
      rule: [
        {required: true, message: '请输入执行人', trigger: 'blur'},
      ]
    },
    {
      "name": "task_content",
      "label": "任务内容",
      "type": "textarea",
      "is_list_item": true,
      "placeholder": "请输入任务内容",
      rule: [
        {required: true, message: '请输入任务内容', trigger: 'blur'},
      ]
    },
    {
      "name": "task_target",
      "label": "任务目标",
      "type": "textarea",
      "is_list_item": true,
      "placeholder": "请输入任务目标",
      rule: [
        {required: true, message: '请输入任务目标', trigger: 'blur'},
      ]
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
    }
  ],
  API_URL: "http://127.0.0.1:8000/api/operation-affairs/patroltask/crud/",
  access_token: localStorage.getItem('access_token'),
})
</script>

<template>
  <GF :schema="schema"></GF>
</template>

<style scoped>
</style>

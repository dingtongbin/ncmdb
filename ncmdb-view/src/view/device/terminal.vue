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
      "placeholder": "自动生成",
      "readonly": true
    },
    {
      "name": "name",
      "width":"180px",
      "label": "终端名称",
      "type": "text",
      "is_list_item": true,
      "placeholder": "请输入终端名称",
      "rule": [
        {required: true, message: '请输入终端名称', trigger: 'blur'},
      ]
    },
    {
      "name": "ip_address",
      "label": "IP 地址",
      "width":"140px",

      "type": "text",
      "is_list_item": true,
      "placeholder": "请输入 IP 地址",
      "rule": [
        {required: true, message: '请输入 IP 地址', trigger: 'blur'},
        {
          pattern: /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/,
          message: '请输入有效的 IPv4 地址，如 192.168.1.1',
          trigger: 'blur'
        }
      ]
    },
    {
      "name": "mac_address",
      "label": "MAC 地址",
      "width":"180px",
      "type": "text",
      "is_list_item": true,
      "placeholder": "请输入 MAC 地址，如 00:1A:2B:3C:4D:5E",
      "rule": [
        {
          pattern: /^([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}$/,
          message: '请输入有效的 MAC 地址，如 00:1A:2B:3C:4D:5E',
          trigger: 'blur'
        }
      ]
    },
    {
      "name": "vlan",
      "label": "VLAN",
      "type": "text",
      "is_list_item": true,
      "placeholder": "请输入 VLAN 信息"
    },
    {
      "name": "remarks",
      "label": "备注",
      "width":"180px",
      "type": "textarea",
      "is_list_item": true,
      "placeholder": "请输入备注信息"
    },
  ],
  API_URL: "http://127.0.0.1:8000/api/device/terminal/",
  access_token: localStorage.getItem('access_token'),
})
</script>

<template>
  <GF :schema="schema"></GF>
</template>

<style scoped>
</style>

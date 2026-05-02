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
      "name": "ip_address",
      "label": "IP 地址",
      "width":"180px",
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
      "name": "dhcp",
      "label": "DHCP",
      "type": "text",
      "is_list_item": true,
      "placeholder": "请输入 DHCP 信息"
    },
    {
      "name": "reserved",
      "label": "保留",
      "type": "text",
      "is_list_item": true,
      "placeholder": "请输入保留信息"
    },
    {
      "name": "vlan",
      "label": "VLAN 接口",
      "type": "text",
      "is_list_item": true,
      "placeholder": "请输入 VLAN 接口",

    },
    {
      "name": "business_system",
      "label": "承载业务",
      "type": "text",
      "is_list_item": true,
      "placeholder": "请输入承载业务系统名称"
    },
    {
      "name": "remarks",
      "label": "备注",
      "type": "textarea",
      "is_list_item": true,
      "placeholder": "请输入备注信息"
    },
  ],
  API_URL: "http://127.0.0.1:8000/api/device/ipam/",
  access_token: localStorage.getItem('access_token'),
})
</script>

<template>
  <GF :schema="schema"></GF>
</template>

<style scoped>
</style>

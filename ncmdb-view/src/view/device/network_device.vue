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
      "name": "device_name",
      "label": "设备名称",
      "width":"180px",
      "type": "text",
      "is_list_item": true,
      "placeholder": "请输入设备名称",
      "rule": [
        {required: true, message: '请输入设备名称', trigger: 'blur'},
        {min: 1, max: 255, message: '设备名称长度应在 1-255 个字符之间', trigger: 'blur'}
      ]
    },
    {
      "name": "ip_address",
      "label": "IP 地址",
      "width":"120px",
      "type": "text",
      "is_list_item": true,
      "placeholder": "请输入 IPv4 地址，如 192.168.1.1",
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
      "name": "is_active",
      "label": "是否在用",
      "width":"90px",
      "type": "select",
      "is_list_item": true,
      "options": [
        {"value": true, "label": "是"},
        {"value": false, "label": "否"},
      ],
      "default": true
    },
    {
      "name": "mac_address",
      "label": "MAC 地址",
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
      "name": "type",
      "label": "设备类型",
      "type": "select",
      "is_list_item": true,
      "options": [
        {"value": "交换机", "label": "交换机"},
        {"value": "路由器", "label": "路由器"},
        {"value": "防火墙", "label": "防火墙"},
        {"value": "无线 AP", "label": "无线 AP"},
        {"value": "服务器", "label": "服务器"},
        {"value": "其他", "label": "其他"},
      ],
      "placeholder": "请选择设备类型",
      "rule": [
        {required: true, message: '请选择设备类型', trigger: 'blur'}
      ]
    },
    {
      "name": "model",
      "label": "设备型号",
      "type": "text",
      "is_list_item": true,
      "placeholder": "请输入设备型号",
      "rule": [
        {min: 0, max: 64, message: '设备型号长度不能超过 64 个字符', trigger: 'blur'}
      ]
    },
    {
      "name": "sn",
      "label": "序列号",
      "type": "text",
      "is_list_item": true,
      "placeholder": "请输入设备序列号",
      "rule": [
        {min: 0, max: 64, message: '序列号长度不能超过 64 个字符', trigger: 'blur'}
      ]
    },
    {
      "name": "location",
      "label": "物理位置",
      "type": "text",
      "is_list_item": true,
      "placeholder": "请输入物理位置，如 3 楼机房 A 排",
      "rule": [
        {min: 0, max: 255, message: '物理位置长度不能超过 255 个字符', trigger: 'blur'}
      ]
    },
    {
      "name": "maintenance_start",
      "label": "维保开始日期",
      "type": "date",
      "is_list_item": true,
      "placeholder": "请选择维保开始日期"
    },
    {
      "name": "maintenance_end",
      "label": "维保截止日期",
      "type": "date",
      "is_list_item": true,
      "placeholder": "请选择维保截止日期"
    },
    {
      "name": "local_admin_name",
      "label": "本地管理员用户名",
      "type": "text",
      "is_list_item": true,
      "placeholder": "请输入本地管理员用户名",
      "rule": [
        {min: 0, max: 64, message: '本地管理员用户名长度不能超过 64 个字符', trigger: 'blur'}
      ]
    },
    {
      "name": "local_admin_password",
      "label": "本地管理员密码",
      "type": "password",
      "is_list_item": false,
      "placeholder": "请输入本地管理员密码",
      "rule": [
        {min: 0, max: 128, message: '本地管理员密码长度不能超过 128 个字符', trigger: 'blur'}
      ]
    },
    {
      "name": "system_info",
      "label": "系统信息",
      "type": "text",
      "is_list_item": true,
      "placeholder": "请输入系统信息，如操作系统、版本、架构等",
      "rule": [
        {min: 0, max: 255, message: '系统信息长度不能超过 255 个字符', trigger: 'blur'}
      ]
    },
    {
      "name": "login_protocol",
      "label": "登录协议",
      "type": "select",
      "is_list_item": true,
      "options": [
        {"value": "ssh", "label": "SSH"},
        {"value": "telnet", "label": "Telnet"},
        {"value": "http", "label": "HTTP"},
        {"value": "https", "label": "HTTPS"},
      ],
      "placeholder": "请选择登录协议",
      "default": "ssh",
      "rule": [
        {required: true, message: '请选择登录协议', trigger: 'blur'}
      ]
    },
    {
      "name": "login_username",
      "label": "登录用户名",
      "type": "text",
      "is_list_item": false,
      "placeholder": "请输入登录用户名",
      "rule": [
        {min: 0, max: 64, message: '登录用户名长度不能超过 64 个字符', trigger: 'blur'}
      ]
    },
    {
      "name": "login_password",
      "label": "登录密码",
      "type": "password",
      "is_list_item": false,
      "placeholder": "请输入登录密码",
      "rule": [
        {min: 0, max: 128, message: '登录密码长度不能超过 128 个字符', trigger: 'blur'}
      ]
    },
    {
      "name": "login_port",
      "label": "端口号",
      "type": "number",
      "is_list_item": false,
      "placeholder": "请输入端口号",
      "default": 22,
      "rule": [
        {
          type: 'number',
          min: 1,
          max: 65535,
          message: '端口号范围应在 1-65535 之间',
          trigger: 'blur'
        }
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
    },
  ],
  API_URL: "http://127.0.0.1:8000/api/device/network/",
  access_token: localStorage.getItem('access_token'),
})
</script>

<template>
  <GF :schema="schema"></GF>
</template>

<style scoped>
</style>

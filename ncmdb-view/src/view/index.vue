/*
 * Copyright 2026 dingtongbin
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
<!-- index.vue -->
<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import {getAlertStatistics} from "../api/statistics.js";

// 统计数据
const deviceCount = ref(0)
const terminalCount = ref(0)
const roomCount = ref(0)
const facilityCount = ref(0)
const cabinetCount = ref(0)
const contactCount = ref(0)

// 图表数据
const alarmData = ref([])
const repairData = ref([])

// ... existing code ...

// 初始化告警图表
const initAlarmChart = () => {
  const chart = echarts.init(document.getElementById('alarmChart'))
  chart.setOption({
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255, 255, 255, 0.9)',
      borderColor: '#ddd',
      borderWidth: 1,
      padding: 12,
      textStyle: {
        color: '#333'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: alarmData.value.map(item => item.month),
      axisLine: {
        lineStyle: {
          color: '#e0e0e0'
        }
      },
      axisLabel: {
        color: '#666'
      }
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        formatter: '{value}',
        color: '#666'
      },
      splitLine: {
        lineStyle: {
          type: 'dashed',
          color: '#f0f0f0'
        }
      }
    },
    series: [{
      name: '告警数量',
      type: 'line',
      data: alarmData.value.map(item => Math.max(0, Math.floor(item.count))),
      smooth: true,
      symbolSize: 8,
      symbol: 'circle',
      lineStyle: {
        width: 3,
        color: '#409EFF'
      },
      areaStyle: {
        opacity: 0.3,
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(64, 158, 255, 0.3)' },
          { offset: 1, color: 'rgba(64, 158, 255, 0.05)' }
        ])
      }
    }]
  })
}

// ... existing code ...

// 初始化报修图表
const initRepairChart = () => {
  const chart = echarts.init(document.getElementById('repairChart'))
  chart.setOption({
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255, 255, 255, 0.9)',
      borderColor: '#ddd',
      borderWidth: 1,
      padding: 12,
      textStyle: {
        color: '#333'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: repairData.value.map(item => item.month),
      axisLine: {
        lineStyle: {
          color: '#e0e0e0'
        }
      },
      axisLabel: {
        color: '#666'
      }
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        formatter: '{value}',
        color: '#666'
      },
      splitLine: {
        lineStyle: {
          type: 'dashed',
          color: '#f0f0f0'
        }
      }
    },
    series: [{
      name: '报修数量',
      type: 'line',
      data: repairData.value.map(item => Math.max(0, Math.floor(item.count))),
      smooth: true,
      symbolSize: 8,
      symbol: 'circle',
      lineStyle: {
        width: 3,
        color: '#67C23A'
      },
      areaStyle: {
        opacity: 0.3,
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(103, 194, 58, 0.3)' },
          { offset: 1, color: 'rgba(103, 194, 58, 0.05)' }
        ])
      }
    }]
  })
}

// ... existing code ...


// 加载数据
const loadData = async () => {
  try {
    const data = await getAlertStatistics()

    // 更新统计数据
    deviceCount.value = data.network_device_count || 0
    roomCount.value = data.equipment_room_count || 0
    cabinetCount.value = data.rack_count || 0
    facilityCount.value = data.infrastructure_count || 0

    // 更新图表数据
    alarmData.value = data.alert_stats || []
    repairData.value = data.work_order_stats || []

    // 重新渲染图表
    setTimeout(() => {
      initAlarmChart()
      initRepairChart()
    }, 100)
  } catch (error) {
    console.error('加载数据失败:', error)
  }
}

// 页面挂载后加载数据
onMounted(() => {
  loadData()
})
</script>

<template>
  <div class="container">
    <!-- 第一排：6 个卡片 -->
    <div class="card-container">
      <div
          v-for="(item, index) in [
          { label: '网络设备数量', value: deviceCount, icon: '💻', color: '#409EFF' },
          { label: '设备间数量', value: roomCount, icon: '🏢', color: '#E6A23C' },
          { label: '机柜数量', value: cabinetCount, icon: '🗄️', color: '#909399' },
          { label: '机柜设备数量', value: facilityCount, icon: '🔋', color: '#F56C6C' },
        ]"
          :key="index"
          class="stat-card"
      >
        <div class="icon" :style="{ backgroundColor: item.color }">{{ item.icon }}</div>
        <div class="content">
          <div class="value">{{ item.value }}</div>
          <div class="label">{{ item.label }}</div>
        </div>
      </div>
    </div>

    <!-- 第二排：两个折线图（水平排列） -->
    <div class="chart-container">
      <!-- 告警数量折线图 -->
      <div class="chart-wrapper">
        <h3>告警数量趋势</h3>
        <div id="alarmChart" class="chart"></div>
      </div>

      <!-- 报修数量折线图 -->
      <div class="chart-wrapper">
        <h3>报修数量趋势</h3>
        <div id="repairChart" class="chart"></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  width: 100%;
  height: 100%;
  background-color: #f5f7fa;
  padding: 20px;
  box-sizing: border-box;
  overflow: hidden;
}

.card-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 30px;
  box-sizing: border-box;
}

.stat-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
  padding: 16px;
  display: flex;
  align-items: center;
  box-sizing: border-box;
}

.icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  margin-right: 16px;
  color: white;
}

.content {
  flex: 1;
}

.value {
  font-size: 24px;
  font-weight: bold;
}

.label {
  color: #666;
  margin-top: 8px;
}

.chart-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 25px;
  box-sizing: border-box;
}

.chart-wrapper {
  background: linear-gradient(145deg, #ffffff, #f8f9fa);
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.12);
  box-sizing: border-box;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}



.chart-wrapper h3 {
  margin: 0 0 20px 0;
  color: #333;
  font-size: 18px;
  font-weight: 600;
  text-align: center;
}

.chart {
  height: 320px;
  width: 100%;
}
</style>

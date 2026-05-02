# Copyright 2026 dingtongbin
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# 这是ai编写的测试数据生成脚本
"""
园区网网络管理和报修系统数据初始化脚本
功能：
1. 创建用户账户（管理员、网工、普通员工）
2. 创建部门和员工信息
3. 创建设备间、机柜
4. 创建网络设备（全部纳入基础设施设备管理）
5. 创建基础设施设备连接关系（清晰的连线管理）
6. 创建员工终端设备
7. 创建 IP 地址管理
8. 创建库存物品
9. 创建联系人（厂商、运维电话）
10. 创建工单（报修申请）- 分散到最近 6 个月
11. 创建巡检计划和任务
12. 创建告警信息 - 几十条告警分散到最近 6 个月

时间范围：最近 6 个月（2025 年 9 月 1 日 - 2026 年 3 月 1 日）
"""

import os
import random
import sys
from datetime import datetime, timedelta

import django
from pypinyin import lazy_pinyin

# 设置 Django 环境
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setting.settings')
django.setup()

from user.models import User
from device.models import NetworkDevice, IPAM, Terminal
from integrated_facility.models import EquipmentRooms, Rack, InfrastructureEquipment, Connection
from inventory.models import InventoryItem
from contact.models import Contact
from repair.models import WorkOrder, WorkOrderHandleLog, WorkOrderEvaluation
from operation_affairs.models import PatrolPlan, PatrolTask
from alert.models import Alert, WebhookReceiver


# ==================== 工具函数 ====================

def generate_password():
    """生成符合要求的密码：大小写字母 + 数字，至少 8 位"""
    import random
    import string

    uppercase = random.choice(string.ascii_uppercase)
    lowercase = random.choice(string.ascii_lowercase)
    digit = random.choice(string.digits)

    remaining_length = random.randint(5, 8)
    remaining = ''.join(random.choices(string.ascii_letters + string.digits, k=remaining_length))

    password = list(uppercase + lowercase + digit + remaining)
    random.shuffle(password)
    return ''.join(password)


def generate_phone(index):
    """生成脱敏的电话号码"""
    prefixes = ['138', '139', '136', '137', '135', '158', '159', '150', '151', '152',
                '188', '187', '182', '183', '184', '178', '198', '195']
    prefix = random.choice(prefixes)
    suffix = str(1000 + index % 9000).zfill(4)
    return f"{prefix}xxxx{suffix}"


def check_user_exists(username):
    """检查用户是否存在"""
    return User.objects.filter(username=username).exists()


def name_to_username(name, existing_usernames, counter_dict):
    """将中文姓名转换为拼音小写作为工号，重复则加数字后缀"""
    pinyin_list = lazy_pinyin(name)
    base_username = ''.join(pinyin_list).lower()

    if base_username in counter_dict:
        counter_dict[base_username] += 1
        username = f"{base_username}{counter_dict[base_username]}"
    else:
        counter_dict[base_username] = 0
        username = base_username

    while username in existing_usernames:
        counter_dict[base_username] += 1
        username = f"{base_username}{counter_dict[base_username]}"

    existing_usernames.add(username)
    return username


def create_user(username, real_name, department, phone=None, is_staff=False, is_superuser=False):
    """创建用户，如果已存在则返回已有用户"""
    if check_user_exists(username):
        print(f"用户 {username} 已存在，跳过")
        return User.objects.get(username=username)

    password = generate_password()

    if is_superuser:
        user = User.objects.create_superuser(
            username=username,
            real_name=real_name,
            password=password,
            phone=phone or generate_phone(hash(username) % 10000),
            department=department,
            is_staff=True,
            is_superuser=True
        )
    elif is_staff:
        user = User.objects.create_user(
            username=username,
            real_name=real_name,
            password=password,
            phone=phone or generate_phone(hash(username) % 10000),
            department=department,
            is_staff=True
        )
    else:
        user = User.objects.create_user(
            username=username,
            real_name=real_name,
            password=password,
            phone=phone or generate_phone(hash(username) % 10000),
            department=department
        )

    print(f"创建用户：{username} ({real_name}), 密码：{password}")
    return user


# ==================== 部门配置 ====================

DEPARTMENTS = [
    '总经理办公室',
    '财务部',
    '人事部',
    '技术部',
    '市场部',
    '销售部',
    '采购部',
    '行政部',
    '生产部',
    '质量部',
]

DEPARTMENT_HEADCOUNT = {
    '总经理办公室': 1,
    '财务部': 15,
    '人事部': 10,
    '技术部': 50,
    '市场部': 30,
    '销售部': 80,
    '采购部': 20,
    '行政部': 25,
    '生产部': 40,
    '质量部': 25,
}

GENERAL_MANAGER_NAME = '李总'

# ==================== 网络设备配置 ====================

DEVICE_MODELS = {
    '核心交换机': 'Huawei S7706',
    '接入交换机': 'Huawei S5735-L48T4X-A',
    'POE 交换机': 'Huawei S5735-L48P4X-A',
    '防火墙': 'Huawei USG6630E',
    'AC 控制器': 'Huawei AC6005',
}

VLAN_CONFIG = {
    '管理 VLAN': {'vlan_id': 100, 'network': '192.168.100.0/23', 'gateway': '192.168.100.1'},
    '总经理 VLAN': {'vlan_id': 101, 'network': '192.168.101.0/24', 'gateway': '192.168.101.1'},
    '财务 VLAN': {'vlan_id': 102, 'network': '192.168.102.0/24', 'gateway': '192.168.102.1'},
    '人事 VLAN': {'vlan_id': 103, 'network': '192.168.103.0/24', 'gateway': '192.168.103.1'},
    '1 楼 VLAN': {'vlan_id': 110, 'network': '192.168.110.0/24', 'gateway': '192.168.110.1'},
    '2 楼 VLAN': {'vlan_id': 120, 'network': '192.168.120.0/24', 'gateway': '192.168.120.1'},
    '3 楼 VLAN': {'vlan_id': 130, 'network': '192.168.130.0/24', 'gateway': '192.168.130.1'},
    '4 楼 VLAN': {'vlan_id': 140, 'network': '192.168.140.0/24', 'gateway': '192.168.140.1'},
    '5 楼 VLAN': {'vlan_id': 150, 'network': '192.168.150.0/24', 'gateway': '192.168.150.1'},
    '6 楼 VLAN': {'vlan_id': 160, 'network': '192.168.160.0/24', 'gateway': '192.168.160.1'},
    '无线 VLAN': {'vlan_id': 200, 'network': '192.168.200.0/23', 'gateway': '192.168.200.1'},
    '监控 VLAN': {'vlan_id': 300, 'network': '192.168.30.0/24', 'gateway': '192.168.30.1'},
}

ISSUE_DESCRIPTIONS = [
    "打印机无法连接，显示脱机状态",
    "会议室 WiFi 信号弱，视频卡顿",
    "办公室无线网络连不上，提示密码错误",
    "打印机打印出来是白纸",
    "电脑无法获取 IP 地址，右下角显示红叉",
    "会议系统麦克风没声音",
    "投影仪连接电脑后显示'超出频率范围'",
    "打印机卡纸了，取出来后还是报错",
    "WiFi 能连接但无法上网",
    "办公室某个网口没反应",
    "打印机扫描功能无法使用",
    "会议室 HDMI 接口没信号",
    "无线网络时断时续",
    "打印机打印速度特别慢",
    "电脑显示'有限的访问权限'",
    "电话会议有杂音",
    "打印机无法双面打印",
    "AP 指示灯不亮",
    "网线水晶头松动",
    "电脑无法识别网络打印机",
    "WiFi 信号满格但网速很慢",
    "打印机连续走纸但不打印",
    "会议室音响啸叫",
    "网络频繁掉线",
    "打印机显示墨粉不足",
]


# ... existing code ...

def main():
    print("=" * 60)
    print("开始初始化园区网网络管理和报修系统数据")
    print("=" * 60)

    # ========== 1. 创建管理员和网工 ==========
    print("\n【1】创建管理员和网工账户...")

    admin = create_user(
        username='admin',
        real_name='系统管理员',
        department='技术部',
        is_superuser=True
    )

    network_engineer = create_user(
        username='wanggong001',
        real_name='张伟',
        department='技术部',
        is_staff=True
    )

    operator = create_user(
        username='operator001',
        real_name='王伟',
        department='技术部',
        is_staff=True
    )

    # ========== 2. 创建各部门员工 ==========
    print("\n【2】创建各部门员工账户...")
    employees = []
    employee_index = 1
    username_counter = {}
    existing_usernames = set()

    for dept, count in DEPARTMENT_HEADCOUNT.items():
        for i in range(count):
            if dept == '总经理办公室':
                real_name = GENERAL_MANAGER_NAME
                username = 'lizong'
                existing_usernames.add(username)
            else:
                surname = \
                    ['赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '蒋', '沈', '韩', '杨', '朱',
                     '秦', '尤', '许', '何'][employee_index % 20]
                number = \
                    ['伟', '芳', '娜', '敏', '静', '丽', '强', '磊', '军', '洋', '勇', '艳', '杰', '涛', '明', '超',
                     '秀英', '俊', '辉', '刚'][employee_index % 20]
                real_name = f"{surname}{number}"
                username = name_to_username(real_name, existing_usernames, username_counter)

            user = create_user(
                username=username,
                real_name=real_name,
                department=dept
            )
            employees.append(user)
            employee_index += 1

    print(f"共创建 {len(employees)} 名员工")

    # ========== 3. 创建设备间 ==========
    print("\n【3】创建设备间...")

    main_room = EquipmentRooms.objects.create(
        name='中心机房',
        location='1 楼东侧',
        remarks='公司主机房，存放核心网络设备'
    )

    weak_rooms = []
    for floor in range(1, 7):
        room = EquipmentRooms.objects.create(
            name=f'{floor}楼弱电间',
            location=f'{floor}楼西侧',
            remarks=f'{floor}楼网络设备间'
        )
        weak_rooms.append(room)

    print(f"创建 {len(weak_rooms) + 1} 个设备间")

    # ========== 4. 创建机柜 ==========
    print("\n【4】创建机柜...")

    racks = []
    main_rack1 = Rack.objects.create(
        equipment_room_id=main_room.id,
        name='中心机房机柜 1',
        height=48,
        width=600,
        depth=1000,
        remarks='核心设备机柜'
    )
    racks.append(main_rack1)

    main_rack2 = Rack.objects.create(
        equipment_room_id=main_room.id,
        name='中心机房机柜 2',
        height=48,
        width=600,
        depth=1000,
        remarks='核心设备机柜'
    )
    racks.append(main_rack2)

    for i, room in enumerate(weak_rooms, 1):
        rack = Rack.objects.create(
            equipment_room_id=room.id,
            name=f'{i}楼弱电间机柜',
            height=48,
            width=600,
            depth=1000,
            remarks=f'{i}楼接入设备机柜'
        )
        racks.append(rack)

    print(f"创建 {len(racks)} 个机柜")

    # ========== 5. 创建网络设备（全部纳入基础设施设备管理）==========
    print("\n【5】创建网络设备（全部纳入基础设施设备管理）...")

    network_devices = []
    infrastructure_devices = []
    ip_counter = 10

    core_switches = []
    for i in range(1, 3):
        device = NetworkDevice.objects.create(
            device_name=f'核心交换机{i}',
            ip_address=f'192.168.100.{ip_counter}',
            mac_address=f'00:18:82:{random.randint(10, 99):02d}:{random.randint(10, 99):02d}:{random.randint(10, 99):02d}',
            type='交换机',
            model=DEVICE_MODELS['核心交换机'],
            sn=f'SN2026CS{i:03d}',
            location='1 楼中心机房机柜 1',
            maintenance_start=datetime(2024, 1, 1),
            maintenance_end=datetime(2028, 12, 31),
            local_admin_name='admin',
            local_admin_password=generate_password(),
            system_info='VRP V800R019C00',
            login_protocol='ssh',
            login_username='admin',
            login_password=generate_password(),
            login_port=22,
            is_active=True
        )
        core_switches.append(device)
        network_devices.append(device)

        infra_device = InfrastructureEquipment.objects.create(
            rack_id=main_rack1.id,
            name=f'核心交换机{i}',
            type='核心交换机',
            brand='华为',
            model=DEVICE_MODELS['核心交换机'],
            serial_number=f'SN2026CS{i:03d}',
            device_number=f'NET-CS-{i:03d}',
            is_active=True,
            remarks=f'网络设备 - 核心交换机{i}，IP: 192.168.100.{ip_counter}'
        )
        infrastructure_devices.append(infra_device)
        ip_counter += 1

    firewall = NetworkDevice.objects.create(
        device_name='出口防火墙',
        ip_address='192.168.100.2',
        mac_address=f'00:18:82:{random.randint(10, 99):02d}:{random.randint(10, 99):02d}:{random.randint(10, 99):02d}',
        type='防火墙',
        model=DEVICE_MODELS['防火墙'],
        sn=f'SN2026FW001',
        location='1 楼中心机房机柜 1',
        maintenance_start=datetime(2024, 1, 1),
        maintenance_end=datetime(2028, 12, 31),
        local_admin_name='admin',
        local_admin_password=generate_password(),
        system_info='USG V600R007C20',
        login_protocol='ssh',
        login_username='admin',
        login_password=generate_password(),
        login_port=22,
        is_active=True
    )
    network_devices.append(firewall)

    fw_infra = InfrastructureEquipment.objects.create(
        rack_id=main_rack1.id,
        name='出口防火墙',
        type='防火墙',
        brand='华为',
        model=DEVICE_MODELS['防火墙'],
        serial_number='SN2026FW001',
        device_number='NET-FW-001',
        is_active=True,
        remarks='网络设备 - 出口防火墙，IP: 192.168.100.2'
    )
    infrastructure_devices.append(fw_infra)

    ac_controller = NetworkDevice.objects.create(
        device_name='无线 AC 控制器',
        ip_address='192.168.100.5',
        mac_address=f'00:18:82:{random.randint(10, 99):02d}:{random.randint(10, 99):02d}:{random.randint(10, 99):02d}',
        type='无线 AP',
        model=DEVICE_MODELS['AC 控制器'],
        sn=f'SN2026AC001',
        location='1 楼中心机房机柜 2',
        maintenance_start=datetime(2024, 1, 1),
        maintenance_end=datetime(2028, 12, 31),
        local_admin_name='admin',
        local_admin_password=generate_password(),
        system_info='AC V200R019C00',
        login_protocol='ssh',
        login_username='admin',
        login_password=generate_password(),
        login_port=22,
        is_active=True
    )
    network_devices.append(ac_controller)

    ac_infra = InfrastructureEquipment.objects.create(
        rack_id=main_rack2.id,
        name='无线 AC 控制器',
        type='AC 控制器',
        brand='华为',
        model=DEVICE_MODELS['AC 控制器'],
        serial_number='SN2026AC001',
        device_number='NET-AC-001',
        is_active=True,
        remarks='网络设备 - 无线 AC 控制器，IP: 192.168.100.5'
    )
    infrastructure_devices.append(ac_infra)

    access_switches = []
    poe_switches = []
    for floor in range(1, 7):
        floor_rack = racks[floor + 1]

        for i in range(1, 4):
            device = NetworkDevice.objects.create(
                device_name=f'{floor}楼接入交换机{i}',
                ip_address=f'192.168.100.{ip_counter}',
                mac_address=f'00:18:82:{random.randint(10, 99):02d}:{random.randint(10, 99):02d}:{random.randint(10, 99):02d}',
                type='交换机',
                model=DEVICE_MODELS['接入交换机'],
                sn=f'SN2026SW{floor}{i:03d}',
                location=f'{floor}楼弱电间机柜',
                maintenance_start=datetime(2024, 1, 1),
                maintenance_end=datetime(2028, 12, 31),
                local_admin_name='admin',
                local_admin_password=generate_password(),
                system_info='VRP V800R019C00',
                login_protocol='ssh',
                login_username='admin',
                login_password=generate_password(),
                login_port=22,
                is_active=True
            )
            access_switches.append(device)
            network_devices.append(device)

            infra_device = InfrastructureEquipment.objects.create(
                rack_id=floor_rack.id,
                name=f'{floor}楼接入交换机{i}',
                type='接入交换机',
                brand='华为',
                model=DEVICE_MODELS['接入交换机'],
                serial_number=f'SN2026SW{floor}{i:03d}',
                device_number=f'NET-AS-{floor}{i:02d}',
                is_active=True,
                remarks=f'网络设备 - {floor}楼接入交换机{i}，IP: 192.168.100.{ip_counter}'
            )
            infrastructure_devices.append(infra_device)
            ip_counter += 1

        for i in range(1, 3):
            device = NetworkDevice.objects.create(
                device_name=f'{floor}楼 POE 交换机{i}',
                ip_address=f'192.168.100.{ip_counter}',
                mac_address=f'00:18:82:{random.randint(10, 99):02d}:{random.randint(10, 99):02d}:{random.randint(10, 99):02d}',
                type='交换机',
                model=DEVICE_MODELS['POE 交换机'],
                sn=f'SN2026POE{floor}{i:03d}',
                location=f'{floor}楼弱电间机柜',
                maintenance_start=datetime(2024, 1, 1),
                maintenance_end=datetime(2028, 12, 31),
                local_admin_name='admin',
                local_admin_password=generate_password(),
                system_info='VRP V800R019C00',
                login_protocol='ssh',
                login_username='admin',
                login_password=generate_password(),
                login_port=22,
                is_active=True
            )
            poe_switches.append(device)
            network_devices.append(device)

            infra_device = InfrastructureEquipment.objects.create(
                rack_id=floor_rack.id,
                name=f'{floor}楼 POE 交换机{i}',
                type='POE 交换机',
                brand='华为',
                model=DEVICE_MODELS['POE 交换机'],
                serial_number=f'SN2026POE{floor}{i:03d}',
                device_number=f'NET-POE-{floor}{i:02d}',
                is_active=True,
                remarks=f'网络设备 - {floor}楼 POE 交换机{i}，IP: 192.168.100.{ip_counter}'
            )
            infrastructure_devices.append(infra_device)
            ip_counter += 1

    print(f"创建 {len(network_devices)} 台网络设备（同时创建 {len(infrastructure_devices)} 个基础设施设备条目）")

    # ========== 6. 创建其他基础设施设备 ==========
    print("\n【6】创建其他基础设施设备...")

    other_infra_devices = []
    device_types = ['配线架', '光纤配线架', '理线器', '电源插座', 'PDU']

    for rack in racks:
        num_devices = random.randint(2, 3)
        for i in range(num_devices):
            device_type = random.choice(device_types)
            device = InfrastructureEquipment.objects.create(
                rack_id=rack.id,
                name=f"{rack.name}-{device_type}{i + 1}",
                type=device_type,
                brand=random.choice(['华为', '海康威视', 'TP-LINK', 'D-Link', '其他']),
                model=f"Model-{random.randint(1000, 9999)}",
                serial_number=f"SN{random.randint(100000, 999999)}",
                device_number=f"INF-{rack.id:03d}{i + 1:02d}",
                is_active=True,
                remarks=f"{rack.name}配套{device_type}"
            )
            other_infra_devices.append(device)
            infrastructure_devices.append(device)

    print(f"创建 {len(other_infra_devices)} 个其他基础设施设备")

    # ========== 7. 创建设备连接关系（清晰的连线管理） ==========
    print("\n【7】创建设备连接关系（清晰的连线管理）...")

    connections = []

    conn = Connection.objects.create(
        device_id=infrastructure_devices[2].id,
        home_interface='GE1/0/1',
        peer_interface='XGigabitEthernet1/0/1',
        peer_device=infrastructure_devices[0].name,
        connection_type='光纤链路聚合',
        remarks='【网络骨干连接】出口防火墙 -> 核心交换机 1（万兆链路）'
    )
    connections.append(conn)

    conn = Connection.objects.create(
        device_id=infrastructure_devices[2].id,
        home_interface='GE1/0/2',
        peer_interface='XGigabitEthernet1/0/2',
        peer_device=infrastructure_devices[1].name,
        connection_type='光纤链路聚合',
        remarks='【网络骨干连接】出口防火墙 -> 核心交换机 2（万兆链路）'
    )
    connections.append(conn)

    conn = Connection.objects.create(
        device_id=infrastructure_devices[0].id,
        home_interface='Stack-Port1',
        peer_interface='Stack-Port1',
        peer_device=infrastructure_devices[1].name,
        connection_type='堆叠线缆',
        remarks='【核心堆叠连接】核心交换机 1 <-> 核心交换机 2（堆叠）'
    )
    connections.append(conn)

    as_index = 4
    for floor in range(1, 7):
        for i, sw_infra in enumerate(infrastructure_devices[as_index:as_index + 5], 1):
            conn = Connection.objects.create(
                device_id=sw_infra.id,
                home_interface='XGigabitEthernet1/0/1',
                peer_interface=f'XGigabitEthernet{floor}/0/1',
                peer_device=infrastructure_devices[0].name,
                connection_type='光纤链路聚合',
                remarks=f'【上联连接】{floor}楼接入/POE 交换机{i} -> 核心交换机 1'
            )
            connections.append(conn)

            conn = Connection.objects.create(
                device_id=sw_infra.id,
                home_interface='XGigabitEthernet1/0/2',
                peer_interface=f'XGigabitEthernet{floor}/0/2',
                peer_device=infrastructure_devices[1].name,
                connection_type='光纤链路聚合',
                remarks=f'【上联连接】{floor}楼接入/POE 交换机{i} -> 核心交换机 2'
            )
            connections.append(conn)
        as_index += 5

    for rack in racks:
        rack_devices = [d for d in infrastructure_devices if
                        d.rack_id == rack.id and d.type in ['配线架', '光纤配线架', '理线器', '电源插座', 'PDU']]

        for i, device in enumerate(rack_devices):
            for j in range(i + 1, len(rack_devices)):
                conn = Connection.objects.create(
                    device_id=device.id,
                    home_interface=f'Port{i + 1}',
                    peer_interface=f'Port{j + 1}',
                    peer_device=rack_devices[j].name,
                    connection_type='网线',
                    remarks=f'【机柜内连接】{rack.name}内设备连接'
                )
                connections.append(conn)

    print(f"创建 {len(connections)} 条设备连接（清晰标注连接关系）")

    # ========== 8. 创建员工终端设备 ==========
    print("\n【8】创建员工终端设备...")

    terminals = []
    for emp in employees:
        terminal = Terminal.objects.create(
            name=f"{emp.real_name}的工作电脑",
            ip_address=f"192.168.{random.randint(110, 160)}.{random.randint(10, 250)}",
            mac_address=f"00:1A:2B:{random.randint(10, 99):02d}:{random.randint(10, 99):02d}:{random.randint(10, 99):02d}",
            vlan=f"VLAN{random.randint(101, 160)}",
            remarks=f"{emp.department} - {emp.username}使用"
        )
        terminals.append(terminal)

    print(f"创建 {len(terminals)} 个员工终端设备")

    # ========== 9. 创建 IP 地址管理 ==========
    print("\n【9】创建 IP 地址管理...")

    ipam_records = []

    for vlan_name, vlan_info in VLAN_CONFIG.items():
        network_parts = vlan_info['network'].split('/')
        network_prefix = '.'.join(network_parts[0].split('.')[:3])

        ipam = IPAM.objects.create(
            ip_address=f"{vlan_info['gateway']}",
            dhcp='静态分配',
            reserved='是',
            vlan=vlan_info['vlan_id'],
            business_system=vlan_name,
            remarks=f"{vlan_name}网关地址"
        )
        ipam_records.append(ipam)

    for device in network_devices:
        ipam = IPAM.objects.create(
            ip_address=device.ip_address,
            dhcp='静态分配',
            reserved='是',
            vlan='100',
            business_system='网络设备管理',
            remarks=f"网络设备：{device.device_name}"
        )
        ipam_records.append(ipam)

    for terminal in terminals:
        ipam = IPAM.objects.create(
            ip_address=terminal.ip_address,
            dhcp='DHCP',
            reserved='否',
            vlan=terminal.vlan.replace('VLAN', ''),
            business_system='办公终端',
            remarks=f"员工终端：{terminal.name}"
        )
        ipam_records.append(ipam)

    print(f"创建 {len(ipam_records)} 条 IP 地址记录")

    # ========== 10. 创建库存物品 ==========
    print("\n【10】创建库存物品...")

    inventory_items = [
        {'name': '扎带', 'item_type': '耗材', 'location': '工具柜 1 层', 'quantity': 500, 'unit': '根',
         'remarks': '各种规格'},
        {'name': '成品网线跳线', 'item_type': '线材', 'location': '工具柜 2 层', 'quantity': 7, 'unit': '对',
         'remarks': 'Cat6 类型，1 米/2 米/3 米'},
        {'name': '光纤跳线', 'item_type': '线材', 'location': '工具柜 2 层', 'quantity': 3, 'unit': '对',
         'remarks': 'LC-LC 多模'},
        {'name': '光模块', 'item_type': '配件', 'location': '防静电盒', 'quantity': 10, 'unit': '个',
         'remarks': 'SFP+ 万兆'},
        {'name': '鼠标', 'item_type': '外设', 'location': '工具柜 3 层', 'quantity': 4, 'unit': '个',
         'remarks': '有线 USB'},
        {'name': '键盘', 'item_type': '外设', 'location': '工具柜 3 层', 'quantity': 4, 'unit': '个',
         'remarks': '有线 USB'},
        {'name': '标签机', 'item_type': '工具', 'location': '工具箱', 'quantity': 1, 'unit': '台', 'remarks': '兄弟牌'},
        {'name': '精明鼠寻线仪', 'item_type': '工具', 'location': '工具箱', 'quantity': 1, 'unit': '套',
         'remarks': 'NF-801B'},
        {'name': '网工钳', 'item_type': '工具', 'location': '工具箱', 'quantity': 1, 'unit': '把',
         'remarks': '多功能压线钳'},
        {'name': '海康摄像头', 'item_type': '备件', 'location': '备件柜', 'quantity': 5, 'unit': '个',
         'remarks': '枪机型 DS-2CD3T47'},
        {'name': '话筒', 'item_type': '会议设备', 'location': '会议室储物柜', 'quantity': 2, 'unit': '对',
         'remarks': '无线手持'},
        {'name': '备用交换机', 'item_type': '备件', 'location': '备件柜', 'quantity': 2, 'unit': '台',
         'remarks': 'S5735-L24T4X-A'},
    ]

    for item_data in inventory_items:
        item = InventoryItem.objects.create(**item_data)

    print(f"创建 {len(inventory_items)} 种库存物品")

    # ========== 11. 创建联系人 ==========
    print("\n【11】创建联系人...")

    contacts = [
        {
            'name': '华为客户服务热线',
            'sex': '男',
            'phone1': '400-822-9999',
            'company': '华为技术有限公司',
            'position': '技术支持',
            'address': '深圳市龙岗区坂田华为基地',
            'remarks': '网络设备售后支持'
        },
        {
            'name': '海康威视客服',
            'sex': '女',
            'phone1': '400-700-5998',
            'company': '海康威视数字技术股份有限公司',
            'position': '售后服务',
            'address': '杭州市滨江区阡陌路 555 号',
            'remarks': '监控系统技术支持'
        },
        {
            'name': '李 xx',
            'sex': '男',
            'phone1': '138xxxx5678',
            'phone2': '0755-2xxx8888',
            'company': '华为授权服务商',
            'position': '工程师',
            'address': '广州市天河区',
            'remarks': '本地驻点工程师'
        },
        {
            'name': '王 xx',
            'sex': '男',
            'phone1': '139xxxx1234',
            'company': 'xx 弱电工程公司',
            'position': '项目经理',
            'address': '本市高新区',
            'remarks': '弱电系统维护'
        },
        {
            'name': '张 xx',
            'sex': '男',
            'phone1': '136xxxx9876',
            'company': 'xx 电力工程公司',
            'position': '电工班长',
            'address': '本市越秀区',
            'remarks': '强电系统维护'
        },
        {
            'name': '联想客服热线',
            'sex': '',
            'phone1': '400-990-0000',
            'company': '联想集团',
            'position': '客服',
            'remarks': '电脑设备售后'
        },
        {
            'name': '打印机维修陈师傅',
            'sex': '男',
            'phone1': '137xxxx4567',
            'company': '个体维修',
            'position': '维修师傅',
            'address': '本市白云区',
            'remarks': '打印机专业维修'
        },
    ]

    for contact_data in contacts:
        contact = Contact.objects.create(**contact_data)

    print(f"创建 {len(contacts)} 个联系人")

    # ========== 12. 创建工单 ==========
    print("\n【12】创建工单...")

    work_orders = []
    # 修正：使用当前时间往前推 6 个月作为时间范围
    now = datetime.now()
    start_date = now - timedelta(days=180)  # 最近 6 个月
    end_date = now
    total_days = (end_date - start_date).days
    total_work_orders = len(employees)

    for i in range(total_work_orders):
        reporter = random.choice(employees)
        days_offset = random.randint(0, total_days)
        created_time = start_date + timedelta(days=days_offset)

        if days_offset > total_days - 3:
            status_choices = ['pending', 'accepted', 'processing']
            status = random.choice(status_choices)
        else:
            status = random.choice(['resolved', 'completed'])

        if status in ['pending']:
            assignee = None
        else:
            assignee = random.choice([network_engineer, operator])

            # 使用外键关联用户，而不是字符串字段
            work_order = WorkOrder.objects.create(
                user=reporter,  # 报修人外键（代替 username/name/phone）
                location=f"{random.choice(['1 楼', '2 楼', '3 楼', '4 楼', '5 楼', '6 楼'])}{random.choice(['办公区', '会议室', '走廊'])}",
                description=random.choice(ISSUE_DESCRIPTIONS),
                level=random.choice(['low', 'normal', 'high']),
                assignee=assignee,  # 处理人外键
                status=status,
                result=random.choice([
                    '已更换网线',
                    '已重新配置打印机',
                    '已重启 AP',
                    '已清理卡纸',
                    '已重新配置 IP',
                    '已更换墨盒',
                    '已调试音响',
                    '已修复网络',
                    None
                ]) if status in ['resolved', 'completed'] else None,
                created_at=created_time,
            )

            work_orders.append(work_order)

            if status in ['accepted', 'processing', 'resolved', 'completed'] and assignee:
                handle_log = WorkOrderHandleLog.objects.create(
                    work_order=work_order,
                    handler=assignee,
                    handle_type=random.choice(['diagnose', 'repair', 'configure', 'other']),
                    content=f"现场查看，{random.choice(['重新插拔网线', '重启设备', '更换配件', '重新配置参数'])}，问题已解决",
                    handle_at=created_time + timedelta(hours=random.randint(1, 24))
                )

            if status == 'completed':
                WorkOrderEvaluation.objects.create(
                    work_order=work_order,
                    satisfaction=random.choice([3, 4, 5, 5, 5]),
                    content=random.choice([
                        '处理及时，态度好',
                        '问题解决很快',
                        '专业',
                        '不错',
                        None
                    ])
                )

    print(f"创建 {len(work_orders)} 个工单")

    # ========== 13. 创建巡检计划 ==========
    print("\n【13】创建巡检计划...")

    patrol_plans = [
        {
            'plan_name': '每日设备状态巡检',
            'start_time': datetime(2025, 9, 1, 7, 0),
            'end_time': datetime(2025, 9, 1, 8, 0),
            'publisher': '张管理员',
            'executor': '王运维',
            'patrol_content': '检查所有网络设备运行状态，查看指示灯和日志',
            'output_content': '设备运行正常，无异常告警',
        },
        {
            'plan_name': '每日机房环境巡检',
            'start_time': datetime(2025, 9, 1, 7, 30),
            'end_time': datetime(2025, 9, 1, 8, 30),
            'publisher': '张管理员',
            'executor': '王运维',
            'patrol_content': '检查机房温度、湿度、卫生情况',
            'output_content': '温度 22℃，湿度 45%，环境良好',
        },
        {
            'plan_name': '周一配置备份',
            'start_time': datetime(2025, 9, 7, 9, 0),
            'end_time': datetime(2025, 9, 7, 12, 0),
            'publisher': '张管理员',
            'executor': '李工',
            'patrol_content': '备份所有网络设备配置文件',
            'output_content': '已完成 28 台设备配置备份',
        },
        {
            'plan_name': '季度机房清洁',
            'start_time': datetime(2025, 12, 1, 9, 0),
            'end_time': datetime(2025, 12, 1, 17, 0),
            'publisher': '张管理员',
            'executor': '王运维',
            'patrol_content': '清理机房和所有弱电间机柜灰尘，整理地面卫生',
            'output_content': '机房和所有弱电间已清理完毕',
        },
    ]

    for plan_data in patrol_plans:
        plan = PatrolPlan.objects.create(**plan_data)

    print(f"创建 {len(patrol_plans)} 个巡检计划")

    # ========== 14. 创建计划任务 ==========
    print("\n【14】创建计划任务...")

    patrol_tasks = [
        {
            'task_name': '大型会议保障',
            'start_time': datetime(2025, 10, 15, 8, 0),
            'end_time': datetime(2025, 10, 15, 18, 0),
            'publisher': '张管理员',
            'executor': '李工',
            'task_content': '保障公司年度大会网络和会议系统正常运行',
            'task_target': '确保视频会议、音响、投影设备正常工作',
        },
        {
            'task_name': '会议室设备维修',
            'start_time': datetime(2025, 11, 5, 9, 0),
            'end_time': datetime(2025, 11, 5, 17, 0),
            'publisher': '张管理员',
            'executor': '王运维',
            'task_content': '联系厂家维修 3 楼会议室故障的音响系统',
            'task_target': '修复话筒啸叫问题，调试音响效果',
        },
        {
            'task_name': '网络优化调整',
            'start_time': datetime(2025, 12, 10, 9, 0),
            'end_time': datetime(2025, 12, 10, 18, 0),
            'publisher': '张管理员',
            'executor': '李工',
            'task_content': '优化 VLAN 配置，调整无线 AP 信道',
            'task_target': '提升无线网络性能，减少干扰',
        },
        {
            'task_name': '年度设备检修',
            'start_time': datetime(2026, 1, 8, 8, 0),
            'end_time': datetime(2026, 1, 8, 20, 0),
            'publisher': '张管理员',
            'executor': '王运维',
            'task_content': '对所有网络设备进行全面检查和清洁',
            'task_target': '确保设备正常运行，清理灰尘',
        },
    ]

    for task_data in patrol_tasks:
        task = PatrolTask.objects.create(**task_data)

    print(f"创建 {len(patrol_tasks)} 个计划任务")

    # ========== 15. 创建告警信息 ==========
    print("\n【15】创建告警信息...")

    alerts = []

    alert_descriptions = [
        ('存储服务器 1 磁盘空间告警', '存储服务器 1 磁盘使用率超过 90%，当前可用空间不足 100GB'),
        ('存储服务器 2 RAID 阵列告警', '存储服务器 2 RAID5 阵列中一块硬盘故障，阵列降级运行'),
        ('核心交换机 CPU 利用率过高', '核心交换机 1 CPU 利用率持续超过 80%'),
        ('5 楼 AP 离线', '5 楼东侧 AP-502 离线超过 10 分钟'),
        ('3 楼接入交换机温度过高', '3 楼接入交换机 2 温度达到 65℃，超过阈值'),
        ('防火墙会话数接近上限', '防火墙当前会话数达到 85 万，接近上限 100 万'),
        ('核心交换机内存使用率高', '核心交换机 2 内存使用率超过 85%'),
        ('2 楼 POE 交换机功率告警', '2 楼 POE 交换机 1 输出功率接近上限'),
        ('无线控制器 AP 数量异常', 'AC 控制器管理的 AP 数量少于预期'),
        ('4 楼网络环路告警', '4 楼接入交换机检测到网络环路'),
        ('机房 UPS 电池电压低', '机房 UPS 电池电压低于正常值'),
        ('6 楼网络拥塞', '6 楼接入交换机端口出现严重拥塞'),
        ('1 楼接入交换机风扇故障', '1 楼接入交换机 3 风扇故障告警'),
        ('出口带宽利用率高', '出口带宽利用率超过 90%'),
        ('DHCP 服务器地址池不足', 'DHCP 地址池剩余地址不足 10%'),
    ]

    # 修正：使用动态计算的 start_date 和 total_days，确保告警均匀散布在 6 个月内
    for i in range(50):
        days_offset = random.randint(0, total_days)
        created_time = start_date + timedelta(days=days_offset, hours=random.randint(0, 23),
                                              minutes=random.randint(0, 59))

        if days_offset < 5:
            status = random.choice(['未确认', '未确认', '已确认'])
        elif days_offset < 30:
            status = random.choice(['已确认', '已恢复'])
        else:
            status = random.choice(['已确认', '已恢复', '已恢复'])

        alert_info = random.choice(alert_descriptions)

        alert = Alert.objects.create(
            source=random.choice(['snmp', 'zabbix', 'netconf']),
            severity=random.choice(['info', 'warning', 'critical']),
            status=status,
            title=alert_info[0],
            description=alert_info[1],
            host=f"server-{random.randint(1, 10):02d}" if '服务器' in alert_info[
                0] else f"switch-{random.randint(1, 28):02d}",
            ip=f"192.168.{random.randint(50, 200)}.{random.randint(1, 254)}",
            raw_data={'oid': f'1.3.6.1.4.1.{random.randint(1000, 9999)}.{random.randint(1, 999)}',
                      'value': f'{random.randint(70, 95)}%'},
            created_at=created_time
        )
        alerts.append(alert)

    print(f"创建 {len(alerts)} 条告警信息")

    # ========== 16. 创建 Webhook 接收器 ==========
    print("\n【16】创建 Webhook 接收器...")

    webhook, created = WebhookReceiver.objects.get_or_create(
        name='Zabbix 告警接收器',
        defaults={
            'source': 'zabbix',
            'is_active': True,
            'api_token': 'zbx_token_2026_ncmdb_system',
            'remarks': '接收 Zabbix 监控平台的告警信息'
        }
    )

    if created:
        print("创建完成")
    else:
        print("Webhook 接收器已存在，跳过创建")

    print("创建完成")

    # ========== 完成 ==========
    print("\n" + "=" * 60)
    print("数据初始化完成！")
    print("=" * 60)
    print(f"\n账户信息：")
    print(f"  管理员：admin / (密码见上方输出)")
    print(f"  网工：wanggong001 / (密码见上方输出)")
    print(f"  运维：operator001 / (密码见上方输出)")
    print(f"  总经理：lizong (李总)")
    print(f"  员工数：{len(employees)}")
    print(f"\n设备信息：")
    print(f"  网络设备总数：{len(network_devices)}")
    print(f"  核心交换机：2 台 (S7706)")
    print(f"  接入交换机：{len(access_switches)}台")
    print(f"  POE 交换机：{len(poe_switches)}台")
    print(f"  防火墙：1 台")
    print(f"  AC 控制器：1 台")
    print(f"\n基础设施：")
    print(f"  设备间：{len(weak_rooms) + 1}个")
    print(f"  机柜：{len(racks)}个")
    print(f"  基础设施设备总数：{len(infrastructure_devices)}个 (包含所有网络设备)")
    print(f"  设备连接：{len(connections)}条 (清晰标注连接关系)")
    print(f"\n其他数据：")
    print(f"  员工终端：{len(terminals)}个")
    print(f"  IP 地址记录：{len(ipam_records)}条")
    print(f"  库存物品：{len(inventory_items)}种")
    print(f"  联系人：{len(contacts)}个")
    print(f"  工单：{len(work_orders)}个 (分散到最近 6 个月)")
    print(f"  巡检计划：{len(patrol_plans)}个")
    print(f"  计划任务：{len(patrol_tasks)}个")
    print(f"  告警信息：{len(alerts)}条 (分散到最近 6 个月)")
    print("\n请妥善保管所有账户密码！")


if __name__ == '__main__':
    main()

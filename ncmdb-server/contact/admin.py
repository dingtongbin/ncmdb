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
from django.contrib import admin

from contact.models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'sex', 'phone1', 'phone2',
        'email', 'company', 'position', 'address'
    ]
    list_filter = ['sex', 'company']
    search_fields = ['name', 'phone1', 'phone2', 'email', 'company', 'position']
    readonly_fields = ['id']
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'sex', 'phone1', 'phone2', 'email')
        }),
        ('工作信息', {
            'fields': ('company', 'position')
        }),
        ('地址与备注', {
            'fields': ('address', 'remarks')
        }),
    )
    ordering = ['name']

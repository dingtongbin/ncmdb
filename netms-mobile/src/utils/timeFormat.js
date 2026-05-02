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
// src/utils/timeFormat.js
export function formatTimeAgo(dateString) {
    if (!dateString) return ''

    const now = new Date()
    const date = new Date(dateString)
    const diff = now - date

    const seconds = Math.floor(diff / 1000)
    const minutes = Math.floor(seconds / 60)
    const hours = Math.floor(minutes / 60)
    const days = Math.floor(hours / 24)

    // 超过 7 天不格式化
    if (days > 7) {
        return date.toLocaleDateString('zh-CN', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit'
        })
    }

    if (days > 0) {
        return `${days}天前`
    }
    if (hours > 0) {
        return `${hours}小时前`
    }
    if (minutes > 0) {
        return `${minutes}分钟前`
    }
    return '刚刚'
}

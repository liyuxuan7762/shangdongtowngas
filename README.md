# HZTownGas

[![HACS Custom](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://hacs.xyz/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

杭州港华燃气 Home Assistant 自定义集成 —— 自动获取燃气表累计用量，对接 HA 能源仪表盘。

> 本集成依赖杭州港华燃气微信公众号 H5 接口，使用前请先在微信中关注「港华燃气」公众号并完成账户绑定。

## 功能

- **燃气表读数**：实时展示累计用气量（m³），支持 HA 能源仪表盘
- **多户号支持**：可添加多个集成实例，每个户号一台设备
- **Token 自动刷新**：独立定时器保活 `refreshToken`，失效后自动触发 reauth 流程
- **维护期自动跳过**：每日 23:30–00:30 CST 维护窗口内不发起数据请求，传感器保持上次读数
- **手动刷新按钮**：随时触发一次数据更新，无需等待定时轮询

## 安装

### 方式一：HACS 安装（推荐）

1. 打开 HACS → 右上角 ⋮ → 自定义存储库（Custom repositories）
2. 填入仓库地址，类别选择 **Integration**：
   ```
   https://github.com/palafin02back/hztowngas
   ```
3. 回到 HACS 首页搜索「HZTownGas」并下载
4. 重启 Home Assistant

### 方式二：手动安装

1. 在 [Releases](https://github.com/palafin02back/hztowngas/releases) 页面下载最新的 `hztowngas.zip`
2. 解压后将 `hztowngas/` 目录放入 HA 的 `config/custom_components/` 下
3. 重启 Home Assistant
4. 进入 **设置 → 设备与服务 → 添加集成**，搜索「港华燃气」

## 获取户号信息（subsId / subsCode）

配置集成时需要填写**户号 ID（subsId）**和**户号（subsCode）**：

**第一步：登录港华燃气网页**

用浏览器打开并完成登录：

```
https://www.towngasvcc.com/?login=true
```

**第二步：获取户号列表**

登录成功后，在**同一浏览器**中访问：

```
https://www.towngasvcc.com/user/querySubsList
```

浏览器返回 JSON，从中提取所需字段：

```json
{
  "datas": [
    {
      "subsId": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
      "subsCode": "1234567890",
      "subsName": "张三",
      "subsAddr": "某某小区 X 栋 XXX"
    }
  ]
}
```

> 名下有多块燃气表时列表中会有多条记录，按地址区分后分别添加集成即可。

## 配置

1. **设置 → 设备与服务 → 添加集成**，搜索「港华燃气」
2. **第一步 — 扫码授权**：页面展示微信授权二维码，用手机微信扫码并确认授权
3. **第二步 — 填写信息**：
   - 将授权完成后跳转地址中的 `authCode`（或完整 URL）粘贴到输入框
   - 填写上一节获取的 **subsId** 和 **subsCode**
   - 可选：调整数据刷新间隔（默认 21600 秒 / 6 小时）和 Token 刷新间隔（默认 1800 秒 / 30 分钟）
   - 默认值对绝大多数用户都够用，只有在 Token 频繁失效时才建议把刷新间隔调小
4. 提交后集成即可使用

### 多户号

重复上述步骤再次添加集成，填入不同的 subsId / subsCode 即可。每个户号会创建独立的设备和实体，互不干扰。同一户号重复添加时会提示「该户号已添加」。

## 实体说明

每个户号对应一台设备，设备下包含以下实体：

| 实体 | 类型 | 说明 | 单位 |
|------|------|------|------|
| 燃气表读数 | 传感器 | 累计用气量（TOTAL_INCREASING）| m³ |
| 立即刷新 | 按钮 | 手动触发一次数据更新 | — |

传感器附加属性：

| 属性 | 说明 |
|------|------|
| `subsCode` / `subsName` / `subsAddr` | 户号、用户名、地址 |
| `recordDate` | 最近抄表日期 |
| `totalFee` / `savingSum` | 账单金额 / 节省金额（不一定有值） |
| `next_data_refresh` | 下次数据刷新的 UTC 时间 |
| `next_data_refresh_in` | 距下次数据刷新的剩余秒数 |
| `next_token_refresh` | 下次 Token 刷新的 UTC 时间 |
| `next_token_refresh_in` | 距下次 Token 刷新的剩余秒数 |

## 注意事项

- 授权走的是微信 OAuth，必须在手机微信内扫码，PC 端浏览器会被拦截
- 每日 23:30–00:30 CST 为港华燃气系统维护窗口，此期间集成自动跳过数据请求，传感器保持上次读数不变；Token 刷新不受影响
- 如果 `refreshToken` 彻底失效，集成会自动触发 HA 的重新认证流程，重新扫码即可恢复

## 免责声明

本项目为个人业余项目，与杭州港华燃气及其关联公司无任何隶属或授权关系。所有接口均基于微信公众号/H5 页面的公开行为自行抓包整理，仅供个人家庭能源监控使用，请勿用于任何商业用途。如官方接口发生变动导致集成失效，本项目不承担任何责任。

## License

本项目基于 [MIT License](LICENSE) 发布。

# HZTownGas

Home Assistant 自定义集成，适用于杭州港华燃气，用于自动获取燃气消耗

需要你的账户绑定过微信公众号，本集成依赖杭州港华燃气微信公众号接口获取

## 功能

- **燃气表读数**：实时展示累计用气量，单位 m³，支持 HA 能源仪表盘
- **多户号支持**：可添加多个集成实例，每个户号一个实体（未实测）
- **自动刷新**：自动刷新token，自动授权
- **维护期自动跳过**：每日 23:30–00:30 CST 维护窗口内不发起 API 请求，传感器保持上次读数
- **手动刷新按钮**：随时触发一次数据更新，无需等待下次定时轮询

## 安装

### 方式一：HACS 安装（推荐）

1. 打开 HACS → 集成 → 右上角 ⋮ → 自定义集成
2. 点击「添加」，填入本仓库地址：
   ```
   https://github.com/palafin02back/hztowngas
   ```
3. 在集成商店中搜索「HZTownGas」并安装
4. 重启 Home Assistant

### 方式二：手动安装

1. 在 [Releases](https://github.com/palafin02back/hztowngas/releases) 页面下载最新的 `hztowngas.zip`
2. 解压后将 `hztowngas/` 目录放入 HA 的 `config/custom_components/` 目录
3. 重启 Home Assistant
4. 进入 设置 → 设备与服务 → 添加集成，搜索「港华燃气」并添加

## 获取户号信息（subsId / subsCode）

配置集成时需要填写**户号 ID（subsId）** 和**户号（subsCode）**，步骤如下：

**第一步：登录港华燃气网页**

用浏览器打开以下地址并完成登录：

```
https://www.towngasvcc.com/?login=true
```

**第二步：获取户号列表**

登录成功后，在**同一浏览器**中直接打开：

```
https://www.towngasvcc.com/user/querySubsList
```

浏览器返回 JSON，从中找到对应字段：

```json
{
  "datas": [
    {
      "subsId": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  ← 填入「户号 ID」
      "subsCode": "1234567890",                      ← 填入「户号」
      "subsName": "张三",
      "subsAddr": "某某小区 X 栋 XXX"
    }
  ]
}
```

> 名下有多块燃气表时，列表中会有多条记录，按地址区分后分别添加集成即可。

## 配置

1. 在 设置 → 设备与服务 → 添加集成 中搜索「港华燃气」
2. **第一步 — 扫码授权**：页面展示微信授权二维码，用手机微信扫码并确认授权
3. **第二步 — 填写信息**：
   - 将授权完成后跳转地址中的 `authCode`（或完整 URL）粘贴到输入框
   - 填写上一节获取的**户号 ID（subsId）** 和**户号（subsCode）**
   - 可选：调整数据刷新间隔（默认 21600 秒 / 6 小时）和 Token 刷新间隔（默认 1800 秒 / 30 分钟）一般
   - 一般默认不要改，除非出现token频繁失效你可以把时间调小一点
4. 提交后集成即可使用

### 多户号

重复上述步骤再次添加集成，填入不同的 subsId / subsCode 即可。每个户号会创建独立的设备和实体，互不干扰。同一户号重复添加时系统会自动提示「该户号已添加」。

## 实体说明

每个户号对应一个设备，设备下包含以下实体：

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

- 授权使用微信 OAuth，需在手机微信内完成扫码，PC 端访问会被拦住
- 每日 23:30–00:30 CST 为港华燃气系统维护窗口，此期间集成自动跳过数据请求，传感器保持上次读数不变，Token 刷新不受影响

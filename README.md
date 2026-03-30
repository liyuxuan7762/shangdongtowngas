# 港华燃气表读数 (TownGas Meter)

Home Assistant 自定义集成，用于获取港华燃气 NB-IoT 智能燃气表的表读数（m³），支持通过 Bearer Token + refreshToken 自动续期，一次授权后可长期使用。

## 功能

- **燃气表读数**：展示当前累计用气量，单位为 m³（立方）
- **自动 token 续期**：access_token 过期时自动使用 refresh_token 刷新，无需重新扫码
- **可配置更新间隔**：在配置流程中可设置 60–7200 秒的更新间隔
- **扩展属性**：展示 `recordDate`（抄表日期）、`resId`、`subsName`、`subsAddr` 等

## 安装

### 方式一：HACS 安装（推荐）

1. 打开 HACS → 集成 → 右上角 ⋮ → 自定义集成
2. 点击「添加」，输入本仓库地址后添加
3. 在集成商店中搜索「港华燃气」并安装
4. 重启 Home Assistant

### 方式二：手动安装

1. 下载本仓库，将 `custom_components/hztowngas` 复制到 Home Assistant 的 `config/custom_components/` 目录
2. 重启 Home Assistant
3. 进入 设置 → 设备与服务 → 添加集成，搜索「港华燃气」并添加

## 获取户号信息（subsId / subsCode）

配置集成时需要填写**户号 ID（subsId）** 和**户号（subsCode）**，通过以下步骤获取：

**第一步：登录港华燃气网页**

用浏览器打开以下地址并完成登录（微信扫码或手机号）：

```
https://www.towngasvcc.com/?login=true
```

**第二步：调用接口获取户号列表**

登录成功后，在**同一浏览器**中直接打开（无需其他操作，Cookie 会自动携带）：

```
https://www.towngasvcc.com/user/querySubsList
```

浏览器会返回 JSON 数据，找到你的户号信息：

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

> 如果名下有多个燃气表，列表中会有多条记录，按地址对应填写即可。

---

## 配置

1. 添加集成后，按提示进入配置流程
2. **第一步**：获取微信授权链接（可扫码打开），完成微信 OAuth 授权
3. **第二步**：将授权完成后的跳转地址中的 `authCode`（或完整 URL）粘贴到输入框
4. 填写上一步获取的 **户号 ID（subsId）** 和 **户号（subsCode）**
5. 可选：设置数据刷新间隔（默认 6 小时）和 Token 刷新间隔（默认 30 分钟）
6. 提交后即可使用

## 实体说明


| 实体    | 说明    | 单位  |
| ----- | ----- | --- |
| 燃气表读数 | 累计用气量 | m³  |


扩展属性中包含：`recordDate`（抄表日期）、`resId`、`subsName`、`subsAddr` 等。

## 注意事项

- 首次配置需在微信中完成授权，以获取 access_token 和 refresh_token
- access_token 有效期约 2 小时，refresh_token 用于自动续期，建议保持更新间隔在 token 有效期内
- 若长时间未使用导致 refresh_token 失效，需重新添加集成并再次完成微信授权


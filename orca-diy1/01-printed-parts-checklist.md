# ORCA Hand 零件打印操作清单

基于 `orcahand_description/v2/models/assets/right/` 中的 STL 文件。

---

## 1. 打印前准备

**耗材建议：**
- **结构件**（指节、掌骨、前臂结构）：PLA / PLA+ / PETG，层高 0.15-0.20mm
- **皮肤/软质件**（带 `Skin` 后缀）：TPU 95A 或柔性树脂，层高 0.12mm
- **支撑**：结构件建议树状支撑（减少打磨），皮肤件免支撑打印方向

**打印机调校：**
- 热床调平 → 首层粘连测试 → 流量校准（挤出 20mm³ 实测）
- 每换一卷耗材重新校准流量

---

## 2. 零件清单（单只右手，47 个 STL）

编号按安装层次分组。

### 2.1 前臂与塔架（3 件）

| # | 文件名 | 数量 | 备注 |
|---|--------|------|------|
| 1 | `TopTower-Model.stl` | 1 | 顶部塔架，电机安装位 |
| 2 | `ForeArmStructure-Model.stl` | 1 | 前臂主体 |
| 3 | `ForeArmStructure-Model_Logo.stl` | 1 | 前臂 Logo 装饰盖 |

### 2.2 掌骨 / 基座（4 件）

| # | 文件名 | 数量 | 备注 |
|---|--------|------|------|
| 4 | `R-Carpals.stl` | 1 | 掌骨主体 |
| 5 | `R-Carpals_CORE.stl` | 1 | 掌骨内核 |
| 6 | `R-Carpals_Skin.stl` | 1 | TPU 掌心皮肤 |
| 7 | `R-Carpals_CarpalsTeeth.stl` | 1 | 掌骨齿 |

### 2.3 大拇指（6 件）

| # | 文件名 | 数量 | 备注 |
|---|--------|------|------|
| 8  | `T-R-Assembly.stl` | 1 | 拇指根部 |
| 9  | `T-TP-R.stl` | 1 | 拇指 TP |
| 10 | `T-PP.stl` | 1 | 拇指近端指节 |
| 11 | `T-PP_Skin.stl` | 1 | TPU |
| 12 | `T-PP_PP.stl` | 1 | |
| 13 | `T-DP.stl` | 1 | 拇指远端指节 |
| 14 | `T-DP_Skin.stl` | 1 | TPU |
| 15 | `T-DP_T-DP.stl` | 1 | |

### 2.4 食指（6 件）

| # | 文件名 | 数量 | 备注 |
|---|--------|------|------|
| 16 | `I-R-Assembly.stl` | 1 | 食指根部 |
| 17 | `I-AP-R.stl` | 1 | 食指 AP |
| 18 | `I-AP-R_AP.stl` | 1 | |
| 19 | `I-PP.stl` | 1 | 近端指节 |
| 20 | `I-PP_Skin.stl` | 1 | TPU |
| 21 | `I-PP_PP.stl` | 1 | |
| 22 | `I-IP_IP.stl` | 1 | 中段指节 |
| 23 | `I-FingerTipAssembly.stl` | 1 | 指尖组件 |
| 24 | `I-FingerTipAssembly_I-IP.stl` | 1 | |
| 25 | `I-FingerTipAssembly_I-DP-Skin.stl` | 1 | TPU 指尖皮肤 |

### 2.5 中指（6 件）

| # | 文件名 | 数量 | 备注 |
|---|--------|------|------|
| 26 | `M-Assembly.stl` | 1 | 中指根部 |
| 27 | `M-AP.stl` | 1 | 中指 AP |
| 28 | `M-AP_AP.stl` | 1 | |
| 29 | `M-PP.stl` | 1 | 近端指节 |
| 30 | `M-PP_Skin.stl` | 1 | TPU |
| 31 | `M-PP_PP.stl` | 1 | |
| 32 | `M-IP_IP.stl` | 1 | 中段指节 |
| 33 | `M-FingerTipAssembly.stl` | 1 | 指尖组件 |
| 34 | `M-FingerTipAssembly_M-IP.stl` | 1 | |
| 35 | `M-FingerTipAssembly_M-DP-Skin.stl` | 1 | TPU 指尖皮肤 |

### 2.6 无名指（6 件）

| # | 文件名 | 数量 | 备注 |
|---|--------|------|------|
| 36 | `P-Assembly.stl` | 1 | 无名指根部 |
| 37 | `P-AP.stl` | 1 | 无名指 AP |
| 38 | `P-AP_AP.stl` | 1 | |
| 39 | `P-PP.stl` | 1 | 近端指节 |
| 40 | `P-PP_Skin.stl` | 1 | TPU |
| 41 | `P-PP_PP.stl` | 1 | |
| 42 | `P-IP_IP.stl` | 1 | 中段指节 |
| 43 | `P-FingerTipAssembly.stl` | 1 | 指尖组件 |
| 44 | `P-FingerTipAssembly_P-IP.stl` | 1 | |
| 45 | `P-FingerTipAssembly_P-DP-Skin.stl` | 1 | TPU 指尖皮肤 |

### 2.7 小指（6 件）

**小指与无名指共用零件**（文件名前缀均为 `P-*`），重复打印一份即可。

| # | 文件名 | 数量 | 备注 |
|---|--------|------|------|
| 46 | `P-Assembly.stl` | 1 | 第二份 |
| 47 | `P-AP.stl` | 1 | 第二份 |
| 48 | `P-AP_AP.stl` | 1 | 第二份 |
| 49 | `P-PP.stl` | 1 | 第二份 |
| 50 | `P-PP_Skin.stl` | 1 | TPU，第二份 |
| 51 | `P-PP_PP.stl` | 1 | 第二份 |
| 52 | `P-IP_IP.stl` | 1 | 第二份 |
| 53 | `P-FingerTipAssembly.stl` | 1 | 第二份 |
| 54 | `P-FingerTipAssembly_P-IP.stl` | 1 | 第二份 |
| 55 | `P-FingerTipAssembly_P-DP-Skin.stl` | 1 | TPU，第二份 |

### 2.8 wrist（1 件）

| # | 文件名 | 数量 | 备注 |
|---|--------|------|------|
| 56 | `R-T-AP.stl` | 1 | 手腕 ABD 转接 |
| 57 | `R-T-AP_AP.stl` | 1 | |

---

## 3. 打印顺序建议

1. **先打小件** — 指尖组件、皮肤 → 验证耗材和支撑设置
2. **再打指节** — 从食指/中指开始，小指最后
3. **再打掌骨** — 体积大，耗时最长
4. **最后打前臂塔架** — 最高，检查热床高度是否够

---

## 4. 两只手所需数量

如果制作左右手各一只，全部零件 ×2。 注意左手文件在 `v2/models/assets/left/` 目录下，文件命名对称（`I-L-Assembly.stl` 等）。

---

## 5. 额外需要打印的工具

在正式 ORCA Hand 仓库中提供，本 repo 包含的文件之外：
- **棘轮扳手**（ratchet）—— 用于肌腱拉紧
- **线轴**（spool）—— 每电机一个，共 17 个/手

参考：[ORCA Core 文档 — 张力与校准](orca_core/docs/pages/getting-started-docs/initial-tensioning-and-calibration.md)

---

## 6. 打印后处理

- 去支撑 → 打磨 × 支撑接触面
- TPU 皮肤件用酒精擦拭去毛边
- 试装配：每个关节应能自由转动
- 孔洞检测：电机安装孔（M2 螺丝）需通止规检查
- 如有毛刺堵塞孔位，用 2mm 钻头手动扩孔

---

## 7. 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| 皮肤件分层剥离 | TPU 干燥不足 | 65°C 烘干 6h 再打印 |
| 指节孔位偏小 | 耗材收缩 | XY 补偿 +0.1mm |
| 皮肤件无法套装到指节上 | TPU 太硬 | 换 95A 以下硬度 / 打磨指节外表面 |

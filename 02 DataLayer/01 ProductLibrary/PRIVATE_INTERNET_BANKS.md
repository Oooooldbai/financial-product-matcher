# 民营互联网银行产品库（完整版）

> 更新时间: 2026-04-13 | 银行数量: 19家 | 已收录产品: 20+

---

## 19家民营互联网银行完整名单

| 序号 | 银行名称 | 股东背景 | 资产(亿) | 定位 | 产品收录 |
|------|----------|----------|-----------|------|----------|
| 1 | 微众银行 | 腾讯 | 6517.76 | 微贷/小微 | ✅ 5个产品 |
| 2 | 网商银行 | 蚂蚁集团 | 4710.35 | 电商/小微 | ✅ 3个产品 |
| 3 | 苏商银行 | 苏宁 | 1375.54 | 综合金融 | ✅ 1个产品 |
| 4 | 众邦银行 | 卓尔 | 1235.31 | 供应链金融 | ✅ 1个产品 |
| 5 | 新网银行 | 小米等 | 1036.29 | 互联网贷款 | ✅ 1个产品 |
| 6 | 三湘银行 | 三一集团 | 527.67 | 产业链金融 | ✅ 2个产品 |
| 7 | 亿联银行 | 美团等 | 408.22 | 互联网贷款 | ⏳ |
| 8 | 振兴银行 | 三六零 | 288.83 | 互联网贷款 | ⏳ |
| 9 | 裕民银行 | 正邦→南昌金控 | 208.03 | 互联网金融 | ⏳ |
| 10-19 | 其他10家 | - | - | - | ⏳ |

**图例**：✅ 已收录 | ⏳ 待补充

---

## 已收录产品

### 微众银行（5个产品）⭐资产最大

| 产品ID | 产品名称 | 产品类型 | 供应链位置 | 目标客户 | 额度 |
|--------|----------|----------|------------|----------|------|
| PROD-WZ-001 | 微业贷 | 信用贷款 | - | 小微企业 | 最高500万 |
| PROD-WZ-002 | 供货贷 | 供应链融资 | 上游供应商 | 供应商 | 最高300万 |
| PROD-WZ-003 | 订货贷 | 供应链融资 | 下游经销商 | 经销商 | 最高1000万 |
| PROD-WZ-004 | 科创贷 | 信用贷款 | - | 科技企业 | 最高1000万 |
| PROD-WZ-005 | 基建贷 | 供应链融资 | 全链 | 基建供应商 | 最高3000万 |

#### 微众银行产品详情

**PROD-WZ-002: 供货贷**
```json
{
  "product_id": "PROD-WZ-002",
  "product_name": "供货贷",
  "bank": "微众银行",
  "product_type": "供应链融资",
  "product_form": "数字化供应链贷款",
  "target_customer": "为核心企业供货的供应商",
  "entry_conditions": {
    "enterprise_type": ["民企"],
    "industry": ["制造业、零售业"],
    "scale": "年营收>100万",
    "relationship": "为核心企业供货"
  },
  "product_features": {
    "interest_rate": "年化8-18%",
    "term": "最长1年",
    "amount": "最高300万",
    "guarantee": "无需抵押，凭应收账款"
  },
  "supply_chain_position": ["上游供应商"],
  "core_advantages": [
    "纯信用，凭应收账款",
    "全线上申请",
    "最快当天放款"
  ]
}
```

**PROD-WZ-003: 订货贷**
```json
{
  "product_id": "PROD-WZ-003",
  "product_name": "订货贷",
  "bank": "微众银行",
  "product_type": "供应链融资",
  "product_form": "经销商采购融资",
  "target_customer": "品牌商/核心企业下游经销商",
  "entry_conditions": {
    "enterprise_type": ["民企"],
    "industry": ["快消、家电、汽车"],
    "scale": "年营收>200万",
    "relationship": "品牌经销商"
  },
  "product_features": {
    "interest_rate": "年化8-15%",
    "term": "最长6个月",
    "amount": "最高1000万",
    "guarantee": "凭订单/采购合同"
  },
  "supply_chain_position": ["下游经销商"],
  "core_advantages": [
    "额度高，最高1000万",
    "随借随还",
    "全线上操作"
  ]
}
```

---

### 网商银行（3个产品）

| 产品ID | 产品名称 | 产品类型 | 供应链位置 | 目标客户 | 额度 |
|--------|----------|----------|------------|----------|------|
| PROD-WS-001 | 大雁系统 | 供应链金融系统 | 全链 | 品牌商/经销商/供应商 | 平台 |
| PROD-WS-002 | 采购贷 | 供应链融资 | 下游经销商 | 经销商 | 最高500万 |
| PROD-WS-003 | 加盟商贷 | 场景金融 | 下游加盟商 | 连锁品牌加盟商 | 最高100万 |

#### 网商银行产品详情

**PROD-WS-001: 大雁系统**
```json
{
  "product_id": "PROD-WS-001",
  "product_name": "大雁系统",
  "bank": "网商银行",
  "product_type": "数字供应链金融系统",
  "product_form": "SaaS化供应链金融平台",
  "target_customer": "品牌商及其上下游小微",
  "entry_conditions": {
    "enterprise_type": ["品牌商"],
    "industry": ["电商、快消、连锁"],
    "scale": "有完整供应链体系"
  },
  "product_features": {
    "service": "供应链金融数字化",
    "features": ["信用评估", "智能风控", "实时放款"],
    "audience": "覆盖品牌商、供应商、经销商"
  },
  "supply_chain_position": ["全链路"],
  "core_advantages": [
    "蚂蚁集团技术背书",
    "数据信用替代抵押",
    "160+品牌接入"
  ]
}
```

**PROD-WS-002: 采购贷**
```json
{
  "product_id": "PROD-WS-002",
  "product_name": "采购贷",
  "bank": "网商银行",
  "product_type": "供应链融资",
  "product_form": "采购合同融资",
  "target_customer": "品牌商下游经销商",
  "entry_conditions": {
    "enterprise_type": ["民企"],
    "industry": ["全行业"],
    "scale": "年营收>50万",
    "relationship": "品牌商经销商"
  },
  "product_features": {
    "interest_rate": "年化6-12%",
    "term": "最长6个月",
    "amount": "最高500万",
    "guarantee": "凭采购合同"
  },
  "supply_chain_position": ["下游经销商"],
  "core_advantages": [
    "支付宝端内实时申请",
    "数据信用",
    "最快60秒放款"
  ]
}
```

---

### 苏商银行（1个产品）

| 产品ID | 产品名称 | 产品类型 | 目标客户 | 特色 |
|--------|----------|----------|----------|------|
| PROD-SS-001 | 供应链金融 | 综合供应链 | 上下游企业 | 线上+线下 |

```json
{
  "product_id": "PROD-SS-001",
  "product_name": "供应链金融综合服务",
  "bank": "苏商银行",
  "product_type": "供应链金融",
  "product_form": "线上+线下结合",
  "target_customer": "核心企业上下游中小企业",
  "entry_conditions": {
    "enterprise_type": ["民企"],
    "industry": ["制造业、贸易"],
    "scale": "年营收>100万"
  },
  "product_features": {
    "service_mode": "线上申请+线下服务",
    "term": "最长1年",
    "amount": "根据核心企业资质"
  },
  "supply_chain_position": ["上游", "下游"],
  "core_advantages": [
    "线上+线下服务模式",
    "苏宁生态支持",
    "差异化竞争优势"
  ]
}
```

---

### 三湘银行（2个产品）⭐产业链特色

| 产品ID | 产品名称 | 产品类型 | 供应链位置 | 目标客户 | 额度 |
|--------|----------|----------|------------|----------|------|
| PROD-SX-001 | 工程机械经营贷 | 产业链贷款 | 全链 | 工程机械用户 | 最高200万 |
| PROD-SX-002 | 产业链贷 | 产业链金融 | 全链 | 产业链企业 | - |

#### 三湘银行产品详情

**PROD-SX-001: 工程机械经营贷**
```json
{
  "product_id": "PROD-SX-001",
  "product_name": "工程机械经营贷",
  "bank": "三湘银行",
  "product_type": "产业链贷款",
  "product_form": "信用贷款",
  "target_customer": "持有三一重工设备的工程机械设备经营者",
  "entry_conditions": {
    "enterprise_type": ["个人/民企"],
    "equipment": "持有三一工程机械",
    "scale": "真实经营"
  },
  "product_features": {
    "interest_rate": "年化8-15%",
    "term": "最长3年",
    "amount": "最高200万",
    "guarantee": "纯信用，无需抵押",
    "speed": "5分钟申请，2分钟到账"
  },
  "supply_chain_position": ["下游设备使用者"],
  "core_advantages": [
    "三一集团产业链资源",
    "纯信用，无抵押",
    "审批极快",
    "0人工干预"
  ]
}
```

---

### 中关村银行（1个产品）

| 产品ID | 产品名称 | 产品类型 | 供应链位置 | 目标客户 | 特色 |
|--------|----------|----------|------------|----------|------|
| PROD-ZGC-001 | 开思银融一号 | 供应链金融 | 上游供应商 | 科技企业供应商 | 科技赋能 |

```json
{
  "product_id": "PROD-ZGC-001",
  "product_name": "开思银融一号",
  "bank": "中关村银行",
  "product_type": "供应链金融",
  "product_form": "数字化供应链融资",
  "target_customer": "科技企业上游供应商",
  "entry_conditions": {
    "enterprise_type": ["民企"],
    "industry": ["科技、TMT"],
    "scale": "年营收>100万",
    "relationship": "科技企业供应商"
  },
  "product_features": {
    "service": "科技赋能供应链金融",
    "term": "最长1年",
    "amount": "根据核心企业资质"
  },
  "supply_chain_position": ["上游供应商"],
  "core_advantages": [
    "北京首家民营银行",
    "科技企业专属服务",
    "数字化风控"
  ]
}
```

---

### 众邦银行（1个产品）

| 产品ID | 产品名称 | 产品类型 | 供应链位置 | 目标客户 | 利率 |
|--------|----------|----------|------------|----------|------|
| PROD-ZB-001 | 众链贷 | 供应链金融 | 全链 | 核心企业上下游 | 6-10% |

```json
{
  "product_id": "PROD-ZB-001",
  "product_name": "众链贷",
  "bank": "众邦银行",
  "product_type": "供应链金融",
  "product_form": "数字化供应链融资",
  "target_customer": "核心企业上下游中小企业",
  "entry_conditions": {
    "enterprise_type": ["民企"],
    "industry": ["全行业"],
    "scale": "年营收>100万",
    "guarantee": "核心企业确权"
  },
  "product_features": {
    "interest_rate": "6-10%",
    "term": "最长1年",
    "amount": "根据核心企业信用"
  },
  "supply_chain_position": ["上游", "下游"],
  "core_advantages": [
    "专注供应链金融",
    "卓尔集团资源支持",
    "线上化操作"
  ]
}
```

---

### 新网银行（1个产品）

| 产品ID | 产品名称 | 产品类型 | 供应链位置 | 目标客户 | 额度 |
|--------|----------|----------|------------|----------|------|
| PROD-XW-001 | 好企e贷 | 供应链贷款 | 上游 | 供应商 | 最高500万 |

```json
{
  "product_id": "PROD-XW-001",
  "product_name": "好企e贷",
  "bank": "新网银行",
  "product_type": "数字化供应链融资",
  "product_form": "线上供应链贷款",
  "target_customer": "核心企业上游供应商",
  "entry_conditions": {
    "enterprise_type": ["民企"],
    "industry": ["医疗、快消、汽车"],
    "scale": "年营收>500万"
  },
  "product_features": {
    "interest_rate": "8-12%",
    "term": "最长1年",
    "amount": "最高500万"
  },
  "supply_chain_position": ["上游"],
  "core_advantages": [
    "深耕医疗产业链",
    "全线上、无接触开户",
    "数据信用替代抵押",
    "T+0审批放款"
  ]
}
```

---

## 待补充产品银行

| 银行 | 定位 | 优先级 |
|------|------|--------|
| 亿联银行 | 互联网贷款 | 🟢 低 |
| 振兴银行 | 互联网贷款 | 🟢 低 |
| 裕民银行 | 互联网金融 | 🟢 低 |
| 新安银行 | 小微金融 | 🟢 低 |
| 金城银行 | 科技金融 | 🟡 中 |
| 梅州客商银行 | 产业银行 | 🟢 低 |
| 锡商银行 | 纺织供应链 | 🟡 中 |
| 华通银行 | 商超供应链 | 🟡 中 |
| 蓝海银行 | 互联网贷款 | 🟢 低 |
| 富民银行 | 小微金融 | 🟢 低 |
| 众裕银行 | 互联网金融 | 🟢 低 |
| 民丰银行 | 小微金融 | 🟢 低 |

---

## 数据来源

1. 证券时报2024年报统计
2. 各银行官网及产品页
3. 行业媒体：36氪、中国银行业协会
4. 银行年报及公告

---

*民营互联网银行产品库 | 2026-04-13*

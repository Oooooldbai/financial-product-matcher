# 数据采集框架

> 金融产品智能匹配工具的基础数据库采集流程

---

## 采集架构

```
数据源 → 采集器 → 标准化处理 → 知识库存储
                              ↓
                         Rules层调用
```

---

## 一、数据源分类

### 产品域数据源

#### 银行类（需补充完整名单）

**国有大行（6家）**
| 银行 | 官网 | 优先级 |
|------|------|---------|
| 工商银行 | icbc.com.cn | ⭐⭐⭐⭐⭐ |
| 农业银行 | abchina.com | ⭐⭐⭐⭐⭐ |
| 中国银行 | boc.cn | ⭐⭐⭐⭐⭐ |
| 建设银行 | ccb.com | ⭐⭐⭐⭐⭐ |
| 交通银行 | bankcomm.com | ⭐⭐⭐⭐ |
| 邮储银行 | psbc.com | ⭐⭐⭐⭐ |

**股份制银行（12家）**
| 银行 | 官网 | 优先级 |
|------|------|---------|
| 招商银行 | cmbchina.com | ⭐⭐⭐⭐⭐ |
| 浦发银行 | spdb.com.cn | ⭐⭐⭐⭐ |
| 中信银行 | citicbank.com | ⭐⭐⭐⭐ |
| 民生银行 | cmbc.com.cn | ⭐⭐⭐⭐ |
| 兴业银行 | cib.com.cn | ⭐⭐⭐⭐ |
| 光大银行 | cebbank.com | ⭐⭐⭐⭐ |
| 平安银行 | bank.pingan.com | ⭐⭐⭐⭐ |
| 华夏银行 | hxb.com.cn | ⭐⭐⭐ |
| 广发银行 | cgbchina.com.cn | ⭐⭐⭐ |
| 浙商银行 | czbank.com | ⭐⭐⭐ |
| 渤海银行 | cbhb.com.cn | ⭐⭐⭐ |
| 恒丰银行 | hfbank.com.cn | ⭐⭐⭐ |

**民营互联网银行（19家）**✅ 数据来源：证券时报2024年报统计
| 银行 | 股东背景 | 2024资产(亿) | 定位 |
|------|----------|--------------|------|
| 微众银行 | 腾讯 | 6517.76 | 微贷/小微 |
| 网商银行 | 蚂蚁集团 | 4710.35 | 电商/小微 |
| 苏商银行 | 苏宁 | 1375.54 | 综合金融 |
| 众邦银行 | 卓尔 | 1235.31 | 供应链金融 |
| 新网银行 | 小米等 | 1036.29 | 互联网贷款 |
| 亿联银行 | 美团等 | 408.22 | 互联网贷款 |
| 三湘银行 | 三一集团 | 527.67 | 产业链金融 |
| 振兴银行 | 三六零 | 288.83 | 互联网贷款 |
| 裕民银行 | 正邦集团→南昌金控 | 208.03 | 互联网金融 |
| 新安银行 | 安徽南翔→合肥金控 | - | 小微金融 |
| 金城银行 | 360等 | - | 科技金融 |
| 梅州客商银行 | 宝新能源 | - | 产业银行 |
| 锡商银行 | 红豆等 | - | 纺织供应链 |
| 华通银行 | 永辉 | - | 商超供应链 |
| 蓝海银行 | 蓝海集团 | - | 互联网贷款 |
| 中关村银行 | 用友等 | - | 科技企业 |
| 富民银行 | 瀚华金控 | - | 小微金融 |
| 众裕银行 | - | - | 互联网金融 |
| 民丰银行 | 温州民企 | - | 小微金融 |

**外资银行**
| 银行 | 官网 | 优先级 |
|------|------|---------|
| 汇丰银行 | hsbc.com.cn | ⭐⭐⭐⭐ |
| 花旗银行 | citibank.com.cn | ⭐⭐⭐⭐ |
| 渣打银行 | sc.com | ⭐⭐⭐⭐ |
| 星展银行 | dbs.com.cn | ⭐⭐⭐ |
| 摩根大通 | jpmorgan.com | ⭐⭐⭐ |

#### 公开数据源（补充渠道）

| 数据源 | 内容 | 优先级 | 采集方式 |
|--------|------|--------|----------|
| **财经媒体** | | | |
| 21经济网 | 金融产品报道 | ⭐⭐⭐⭐ | 搜索 |
| 第一财经 | 金融产品评测 | ⭐⭐⭐⭐ | 搜索 |
| 证券时报 | 金融产品信息 | ⭐⭐⭐⭐ | 搜索 |
| **行业平台** | | | |
| 企业预警通 | 金融产品库 | ⭐⭐⭐⭐⭐ | API/搜索 |
| 信贷经理网 | 金融产品对比 | ⭐⭐⭐⭐⭐ | 搜索 |
| 同业金融 | 供应链金融 | ⭐⭐⭐⭐ | 搜索 |
| **监管平台** | | | |
| 票交所 | 票据产品 | ⭐⭐⭐⭐⭐ | API |
| 中国支付清算协会 | 支付产品 | ⭐⭐⭐ | 搜索 |
| **金融科技平台** | | | |
| 京东供应链金融 | SCF产品 | ⭐⭐⭐⭐ | 搜索 |
| 蚂蚁链 | 供应链金融 | ⭐⭐⭐⭐ | 搜索 |
| 中企云链 | 供应链金融 | ⭐⭐⭐⭐ | 搜索 |
| 苏宁供应链金融 | SCF产品 | ⭐⭐⭐ | 搜索 |
| **保理公司** | | | |
| 鑫银保理 | 保理产品 | ⭐⭐⭐⭐ | 搜索 |
| 摩银保理 | 保理产品 | ⭐⭐⭐ | 搜索 |

### 客户域数据源

| 数据源 | 类型 | 优先级 | 更新频率 | 采集方式 |
|--------|------|--------|----------|----------|
| 天眼查/企查查 | 企业基础信息 | ⭐⭐⭐⭐⭐ | 按需 | API |
| 巨潮资讯（年报） | 财务数据 | ⭐⭐⭐⭐ | 季度 | 搜索 |
| 东方财富 | 行业数据 | ⭐⭐⭐⭐ | 月度 | API |
| 央行征信 | 信用数据 | ⭐⭐⭐ | 月度 | API |

### 政策法规域数据源

| 数据源 | 类型 | 优先级 | 更新频率 | 采集方式 |
|--------|------|--------|----------|----------|
| 央行官网 | 政策文件 | ⭐⭐⭐⭐⭐ | 实时 | RSS+搜索 |
| 银保监会官网 | 监管规定 | ⭐⭐⭐⭐⭐ | 实时 | RSS+搜索 |
| 证监会官网 | ABS/债券规定 | ⭐⭐⭐⭐ | 实时 | RSS+搜索 |
| 财政部官网 | 会计准则 | ⭐⭐⭐⭐ | 按需 | 搜索 |
| 税务总局官网 | 税务规定 | ⭐⭐⭐⭐ | 按需 | 搜索 |
| 人大官网 | 法律法规 | ⭐⭐⭐⭐ | 按需 | 搜索 |

---

## 二、采集器设计

### 采集器列表

```
scripts/
├── collectors/
│   ├── bank_product_collector.py      # 银行产品采集器 ⭐每日(前期)
│   ├── policy_collector.py             # 政策采集器 ⭐每周
│   ├── regulation_collector.py        # 法规采集器 ⭐每周
│   ├── enterprise_collector.py         # 企业信息采集器 按需
│   └── financial_data_collector.py     # 财务数据采集器 每季度
│
├── processors/
│   ├── text_normalizer.py             # 文本标准化
│   ├── data_extractor.py              # 数据提取
│   └── knowledge_formatter.py        # 知识库格式化
│
├── updaters/
│   ├── daily_updater.py              # 每日更新
│   ├── weekly_updater.py             # 每周更新
│   └── monthly_updater.py            # 每月更新
│
└── schedulers/
    ├── cron_scheduler.py             # 定时任务
    └── trigger_updater.py            # 触发更新
```

---

## 三、产品域采集流程

### 3.1 银行产品采集

```python
# bank_product_collector.py

"""
银行产品信息采集器
目标：采集各银行供应链金融产品信息
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

BANK_PRODUCTS = {
    "ICBC": "https://www.icbc.com.cn/icbc/",
    "ABC": "https://www.abchina.com/cn/",
    "BOC": "https://www.boc.cn/",
    "CCB": "https://www.ccb.com/",
    "CMB": "https://www.cmbchina.com/",
    "PINGAN": "https://bank.pingan.com/",
}

def collect_bank_products():
    """
    采集银行产品信息
    输出：产品基础信息JSON
    """
    results = []
    
    for bank_name, url in BANK_PRODUCTS.items():
        # 1. 访问银行官网
        # 2. 查找供应链金融/贸易金融产品
        # 3. 提取产品信息
        # 4. 标准化存储
        
        product_info = {
            "bank_name": bank_name,
            "products": [],
            "collected_at": datetime.now().isoformat(),
            "source_url": url
        }
        results.append(product_info)
    
    return results

def extract_product_details(html):
    """
    从HTML中提取产品详情
    """
    soup = BeautifulSoup(html, 'html.parser')
    
    # 提取产品名称、利率、期限、准入条件等
    # ...
    
    return {
        "product_name": "",
        "product_type": "",
        "interest_rate": "",
        "term_range": "",
        "min_amount": "",
        "max_amount": "",
        "requirements": [],
        "documents_needed": []
    }
```

### 3.2 产品标准化模板

```json
{
  "product_id": "xxx",
  "product_name": "产品名称",
  "product_type": "DD/SCF/保理/票据/ABS/其他",
  "provider": {
    "name": "机构名称",
    "type": "银行/保理/核心企业/其他",
    "license": "牌照类型"
  },
  "basic_info": {
    "min_amount": "最低额度",
    "max_amount": "最高额度",
    "interest_rate": "利率区间",
    "term_range": "期限范围",
    "repayment_method": "还款方式"
  },
  "requirements": {
    "enterprise_type": ["民营上市", "国央企", "外资"],
    "industry": ["制造业", "零售", "医药", "科技", "汽车"],
    "min_scale": "最低规模门槛",
    "min_years": "成立年限要求",
    "credit_requirement": "信用要求",
    "trade_background": "贸易背景要求"
  },
  "risk_control": {
    "guarantee_type": "担保类型",
    "core_enterprise_requirement": "核心企业要求",
    "financing_ratio": "融资比例"
  },
  "documents_needed": ["所需材料清单"],
  "process_steps": ["业务流程"],
  "source_url": "来源URL",
  "collected_at": "采集时间",
  "updated_at": "更新时间"
}
```

---

## 四、政策法规域采集流程

### 4.1 政策采集器

```python
# policy_collector.py

"""
政策文件采集器
目标：实时采集央行、银保监、证监会等政策文件
"""

import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

POLICY_SOURCES = {
    "央行": "http://www.pbc.gov.cn/",
    "银保监会": "http://www.cbirc.gov.cn/",
    "证监会": "http://www.csrc.gov.cn/",
    "财政部": "http://www.mof.gov.cn/",
    "税务总局": "http://www.chinatax.gov.cn/",
}

RSS_FEEDS = {
    "央行": "http://www.pbc.gov.cn/rss.xml",
    "银保监会": "http://www.cbirc.gov.cn/rss.xml",
    "证监会": "http://www.csrc.gov.cn/rss.xml",
}

def collect_policies(days=7):
    """
    采集近N天的政策文件
    """
    new_policies = []
    
    for source, rss_url in RSS_FEEDS.items():
        feed = feedparser.parse(rss_url)
        
        for entry in feed.entries[:20]:  # 最近20条
            if is_recent(entry.published, days):
                policy = {
                    "title": entry.title,
                    "source": source,
                    "url": entry.link,
                    "published_at": entry.published,
                    "content": fetch_policy_content(entry.link)
                }
                new_policies.append(policy)
    
    return new_policies

def is_recent(published_str, days):
    """判断是否在近N天内"""
    # ...
    pass

def fetch_policy_content(url):
    """获取政策全文"""
    # ...
    pass

def classify_policy(policy):
    """
    政策分类
    - 供应链金融相关
    - 票据相关
    - 保理相关
    - ABS相关
    """
    keywords = {
        "供应链金融": ["供应链", "SCF", "应付账款"],
        "票据": ["票据", "银票", "商票", "贴现"],
        "保理": ["保理", "应收账款"],
        "ABS": ["资产支持", "ABS", "证券化"]
    }
    
    for category, kws in keywords.items():
        if any(kw in policy["title"] for kw in kws):
            return category
    
    return "其他"
```

### 4.2 政策标准化模板

```json
{
  "policy_id": "xxx",
  "title": "政策标题",
  "document_number": "文号",
  "source": "央行/银保监会/证监会/财政部/税务总局/其他",
  "issued_by": "发布机构",
  "issued_at": "发布日期",
  "category": "供应链金融/票据/保理/ABS/企业信贷/其他",
  "keywords": ["关键词1", "关键词2"],
  "summary": "政策摘要",
  "key_points": ["要点1", "要点2"],
  "affected_products": ["影响的产品类型"],
  "compliance_requirements": ["合规要求"],
  "risk_warnings": ["风险提示"],
  "effective_date": "生效日期",
  "source_url": "原文URL",
  "content": "政策全文",
  "collected_at": "采集时间"
}
```

---

## 五、客户域采集流程

### 5.1 企业信息采集

```python
# enterprise_collector.py

"""
企业信息采集器
目标：采集企业基础信息和财务数据
"""

ENTERPRISE_DATA_SOURCES = {
    "tianyancha": "https://www.tianyancha.com/",  # 需要API
    "annual_report": "http://www.cninfo.com.cn/",  # 年报
    "eastmoney": "https://www.eastmoney.com/",  # 行业数据
}

def collect_enterprise_info(enterprise_name):
    """
    采集企业信息
    """
    enterprise = {
        "name": enterprise_name,
        "basic_info": {},
        "financial_data": {},
        "industry_info": {},
        "credit_info": {}
    }
    
    # 1. 天眼查/企查查 - 企业基础信息
    # basic = fetch_basic_info(enterprise_name)
    # enterprise["basic_info"] = basic
    
    # 2. 年报 - 财务数据
    # financial = fetch_financial_data(enterprise_name)
    # enterprise["financial_data"] = financial
    
    # 3. 行业数据
    # industry = fetch_industry_data(enterprise)
    # enterprise["industry_info"] = industry
    
    return enterprise
```

### 5.2 企业标准化模板

```json
{
  "enterprise_id": "xxx",
  "name": "企业名称",
  "alias": ["别名/简称"],
  "basic_info": {
    "unified_credit_code": "统一社会信用代码",
    "legal_representative": "法定代表人",
    "established_date": "成立日期",
    "registered_capital": "注册资本",
    "industry": "所属行业",
    "enterprise_type": "企业类型",
    "employee_count": "员工人数",
    "address": "地址"
  },
  "financial_data": {
    "latest_year": "2024",
    "annual_revenue": "年营收",
    "total_assets": "总资产",
    "total_liabilities": "总负债",
    "liability_ratio": "资产负债率",
    "net_profit": "净利润",
    "annual_payable": "年应付账款",
    "average_payment_period": "平均账期(天)",
    "cash_flow": "现金流状况"
  },
  "industry_info": {
    "industry_category": "行业分类",
    "industry_position": "行业地位",
    "main_products": "主要产品",
    "suppliers_count": "供应商数量",
    "customers_count": "客户数量",
    "erp_system": "ERP系统"
  },
  "credit_info": {
    "credit_rating": "信用评级",
    "bank_credit_limit": "银行授信额度",
    "used_credit_limit": "已用授信",
    "default_records": "违约记录"
  },
  "supply_chain_position": {
    "position": "核心企业/一级供应商/二级供应商/其他",
    "core_enterprise_relation": "与核心企业关系",
    "target_customers": "目标客户类型"
  },
  "collected_at": "采集时间",
  "updated_at": "更新时间"
}
```

---

## 六、更新机制

### 6.1 更新频率

| 数据类型 | 前期频率 | 后期频率 | 说明 |
|----------|----------|----------|------|
| 产品信息 | **每日** | 每周 | 前期快速填充，后期稳定后降低 |
| 政策文件 | **每周** | 每月 | 政策变化频率低 |
| 法规条文 | 按需 | 按需 | 非实时，有沉淀期 |
| 企业信息 | 按需 | 按需 | 查询时更新 |
| 财务数据 | 每季度 | 每季度 | 年报发布季 |
| 行业数据 | 每月 | 每季度 | 变化较慢 |

### 6.2 定时任务配置

```python
# schedulers/cron_tasks.py

"""
定时任务配置
前期：快速填充数据，提高频率
后期：稳定维护，降低频率
"""

CRON_TASKS = {
    # ========== 前期（快速填充阶段）==========
    "daily": {
        "bank_product_update": "0 9 * * *",  # 每天9点 - 产品信息采集
        "industry_news": "0 8 * * *",         # 每天8点 - 行业动态
    },
    "weekly": {
        "policy_monitor": "0 10 * * 1",      # 每周一10点 - 政策文件采集
        "regulation_update": "0 10 * * 3",    # 每周三10点 - 法规更新
        "enterprise_news": "0 9 * * 5",      # 每周五9点 - 企业动态
    },
    
    # ========== 后期（稳定维护阶段）==========
    "weekly_stable": {
        "bank_product_update": "0 10 * * 1", # 每周一10点 - 产品信息
        "policy_monitor": "0 10 * * 1",      # 每周一10点 - 政策文件
    },
    "monthly": {
        "comprehensive_update": "0 10 1 * *",  # 每月1号10点
        "data_cleanup": "0 2 1 * *",             # 每月1号2点
    },
    "quarterly": {
        "financial_data_update": "0 10 15 */3 *",  # 每季度15号
        "product_catalog_update": "0 10 20 */3 *"   # 每季度20号
    }
}

# 切换标志（用于控制前期/后期模式）
PHASE = "early"  # "early" = 前期, "stable" = 后期
```

---

## 七、采集状态追踪

### 7.1 采集日志

```json
{
  "collector_name": "bank_product_collector",
  "last_run": "2026-04-12T14:53:00",
  "status": "success/failed/running",
  "items_collected": 15,
  "errors": [],
  "next_run": "2026-04-19T14:53:00"
}
```

### 7.2 数据质量检查

```python
def quality_check(data):
    """
    数据质量检查
    - 完整性：必填字段是否齐全
    - 准确性：数据格式是否正确
    - 时效性：数据是否过期
    - 一致性：同类数据是否一致
    """
    issues = []
    
    # 检查完整性
    required_fields = ["name", "type", "collected_at"]
    for field in required_fields:
        if field not in data or not data[field]:
            issues.append(f"Missing required field: {field}")
    
    # 检查准确性
    if "interest_rate" in data:
        try:
            rate = float(data["interest_rate"].replace("%", ""))
            if rate < 0 or rate > 100:
                issues.append(f"Invalid interest rate: {rate}")
        except:
            issues.append(f"Cannot parse interest rate: {data['interest_rate']}")
    
    return {
        "passed": len(issues) == 0,
        "issues": issues
    }
```

---

## 八、下一步

### 优先级1：建立采集器框架
- [ ] 创建 `scripts/collectors/` 目录
- [ ] 实现基础采集器模板
- [ ] 实现定时任务配置

### 优先级2：先实现政策采集
- [ ] 政策采集器（最重要，风险评估需要）
- [ ] RSS监控
- [ ] 政策分类

### 优先级3：再实现产品采集
- [ ] 银行产品采集器
- [ ] 产品标准化
- [ ] 定期更新

---

*数据采集框架 | 最后更新: 2026-04-12*

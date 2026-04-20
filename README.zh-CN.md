# TdxQuant - 通达信量化平台

## 项目简介

TdxQuant 是由深圳市财富趋势科技股份有限公司研发的专业量化投研平台，专注于为国内量化投资者提供从策略研究到投资决策的全流程解决方案。本项目提供将通达信量化平台的核心Python组件转换成可以编辑的Python安装包。

项目内容与<通达信安装目录>/PYPlugins/user/目录下的文件保持一致。添加了pyproject.toml文件，用于管理项目依赖。

## 运行环境要求

### 系统要求

- **操作系统**：Windows平台
- **Python版本**：Python 3.13（推荐）

### 核心依赖

```
backtrader>=1.9.78.123
numpy>=2.4.3
pandas>=3.0.1
vectorbt>=0.28.2
```

### 前置条件

- **必须预先启动通达信客户端**：需使用支持TQ策略功能的通达信专业研究版、量化模拟版或期货通等版本
- **必须登录通达信账户**：确保客户端已正常登录并具备相应的数据权限

## 安装方法

### ⚠️ 重要说明：路径依赖与安装模式

本项目作为通达信量化平台的组成部分，具有**固定的路径依赖关系**，Python包**不支持发布模式**。在开发和使用过程中，**必须**通过可编辑模式安装项目依赖。

### 安装步骤

#### 1. 确认项目路径

确保项目位于通达信客户端的正确路径下：

```
<通达信安装目录>/PYPlugins/user/
```

#### 2. 可编辑模式安装（必须）

在项目根目录下执行以下命令：

```bash
pip install -e .
```

**说明**：

- `-e` 参数表示以可编辑模式（editable mode）安装，允许开发者在不重新安装的情况下直接修改代码
- 此安装方式确保项目能够正确访问通达信客户端的DLL文件及其他依赖资源
- 安装后可直接导入 `tqcenter` 模块使用

#### 3. 验证安装

```python
from tqcenter import tq
print("TdxQuant 安装成功！")
```

## 路径依赖说明

### 核心依赖文件

项目依赖通达信客户端提供的核心动态链接库：

```
<通达信安装目录>/PYPlugins/TPythClient.dll
```

### 路径解析机制

- 项目通过相对路径自动定位DLL文件：`Path(__file__).resolve().parents[1] / 'TPythClient.dll'`
- 这要求项目必须保持在通达信客户端的标准目录结构中
- **切勿移动或重命名项目目录**，否则将导致DLL加载失败

## 核心功能模块

### 1. 数据获取模块

#### K线数据获取

```python
from tqcenter import tq

tq.initialize(__file__)

df = tq.get_market_data(
    field_list=['Open', 'High', 'Low', 'Close', 'Volume'],
    stock_list=['688318.SH'],
    start_time='20250101',
    end_time='20250601',
    period='1d',
    dividend_type='none'
)
```

**支持的K线周期**：1d、1w、1m、5m、15m、30m、60m等

**复权类型**：

- `none`：不复权
- `front`：前复权
- `back`：后复权

#### 市场快照数据

```python
snapshot = tq.get_market_snapshot(stock_code='688318.SH')
```

#### 财务数据获取

```python
basic_financial = tq.get_stock_info(stock_code='688318.SH')

professional_financial = tq.get_financial_data(
    stock_list=['688318.SH'],
    field_list=['Fn193', 'Fn194'],
    start_time='20250101',
    report_type='announce_time'
)
```

### 2. 交易日历与股票列表

#### 交易日获取

```python
trade_dates = tq.get_trading_dates(
    market='SH',
    start_time='20250101',
    end_time='20251231'
)
```

#### 股票列表获取

```python
all_stocks = tq.get_stock_list('5')
etf_list = tq.get_stock_list('31')
```

**列表类型代码**：

- `5`：所有A股
- `31`：ETF基金
- `32`：可转债
- `51`：创业板
- `52`：科创板
- `53`：北交所

### 3. 板块管理

#### 获取板块列表

```python
block_list = tq.get_sector_list()
```

#### 获取板块成分股

```python
stocks = tq.get_stock_list_in_sector('钛金属')
```

#### 自定义板块管理

```python
tq.create_sector(block_code='MYBK', block_name='我的板块')
tq.send_user_block(block_code='MYBK', stocks=['688318.SH', '600519.SH'])
tq.delete_sector(block_code='MYBK')
```

### 4. 通达信公式集成

#### 指标公式调用

```python
macd_result = tq.formula_zb(formula_name='MACD', formula_arg='12,26,9')
```

#### 条件选股公式

```python
selected_stocks = tq.formula_xg(formula_name='UPN', formula_arg='3')
```

#### 批量公式处理

```python
results = tq.formula_process_mul_zb(
    formula_name='MACD',
    formula_arg='12,26,9',
    stock_list=['688318.SH', '600519.SH'],
    stock_period='1d',
    count=100
)
```

### 5. 实时订阅与预警

#### 订阅股票更新

```python
def my_callback(data_str):
    import json
    data = json.loads(data_str)
    print(f"股票 {data['Code']} 有更新")

tq.subscribe_hq(stock_list=['688318.SH'], callback=my_callback)
```

#### 发送预警信号

```python
tq.send_warn(
    stock_list=['688318.SH'],
    time_list=['20250620143000'],
    price_list=['123.45'],
    close_list=['122.50'],
    volum_list=['1000'],
    reason_list=['价格突破预警线'],
    count=1
)
```

### 6. 数据导出与可视化

#### 导出因子数据

```python
import pandas as pd

df = pd.DataFrame({
    '日期': ['2025-01-01', '2025-01-02'],
    '因子1': [1.2, 1.3],
    '因子2': [2.1, 2.2]
})

tq.print_to_tdx(
    df_list=[df],
    sp_name='我的因子',
    xml_filename='factor.xml'
)
```

## 与通达信量化平台的集成要点

### 1. 初始化连接

**所有策略必须首先调用初始化函数**：

```python
from tqcenter import tq

tq.initialize(__file__)
```

此函数将：

- 建立与通达信客户端的连接
- 加载必要的DLL资源
- 初始化数据通道

### 2. 数据权限与下载

- 部分历史数据需要先在通达信客户端中下载对应的盘后数据
- 专业财务数据需在客户端中预先下载
- 建议在策略运行前刷新行情缓存：

```python
tq.refresh_cache()
```

### 3. 策略生命周期管理

```python
from tqcenter import tq

try:
    tq.initialize(__file__)
    
    # 策略逻辑代码
    # ...
    
finally:
    # 确保正确关闭连接
    tq.close()
```

**重要**：

- 程序退出时会自动断开连接
- 如遇异常退出，需在通达信策略管理器中手动删除策略记录

### 4. 股票代码格式规范

**必须使用标准格式**：`6位数字代码.市场后缀`

**示例**：

- 上海证券交易所：`600519.SH`、`688318.SH`
- 深圳证券交易所：`000001.SZ`、`300750.SZ`
- 北京证券交易所：`832566.BJ`

### 5. 时间格式规范

- **日期格式**：`YYYYMMDD`（如：`20250620`）
- **日期时间格式**：`YYYYMMDDHHMMSS`（如：`20250620143000`）

### 6. 数据单位说明

- **价格数据**：单位为元
- **成交量**：单位为手
- **成交额**：单位为万元
- **财务数据**（股本、资产、负债等）：单位为万元

## 快速开始示例

### 完整策略示例

```python
from tqcenter import tq
import pandas as pd

def simple_strategy():
    try:
        # 1. 初始化连接
        tq.initialize(__file__)
        
        # 2. 获取股票列表
        stock_list = tq.get_stock_list('5')
        
        # 3. 获取K线数据
        df = tq.get_market_data(
            stock_list=['688318.SH'],
            start_time='20250101',
            end_time='20250601',
            period='1d',
            dividend_type='front'
        )
        
        # 4. 计算简单指标
        close_prices = tq.price_df(df, 'Close')
        ma20 = close_prices.rolling(window=20).mean()
        
        # 5. 发送消息到客户端
        tq.send_message("策略运行完成 | 已计算20日均线")
        
        # 6. 导出因子数据
        tq.print_to_tdx(
            df_list=[ma20],
            sp_name='MA20因子',
            xml_filename='ma20_factor.xml'
        )
        
        print("策略执行成功！")
        
    except Exception as e:
        print(f"策略执行出错: {e}")
        tq.send_message(f"策略错误: {str(e)}")
        
    finally:
        # 7. 关闭连接
        tq.close()

if __name__ == '__main__':
    simple_strategy()
```

## 注意事项

### ⚠️ 重要警告

1. **必须使用可编辑模式安装**
   - 项目不支持 `pip install` 的常规安装模式
   - 必须使用 `pip install -e .` 进行可编辑模式安装
   - 不支持发布到PyPI或其他包管理平台
2. **路径依赖不可更改**
   - 项目必须在通达信客户端的标准目录结构中运行
   - 切勿移动、重命名项目目录或修改相对路径结构
3. **客户端依赖**
   - 运行前必须启动通达信客户端并登录
   - 需使用支持TQ策略功能的客户端版本
   - 确保客户端具备相应的数据权限
4. **数据准备**
   - 历史K线数据需在客户端中预先下载
   - 专业财务数据需在客户端中预先下载
   - 建议定期刷新行情缓存
5. **连接管理**
   - 策略结束时务必调用 `tq.close()` 关闭连接
   - 异常退出后需在策略管理器中清理策略记录
   - 避免同时运行多个同名策略实例

### 💡 最佳实践

1. **错误处理**
   ```python
   try:
       tq.initialize(__file__)
       # 策略逻辑
   except Exception as e:
       print(f"错误: {e}")
       tq.send_message(f"策略异常: {str(e)}")
   finally:
       tq.close()
   ```
2. **数据验证**
   ```python
   # 验证股票代码格式
   if not check_stock_code_format('688318.SH'):
       print("股票代码格式错误")
   ```
3. **性能优化**
   - 批量获取数据而非逐只股票获取
   - 合理使用缓存机制
   - 避免频繁刷新行情数据

## 技术支持

- **官方文档**：<https://help.tdx.com.cn/quant/docs/markdown/mindoc-1cfsjkbf8f3is/>

## 许可声明

本项目为通达信量化平台的核心组件，使用需遵守通达信相关许可协议。未经授权，不得用于商业用途或二次分发。

***


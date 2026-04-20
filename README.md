# TdxQuant - TongDaXin Quantitative Platform

(通达信量化平台)

## Project Introduction

TdxQuant is a professional quantitative investment research platform developed by Shenzhen Wealth Trend Technology Co., Ltd., focusing on providing a full-process solution from strategy research to investment decisions for domestic quantitative investors. This project provides the conversion of the core Python components of the TongDaXin quantitative platform into an editable Python installation package.

The project content is consistent with the files in the `<TongDaXin Installation Directory>/PYPlugins/user/` directory. A `pyproject.toml` file has been added to manage project dependencies.

## Runtime Environment Requirements

### System Requirements

- **Operating System**: Windows platform
- **Python Version**: Python 3.13 (recommended)

### Core Dependencies

```
backtrader>=1.9.78.123
numpy>=2.4.3
pandas>=3.0.1
vectorbt>=0.28.2
```

### Prerequisites

- **Must start TongDaXin client first**: Need to use TongDaXin Professional Research Edition, Quantitative Simulation Edition, or Futures Edition that supports TQ strategy functionality
- **Must login to TongDaXin account**: Ensure the client has logged in normally and has the corresponding data permissions

## Installation Method

### ⚠️ Important Note: Path Dependency and Installation Mode

This project, as a component of the TongDaXin quantitative platform, has **fixed path dependencies**, and the Python package **does not support release mode**. During development and use, project dependencies **must** be installed through editable mode.

### Installation Steps

#### 1. Confirm Project Path

Ensure the project is located in the correct path of the TongDaXin client:

```
<TongDaXin Installation Directory>/PYPlugins/user/
```

#### 2. Editable Mode Installation (Required)

Execute the following command in the project root directory:

```bash
pip install -e .
```

**Explanation**:

- The `-e` parameter indicates installation in editable mode, allowing developers to modify code directly without reinstalling
- This installation method ensures the project can correctly access the TongDaXin client's DLL files and other dependent resources
- After installation, you can directly import the `tqcenter` module for use

#### 3. Verify Installation

```python
from tqcenter import tq
print("TdxQuant installed successfully!")
```

## Path Dependency Instructions

### Core Dependency Files

The project depends on the core dynamic link library provided by the TongDaXin client:

```
<TongDaXin Installation Directory>/PYPlugins/TPythClient.dll
```

### Path Resolution Mechanism

- The project automatically locates DLL files through relative paths: `Path(__file__).resolve().parents[1] / 'TPythClient.dll'`
- This requires the project to remain in the standard directory structure of the TongDaXin client
- **Never move or rename the project directory**, otherwise DLL loading will fail

## Core Functional Modules

### 1. Data Acquisition Module

#### K-Line Data Acquisition

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

**Supported K-line periods**: 1d, 1w, 1m, 5m, 15m, 30m, 60m, etc.

**Adjustment types**:

- `none`: No adjustment
- `front`: Forward adjustment
- `back`: Backward adjustment

#### Market Snapshot Data

```python
snapshot = tq.get_market_snapshot(stock_code='688318.SH')
```

#### Financial Data Acquisition

```python
basic_financial = tq.get_stock_info(stock_code='688318.SH')

professional_financial = tq.get_financial_data(
    stock_list=['688318.SH'],
    field_list=['Fn193', 'Fn194'],
    start_time='20250101',
    report_type='announce_time'
)
```

### 2. Trading Calendar and Stock List

#### Trading Date Acquisition

```python
trade_dates = tq.get_trading_dates(
    market='SH',
    start_time='20250101',
    end_time='20251231'
)
```

#### Stock List Acquisition

```python
all_stocks = tq.get_stock_list('5')
etf_list = tq.get_stock_list('31')
```

**List type codes**:

- `5`: All A-shares
- `31`: ETF funds
- `32`: Convertible bonds
- `51`: ChiNext
- `52`: STAR Market
- `53`: Beijing Stock Exchange

### 3. Sector Management

#### Get Sector List

```python
block_list = tq.get_sector_list()
```

#### Get Sector Constituents

```python
stocks = tq.get_stock_list_in_sector('Titanium Metal')
```

#### Custom Sector Management

```python
tq.create_sector(block_code='MYBK', block_name='My Sector')
tq.send_user_block(block_code='MYBK', stocks=['688318.SH', '600519.SH'])
tq.delete_sector(block_code='MYBK')
```

### 4. TongDaXin Formula Integration

#### Indicator Formula Call

```python
macd_result = tq.formula_zb(formula_name='MACD', formula_arg='12,26,9')
```

#### Condition Stock Selection Formula

```python
selected_stocks = tq.formula_xg(formula_name='UPN', formula_arg='3')
```

#### Batch Formula Processing

```python
results = tq.formula_process_mul_zb(
    formula_name='MACD',
    formula_arg='12,26,9',
    stock_list=['688318.SH', '600519.SH'],
    stock_period='1d',
    count=100
)
```

### 5. Real-time Subscription and Alerts

#### Subscribe to Stock Updates

```python
def my_callback(data_str):
    import json
    data = json.loads(data_str)
    print(f"Stock {data['Code']} has an update")

tq.subscribe_hq(stock_list=['688318.SH'], callback=my_callback)
```

#### Send Alert Signal

```python
tq.send_warn(
    stock_list=['688318.SH'],
    time_list=['20250620143000'],
    price_list=['123.45'],
    close_list=['122.50'],
    volum_list=['1000'],
    reason_list=['Price breakthrough alert line'],
    count=1
)
```

### 6. Data Export and Visualization

#### Export Factor Data

```python
import pandas as pd

df = pd.DataFrame({
    'Date': ['2025-01-01', '2025-01-02'],
    'Factor1': [1.2, 1.3],
    'Factor2': [2.1, 2.2]
})

tq.print_to_tdx(
    df_list=[df],
    sp_name='My Factor',
    xml_filename='factor.xml'
)
```

## Integration Points with TongDaXin Quantitative Platform

### 1. Initialize Connection

**All strategies must first call the initialization function**:

```python
from tqcenter import tq

tq.initialize(__file__)
```

This function will:

- Establish connection with the TongDaXin client
- Load necessary DLL resources
- Initialize data channels

### 2. Data Permissions and Download

- Some historical data needs to be downloaded in the TongDaXin client first
- Professional financial data needs to be pre-downloaded in the client
- It is recommended to refresh the market cache before running the strategy:

```python
tq.refresh_cache()
```

### 3. Strategy Lifecycle Management

```python
from tqcenter import tq

try:
    tq.initialize(__file__)
    
    # Strategy logic code
    # ...
    
finally:
    # Ensure proper connection closure
    tq.close()
```

**Important**:

- The connection will be automatically disconnected when the program exits
- If there is an abnormal exit, you need to manually delete the strategy record in the TongDaXin strategy manager

### 4. Stock Code Format Specification

**Must use standard format**: `6-digit code.market suffix`

**Examples**:

- Shanghai Stock Exchange: `600519.SH`, `688318.SH`
- Shenzhen Stock Exchange: `000001.SZ`, `300750.SZ`
- Beijing Stock Exchange: `832566.BJ`

### 5. Time Format Specification

- **Date format**: `YYYYMMDD` (e.g.: `20250620`)
- **Datetime format**: `YYYYMMDDHHMMSS` (e.g.: `20250620143000`)

### 6. Data Unit Description

- **Price data**: Unit is Yuan
- **Volume**: Unit is lots
- **Turnover**: Unit is ten thousand Yuan
- **Financial data** (share capital, assets, liabilities, etc.): Unit is ten thousand Yuan

## Quick Start Example

### Complete Strategy Example

```python
from tqcenter import tq
import pandas as pd

def simple_strategy():
    try:
        # 1. Initialize connection
        tq.initialize(__file__)
        
        # 2. Get stock list
        stock_list = tq.get_stock_list('5')
        
        # 3. Get K-line data
        df = tq.get_market_data(
            stock_list=['688318.SH'],
            start_time='20250101',
            end_time='20250601',
            period='1d',
            dividend_type='front'
        )
        
        # 4. Calculate simple indicator
        close_prices = tq.price_df(df, 'Close')
        ma20 = close_prices.rolling(window=20).mean()
        
        # 5. Send message to client
        tq.send_message("Strategy completed | 20-day moving average calculated")
        
        # 6. Export factor data
        tq.print_to_tdx(
            df_list=[ma20],
            sp_name='MA20 Factor',
            xml_filename='ma20_factor.xml'
        )
        
        print("Strategy executed successfully!")
        
    except Exception as e:
        print(f"Strategy execution error: {e}")
        tq.send_message(f"Strategy error: {str(e)}")
        
    finally:
        # 7. Close connection
        tq.close()

if __name__ == '__main__':
    simple_strategy()
```

## Precautions

### ⚠️ Important Warnings

1. **Must use editable mode installation**
   - The project does not support the regular installation mode of `pip install`
   - Must use `pip install -e .` for editable mode installation
   - Does not support publishing to PyPI or other package management platforms
2. **Path dependency cannot be changed**
   - The project must run in the standard directory structure of the TongDaXin client
   - Never move, rename the project directory, or modify the relative path structure
3. **Client dependency**
   - Must start the TongDaXin client and login before running
   - Need to use a client version that supports TQ strategy functionality
   - Ensure the client has the corresponding data permissions
4. **Data preparation**
   - Historical K-line data needs to be pre-downloaded in the client
   - Professional financial data needs to be pre-downloaded in the client
   - It is recommended to refresh the market cache regularly
5. **Connection management**
   - Be sure to call `tq.close()` to close the connection when the strategy ends
   - After abnormal exit, you need to clean up the strategy record in the strategy manager
   - Avoid running multiple strategy instances with the same name simultaneously

### 💡 Best Practices

1. **Error handling**
   ```python
   try:
       tq.initialize(__file__)
       # Strategy logic
   except Exception as e:
       print(f"Error: {e}")
       tq.send_message(f"Strategy exception: {str(e)}")
   finally:
       tq.close()
   ```
2. **Data validation**
   ```python
   # Validate stock code format
   if not check_stock_code_format('688318.SH'):
       print("Stock code format error")
   ```
3. **Performance optimization**
   - Batch data retrieval instead of fetching stock by stock
   - Reasonable use of caching mechanisms
   - Avoid frequent market data refresh

## Technical Support

- **Official Documentation**: <https://help.tdx.com.cn/quant/docs/markdown/mindoc-1cfsjkbf8f3is/>

## License Statement

This project is a core component of the TongDaXin quantitative platform, and its use must comply with the relevant license agreements of TongDaXin. Unauthorized use for commercial purposes or secondary distribution is prohibited.

***


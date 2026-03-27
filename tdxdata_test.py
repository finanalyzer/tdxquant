import numpy as np 
import pandas as pd 
from tqcenter import tq
import time
import json

"""
    这里是tq的简单使用示例
    使用时请确保已经启动通达信客户端并登录
    取消对应注释即可运行对应功能
"""

"""
    参数设置
"""
codes = ["688318.SH"] #传入的股票代码格式必须是标准格式：6位数+市场后缀（.SH/.SZ/.JJ等）
startime = "20250620" #传入的时间格式必须是：YYYYMMDD 或 YYYYMMDDHHMMSS 
endtime = "20250801"
period = '1d' #K线周期：1d/1w/1m/5m/15m/30m/60m等
dividend_type='none' #复权类型：none-不复权，front-前复权，back-后复权

#初始化
tq.initialize(__file__) #所有策略连接通达信客户端都必须调用此函数进行初始化

'''
    刷新行情缓存 刷新后5分钟内取最新report和k线数据不会触发刷新
    force参数表示是否强制刷新 默认False
    market参数表示指定市场刷新
    'AG'表示A股 'HK'表示港股 'US'表示美股 'QH'表示期货  'QQ'表示期权  'ZZ'表示中证国证指数
'''
# refresh_cache = tq.refresh_cache()
# print(refresh_cache)

'''
    缓存历史K线 目前仅支持1m 5m 1d三种类型数据 不建议一次更新太多，会堵塞策略和客户端
'''
# refresh_kline = tq.refresh_kline(stock_list=['688318.SH'],period='1d')
# print(refresh_kline)

'''
    获取K线数据  获取K线数据需要先在客户端中下载对应盘后数据，调用会触发客户端刷新数据，耗时过长请耐心等待
    field_list可以筛选返回字段，默认返回全部字段 比如 field_list=['Open','Close'] 就是只取开盘价和收盘价
    count可以设置每只股票取的数据量
    暂时不支持获取分笔数据
    开高低收单位为元，成交量单位为手，成交额单位为万元
'''
# df = tq.get_market_data(
#         field_list=[],
#         stock_list=['688318.SH'],
#         start_time='',
#         end_time='',
#         count=1,
#         dividend_type='none',
#         period='1d',
#         fill_data=False
#     )
# print(df)

'''
    获取分红送配数据
'''
# divid_factors = tq.get_divid_factors(
#         stock_code='688318.SH',
#         start_time='',
#         end_time='')
# print(divid_factors)

'''
    获取市场快照数据,调用会触发客户端刷新数据，耗时过长请耐心等待
    总成交额为万位，其他无特殊说明均为个位
    曾用名：get_full_tick get_report_data
'''
# market_snapshot = tq.get_market_snapshot(stock_code = '688318.SH', field_list=['Buyp'])
# print(market_snapshot)

'''
    获取可转债基础数据
'''
# cb_info = tq.get_cb_info(stock_code = '123049.SZ', field_list=['CurRate'])
# print(cb_info)

'''
    获取新股申购信息（不包含历史）
    ipo_type=0 表示获取所有新股申购信息
    ipo_type=1 表示获取所有新发债信息
    ipo_date=0 表示只获取今天信息
    ipo_date=1 表示获取今天及以后信息
'''
# ipo_info = tq.get_ipo_info(ipo_type=2, ipo_date=1)
# print(ipo_info)

'''
    获取股票更多数据
'''
more_info = tq.get_more_info(stock_code = '880544.SH', field_list=['ZTGPNum'])
print(more_info)

'''
    获取股本数据
    传入的日期列表顺序需要从小到大排列
'''
# gb_info = tq.get_gb_info(stock_code = '688318.SH', date_list=['20250101','20250601'], count=2)
# print(gb_info)

'''
    获取基础财务数据 与专业财务数据有区别 不需要下载专业财务数据
    field_list可以筛选返回字段，默认返回全部字段 比如 field_list=['J_zgb','ActiveCapital'] 就是只取总股本和流通股本
    股本 资产 负债 利润 现金流量等数据均为万位
'''
# fdc = tq.get_stock_info(stock_code='688318.SH', field_list=[])
# print(fdc)

'''
    专业财务数据 需要先在客户端下载专业财务数据 
    table_list可以筛选返回字段 格式为 FNXXX 比如 ['Fn193','Fn194']
    report_type 可选 'report_time' 按截止日期 'announce_time' 按公告日期 进行筛选
'''
# fd = tq.get_financial_data(
#         stock_list=['688318.SH'],
#         field_list=['Fn193','Fn194','Fn195','Fn196','Fn197'],
#         start_time='20250101',
#         end_time='',
#         report_type='announce_time')
# print(fd)

'''
    按指定日期获取专业财务数据 
'''
# fd = tq.get_financial_data_by_date(
#         stock_list=['688318.SH'],
#         field_list=['Fn193','Fn194','Fn195','Fn196','Fn197'],
#         year=0,
#         mmdd=0)
# print(fd)

'''
    获取股票交易数据
'''
# gp_val = tq.get_gpjy_value(
#         stock_list=['688318.SH'],
#         field_list=['GP1','GP2','GP3','GP4','GP5'],
#         start_time='20250101',
#         end_time='20250102')
# print(gp_val)

# gp_one = tq.get_gpjy_value_by_date(
#         stock_list=['688318.SH'],
#         field_list=['GP1','GP2','GP3','GP4','GP5'],
#         year=0,mmdd=0)
# print(gp_one)

'''
    获取板块交易数据
'''
# bk_data = tq.get_bkjy_value(stock_list=['880660.SH'],
#         field_list=['BK5','BK6','BK7','BK8','BK9'],
#         start_time='20250101',
#         end_time='20250102')
# print(bk_data)

# bk_one = tq.get_bkjy_value_by_date(stock_list=['880660.SH'],
#                                    field_list=['BK9','BK10','BK11','BK12','BK13'],
#                                    year=0,mmdd=0)
# print(bk_one)

'''
    获取市场交易数据
'''
# sc_val = tq.get_scjy_value(field_list=['SC1','SC2','SC3','SC4','SC5'],
#         start_time='20250101',end_time='20250102')
# print(sc_val)

# sc_one = tq.get_scjy_value_by_date(field_list=['SC6','SC7','SC8','SC9','SC10'],year=0,mmdd=0)
# print(sc_one)

'''
    获取股票单个数据
'''
# go = tq.get_gp_one_data(stock_list=['688318.SH'],field_list=['GO1','GO2','GO3','GO4','GO47'])
# print(go)

'''
    下载10大股东数据或ETF申赎数据
    下载的文件保存在 .\\PYPlugins\\data 文件夹
    down_type=1时，下载10大股东数据，down_time只生效年份
    down_type=2时，下载ETF申赎清单，down_time生效到日期
    down_type=3时，下载最近舆情，其余两项无效
    down_type=4时，下载综合信息文件，其余两项无效
'''
# down_ptr_10 = tq.download_file(stock_code='688318.SH', down_time='20260227',down_type=1)
# print(down_ptr_10)
# dowm_ptr_etf = tq.download_file(stock_code='159109.SH', down_time='20260227',down_type=2)
# print(dowm_ptr_etf)

'''
    获取交易日列表 需要现在客户端下载上证指数（999999）的盘后数据 目前仅支持A股
    count参数表示获取的交易日数量
'''
# trade_dates = tq.get_trading_dates(market = 'SH', start_time = '20220101', end_time = '', count = 10);
# print(trade_dates)

'''
    获取股票代码
    默认为全部A股
    0:自选股 1:持仓股
    5:所有A股 6:上证指数成份股 7:上证主板 8:深证主板 9:重点指数 
    10:所有板块指数 11:缺省行业板块 12:概念板块 13:风格板块 14:地区板块 15:缺省行业分类+概念板块 16:研究行业一级 17:研究行业二级 18:研究行业三级
    21:含H股 22:含可转债 23:沪深300 24:中证500 25:中证1000 26:国证2000 27:中证2000 28:中证A500
    30:REITs 31:ETF基金 32:可转债 33:LOF基金 34:所有可交易基金 35:所有沪深基金 36:T+0基金
    49:金融类企业 50:沪深A股 51:创业板 52:科创板 53:北交所
    101:国内期货 102:港股 103:美股
'''
# stock_list = tq.get_stock_list('31', list_type=1)
# print(stock_list)
# print(len(stock_list))

'''
    获取A股全部板块
'''
# block_list = tq.get_sector_list(list_type=1)
# print(block_list)
# print(len(block_list))

'''
    获取用户自定义板块
'''
# user_list = tq.get_user_sector()
# print(user_list)
# print(len(user_list))

'''
    获取板块成分股 
    支持板块名称或板块代码两种方式传入
    block_type=0 表示传入板块代码或名称（默认）
    block_type=1 表示传入自定义板块简称 需要是客户端中预先定义好板块简称 不能是 自选股 或 临时条件股
'''
# block_stocks = tq.get_stock_list_in_sector('880081.SH')
# print(block_stocks)
# print(len(block_stocks))

# block_stocks = tq.get_stock_list_in_sector('钛金属',list_type=1)
# print(block_stocks)
# print(len(block_stocks))

# block_stocks = tq.get_stock_list_in_sector('CSBK', block_type = 1)
# print(block_stocks)
# print(len(block_stocks))

'''
    发送消息给通达信客户端的TQ策略界面 
    传入的字符串使用 | 可以让客户端将其分为两条（插入 \n 也可以分行显示）
'''
# msg_str = "这是第一行. | 这是第二行. "
# tq.send_message(msg_str)

'''
    创建自定义板块
    block_code为板块简称 block_name为板块名称
'''
# create_ptr = tq.create_sector(block_code='CSBK2', block_name='测试板块2')
# print(create_ptr)

'''
    删除自定义板块
'''
# delete_ptr = tq.delete_sector(block_code='CSBK2')
# print(delete_ptr)

'''
    重命名自定义板块
    重命名自定义板块仅能重命名板块名而不能改板块简称
'''
# rename_ptr = tq.rename_sector(block_code='CSBK', block_name='测试板块重命名')
# print(rename_ptr)

'''
    清空板块成份股
'''
# clear_ptr = tq.clear_sector(block_code='CSBK')
# print(clear_ptr)

'''
    添加自选股 到 通达信客户端的临时条件股列表
    block_code 为客户端已有的自定义板块简称，如果不存在则无效果，空则为添加到临时条件股
    block_code存在，传入空列表则表示清空该板块所有股票，否则为添加新股票
    自选股的block_code为ZXG
    shows 参数表示是否在客户端显示该自选股窗口
'''
# zxg_result = tq.send_user_block(block_code='ZXG', stocks=["600000.SH","600004.SH","000001.SZ","000002.SZ"], show=True)
# zxg_result = tq.send_user_block(block_code='CSBK', stocks=[])
# zxg_result = tq.send_user_block(block_code='', stocks=[])

'''
    发送文件路径给通达信客户端的TQ策略界面 可供客户端打开
    file 放于 ./PYPlugins/file 文件夹下 时为文件名
    file 放于其他路径时 为绝对路径
'''
# file = "test.txt"
# tq.send_file(file)

'''
    发送预警信号给通达信客户端的TQ策略界面
    price_list close_list volum_list bs_flag_list warn_type_list 均要求为纯数字字符串List
    bs_flag_list 0买1卖2未知
    warn_type_list 0常规预警（目前仅支持）
    reason_list每个元素有效长度为25个汉字（50个英文）
'''
# warn_res = tq.send_warn(stock_list = ['688318.SH','688318.SH','600519.SH'],
#              time_list = ['20251215141115','20251215142100','20251215143101'],
#              price_list= ['123.45','133.45','1823.45'],
#              close_list= ['122.50','132.50','1822.50'],
#              volum_list= ['1000','2000','15000'],
#              bs_flag_list= ['0','1','2'],
#              warn_type_list= ['0'],
#              reason_list= ['价格突破预警线','收盘价突破预警线','成交量突破预警线'],
#              count=3)
# print(warn_res)

'''
    发送回测结果给通达信客户端的TQ策略界面
    data_list为二维List，每个子元素对应time_list的一个元素时间点，且每个孙元素最多有16个有效纯数字字符串
'''
# bt_data = tq.send_bt_data(stock_code = '688318.SH',
#                           time_list = ['20251215141115','20251215141415'],
#                           data_list = [['1','0','1','0','210','220','230','240','250','260'],['0','1']],
#                           count = 1)
# print(bt_data)

'''
    订阅股票更新 传入回调函数，订阅的股票有更新时，系统会调用回调函数，本例中回调函数功能为订阅股票有更新后获取最新的report数据
    一共最多定订阅100条
    回调函数格式定义为on_data(datas)  datas格式为 {"Code":"XXXXXX.XX","ErrorId":"0"}
'''
# def my_callback_func(data_str):
#     print("Callback received data:", data_str)
#     code_json = json.loads(data_str)
#     print(f"codes = {code_json.get('Code')}")
#     report_ptr = tq.get_market_snapshot(code_json.get('Code'))
#     print(report_ptr)
#     return None

# sub_hq = tq.subscribe_hq(stock_list=['688318.SH'], callback=my_callback_func)
# print(sub_hq)

'''
    取消股票订阅更新
'''
# un_sub_ptr = tq.unsubscribe_hq(stock_list=['688318.SH'])
# print(un_sub_ptr)

'''
    获取当前订阅更新的股票列表
'''
# sub_list = tq.get_subscribe_hq_stock_list()
# print(sub_list)

'''
    通达信公式设置股票参数
'''
# test_md = tq.get_market_data(stock_list=['688318.SH'], count=5, period='1d')
# format_md = tq.formula_format_data(test_md)
# print(format_md)
# formula_set_k = tq.formula_set_data(stock_code='688318.SH', stock_period='1d', stock_data=format_md['688318.SH'], count=len(format_md['688318.SH']))
# print(formula_set_k)

# formula_set_res = tq.formula_set_data_info(stock_code='688318.SH',stock_period='1d', start_time='20250101',end_time='20250126',dividend_type=1)
# formula_set_res = tq.formula_set_data_info(stock_code='688318.SH',stock_period='1d', count=20,dividend_type=1)
# print(formula_set_res)

'''
    获取设置的通达信公式股票参数对应的K线数据
'''
# formula_kline = tq.formula_get_data()
# print(formula_kline)

'''
    调用通达信公式 
'''
# formula_zb = tq.formula_zb(formula_name='MACD', formula_arg='12,26,9', xsflag=6)
# print(formula_zb)
# formula_zb = tq.formula_zb(formula_name='CYX', formula_arg='10')
# print(formula_zb)

# formula_xg = tq.formula_xg(formula_name='UPN', formula_arg='3')
# print(formula_xg)

# formula_exp = tq.formula_exp(formula_name='CCI', formula_arg='12')
# print(formula_exp)

'''
    批量调用通达信条件选股公式
'''
# mul_xg_res = tq.formula_process_mul_xg(
#     formula_name='UPN',
#     formula_arg='3',
#     retrun_count=3,
#     return_date=True,
#     stock_list=['688318.SH','600519.SH','000001.SZ'],
#     stock_period='1d',
#     count=5,
#     dividend_type=1)
# print(mul_xg_res)

'''
    批量调用通达信指标公式
'''
# mul_zb_res = tq.formula_process_mul_zb(
#     formula_name='MACD',
#     formula_arg='12,26,9',
#     retrun_count=1,
#     return_date=False,
#     stock_list=['688318.SH','600519.SH','000001.SZ'],
#     stock_period='1d',
#     count=5,
#     dividend_type=1)
# print(mul_zb_res)

# mul_zb_res = tq.formula_process_mul_zb(
#     formula_name='CYX',
#     formula_arg='12',
#     retrun_count=3,
#     return_date=True,
#     stock_list=['688318.SH','600519.SH','000001.SZ'],
#     stock_period='1d',
#     count=5,
#     dividend_type=1)
# print(mul_zb_res)

'''
    手动断开连接 在策略退出前或错误处理中调用 比如取到数据为空 中途退出策略 调用close 这样才能配合TQ策略管理器关闭策略
    目前已经基本实现程序退出时自动断开连接，如国未能正常close会导致策略管理器中该策略运行状态始终处于运行状态，无法二次启动
    如果遇到这种情况，在策略管理器中删除该策略即可
'''
# tq.close()

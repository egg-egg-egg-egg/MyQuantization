import time
import os
import sys
import datetime

import schedule
import chinese_calendar

from lof import lof_premium
import logging


logging.basicConfig(
    level=logging.INFO, 
    filename='schedule.log', 
    filemode='a', 
    encoding='utf-8',
    format='%(asctime)s - %(levelname)s - %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S'
)


def job():
    df_lof = lof_premium()

    rate:int = 5 # 溢价率±5%
    columns = ["场外代码",'场内代码', '名称', '最新价', '最新净值/万份收益', '溢价率%', '申购状态',
       '赎回状态', '下一开放日',"买入确认日","卖出确认日", '购买起点', '日累计限定金额', '手续费']
    
    filtered_df = df_lof[(df_lof['溢价率%'] >= rate) | (df_lof['溢价率%'] <= -rate)][columns]
    # 如果lof_premium文件夹不存在，则创建
    if not os.path.exists('lof_premium'):
        os.makedirs('lof_premium')
    # 保存文件到lof_premium文件夹
    # 获取当前年月日
    today = time.strftime("%Y%m%d")
    save_path = f'./lof_premium/{today}.csv'
    filtered_df.to_csv(save_path, index=False, encoding='utf-8-sig')
    logging.info(f"数据已保存到 {save_path}")


# ...existing code...

def is_a_share_trading_day(date=None):
    """判断是否为A股交易日"""
    if date is None:
        date = time.localtime()
    y, m, d = date.tm_year, date.tm_mon, date.tm_mday
    return chinese_calendar.is_workday(datetime.date(y, m, d))

def job_if_trading_day():
    if is_a_share_trading_day():
        logging.info("A股交易日，开始执行job任务")
        job()
    else:
        logging.info("非A股交易日，跳过job任务")

def upgrade_chinesecalendar():
    logging.info("开始升级chinesecalendar")
    os.system(f'"{sys.executable}" -m pip install -U chinesecalendar')



if __name__ == "__main__":
    # 每天下午14:40执行一次，如果是A股交易日则运行job
    schedule.every().day.at("14:40").do(job_if_trading_day)
    # 每26周升级一次chinesecalendar
    schedule.every(26).weeks.do(upgrade_chinesecalendar)

    logging.info("定时任务启动")
    while True:
        schedule.run_pending()
        time.sleep(30)
# ...existing code...
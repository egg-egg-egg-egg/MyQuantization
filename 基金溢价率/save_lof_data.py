import os
import time
from lof import lof_premium

def save_lof_data():
    """调用 lof_premium 函数并保存数据到 data 文件夹"""
    df_lof = lof_premium()
    columns = ["场外代码", '场内代码', '名称', '最新价', '最新净值/万份收益', '溢价率%', '申购状态',
               '赎回状态', '下一开放日', "买入确认日", "卖出确认日", '购买起点', '日累计限定金额', '手续费']
    filtered_df = df_lof[columns]

    # 如果 data 文件夹不存在，则创建
    if not os.path.exists('data'):
        os.makedirs('data')

    # 获取当前年月日
    today = time.strftime("%Y%m%d")
    save_path = f'./data/{today}.csv'

    # 保存文件
    filtered_df.to_csv(save_path, index=False, encoding='utf-8-sig')
    print(f"数据已保存到 {save_path}")

if __name__ == "__main__":
    save_lof_data()

import json
from datetime import datetime, timedelta


def filter_last_10_tokens(all_json_data):
    temp_json_data = all_json_data
    last = 10
    if last > len(temp_json_data):
        last = len(temp_json_data)
    filtered_tokens = []
    # 遍历 JSON 数据中的每个币
    for token in temp_json_data[:last]:
        # 获取最后更新日期，并将其转化为 datetime 对象
        name = token.get('name')
        chain = token.get('chain')
        address = token.get('contractAddress')
        filtered_tokens.append({
            'name': name,
            'chain': chain,
            'contractAddress': address
        })

    return filtered_tokens



def filter_new_or_updated_tokens(all_json_data):
    if all_json_data is None:
      return []
    temp_json_data = all_json_data

    """
    从 JSON 数据中提取在 24 小时内上线或更新的币的名称、链和地址。

    :param json_data: 包含币数据的 JSON 数据
    :return: 包含筛选结果的列表，形式为 [{'name': 'token_name', 'chain': 'chain_name', 'address': 'contract_address'}, ...]
    """
    # 当前时间
    current_time = datetime.utcnow()
    # 定义 24 小时前的时间
    time_threshold = current_time - timedelta(hours=24)

    # 存储结果的列表
    filtered_tokens = []

    # 遍历 JSON 数据中的每个币
    for token in temp_json_data:
        # 获取最后更新日期，并将其转化为 datetime 对象
        last_update_str = token.get('listedAt')
        if last_update_str:
            # 尝试解析带微秒和不带微秒的时间格式
            try:
                last_update_time = datetime.strptime(last_update_str, '%Y-%m-%dT%H:%M:%S.%fZ')
            except ValueError:
                last_update_time = datetime.strptime(last_update_str, '%Y-%m-%dT%H:%M:%SZ')
            # 如果最后更新日期在过去24小时内
            if last_update_time >= time_threshold:
                # 获取币的名称、链和合约地址
                name = token.get('name')
                chain = token.get('chain')
                address = token.get('contractAddress')

                # 添加到结果列表中
                filtered_tokens.append({
                    'name': name,
                    'chain': chain,
                    'contractAddress': address
                })

    return filtered_tokens


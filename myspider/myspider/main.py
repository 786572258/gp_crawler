from collections import defaultdict
from datetime import datetime
from flask_cors import CORS

from flask import Flask, jsonify, request

from repo.common_repo import CommonRepo

app = Flask(__name__)
CORS(app)


# 示例数据
# {
#     "data": {
#         "industry_name_daily_data": {
#             "A": [1, 2, 4, -4],
#             "B": [1, 2, 4, -4],
#         },
#         "date_list": ["2023-12-01", "2023-12-01", ]
#     }
# }

# 获取所有数据
@app.route('/api/industry_daily_data', methods=['GET'])
def get_industry_daily_data():

    days = request.args.get('days')
    print(days)

    common_repo = CommonRepo()
    all_industry_daily_data = common_repo.find_industry_daily_data(days)
    # 转换后的数据结构
    converted_data = {
        "industry_name_daily_data": defaultdict(list),
        "date_list": []
    }

    # 遍历原始数据
    industry_name_list = []
    for item in all_industry_daily_data:
        # 获取行业名称
        industry_name = item['name']
        # 解析日期字符串
        date = item['date']
        # date_object = datetime.strptime(date_str, '%Y%m%d')
        # formatted_date_str = date_object.strftime('%Y-%m-%d')

        # 将日期数字加入到日期列表中
        if date not in converted_data["date_list"]:
            converted_data["date_list"].append(date)

        if industry_name not in industry_name_list:
            industry_name_list.append(industry_name)

        #
        # # 将数据添加到对应的行业数据列表中
        # converted_data["industry_name_daily_data"][industry_name].append(item['fluctuation_range'])

    # 转换日期列表为有序的日期字符串列表
    converted_data["date_list"] = sorted(converted_data["date_list"])

    # 将原始数据转换为字典，以便更快地进行检索
    data_dict = {(item['date'], item['name']): item['closing_price'] for item in all_industry_daily_data}

    # 遍历日期和行业名称
    for date in converted_data["date_list"]:
        for industry_name in industry_name_list:
            key = (date, industry_name)
            converted_data['industry_name_daily_data'][industry_name].append(data_dict.get(key, 0))

    # for date in converted_data["date_list"]:
    #     for industry_name in industry_name_list:
    #         is_search = False
    #         for item in all_industry_daily_data:
    #             if date == item['date'] and industry_name == item['name']:
    #                 converted_data['industry_name_daily_data'][industry_name].append(item['closing_price'])
    #                 is_search = True
    #                 break
    #         if is_search is False:
    #             converted_data['industry_name_daily_data'][industry_name].append(0)

    for i, date in enumerate(converted_data["date_list"]):
        date_str = str(date)
        date_object = datetime.strptime(date_str, '%Y%m%d')
        formatted_date_str = date_object.strftime('%Y-%m-%d')
        # 更新列表中的日期
        converted_data["date_list"][i] = formatted_date_str

    # 打印转换后的数据
    print(converted_data)

    return jsonify({'data': converted_data})

# 获取特定ID的数据
@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in data if item['id'] == item_id), None)
    if item:
        return jsonify({'data': item})
    else:
        return jsonify({'message': 'Item not found'}), 404

# 创建新数据
@app.route('/api/items', methods=['POST'])
def create_item():
    new_item = {'id': len(data) + 1, 'name': request.json['name']}
    data.append(new_item)
    return jsonify({'message': 'Item created successfully', 'data': new_item}), 201

# 更新数据
@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = next((item for item in data if item['id'] == item_id), None)
    if item:
        item['name'] = request.json['name']
        return jsonify({'message': 'Item updated successfully', 'data': item})
    else:
        return jsonify({'message': 'Item not found'}), 404

# 删除数据
@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global data
    data = [item for item in data if item['id'] != item_id]
    return jsonify({'message': 'Item deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, jsonify, request

app = Flask(__name__)

# 示例数据
data = [
    {'id': 1, 'name': 'Item 1'},
    {'id': 2, 'name': 'Item 2'},
    {'id': 3, 'name': 'Item 3'},
]

# 获取所有数据
@app.route('/api/items', methods=['GET'])
def get_items():
    return jsonify({'data': data})

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

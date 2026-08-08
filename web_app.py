from flask import Flask, jsonify, request, render_template
import csv
import os

CSV_FILE = 'inventory.csv'

def load_items():
    items = []
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'name', 'quantity', 'price'])
        return items
    with open(CSV_FILE, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                items.append({
                    'id': int(row['id']),
                    'name': row['name'],
                    'quantity': int(row['quantity']),
                    'price': float(row['price'])
                })
            except Exception:
                continue
    return items

def save_items(items):
    with open(CSV_FILE, 'w', newline='') as f:
        fieldnames = ['id', 'name', 'quantity', 'price']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for it in items:
            writer.writerow({'id': it['id'], 'name': it['name'], 'quantity': it['quantity'], 'price': it['price']})

def next_id(items):
    if not items:
        return 1
    return max(i['id'] for i in items) + 1

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/items', methods=['GET'])
def api_get_items():
    return jsonify(load_items())

@app.route('/api/items', methods=['POST'])
def api_add_item():
    data = request.get_json() or {}
    name = data.get('name','').strip()
    try:
        qty = int(data.get('quantity',0))
        price = float(data.get('price',0))
    except Exception:
        return jsonify({'error':'invalid quantity or price'}), 400
    if not name:
        return jsonify({'error':'name required'}), 400
    items = load_items()
    item = {'id': next_id(items), 'name': name, 'quantity': qty, 'price': price}
    items.append(item)
    save_items(items)
    return jsonify(item), 201

@app.route('/api/items/<int:item_id>', methods=['PUT'])
def api_update_item(item_id):
    data = request.get_json() or {}
    name = data.get('name','').strip()
    try:
        qty = int(data.get('quantity',0))
        price = float(data.get('price',0))
    except Exception:
        return jsonify({'error':'invalid quantity or price'}), 400
    if not name:
        return jsonify({'error':'name required'}), 400
    items = load_items()
    for it in items:
        if it['id'] == item_id:
            it['name']=name; it['quantity']=qty; it['price']=price
            save_items(items)
            return jsonify(it)
    return jsonify({'error':'not found'}), 404

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def api_delete_item(item_id):
    items = load_items()
    new_items = [it for it in items if it['id'] != item_id]
    if len(new_items) == len(items):
        return jsonify({'error':'not found'}), 404
    save_items(new_items)
    return ('',204)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

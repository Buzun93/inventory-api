
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/calculate_inventory", methods=["POST"])
def calculate_inventory():
    data = request.json
    items = data.get("items", [])
    cialo = data.get("attributes", {}).get("Cialo", 5)
    base_capacity = cialo * 4

    total_weight = 0
    total_cost = 0

    for item in items:
        name = item.get("name", "")
        weight = item.get("weight", 0)
        value = item.get("value", 0)
        amount = item.get("amount", 1)
        item_type = item.get("type", "")
        category = item.get("category", "")
        container = item.get("container", False)

        if name.lower() == "kapsle":
            if amount >= 100:
                total_weight += 0.1 * (amount // 100)
        elif item_type == "tabletki" and not container:
            continue
        elif category == "drobiazgi" and amount >= 50:
            total_weight += 0.1 * (amount // 50)
        else:
            total_weight += weight * amount

        total_cost += value * amount

    result = {
        "total_weight": round(total_weight, 2),
        "total_cost": total_cost,
        "capacity": base_capacity,
        "valid_weight": total_weight <= base_capacity,
        "valid_cost": total_cost <= 800
    }

    return jsonify(result)

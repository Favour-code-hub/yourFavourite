from flask import Flask, render_template, request
import json
import os

app = Flask(__name__, static_folder='static', static_url_path='/static')

# Menu data with prices
MENU = {
    "jollof_jumbo": {"name": "Chef's Special Jollof - Jumbo", "price": 3500, "image": "jollof.jpg"},
    "jollof_family": {"name": "Chef's Special Jollof - Family", "price": 15500, "image": "jollof.jpg"},
    "salad_one portion": {"name": "Salad-One Portion", "price": 2500, "image": "salad.jpg"},
    "fried_jumbo": {"name": "Fried Rice - Jumbo", "price": 3300, "image": "fried.jpg"},
    "fried_family": {"name": "Fried Rice - Family", "price": 15000, "image": "fried.jpg"},
    "basmati_jumbo": {"name": "Basmati Rice - Jumbo", "price": 6400, "image": "chinese.jpg"},
    "basmati_family": {"name": "Basmati Rice - Family", "price": 30000, "image": "chinese.jpg"},
    "coconut_jumbo": {"name": "Coconut Rice - Jumbo", "price": 4000, "image": "coconut.jpg"},
    "coconut_family": {"name": "Coconut Rice - Family", "price": 18200, "image": "coconut.jpg"},
    "native_jumbo": {"name": "Native Rice - Jumbo", "price": 4000, "image": "native.jpg"},
    "native_family": {"name": "Native Rice - Family", "price": 18200, "image": "native.jpg"},
    "beefy_jumbo": {"name": "Beefy Rice - Jumbo", "price": 5700, "image": "beefy.jpg"},
    "beefy_family": {"name": "Beefy Rice - Family", "price": 26300, "image": "beefy.jpg"},
    "white_jumbo": {"name": "White Rice - Jumbo", "price": 500, "image":"white.jpg"},
    "white_family":{"name": "White Rice - Family", "price": 2500, "image": "white.jpg"},
    "white rice and beans_jumbo": {"name": "White Rice and Beans - Jumbo", "price": 900, "image": "rice & beans.jpg"},
    "white rice and beans_family": {"name": "White Rice and Beans - Family", "price": 4000, "image": "rice & beans.jpg"},
    "adalu_jumbo": {"name": "Adalu Rice- Jumbo", "price": 3600, "image": "adalu.jpg"},
    "adalu_family": {"name": "Adalu Rice - Family", "price": 15600, "image": "adalu.jpg"},
    "stew_jumbo": {"name": "Stew - Jumbo", "price": 2100, "image": "stew.jpg"},
    "stew_family": {"name": "Stew - Family", "price": 9000, "image": "stew.jpg"},
    "pasta_jumbo": {"name": "Pasta - Jumbo", "price": 4800, "image": "pasta.jpg"},
    "pasta_family": {"name": "Pasta - Family", "price": 22000, "image": "pasta.jpg"},
    "asian_jumbo": {"name": "Asian Pasta - Jumbo", "price": 5600, "image": "asian.jpg"},
    "asian_family": {"name": "Asian Pasta - Family", "price": 26000, "image": "asian.jpg"},
    "catfish_jumbo": {"name": "Catfish sauce - Jumbo", "price": 10000, "image": "catfish.jpg"},
    "catfish_family": {"name": "Catfish sauce - Family", "price": 48000, "image": "catfish.jpg"},
    "ukazi_jumbo": {"name": "Ukazi soup - Jumbo", "price": 4800, "image": "ukazi.jpg"},
    "ukazi_family": {"name": "Ukazi soup - Family", "price": 24500, "image": "ukazi.jpg"},
    "edik_jumbo": {"name": "Edikaikong soup - Jumbo", "price": 4300, "image": "edik.jpg"},
    "edik_Family": {"name": "Edikaikong soup - Family", "price": 21000, "image": "edik.jpg"},
    "afang_jumbo": {"name": "Afang soup - Jumbo", "price": 6300, "image": "afang.jpg"},
    "afang_Family": {"name": "Afang soup - Family", "price": 28500, "image": "afang.jpg"},
    "oha_jumbo": {"name": "Oha soup - Jumbo", "price": 4000, "image":"oha.jpg"},
    "oha_Family": {"name": "Oha soup - Family", "price": 19500, "image":"oha.jpg"},
    "egusi_jumbo": {"name": "Egusi soup - Jumbo", "price": 4200, "image":"egusi.jpg"},
    "egusi_Family": {"name": "Egusi soup - Family", "price": 20800, "image": "egusi.jpg"},
    "okro_jumbo": {"name": "Okro soup - Jumbo", "price": 5000, "image": "okro.jpg"},
    "okro_family": {"name": "Okro soup - Family", "price": 25000, "image":"okro.jpg"},
    "ogbono_jumbo": {"name": "Ogbono soup - Jumbo", "price": 5500, "image": "ogbono.jpg"},
    "ogbono_family": {"name": "Ogbono soup - Family", "price": 27000, "image": "ogbono.jpg"},
    "fisherman_jumbo": {"name": "Fisherman soup - Jumbo", "price": 15000, "image": "fisherman.jpg"},
    "fisherman_family": {"name": "Fisherman soup - Family", "price": 71000, "image": "fisherman.jpg"},
    "wheat_one portion": {"name": "wheat - One Portion", "price": 900, "image": "wheat.jpg"},
    "Garri_one portion": {"name": "Garri - One Portion", "price": 500, "image": "garri.jpg"},
    "Semo_one portion": {"name": "Semo - One Portion", "price": 1000, "image": "semo.jpg"},
    "plantain_jumbo": {"name": "Porridge Plantain - Jumbo", "price": 6200, "image": "plantain.jpg"},
    "plantain_family": {"name": "Porridge Plantain - Family", "price": 29000, "image": "plantain.jpg"},
    "beans_jumbo": {"name": "Porridge Beans - Jumbo", "price": 4200, "image": "beans.jpg"},
    "beans_family": {"name": "Porridge Beans - Family", "price": 18200, "image": "beans.jpg"},
    "yam_jumbo": {"name": "Porridge Yam - Jumbo", "price": 5000, "image": "yam.jpg"},
    "yam_family": {"name": "Porridge Yam - Family", "price": 26000, "image": "yam.jpg"},
    "moi-moi_jumbo": {"name": "Moi-Moi - Jumbo", "price": 2300, "image": "moi-moi.jpg"},
    "boiled yam_jumbo": {"name": "Boiled Yam - Jumbo", "price": 2000, "image": "boiled yam.jpg"},
    "boiled yam_family": {"name": "Boiled Yam - Family", "price": 10000, "image": "boiled yam.jpg"},
    "egg_jumbo": {"name": "Egg sauce - Jumbo", "price": 3700, "image": "egg.jpg"},
    "egg_family": {"name": "Egg sauce - Family", "price": 15800, "image": "egg.jpg"},
    "croquettes_jumbo": {"name": "Yam Croquettes - Jumbo", "price": 4300, "image": "croquettes.jpg"},
    "croquettes_family": {"name": "Yam Croquettes - Family", "price": 19100, "image": "croquettes.jpg"},
    "potatoes_jumbo": {"name": "Fried Potatoes - Jumbo", "price": 2500, "image": "potatoes.jpg"},
    "potatoes_family": {"name": "Fried Potatoes - Family", "price": 11500, "image": "potatoes.jpg"},
    "dodo_one portion": {"name": "Dodo - One Portion", "price": 1500, "image": "dodo.jpg"},
    
}

# Protein pricing
PROTEINS = {
    "Chicken": {"name": "Chicken", "price": 4600},
    "Beef": {"name": "Beef", "price": 1000},
    "Fish": {"name": "Fish", "price": 3100},
    "Turkey": {"name": "Turkey", "price": 6500},
    "vegetarian": {"name": "Vegetarian (No Protein)", "price": 0},
    "beef kebab": {"name": "beef kebab", "price": 4100},
    "Cowhead": {"name": "Cowhead", "price": 3500},
    "Goatmeat":{"name": "Goatmeat", "price": 1800},
    "Asun":{"name": "Asun", "price":5550},
    "Extra Beef": {"name": "Extra Beef", "price":1000},
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/menu")
def menu():
    return render_template("menu.html", proteins=PROTEINS)

@app.route("/api/order", methods=["POST"])
def process_order():
    """API endpoint to process order and send to WhatsApp"""
    try:
        from urllib.parse import quote
        
        data = request.json
        order_items = data.get("items", [])
        customer_name = data.get("name", "Customer")
        customer_phone = data.get("phone", "")
        
        # Build order message
        order_message = "🍲 *YUMMY CHOW ORDER* 🍲\n\n"
        order_message += f"*Customer Name:* {customer_name}\n"
        if customer_phone:
            order_message += f"*Phone:* {customer_phone}\n"
        order_message += "\n*Order Details:*\n"
        
        total_amount = 0
        for item in order_items:
            item_id = item.get("id")
            quantity = item.get("qty", 1)
            protein = item.get("protein", "")
            
            # Get base item price
            if item_id in MENU:
                menu_item = MENU[item_id]
                item_price = menu_item["price"]
                
                # Add protein cost if selected
                protein_cost = 0
                protein_text = ""
                if protein:
                    # Try to find the protein in the PROTEINS dict
                    for protein_key, protein_data in PROTEINS.items():
                        if protein_data["name"] == protein or protein_key == protein.lower():
                            protein_cost = protein_data["price"]
                            protein_text = f" + {protein} (+₦{protein_cost:,})"
                            break
                
                # Calculate total for this item
                item_total = (item_price + protein_cost) * quantity
                total_amount += item_total
                
                # Format message line
                base_price_text = f"₦{item_price:,}"
                if protein_cost > 0:
                    base_price_text += f" + ₦{protein_cost:,}"
                
                order_message += f"• {menu_item['name']}{protein_text}\n"
                order_message += f"  {base_price_text} x {quantity} = ₦{item_total:,}\n"
        
        order_message += f"\n{'='*40}\n"
        order_message += f"*💰 TOTAL AMOUNT: ₦{total_amount:,}*\n"
        order_message += f"{'='*40}\n"
        order_message += f"\n📍 *Please provide delivery location*\n"
        
        # WhatsApp integration - your actual business number
        whatsapp_number = "2349067837210"
        
        # URL encode the message properly
        encoded_message = quote(order_message)
        whatsapp_url = f"https://wa.me/{whatsapp_number}?text={encoded_message}"
        
        return {
            "status": "success",
            "message": order_message,
            "whatsapp_url": whatsapp_url,
            "total": total_amount
        }
    except Exception as e:
        print(f"Error processing order: {str(e)}")
        return {"status": "error", "message": str(e)}, 400

@app.route("/confirm")
def confirm():
    """Confirmation page - now handled via API"""
    return render_template("confirm.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
    from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
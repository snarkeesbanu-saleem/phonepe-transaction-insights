import os
import json
import pandas as pd

# Define paths
base_dir = r"data"
agg_trans_path = os.path.join(base_dir, "aggregated", "transaction", "country", "india", "state")
agg_user_path = os.path.join(base_dir, "aggregated", "user", "country", "india", "state")
map_trans_path = os.path.join(base_dir, "map", "transaction", "hover", "country", "india", "state")
map_user_path = os.path.join(base_dir, "map", "user", "hover", "country", "india", "state")
top_trans_path = os.path.join(base_dir, "top", "transaction", "country", "india", "state")
top_user_path = os.path.join(base_dir, "top", "user", "country", "india", "state")

# Helper function to get clean state name
def clean_state(name):
    # e.g., "andaman-&-nicobar-islands" -> "Andaman & Nicobar Islands"
    return name.replace('-', ' ').title()

# 1. Extract Aggregated Transactions
print("1. Extracting Aggregated Transactions...")
agg_trans_records = []
if os.path.exists(agg_trans_path):
    for state in os.listdir(agg_trans_path):
        state_dir = os.path.join(agg_trans_path, state)
        if not os.path.isdir(state_dir): continue
        for year in os.listdir(state_dir):
            year_dir = os.path.join(state_dir, year)
            if not os.path.isdir(year_dir): continue
            for file in os.listdir(year_dir):
                if file.endswith('.json'):
                    q = int(file.split('.')[0])
                    filepath = os.path.join(year_dir, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        tx_data = data.get('data', {}).get('transactionData', [])
                        if tx_data:
                            for item in tx_data:
                                agg_trans_records.append({
                                    'state': clean_state(state),
                                    'year': int(year),
                                    'quarter': q,
                                    'transaction_type': item.get('name'),
                                    'transaction_count': item['paymentInstruments'][0]['count'],
                                    'transaction_amount': round(item['paymentInstruments'][0]['amount'], 2)
                                })
                    except Exception as e:
                        print(f"Error parsing {filepath}: {e}")

df_agg_trans = pd.DataFrame(agg_trans_records)
df_agg_trans.to_csv('aggregated_transaction.csv', index=False)
print(f"   Done. Saved {len(df_agg_trans)} records to aggregated_transaction.csv")

# 2. Extract Aggregated Users and Brand Share
print("2. Extracting Aggregated Users and Brand Devices...")
agg_user_records = []
brand_records = []
if os.path.exists(agg_user_path):
    for state in os.listdir(agg_user_path):
        state_dir = os.path.join(agg_user_path, state)
        if not os.path.isdir(state_dir): continue
        for year in os.listdir(state_dir):
            year_dir = os.path.join(state_dir, year)
            if not os.path.isdir(year_dir): continue
            for file in os.listdir(year_dir):
                if file.endswith('.json'):
                    q = int(file.split('.')[0])
                    filepath = os.path.join(year_dir, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        
                        user_data = data.get('data', {})
                        agg_info = user_data.get('aggregated', {})
                        if agg_info:
                            agg_user_records.append({
                                'state': clean_state(state),
                                'year': int(year),
                                'quarter': q,
                                'registered_users': agg_info.get('registeredUsers', 0),
                                'app_opens': agg_info.get('appOpens', 0)
                            })
                        
                        devices = user_data.get('usersByDevice', [])
                        if devices:
                            for dev in devices:
                                brand_records.append({
                                    'state': clean_state(state),
                                    'year': int(year),
                                    'quarter': q,
                                    'brand': dev.get('brand'),
                                    'count': dev.get('count', 0),
                                    'percentage': dev.get('percentage', 0.0)
                                })
                    except Exception as e:
                        print(f"Error parsing {filepath}: {e}")

df_agg_user = pd.DataFrame(agg_user_records)
df_agg_user.to_csv('top_user_state.csv', index=False)
print(f"   Done. Saved {len(df_agg_user)} records to top_user_state.csv")

df_brands = pd.DataFrame(brand_records)
df_brands.to_csv('user_devices.csv', index=False)
print(f"   Done. Saved {len(df_brands)} records to user_devices.csv")

# 3. Extract Map Transactions
print("3. Extracting Map Transactions...")
map_trans_records = []
if os.path.exists(map_trans_path):
    for state in os.listdir(map_trans_path):
        state_dir = os.path.join(map_trans_path, state)
        if not os.path.isdir(state_dir): continue
        for year in os.listdir(state_dir):
            year_dir = os.path.join(state_dir, year)
            if not os.path.isdir(year_dir): continue
            for file in os.listdir(year_dir):
                if file.endswith('.json'):
                    q = int(file.split('.')[0])
                    filepath = os.path.join(year_dir, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        hover_list = data.get('data', {}).get('hoverDataList', [])
                        if hover_list:
                            for item in hover_list:
                                map_trans_records.append({
                                    'state': clean_state(state),
                                    'year': int(year),
                                    'quarter': q,
                                    'district': item.get('name').title(),
                                    'count': item['metric'][0]['count'],
                                    'amount': round(item['metric'][0]['amount'], 2)
                                })
                    except Exception as e:
                        print(f"Error parsing {filepath}: {e}")

df_map_trans = pd.DataFrame(map_trans_records)
df_map_trans.to_csv('map_transaction.csv', index=False)
print(f"   Done. Saved {len(df_map_trans)} records to map_transaction.csv")

# 4. Extract Map Users
print("4. Extracting Map Users...")
map_user_records = []
if os.path.exists(map_user_path):
    for state in os.listdir(map_user_path):
        state_dir = os.path.join(map_user_path, state)
        if not os.path.isdir(state_dir): continue
        for year in os.listdir(state_dir):
            year_dir = os.path.join(state_dir, year)
            if not os.path.isdir(year_dir): continue
            for file in os.listdir(year_dir):
                if file.endswith('.json'):
                    q = int(file.split('.')[0])
                    filepath = os.path.join(year_dir, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        hover_data = data.get('data', {}).get('hoverData', {})
                        for dist, val in hover_data.items():
                            map_user_records.append({
                                'state': clean_state(state),
                                'year': int(year),
                                'quarter': q,
                                'district': dist.title(),
                                'registered_users': val.get('registeredUsers', 0),
                                'app_opens': val.get('appOpens', 0)
                            })
                    except Exception as e:
                        print(f"Error parsing {filepath}: {e}")

df_map_user = pd.DataFrame(map_user_records)
df_map_user.to_csv('map_user.csv', index=False)
print(f"   Done. Saved {len(df_map_user)} records to map_user.csv")

# 5. Extract Top Transactions (Pincodes)
print("5. Extracting Top Transactions (Pincodes)...")
top_trans_records = []
if os.path.exists(top_trans_path):
    for state in os.listdir(top_trans_path):
        state_dir = os.path.join(top_trans_path, state)
        if not os.path.isdir(state_dir): continue
        for year in os.listdir(state_dir):
            year_dir = os.path.join(state_dir, year)
            if not os.path.isdir(year_dir): continue
            for file in os.listdir(year_dir):
                if file.endswith('.json'):
                    q = int(file.split('.')[0])
                    filepath = os.path.join(year_dir, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        pincodes = data.get('data', {}).get('pincodes', [])
                        if pincodes:
                            for pin in pincodes:
                                top_trans_records.append({
                                    'state': clean_state(state),
                                    'year': int(year),
                                    'quarter': q,
                                    'pincode': pin.get('entityName'),
                                    'transaction_count': pin['metric']['count'],
                                    'transaction_amount': round(pin['metric']['amount'], 2)
                                })
                    except Exception as e:
                        print(f"Error parsing {filepath}: {e}")

df_top_trans = pd.DataFrame(top_trans_records)
df_top_trans.to_csv('top_transaction_pincode.csv', index=False)
print(f"   Done. Saved {len(df_top_trans)} records to top_transaction_pincode.csv")

# 6. Extract Top Users (Pincodes)
print("6. Extracting Top Users (Pincodes)...")
top_user_records = []
if os.path.exists(top_user_path):
    for state in os.listdir(top_user_path):
        state_dir = os.path.join(top_user_path, state)
        if not os.path.isdir(state_dir): continue
        for year in os.listdir(state_dir):
            year_dir = os.path.join(state_dir, year)
            if not os.path.isdir(year_dir): continue
            for file in os.listdir(year_dir):
                if file.endswith('.json'):
                    q = int(file.split('.')[0])
                    filepath = os.path.join(year_dir, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        pincodes = data.get('data', {}).get('pincodes', [])
                        if pincodes:
                            for pin in pincodes:
                                top_user_records.append({
                                    'state': clean_state(state),
                                    'year': int(year),
                                    'quarter': q,
                                    'pincode': pin.get('name'),
                                    'registered_users': pin.get('registeredUsers', 0)
                                })
                    except Exception as e:
                        print(f"Error parsing {filepath}: {e}")

df_top_user = pd.DataFrame(top_user_records)
df_top_user.to_csv('top_user_pincode.csv', index=False)
print(f"   Done. Saved {len(df_top_user)} records to top_user_pincode.csv")

print("\n[SUCCESS] All data extracted successfully!")

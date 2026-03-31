import os
import json
import pandas as pd

print('🚀 Extracting PhonePe Data...')

df_list = []

# Extract Aggregated Transaction Data
path = r'data\aggregated\transaction\country\india\state'
if os.path.exists(path):
    for state in os.listdir(path):
        state_path = os.path.join(path, state)
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            for file in os.listdir(year_path):
                if file.endswith('.json'):
                    with open(os.path.join(year_path, file), 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    for item in data['data']['transactionData']:
                        df_list.append({
                            'State': state.replace('-', ' ').title(),
                            'Year': int(year),
                            'Quarter': int(file.split('.')[0]),
                            'Transaction_type': item['name'],
                            'Transaction_count': item['paymentInstruments'][0]['count'],
                            'Transaction_amount': item['paymentInstruments'][0]['amount']
                        })

df = pd.DataFrame(df_list)
df.to_csv('aggregated_transaction.csv', index=False)

print(f'✅ Successfully extracted {len(df)} records!')
print('File created: aggregated_transaction.csv')
print(df['State'].value_counts().head())

import os
import json
import pandas as pd

print('🔄 Creating Clean Data File...')

records = []
path = r'data\aggregated\transaction\country\india\state'

for state_folder in os.listdir(path):
    state_path = os.path.join(path, state_folder)
    if not os.path.isdir(state_path): continue
    
    for year in os.listdir(state_path):
        year_path = os.path.join(state_path, year)
        if not os.path.isdir(year_path): continue
        
        for q_file in os.listdir(year_path):
            if q_file.endswith('.json'):
                q = int(q_file.split('.')[0])
                filepath = os.path.join(year_path, q_file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    for item in data.get('data', {}).get('transactionData', []):
                        records.append({
                            'State': state_folder.replace('-', ' ').title(),
                            'Year': int(year),
                            'Quarter': q,
                            'Transaction_type': item.get('name'),
                            'Transaction_count': item['paymentInstruments'][0]['count'],
                            'Transaction_amount': round(item['paymentInstruments'][0]['amount'], 2)
                        })
                except:
                    pass

df = pd.DataFrame(records)
df.to_csv('aggregated_transaction.csv', index=False)

print(f'✅ Cleaned Successfully! Total Records: {len(df)}')
print('\\nFirst 10 rows of clean data:')
print(df.head(10).to_string(index=False))
print('\\nColumns:', df.columns.tolist())

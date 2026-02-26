import pandas as pd

def process_data(file_path):
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)
    
    mapping = {
        'Talaba ID': 'ID',
        'To‘liq ismi': 'Ism',
        'Toliq ismi': 'Ism'
    }
    df = df.rename(columns=mapping)
    df.columns = df.columns.str.strip()

    if 'Guruh' in df.columns:
        df['Fak_Kod'] = df['Guruh'].str[:2].str.upper()
    else:
        df['Fak_Kod'] = "NOMA'LUM"
        
    return df

def apply_filters(df, faculty="Barcha", category="Barcha"):
    temp_df = df.copy()
    if faculty != "Barcha":
        temp_df = temp_df[temp_df['Fak_Kod'] == faculty]
    
    if category == "Yiqilayotganlar":
        temp_df = temp_df[temp_df['GPA'] < 3.0]
    elif category == "3 ga o'qiydiganlar":
        temp_df = temp_df[(temp_df['GPA'] >= 3.0) & (temp_df['GPA'] < 4.0)]
    elif category == "4-5 ga o'qiydiganlar":
        temp_df = temp_df[temp_df['GPA'] >= 4.0]
    return temp_df

def search_by_id(df, query):
    return df[df['ID'].astype(str).str.contains(str(query).strip(), na=False)]

def search_by_name(df, query):
    return df[df['Ism'].str.lower().str.contains(str(query).strip().lower(), na=False)]
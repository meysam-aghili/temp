import pandas as pd
import re
import os
from traceback import format_exc
import sys
import json
import hashlib


def get_mbf_file_paths(dir:str) -> list:
    file_paths = []
    for (dir_path, dir_names, file_names) in os.walk(dir):
        for file in file_names:
            if file.endswith('.mbf'):
                file_path = os.path.join(dir_path, file)
                file_paths.append(file_path)
    return file_paths

def read_mbf_file(file_path:str) -> list:
    with open(file_path, mode='r', encoding = "utf-8", errors='ignore') as file:
        return file.readlines()

def extract_data_dict(file_content:list) -> dict:
    splited_list_of_lines = [l.split('\x00') for l in file_content]
    splited_list_of_lines_flat = [item for sublist in splited_list_of_lines for item in sublist]
    data_dict = {}
    for i in splited_list_of_lines_flat:
        property_list = i.split()
        if len(property_list) >= 2:
            property_dict = {property_list[0]:" ".join(property_list[1:])}
            data_dict.update(property_dict)
    check_cols = [
        '@Number','@Date'
        ,'@CustName','@CustTell','@CustMobile'
        ,'@PriceUnit'
        ,'&takhfif','~takhfif','^takhfif','%takhfif'
        ,'&maliyat','~maliyat','^maliyat', '%maliyat'
        ,'&avarez','~avarez','^avarez', '%avarez'
    ]
    for c in check_cols:
        if data_dict.get(c) == None:
            data_dict.update({c:''})
    return data_dict

def extract_dataframe(data_dict:dict) -> pd.DataFrame:
    select_cols = [
        '@Number','@Date'
        ,'@CustName','@CustTell','@CustMobile'
        ,'@PriceUnit'
        ,'&takhfif','~takhfif','^takhfif','%takhfif'
        ,'&maliyat','~maliyat','^maliyat', '%maliyat'
        ,'&avarez','~avarez','^avarez', '%avarez'
    ]
    rename_cols = {
        '@Number':'order_code','@Date':'date'
        ,'@CustName':'customer_name','@CustTell':'customer_phone' ,'@CustMobile':'customer_mobile'
        ,'@PriceUnit' : 'unit_price'
        ,'%takhfif' : 'tafzil1_price','&takhfif' : 'tafzil1_title', '~takhfif' : 'tafzil1_is_percent', '^takhfif' : 'tafzil1_math_action'
        ,'%maliyat' : 'tafzil2_price','&maliyat' : 'tafzil2_title', '~maliyat' : 'tafzil2_is_percent', '^maliyat' : 'tafzil2_math_action'
        ,'%avarez' : 'tafzil3_price','&avarez' : 'tafzil3_title'  , '~avarez'  : 'tafzil3_is_percent', '^avarez'  : 'tafzil3_math_action'
    }
    order_df = pd.DataFrame([data_dict])[select_cols].rename(rename_cols, axis=1)

    keys_detail = list(filter(re.compile("#[A-G]\d").match, list(data_dict.keys())))
    keys_detail_A = list(filter(re.compile("#A\d").match, keys_detail))
    keys_detail_B = ['#B' + str(x+1) for x in range(len(keys_detail_A))]
    keys_detail_C = ['#C' + str(x+1) for x in range(len(keys_detail_A))]
    keys_detail_D = ['#D' + str(x+1) for x in range(len(keys_detail_A))]
    keys_detail_E = ['#E' + str(x+1) for x in range(len(keys_detail_A))]
    keys_detail_F = ['#F' + str(x+1) for x in range(len(keys_detail_A))]
    keys_detail_G = ['#G' + str(x+1) for x in range(len(keys_detail_A))]
    detail_dict = {'row'                    : [data_dict.get(a, '') for a in keys_detail_A]}
    detail_dict.update({'product_title'     : [data_dict.get(b, '') for b in keys_detail_B]})
    detail_dict.update({'quantity'          : [data_dict.get(c, '') for c in keys_detail_C]})
    detail_dict.update({'fee'               : [data_dict.get(d, '') for d in keys_detail_D]})
    detail_dict.update({'total_price'       : [data_dict.get(e, '') for e in keys_detail_E]})
    detail_dict.update({'consideration'     : [data_dict.get(f, '') for f in keys_detail_F]})
    detail_dict.update({'product_shenase'   : [data_dict.get(g, '') for g in keys_detail_G]})

    detail_df = pd.DataFrame(detail_dict)
    
    order_df['tmp'] = 1
    detail_df['tmp'] = 1
    df = order_df.merge(detail_df, on='tmp').reset_index(drop=True)
    return df

def get_dataframe(file_path:str) -> pd.DataFrame:
    file_content = read_mbf_file(file_path)
    data_dict = extract_data_dict(file_content)
    dataframe = extract_dataframe(data_dict)
    return dataframe

def load_excel(df:pd.DataFrame, excel_file_path:str):
    with pd.ExcelWriter(excel_file_path, engine='xlsxwriter') as excel_writer:
        df.style.set_properties(**{'text-align': 'center'}).to_excel(excel_writer, sheet_name='Sales', index=False)
        worksheet = excel_writer.sheets['Sales']
        worksheet.add_table(0, 0, df.shape[0], df.shape[1] - 1, {'columns': [{'header': header} for header in df.columns]})
        worksheet.autofit()

def get_file_hash(file_path):
    with open(file_path,'rb') as f:
        hash = hashlib.md5(f.read()).hexdigest()
    return hash

def get_dataframes(file_paths:list) -> pd.DataFrame:
    general_dataframe = pd.DataFrame()
    for i,file_path in enumerate(file_paths):
        dataframe = get_dataframe(file_path)
        dataframe['file_path'] = file_path
        dataframe['hash'] = get_file_hash(file_path)
        general_dataframe = pd.concat([general_dataframe, dataframe])
        print('File ',i+1,'processed.')
    price_cols = ['tafzil1_price','tafzil2_price','tafzil3_price','quantity','fee','total_price']
    for c in price_cols:
        general_dataframe[c] = general_dataframe[c].astype('str').str.replace(',', '')
    general_dataframe['total_price'] = general_dataframe['total_price'].str.replace('÷','')
    general_dataframe['quantity'] = general_dataframe.apply(lambda x: x['total_price']//x['fee'] if x['quantity']=='÷' else x['quantity'], axis=1)
    dtypes = {
        'tafzil1_is_percent':'bool','tafzil2_is_percent':'bool','tafzil3_is_percent':'bool'
        ,'tafzil1_price':'float','tafzil2_price':'float','tafzil3_price':'float'
        ,'row':'float','quantity':'float','fee':'float','total_price':'float'
    }
    general_dataframe = general_dataframe.astype(dtypes, errors='ignore')
    return general_dataframe.reset_index(drop=True)

def get_file_hashes(file_paths):
    file_hash = [get_file_hash(file_path) for file_path in file_paths]
    file_hash_unq = set()
    dupes = []
    for x in file_hash:
        if x in file_hash_unq:
            dupes.append(x)
        else:
            file_hash_unq.add((file_paths[file_hash.index(x)],x))
    dupelicated_files = [file_paths[file_hash.index(d)] for d in dupes]
    print(len(dupelicated_files),' files are duplicated.\n')
    print(dupelicated_files)
    return file_hash_unq

def get_updated_mbf_file_paths(file_paths):
    file_hash = pd.DataFrame([[file_path,get_file_hash(file_path)] for file_path in file_paths]).rename({0:'file_path',1:'hash'},axis=1)
    file_hash['is_duplicated'] = file_hash['hash'].duplicated()
    dupelicated_df = file_hash[file_hash['is_duplicated']==True].reset_index(drop=True)
    if os.path.isfile(config['excel_file_dir']):
        excel_df = pd.read_excel(config['excel_file_dir'])
        excel_hash = excel_df['hash'].drop_duplicates().reset_index().rename({'index':'is_exists'},axis=1)
        hash_df = file_hash.merge( excel_hash, how='left', on='hash',suffixes=('_left', '_right'))
        hash_df['is_exists'] = hash_df['is_exists'].apply(lambda x: False if pd.isna(x) else True)
        updated_df = hash_df[(hash_df['is_duplicated']==False) & (hash_df['is_exists']==False)].reset_index(drop=True)
        not_updated_df = hash_df[(hash_df['is_duplicated']==False) & (hash_df['is_exists']==True)].reset_index(drop=True)
        not_updated_excel_df = excel_df[excel_df['hash'].isin(not_updated_df['hash'])]
        deleted_df = excel_df.merge(file_hash, how='left', on='hash', suffixes=(None,'_y'))
        deleted = deleted_df[pd.isna(deleted_df['file_path_y'])]['hash'].to_list()
        return dupelicated_df['file_path'].to_list(), updated_df['file_path'].to_list(), not_updated_excel_df, deleted
    else:
        return dupelicated_df['file_path'].to_list(), file_hash[file_hash['is_duplicated']==False]['file_path'].to_list(), pd.DataFrame(), []

def run(mbf_root_folder:str, excel_file_path:str):
    try:
        print('Starting...')
        file_paths = get_mbf_file_paths(mbf_root_folder)
        print(len(file_paths),' files were found.')
        if len(file_paths)>0:
            dupelicated_file_paths, updated_file_paths, not_updated_excel_df, deleted = get_updated_mbf_file_paths(file_paths)
            print(len(updated_file_paths),' upserted files were found.')
            print(len(deleted),' deleted files were found.')
            print(len(dupelicated_file_paths),' dupelicated files were found.')
            if len(updated_file_paths)>0:
                general_dataframe = get_dataframes(updated_file_paths)
                general_dataframe = pd.concat([not_updated_excel_df, general_dataframe]).reset_index(drop=True)
                general_dataframe['order_id'] = pd.factorize(general_dataframe['hash'])[0]+1
                'Processing finished.'
                if not general_dataframe.empty:
                    load_excel(general_dataframe, excel_file_path)
                    print('loaded to excel file.')
            elif not not_updated_excel_df.empty:
                load_excel(not_updated_excel_df, excel_file_path)
                print('loaded to excel file.')
            if len(dupelicated_file_paths)>0:
                print('dupelicated_file_paths : \n',dupelicated_file_paths)
        print('Finished.')
    except PermissionError:
        print('-------------------------')
        print('Error message : please close the excel.')
    except Exception:
        error_type, error_message, _ = sys.exc_info()
        stack_trace = format_exc()
        print('-------------------------')
        print('Error type : ',error_type.__name__)
        print('Error message : ',error_message)
        print('Error trace : ',stack_trace)

if __name__=='__main__':
    if os.path.isfile("./config.json"):
        with open("./config.json") as config_file:
            config = json.load(config_file)
        run(config['mbf_file_dir'],config['excel_file_dir'])
    else:
        print('config.json file does not exists.')
    while True:pass
    
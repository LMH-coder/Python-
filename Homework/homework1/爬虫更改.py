import pandas as pd
import ast

def process_final_v2(input_filename, output_path):
    """
    使用Pandas的'python'引擎来读取格式不规范的CSV文件，
    然后解析'hs_Character'列并填充数据。
    """
    print(f"开始最终处理流程 (V2): {input_filename}")

    try:
        # --- 步骤1: 使用更强大的'python'引擎读取CSV文件 ---
        # 这个引擎能更好地处理引号、换行符等复杂情况。
        df = pd.read_csv(input_filename, sep=',', engine='python')
        
        print("文件读取成功！Pandas已正确分离列。")
        print("数据预览：")
        print(df.head())
        print("\n识别出的列名：")
        print(df.columns)
        
        # --- 步骤2: 执行我们已经写好的、健壮的解析逻辑 ---
        mapping_rules = {
            'hs_Character_Nationality': 'hs_Rank_Rich_Nationality',
            'hs_Character_NativePlace_Cn': 'hs_Rank_Rich_NativePlace_Cn',
            'hs_Character_NativePlace_En': 'hs_Rank_Rich_NativePlace_En',
            'hs_Character_BirthPlace_Cn': 'hs_Rank_Rich_BirthPlace_Cn',
            'hs_Character_BirthPlace_En': 'hs_Rank_Rich_BirthPlace_En',
            'hs_Character_Permanent_Cn': 'hs_Rank_Rich_Permanent_Cn',
            'hs_Character_Permanent_En': 'hs_Rank_Rich_Permanent_En',
            'hs_Character_Photo': 'hs_Rank_Rich_Photo',
            'hs_Character_Age': 'hs_Rank_Rich_Age',
            'hs_Character_Gender': 'hs_Rank_Rich_Gender',
            'hs_Character_Education_Cn': 'hs_Rank_Rich_Education_Cn',
            'hs_Character_Education_En': 'hs_Rank_Rich_Education_En',
            'hs_Character_School_Cn': 'hs_Rank_Rich_School_Cn',
            'hs_Character_School_En': 'hs_Rank_Rich_School_En'
        }
        
        def parse_and_fill(row):
            if 'hs_Character' not in row or pd.isna(row['hs_Character']):
                return row
            
            char_string = row['hs_Character']
            if not isinstance(char_string, str) or not char_string.startswith('['):
                return row

            try:
                data_list = ast.literal_eval(char_string)
                if isinstance(data_list, list) and len(data_list) > 0:
                    char_data = data_list[0]
                    if isinstance(char_data, dict):
                        for source_key, target_column in mapping_rules.items():
                            value = char_data.get(source_key)
                            if target_column in row.index:
                                row[target_column] = value
            except (ValueError, SyntaxError):
                # 如果某行格式错误，静默跳过或打印警告
                # print(f"警告: 在行 {row.name} 解析失败")
                pass
            
            return row

        print("\n开始解析 'hs_Character' 列并填充数据...")
        df_processed = df.apply(parse_and_fill, axis=1)
        print("数据填充完成。")

        # --- 步骤3: 清理和保存 ---
        if 'hs_Character' in df_processed.columns:
            df_processed = df_processed.drop(columns=['hs_Character'])
            print("'hs_Character' 列已删除。")

        df_processed.to_excel(output_path, index=False, engine='openpyxl')
        print(f"\n处理成功！最终结果已保存至: {output_path}")

    except FileNotFoundError:
        print(f"错误：找不到文件 '{input_filename}'。")
    except Exception as e:
        print(f"处理过程中发生未知错误: {e}")

# --- 主程序运行部分 ---
input_file = '胡润百富榜完整数据.csv'
output_file = '胡润百富榜完整数据2.0.xlsx'

process_final_v2(input_file, output_file)

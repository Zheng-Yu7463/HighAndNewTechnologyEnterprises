import pdfplumber
import camelot
import re
import os
import json
import pandas as pd


# --- 1. 定义解析结构化表格的函数 (通用尝试) ---
def parse_structured_table_pdf(pdf_path):
    """
    尝试使用 Camelot 解析结构化表格中的公司名称和编号。
    这适用于有明确表格线的PDF。
    """
    extracted_companies = []
    print(f"  尝试使用 Camelot 提取表格...")
    try:
        tables = camelot.read_pdf(pdf_path, flavor='lattice', pages='all', line_scale=40)

        if not tables:
            print(f"  Camelot 未提取到任何表格。")
            return []

        print(f"  Camelot 提取到 {len(tables)} 个表格。开始解析...")
        for table in tables:
            df = table.df  # 将表格转换为 Pandas DataFrame

            name_headers = ["企业名称", "公司名称", "名称"]
            id_headers = ["证书编号", "编号", "高新企业编号"]

            name_col_idx = -1
            id_col_idx = -1

            # 尝试在第一行找表头
            header_row = df.iloc[0].astype(str).tolist()
            for i, header_cell in enumerate(header_row):
                for nh in name_headers:
                    if nh in header_cell:
                        name_col_idx = i
                        break
                for ih in id_headers:
                    if ih in header_cell:
                        id_col_idx = i
                        break
                if name_col_idx != -1 and id_col_idx != -1:
                    break

            # 如果没找到，尝试在所有列中通过内容特征找（修复警告：使用非捕获组(?:)）
            if name_col_idx == -1 and df.shape[1] > 1:
                for col_idx in range(df.shape[1]):
                    sample_data = df.iloc[1:min(5, df.shape[0])][col_idx].astype(str)
                    # 修复警告：将捕获组 (公司|厂|研究院|中心|所) 更改为非捕获组 (?:公司|厂|研究院|中心|所)
                    if sample_data.str.contains(r'(?:公司|厂|研究院|中心|所)').any() and len(sample_data.iloc[0]) > 3:
                        name_col_idx = col_idx
                        break

            if id_col_idx == -1 and df.shape[1] > 1:
                for col_idx in range(df.shape[1]):
                    sample_data = df.iloc[1:min(5, df.shape[0])][col_idx].astype(str)
                    # 修复警告：将捕获组 (GR|GS) 更改为非捕获组 (?:GR|GS)
                    if sample_data.str.contains(r'^(?:GR|GS)\d{12,}').any():
                        id_col_idx = col_idx
                        break

            if name_col_idx == -1 or id_col_idx == -1:
                continue

            start_row_idx = 0
            if "企业名称" in str(df.iloc[0, name_col_idx]) or "证书编号" in str(df.iloc[0, id_col_idx]):
                start_row_idx = 1

            for index, row in df.iloc[start_row_idx:].iterrows():
                try:
                    company_name = str(row[name_col_idx]).strip()
                    company_id = str(row[id_col_idx]).strip()

                    if company_name and len(company_name) > 3 and company_id and re.match(r'^(GR|GS)\d{12,}$',
                                                                                          company_id):
                        extracted_companies.append({"名称": company_name, "编号": company_id})
                except IndexError:
                    continue

    except Exception as e:
        print(f"  Camelot 提取表格时发生错误: {e}")
    return extracted_companies


# --- 2. 定义解析文本流的函数 (通用尝试，包含针对特定格式的适配) ---
def parse_text_stream_pdf(pdf_path):
    """
    使用 pdfplumber 提取文本，然后用正则表达式解析公司名称和编号。
    适用于各种文本流格式，包括列表形式和仅有编号的形式。
    """
    extracted_companies = []
    print(f"  尝试使用 pdfplumber 和正则表达式提取文本...")
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if not text:
                    continue

                # 策略 A: 匹配 "序号 公司名称 编号" 格式 (适用于福建省文件)
                # 修复警告：将捕获组 ((?:GR|GS)\d{12,}) 更改为非捕获组 ((?:GR|GS)\d{12,})
                pattern_A = re.compile(
                    r'^\s*\d+\s+([\u4e00-\u9fa5a-zA-Z0-9\(\)\[\]【】\uFF08\uFF09\uFF3B\uFF3D\u300A\u300B\u2014\u2013\uff0c\uff0e\u3001\uff1a\uff1b\uff1f\uff01\u00B7\uFE30-\uFE4F\s]+?)\s+((?:GR|GS)\d{12,})\s*$',
                    re.MULTILINE
                )

                matches_A = pattern_A.finditer(text)
                for match in matches_A:
                    company_name = match.group(1).strip()
                    company_id = match.group(2).strip()
                    if company_name and len(company_name) > 3 and not company_name.isdigit() and company_id:
                        extracted_companies.append({"名称": company_name, "编号": company_id})

                if extracted_companies:
                    return extracted_companies

                    # 策略 B: 匹配 "序号,,编号" 或 "序号,名称,编号" 这种CSV-like的格式 (适用于北京市文件)
                # 修复警告：将捕获组 ((?:GR|GS)\d{12,}) 更改为非捕获组 ((?:GR|GS)\d{12,})
                pattern_B = re.compile(
                    r'^\s*\d+\s*,\s*(.*?)\s*,\s*((?:GR|GS)\d{12,})\s*$',
                    re.MULTILINE
                )
                matches_B = pattern_B.finditer(text)
                for match in matches_B:
                    company_name = match.group(1).strip()
                    company_id = match.group(2).strip()

                    if not company_name:
                        company_name = None

                    if company_id and re.match(r'^(GR|GS)\d{12,}$', company_id):
                        extracted_companies.append({"名称": company_name, "编号": company_id})

    except Exception as e:
        print(f"  pdfplumber 和正则表达式提取文本时发生错误: {e}")
    return extracted_companies


# --- 主处理逻辑 ---
def process_pdf_files(directory="."):
    """
    遍历指定目录下的所有PDF文件，并根据启发式策略选择解析方法。
    """
    all_extracted_data = {}

    # 确保输出目录存在
    output_dir = os.path.join(directory, "json_results")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    pdf_files = [f for f in os.listdir(directory) if f.lower().endswith(".pdf")]

    if not pdf_files:
        print(f"在目录 '{directory}' 中未找到任何 PDF 文件。")
        return all_extracted_data

    for pdf_file_name in pdf_files:
        pdf_path = os.path.join(directory, pdf_file_name)
        # 构建目标 JSON 文件的完整路径
        output_json_file = os.path.join(output_dir, f"{os.path.splitext(pdf_file_name)[0]}.json")

        # --- 新增的检查逻辑 ---
        if os.path.exists(output_json_file):
            print(f"\n--- 文件: {pdf_file_name} ---")
            print(f"  [{output_json_file}] 已存在，跳过解析。")
            # 如果需要，可以加载已存在的数据到 all_extracted_data 中
            # try:
            #     with open(output_json_file, 'r', encoding='utf-8') as f:
            #         all_extracted_data[pdf_file_name] = json.load(f)
            # except json.JSONDecodeError:
            #     print(f"  警告: 无法加载已存在的JSON文件 '{output_json_file}'。")
            all_extracted_data[pdf_file_name] = []  # 或者保持为空，取决于你是否需要汇总
            continue  # 跳过当前文件的解析，进入下一个文件
        # --- 新增检查结束 ---

        extracted_data_for_file = []

        print(f"\n--- 正在处理文件: {pdf_file_name} ---")

        camelot_data = parse_structured_table_pdf(pdf_path)
        if camelot_data:
            print(f"  Camelot 成功提取 {len(camelot_data)} 条公司信息。使用 Camelot 结果。")
            extracted_data_for_file = camelot_data
        else:
            print(f"  Camelot 未能有效提取数据，尝试 pdfplumber + 正则表达式。")
            text_stream_data = parse_text_stream_pdf(pdf_path)
            if text_stream_data:
                print(f"  pdfplumber + 正则表达式成功提取 {len(text_stream_data)} 条公司信息。使用此结果。")
                extracted_data_for_file = text_stream_data
            else:
                print(f"  所有解析策略均未能从 [{pdf_file_name}] 提取到公司信息。")

        all_extracted_data[pdf_file_name] = extracted_data_for_file

        # 每个 PDF 的结果单独保存到 JSON 文件
        with open(output_json_file, 'w', encoding='utf-8') as f:
            json.dump(extracted_data_for_file, f, ensure_ascii=False, indent=2)
        print(f"  [{pdf_file_name}] 结果已保存到 '{output_json_file}'")

    return all_extracted_data


# --- 执行脚本 ---
if __name__ == "__main__":
    results_directory = "results"

    if not os.path.exists(results_directory):
        print(f"错误: 目录 '{results_directory}' 不存在。请创建该目录并将PDF文件放入其中。")
    else:
        extracted_results_summary = process_pdf_files(results_directory)

        print("\n=== 所有文件处理完毕 ===")
        print(f"详细结果已保存到 '{os.path.join(results_directory, 'json_results')}' 目录下。")

        for filename, data in extracted_results_summary.items():
            print(f"  文件: {filename} -> 提取条数: {len(data)}")
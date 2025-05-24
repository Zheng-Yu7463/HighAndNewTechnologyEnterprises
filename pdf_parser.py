import os
import json
import pandas as pd
import re


def identify_empty_json_files(json_results_dir, output_excel_path):
    """
    遍历指定目录下的JSON文件，找出内容为空的（[]）文件，
    并将其文件名、提取到的时间、地区信息整合到Excel中。

    Args:
        json_results_dir (str): 存放JSON结果的目录路径。
        output_excel_path (str): 输出Excel文件的完整路径。
    """

    empty_files_data = []

    # 预定义的地区列表（与之前的脚本保持一致，并进行排序）
    regs = [
        '北京市', '天津市', '河北省', '山西省', '内蒙古自治区', '辽宁省', '大连市', '吉林省',
        '黑龙江省', '上海市', '江苏省', '浙江省', '宁波市', '安徽省', '福建省', '厦门市',
        '江西省', '山东省', '青岛市', '河南省', '湖北省', '湖南省', '广东省', '深圳市',
        '广西壮族自治区', '海南省', '重庆市', '四川省', '贵州省', '云南省', '西藏自治区',
        '陕西省', '甘肃省', '青海省', '宁夏回族自治区', '新疆维吾尔自治区',
        '北京', '天津', '河北', '山西', '内蒙古', '辽宁', '吉林', '黑龙江', '上海',
        '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南', '广东',
        '广西', '海南', '重庆', '四川', '贵州', '云南', '西藏', '陕西', '甘肃', '青海',
        '宁夏', '新疆'
    ]
    regs.sort(key=len, reverse=True)  # 确保优先匹配完整的地区名称

    print(f"开始检查 '{json_results_dir}' 目录下的JSON文件...")

    # 遍历json_results目录下的所有文件
    for filename in os.listdir(json_results_dir):
        if filename.lower().endswith(".json"):
            json_file_path = os.path.join(json_results_dir, filename)

            # 1. 提取时间
            time_match = re.search(r'&(\d{4}-\d{2}-\d{2})\.json$', filename)
            extracted_time = time_match.group(1) if time_match else "未知时间"

            # 2. 提取地区
            extracted_region = "未知地区"
            file_name_body = os.path.splitext(filename)[0]
            if '&' in file_name_body:
                file_name_body = file_name_body.split('&')[0]

            for reg in regs:
                if reg in file_name_body:
                    extracted_region = reg
                    break

            # 3. 读取JSON文件内容并判断是否为空列表
            try:
                with open(json_file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list) and not data:  # 判断是否为[]
                        print(f"  发现空文件: {filename}")
                        empty_files_data.append({
                            "文件名": filename,
                            "时间": extracted_time,
                            "地区": extracted_region,
                            "备注": "未提取到公司数据"
                        })
            except json.JSONDecodeError as e:
                print(f"  错误: 文件 '{filename}' JSON格式错误，跳过处理: {e}")
                empty_files_data.append({
                    "文件名": filename,
                    "时间": extracted_time,
                    "地区": extracted_region,
                    "备注": f"JSON格式错误: {e}"
                })
            except Exception as e:
                print(f"  错误: 处理文件 '{filename}' 时发生未知错误，跳过处理: {e}")
                empty_files_data.append({
                    "文件名": filename,
                    "时间": extracted_time,
                    "地区": extracted_region,
                    "备注": f"未知错误: {e}"
                })

    # 4. 转换为DataFrame并写入Excel
    if empty_files_data:
        df = pd.DataFrame(empty_files_data)
        try:
            df.to_excel(output_excel_path, index=False, engine='openpyxl')
            print(f"\n所有空文件信息已成功整合并保存到 '{output_excel_path}'")
        except Exception as e:
            print(f"\n错误: 写入Excel文件 '{output_excel_path}' 时发生错误: {e}")
    else:
        print("\n未发现任何内容为空的JSON文件。")


# --- 主执行部分 ---
if __name__ == "__main__":
    # 假设 json_results 目录在当前脚本所在的 results 目录下
    base_directory = "results"
    json_results_folder = os.path.join(base_directory, "json_results")
    output_excel_file = os.path.join(base_directory, "未解析文件统计.xlsx")  # 输出文件名称

    # 确保 json_results 目录存在
    if not os.path.exists(json_results_folder):
        print(f"错误: JSON结果目录 '{json_results_folder}' 不存在。请先运行PDF解析脚本生成JSON文件。")
    else:
        identify_empty_json_files(json_results_folder, output_excel_file)
import yaml
import re
import sys
import os

# 处理函数：清理域名
def clean_domain(domain):
    # 使用正则去掉开头的 "- '+." 和结尾的 "'" 以及注释部分
    cleaned_domain = re.sub(r"^\- '\+\.(.*?)'\s*#.*$", r"\1", domain)
    return cleaned_domain

# 判断域名并加上对应前缀，若无 `.` 则删除该行
def add_domain_prefix(domain):
    # 计算 `.` 的数量
    dot_count = domain.count('.')
    
    if dot_count == 1:
        return f"DOMAIN-SUFFIX,{domain},Proxy"
    elif dot_count >= 2:
        return f"DOMAIN,{domain},Proxy"
    else:
        return None  # 无 `.` 的行返回 None，后面会被忽略

# 处理 YAML 文件
def process_yaml_file(file_path):
    try:
        # 读取 YAML 文件
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)

        # 如果文件开头有 'payload:'，删除该行
        if isinstance(data, list) and data and isinstance(data[0], str) and data[0].startswith("payload:"):
            data = data[1:]  # 删除第一行

        # 假设文件中的数据是一个列表，逐一处理每个域名
        cleaned_data = [clean_domain(domain) for domain in data]

        # 根据域名的 `.` 数量，添加相应的前缀，并去掉不符合的行
        processed_data = [add_domain_prefix(domain) for domain in cleaned_data]

        # 过滤掉 None 值的行（即不包含 `.` 的行）
        processed_data = [domain for domain in processed_data if domain is not None]

        # 返回处理后的数据
        return processed_data

    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")
        return None

# 将处理结果写入新文件（每个域名单独一行）
def write_to_file(output_path, data):
    try:
        # 以追加模式将每个域名写入文件，每行一个
        with open(output_path, 'a', encoding='utf-8') as file:
            for domain in data:
                file.write(domain + '\n')
        print(f"处理结果已保存到 {output_path}")
    except Exception as e:
        print(f"写入文件 {output_path} 时出错: {e}")

# 定义输入文件所在的目录路径
directory_path = '/home/runner/work/Clash_Config/Clash_Config'

# 主函数：处理多个文件并保存结果
def main():
    yaml_files = sys.argv[2:]  # 获取所有输入文件名（不包括目录）
    output_file = sys.argv[1]   # 获取输出文件路径
    
    # 处理每个输入的 YAML 文件
    for file_name in yaml_files:
        # 拼接目录路径和文件名
        file_path = os.path.join(directory_path, file_name)
        
        print(f"正在处理文件: {file_path}")
        
        # 处理 YAML 文件
        processed_domains = process_yaml_file(file_path)
        
        if processed_domains is not None:
            # 将处理后的域名写入输出文件（以追加模式）
            write_to_file(output_file, processed_domains)
        else:
            print(f"文件 {file_path} 处理失败。")

if __name__ == "__main__":
    main()

import yaml
import json
import os
import sys

def extract_domains(yaml_file):
    with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file)

    domains = []
    for url in data.get('payload', []):
        # 移除前缀 '+.' 并添加到 domains 列表
        domain = url.lstrip('+.')
        domains.append(domain)
    
    return domains

def convert_to_json(domains):
    result = {
        "version": 1,
        "rules": [
            {
                "domain_suffix": domains
            }
        ]
    }
    return result

#1 文件路径
#1yaml_file_path = '/home/runner/work/Clash_Config/Clash_Config/Extended.yaml'
#1output_file_path = '/home/runner/work/Clash_Config/Clash_Config/rule/extended.json'

# 目录路径
directory_path = '/home/runner/work/Clash_Config/Clash_Config'  # 修改为你的目录路径

# 获取命令行参数
file_names = sys.argv[1:]

# 遍历指定的文件名
for filename in file_names:
    yaml_file_path = os.path.join(directory_path, filename)

    if os.path.exists(yaml_file_path) and (filename.endswith('.yaml') or filename.endswith('.yml')):
        # 提取域名并转换为 JSON
        domains = extract_domains(yaml_file_path)
        json_output = convert_to_json(domains)

        # 生成输出 JSON 文件名
        json_filename = f"{os.path.splitext(filename)[0]}.json"
        json_file_path = os.path.join('/home/runner/work/Clash_Config/Clash_Config/Rules', json_filename)

        # 将结果保存到新文件
        with open(json_file_path, 'w') as output_file:
            json.dump(json_output, output_file, indent=2, ensure_ascii=False)

        print(f'转换结果已保存到 {json_file_path}')
    else:
        print(f'文件 {filename} 不存在或不是 YAML 文件。')


#1 提取域名并转换为 JSON
#1domains = extract_domains(yaml_file_path)
#1json_output = convert_to_json(domains)

#1 将结果保存到新文件
#1with open(output_file_path, 'w') as output_file:
#1    json.dump(json_output, output_file, indent=2, ensure_ascii=False)

#1print(f'转换结果已保存到 {output_file_path}')

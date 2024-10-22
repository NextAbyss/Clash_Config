import yaml
import json

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

# 文件路径
yaml_file_path = '/root/ex1.yaml'
output_file_path = '/root/exs1.json'

# 提取域名并转换为 JSON
domains = extract_domains(yaml_file_path)
json_output = convert_to_json(domains)

# 将结果保存到新文件
with open(output_file_path, 'w') as output_file:
    json.dump(json_output, output_file, indent=2, ensure_ascii=False)

print(f'转换结果已保存到 {output_file_path}')

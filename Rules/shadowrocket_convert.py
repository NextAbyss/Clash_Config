import yaml
import sys

def process_line(line):
    # 删除前缀 '- '+.' 和处理后缀
    domain = line.strip("'").lstrip("- '+.")
    # 判断有多少个点来决定使用 DOMAIN 或 DOMAIN-SUFFIX
    if domain.count('.') == 1:
        processed_line = f"DOMAIN,{domain},Proxy"
    else:
        processed_line = f"DOMAIN-SUFFIX,{domain},Proxy"
    return processed_line

def process_file(input_file):
    with open(input_file, 'r') as file:
        content = file.readlines()

    result = []
    in_payload = False
    for line in content:
        line = line.strip()
        
        # 忽略 payload 和注释行
        if line.startswith("payload:") or line.startswith("##"):
            continue
        
        # 处理有效的域名行
        if line.startswith("-"):
            result.append(process_line(line))
    return result

def main(output_file, *input_files):
    all_results = []

    for input_file in input_files:
        all_results.extend(process_file(input_file))

    # 写入输出文件
    with open(output_file, 'w') as outfile:
        for line in all_results:
            outfile.write(line + "\n")

if __name__ == "__main__":
    # 获取命令行参数
    output_file = sys.argv[1]
    input_files = sys.argv[2:]
    
    # 执行处理
    main(output_file, *input_files)

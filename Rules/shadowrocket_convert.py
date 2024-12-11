import yaml
import sys
import os

def is_root_domain(domain):
    # A domain is considered a root domain if it contains exactly one dot
    return domain.count('.') == 1

def convert_multiple_yaml_to_domain_suffix(yaml_files, output_file, directory_path):
    try:
        all_domains = []

        for yaml_file in yaml_files:
            full_path = os.path.join(directory_path, yaml_file)  # Construct full path
            with open(full_path, 'r') as file:
                data = yaml.safe_load(file)

                # Extract and format the domains
                for item in data['payload']:
                    domain = item.strip("+-'")  # Remove prefixes, suffixes, and quotes
                    if domain.startswith('.'): 
                        domain = domain[1:]  # Remove leading dot

                    # Determine the format based on whether it's a root domain
                    if is_root_domain(domain):
                        all_domains.append(f"DOMAIN,{domain},Proxy")
                    else:
                        all_domains.append(f"DOMAIN-SUFFIX,{domain},Proxy")

        # Write to the output file
        with open(output_file, 'w') as file:
            file.write("\n".join(all_domains))

        print(f"Successfully merged and converted YAML files to DOMAIN/DOMAIN-SUFFIX format and saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")
        
directory_path = '/home/runner/work/Clash_Config/Clash_Config'

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Usage: python script.py <output_file> <input_file1> <input_file2> ...")
        sys.exit(1)

    output_file = sys.argv[1]
    input_files = sys.argv[2:]
    convert_multiple_yaml_to_domain_suffix(input_files, output_file, directory_path)

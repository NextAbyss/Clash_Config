import yaml
import sys

def is_root_domain(domain):
    # Check if the domain is a root domain (contains no dots other than the final dot in TLD)
    return domain.count('.') == 1

def convert_multiple_yaml_to_domain_suffix(yaml_files, output_file):
    try:
        all_domains = []

        for yaml_file in yaml_files:
            with open(yaml_file, 'r') as file:
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

# Example usage
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <output_file> <input_file1> <input_file2> ...")
        sys.exit(1)

    output_file = sys.argv[1]
    input_files = sys.argv[2:]
    convert_multiple_yaml_to_domain_suffix(input_files, output_file)

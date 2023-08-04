import csv
import requests
import time


def read_domain_names_from_file(file_path):
    with open(file_path,'r', encoding="utf-8") as file:
        domain_names = [line.strip() for line in file]
    return domain_names


def validate_domains(domain_names, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as output:
        csv_writer = csv.writer(output)
        csv_writer.writerow(
            ['Domain', 'HTTP Status Code', 'HTTP Content Size', 'HTTPS Status Code', 'HTTPS Content Size'])

        for domain in domain_names:
            http_status_code = None
            http_content_length = None
            https_status_code = None
            https_content_length = None

            try:
                # HTTP request
                http_response = requests.get('http://' + domain, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'},
                                             timeout=5)
                http_status_code = http_response.status_code
                http_content_length = len(http_response.content) if http_response.content else 0

                # HTTPS request
                https_response = requests.get('https://' + domain, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'},
                                              timeout=5)
                https_status_code = https_response.status_code
                https_content_length = len(https_response.content) if https_response.content else 0

            except requests.RequestException as e:
                print(f"An error occurred while processing '{domain}': {str(e)}")

            csv_writer.writerow(
                [domain, http_status_code, http_content_length, https_status_code, https_content_length])
            time.sleep(1)


if __name__ == '__main__':
    txt_file_path = 'input.txt'
    csv_file_path = 'output.csv'

    domain_names = read_domain_names_from_file(txt_file_path)
    validate_domains(domain_names, csv_file_path)

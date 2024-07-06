import re
from collections import defaultdict, Counter


# Function to parse a log line
def parse_log_line(line):
    log_pattern = re.compile(r'(\S+) - - \[(.*?)\] "(.*?)" (\d{3}) (\d+|-) "(.*?)" "(.*?)"')
    match = log_pattern.match(line)
    if match:
        ip = match.group(1)
        datetime = match.group(2)
        request = match.group(3)
        status_code = match.group(4)
        size = match.group(5)
        referer = match.group(6)
        user_agent = match.group(7)
        return ip, datetime, request, status_code, size, referer, user_agent
    return None


# Function to analyze log file
def analyze_log_file(log_file_path):
    with open(log_file_path, 'r') as file:
        lines = file.readlines()

    ip_counter = Counter()
    page_counter = Counter()
    error_404_count = 0

    for line in lines:
        parsed_line = parse_log_line(line)
        if parsed_line:
            ip, datetime, request, status_code, size, referer, user_agent = parsed_line


            ip_counter[ip] += 1


            page = request.split(' ')[1] if request else '-'
            page_counter[page] += 1


            if status_code == '404':
                error_404_count += 1

    return ip_counter, page_counter, error_404_count


# Function to print the summarized report
def print_summary(ip_counter, page_counter, error_404_count):
    print("\nSummarized Report:")
    print("===================")
    print(f"Number of 404 errors: {error_404_count}\n")

    print("Top 10 Most Requested Pages:")
    print("----------------------------")
    for page, count in page_counter.most_common(10):
        print(f"{page}: {count} requests")

    print("\nTop 10 IP Addresses with Most Requests:")
    print("---------------------------------------")
    for ip, count in ip_counter.most_common(10):
        print(f"{ip}: {count} requests")


# Main function
if __name__ == "__main__":
    log_file_path = 'path/to/your/logfile.log'  # Replace with the path to your log file
    ip_counter, page_counter, error_404_count = analyze_log_file(log_file_path)
    print_summary(ip_counter, page_counter, error_404_count)

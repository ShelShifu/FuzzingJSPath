import argparse
import re
import requests
import csv
from urllib.parse import urljoin

def main():
    parser = argparse.ArgumentParser(description="Script to filter response using a regular expression.")
    parser.add_argument("-u", "--url", required=True, help="Target site URL")
    args = parser.parse_args()

    target_url = args.url
    regex_pattern_1 = r"\/[a-z]\S+?\.js"
    regex_pattern_2 = r"\=[a-z]\S+?\.js"
    regex_pattern_3 = r"=\"[a-z]\S+?\.js"

    try:
        response = requests.get(target_url, verify=False)
        response.raise_for_status()

        matches = []
        matches.extend(re.findall(regex_pattern_1, response.text))
        
        matches_2 = re.findall(regex_pattern_2, response.text)
        for match in matches_2:
            cleaned_match = match.replace("=", "")
            matches.append(cleaned_match)

        matches_3 = re.findall(regex_pattern_3, response.text)
        for match in matches_3:
            cleaned_match = match.replace("=\"", "")
            matches.append(cleaned_match)

        if matches:
            print("Matches found:")
            cleaned_and_unique_matches = set()

            for match in matches:
                full_js_url = urljoin(target_url, match)
                print("JS URL:", full_js_url)
                try:
                    js_response = requests.get(full_js_url, verify=False)
                    js_response.raise_for_status()

                    secondary_matches = re.findall(r"\"\/[a-z]\S+?\"", js_response.text)
                    cleaned_matches = clean_and_unique(secondary_matches)
                    cleaned_and_unique_matches.update(cleaned_matches)

                except requests.exceptions.RequestException as js_e:
                    print("Error accessing JS URL:", js_e)

            process_and_save_results(target_url, cleaned_and_unique_matches)
        else:
            print("No matches found.")
    except requests.exceptions.RequestException as e:
        print("Error:", e)

def clean_and_unique(matches):
    cleaned_matches = set()
    for match in matches:
        cleaned_match = match.strip('"')
        cleaned_matches.add(cleaned_match)
    return cleaned_matches

def process_and_save_results(base_url, paths):
    result_data = []

    for path in paths:
        full_path = urljoin(base_url, path)
        try:
            path_response = requests.get(full_path, verify=False)
            path_response.raise_for_status()

            result_data.append((full_path, path_response.status_code, len(path_response.text)))
        except requests.exceptions.RequestException as path_e:
            print("Error accessing path URL:", path_e)

    save_to_csv(result_data)
    print("Results saved to 'output.csv'.")

def save_to_csv(data):
    with open("output.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Path", "HTTP Status Code", "Response Size"])
        writer.writerows(data)

if __name__ == "__main__":
    main()

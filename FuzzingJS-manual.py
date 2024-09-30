import argparse
import re
import requests
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
        response = requests.get(target_url,verify=False)
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
                    js_response = requests.get(full_js_url,verify=False)
                    js_response.raise_for_status()

                    secondary_matches = re.findall(r"\"\/[a-z]\S+?\"", js_response.text)
                    cleaned_matches = clean_and_unique(secondary_matches)
                    cleaned_and_unique_matches.update(cleaned_matches)

                except requests.exceptions.RequestException as js_e:
                    print("Error accessing JS URL:", js_e)

            save_to_txt(cleaned_and_unique_matches)
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

def save_to_txt(matches_set):
    with open("cleaned_matches.txt", mode="w", encoding="utf-8") as file:
        for match in matches_set:
            file.write(match + "\n")
    print("Cleaned and unique matches saved to 'cleaned_matches.txt'.")

if __name__ == "__main__":
    main()

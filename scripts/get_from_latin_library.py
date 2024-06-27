import re
import requests
from bs4 import BeautifulSoup
import argparse

def main():
    url = args.url
    output = args.output

    # Get the page
    r = requests.get(url)
    r.raise_for_status()

    # Parse the page
    soup = BeautifulSoup(r.text, 'html.parser')

    # Get the title
    title = soup.find('h1').get_text()

    # Get the text from each <p> tag as a list
    texts = [p.get_text() for p in soup.find_all('p')][1:]

    # seperate the texts by the numbered verses
    seperated_texts = []
    for text in texts:
        seperated_texts.append(re.split(r'\d+\s', text)[1:])

    # Save the text
    with open(output, 'w') as f:
        f.write(title + '\n\n')
        for text in seperated_texts:
            for line in text:
                if line != '':
                    f.write(line + '\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download a text from the Latin Library')
    parser.add_argument('url', type=str, help='URL of the text to download')
    parser.add_argument('output', type=str, help='Output file')
    args = parser.parse_args()

    main()
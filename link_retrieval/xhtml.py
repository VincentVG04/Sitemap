import requests
import xml.etree.ElementTree as ET

def validate_sitemap_links(url):
    all_links = []
    faulty_links = []
    try:
        response = requests.get(url)
        if response.status_code == 200:
            try:
                root = ET.fromstring(response.content)
                # Search for elements without namespace prefixes
                for element in root.findall(".//{*}link[@rel='alternate']"):
                    href = element.attrib.get('href')
                    all_links.append(href)
                    link_response = requests.head(href)
                    if link_response.status_code == 404:
                        faulty_links.append(href)
            except ET.ParseError:
                print("Error: Sitemap is not a valid XML.")
        else:
            print("Error: Unable to fetch sitemap. Status code:", response.status_code)
    except requests.RequestException as e:
        print("Error:", e)
    finally:
        if faulty_links:
            print("Faulty links found:")
            for link in faulty_links:
                print(f"- {link}")
        else:
            print("All links:")
            for link in all_links:
                print(f"- {link}")

# Example usage:
sitemap_url = "http://transdev.nl/sitemap.xml"
validate_sitemap_links(sitemap_url)

import requests
import xml.etree.ElementTree as ET

def validate_sitemap_links(url):
    total_links = 0
    try:
        response = requests.get(url)
        if response.status_code == 200:
            try:
                root = ET.fromstring(response.content)
                for child in root:
                    total_links += 1
                    loc = child.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc").text
                    link_response = requests.head(loc)
                    if link_response.status_code == 404:
                        print(f"{loc} returned a 404 error.")
                    print (loc)
            except ET.ParseError:
                print("Error: Sitemap is not a valid XML.")
        else:
            print("Error: Unable to fetch sitemap. Status code:", response.status_code)
    except requests.RequestException as e:
        print("Error:", e)
    finally:
        print(f"Total number of links: {total_links}")

# Example usage:
sitemap_url = "https://www.enigmatry.com/nl/sitemap.xml"
validate_sitemap_links(sitemap_url)

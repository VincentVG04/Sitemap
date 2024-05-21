# This tool reads an entire URL, divides it into segments and checks if each segment is accessible or returns a 404 error.
import requests
from urllib.parse import urlparse, urljoin

def check_link_validity(url):
    response = requests.get(url, allow_redirects=False)

    try:
        # Parse the URL to extract the directory path
        parsed_url = urlparse(url)
        directory_path = parsed_url.path

        # Initialize the base URL
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

        # Initialize the current URL before the loop
        current_url = base_url

        # Iterate through path segments to check the validity of each intermediate URL
        for segment in directory_path.split('/'):
            if segment:
                # Update the current URL inside the loop
                current_url += '/' + segment
                response = requests.get(current_url)
                if response.status_code == 404:
                    print(f"The URL {current_url} does not exist.")
                    print (f"{url} is not accessible through the website.")
                    return
                elif response.status_code != 200:
                    print(f"Failed to access the URL {current_url}. Status code: {response.status_code}")
                    return

        # If all intermediate URLs are valid, check the final URL
        response = requests.get(current_url)
        if response.status_code == 200:
            print(f"The URL {url} is accessible.")
        else:
            print(f"Failed to access the URL {url}. Status code: {response.status_code}")

    except requests.RequestException as e:
        print(f"An error occurred while accessing the URL: {e}")

# Example usage:
url = "https://www.connexxion.nl/sitemap.xml"
check_link_validity(url)

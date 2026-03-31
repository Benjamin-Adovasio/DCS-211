import requests
import time
from bs4 import BeautifulSoup


def fetchAndPrintQuakes(start_date, end_date, min_magnitude):
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    
    params = {
        "method": "query",
        "format": "geojson",
        "starttime": start_date,
        "endtime": end_date,
        "minmagnitude": min_magnitude
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    for quake in data["features"]:
        properties = quake["properties"]
        
        magnitude = properties["mag"]
        location = properties["place"]
        timestamp = properties["time"] / 1000
        
        time_str = time.strftime("%H:%M:%S", time.gmtime(timestamp))
        date_str = time.strftime("%a, %d %b %Y", time.gmtime(timestamp))
        
        print(f"At {time_str} on {date_str}: earthquake of magnitude {magnitude} at {location}")


def printAllLinks(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    for link in soup.find_all("a"):
        print(link.get("href"))


def main():
    print("Earthquakes:")
    fetchAndPrintQuakes("2023-10-01", "2023-10-03", 5.0)
    
    print("\nLinks from example.com:")
    printAllLinks("https://example.com")


if __name__ == "__main__":
    main()
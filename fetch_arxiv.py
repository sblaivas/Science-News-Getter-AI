#Import to hit the API
import requests

import xml.etree.ElementTree as ET

def fetch_arxiv(query, max_results=10):
    #build the request
    url = "https://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{query}",
        "max_results": max_results
    }
    #send the request
    response = requests.get(url, params=params)
    # Check if the request worked
    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
        return None

    #turn the xml into somethinng searchable
    xml_data = response.text
    root = ET.fromstring(xml_data)

    #arXiv's Atom feed uses a namespace, so tags must be prefixed
    ns = {"atom": "http://www.w3.org/2005/Atom"}

    #pull out each paper
    paper_search = []
    # gets every paper, and for each paper
    # 1) find the tag
    # 2) take its text
    # 3) strip the whitespace
    # 4) put the three clean values into a dictionary
    # 5) append it to the list.
    for entry in root.findall("atom:entry", ns):
        title = entry.find("atom:title", ns).text.strip()
        summary = entry.find("atom:summary", ns).text.strip()
        url_link = entry.find("atom:id", ns).text.strip()
        paper_search.append({
            "title": title,
            "summary": summary,
            "url": url_link
        })

    return paper_search

if __name__ == "__main__":
    results = fetch_arxiv("black holes")
    print(results)
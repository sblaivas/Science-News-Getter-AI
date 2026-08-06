#Import to hit the API
import requests

import xml.etree.ElementTree as ET

def fetch_arxiv(query, max_results=10):
    url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{query}",
        "max_results": max_results
    }
    #match the request
    response = requests.get(url, params=params)

    xml_data = response.text

    root = ET.fromstring(xml_data)

    #arXiv's Atom feed uses a namespace, so tags must be prefixed
    ns = {"atom": "http://www.w3.org/2005/Atom"}

    paper_search = []
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
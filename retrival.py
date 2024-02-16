import logging
import sys
import lucene
import os
from org.apache.lucene.store import NIOFSDirectory
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.search import IndexSearcher

def retrieve(storedir, query):
    searchDir = NIOFSDirectory(Paths.get(storedir))
    searcher = IndexSearcher(DirectoryReader.open(searchDir))

    parser = QueryParser('name', StandardAnalyzer())
    parsed_query = parser.parse(query)

    topDocs = searcher.search(parsed_query, 10).scoreDocs
    topkdocs = []
    for hit in topDocs:
        doc = searcher.doc(hit.doc)
        topkdocs.append({
            "score": hit.score,
            "name": doc.get("name"),
            "cuisine": doc.get("cuisine"),
            "ingredients": doc.get("ingredients"),
            "url": doc.get("url")
        })

    return topkdocs

def main():
    lucene.initVM()

    # Take user input for the query
    query = input("Enter your query: ")

    # Retrieve documents matching the query
    results = retrieve('sample_lucene_index/', query)

    # Print the formatted output
    print("Search Results:")
    for idx, result in enumerate(results, start=1):
        print(f"Result {idx}:")
        print(f"Name: {result['name']}")
        print(f"Cuisine: {result['cuisine']}")
        print(f"Ingredients: {result['ingredients']}")
        print(f"URL: {result['url']}")
        print(f"Score: {result['score']}")
        print()

if __name__ == "__main__":
    main()

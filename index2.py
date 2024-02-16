import logging
import sys
import json
import lucene
import os
from org.apache.lucene.store import SimpleFSDirectory
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, IndexOptions
from java.nio.file import Paths

def create_index(json_file, index_dir):
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)

    store = SimpleFSDirectory(Paths.get(index_dir))
    analyzer = StandardAnalyzer()
    config = IndexWriterConfig(analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer = IndexWriter(store, config)

    metaType = FieldType()
    metaType.setStored(True)
    metaType.setTokenized(False)

    contextType = FieldType()
    contextType.setStored(True)
    contextType.setTokenized(True)
    contextType.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

    with open(json_file, 'r') as f:
        data = json.load(f)
        for sample in data:
            doc = Document()
            if isinstance(sample, dict):
                for key, info in sample.items():
                    if isinstance(info, list):
                        info = ', '.join(info)
                    if key in ["name", "ingredients", "cuisine", "cooking_time"]:
                        doc.add(Field(key, info, contextType))
                    else:
                        doc.add(Field(key, info, metaType))
            writer.addDocument(doc)

    writer.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input_json_file index_directory")
        sys.exit(1)

    input_json_file = sys.argv[1]
    index_directory = sys.argv[2]

    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    create_index(input_json_file, index_directory)
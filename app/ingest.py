from pathlib import Path

from llama_index.core import SimpleDirectoryReader, StorageContext, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter

from app.config import config
from app.services.llm import configure_models


"""
Phase 3 Testing:
Since my documents currently are very small, testing with 3 different chunking variables did not result in any differences.
TODO: Experiment
Create three index variants and compare the retrieved context for the same ten questions:
chunk_size=350, chunk_overlap=50
chunk_size=700, chunk_overlap=100
chunk_size=1200, chunk_overlap=150
Record whether smaller chunks increase precision but lose context, and whether larger chunks improve context completeness but introduce irrelevant text.

"""

def build_index() -> None:
    configure_models()
    data_path = Path(config.data_dir)
    storage_path = Path(config.storage_dir)
    storage_path.mkdir(parents=True, exist_ok=True)

    reader = SimpleDirectoryReader(str(data_path), recursive=True)
    documents = reader.load_data()

    for document in documents:
        file_name = document.metadata.get("file_name", "unknown")
        document.metadata["source_type"] = Path(file_name).suffix.lower()
        document.metadata["collection"] = "bootcamp_knowledge"

    splitter = SentenceSplitter(chunk_size=700, chunk_overlap=100)
    nodes = splitter.get_nodes_from_documents(documents)

    if not documents:
        raise RuntimeError("No documents found in the data directory.")

    index = VectorStoreIndex(nodes)
    # index = VectorStoreIndex.from_documents(documents, show_progress=True)
    index.storage_context.persist(persist_dir=str(storage_path))
    print(f"Indexed {len(documents)} document(s) into {storage_path}.")


"""
testing
"""
if __name__ == "__main__":
    build_index()





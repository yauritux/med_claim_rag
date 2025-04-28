import chromadb
from chromadb.utils import embedding_functions

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="./chroma_claims")

# Use the same embedding function as before
embedding_function = embedding_functions.DefaultEmbeddingFunction()

# Get the collection
collection = chroma_client.get_collection(
    name="claims_collection",
    embedding_function=embedding_function
)

def semantic_search(query, n_results=3):
    """Perform semantic search based on query text"""
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results

# Example 1: Search for claims with specific diagnosis
print("\n=== Example 1: Search for claims with back pain ===")
results = semantic_search("back pain")
for i, doc in enumerate(results['documents'][0]):
    print(f"\nResult {i+1}:")
    print(doc)

# Example 2: Search for specific type of claims
print("\n=== Example 2: Search for outpatient claims ===")
results = semantic_search("outpatient clinic OPC")
for i, doc in enumerate(results['documents'][0]):
    print(f"\nResult {i+1}:")
    print(doc)

# Example 3: Search by medical provider
print("\n=== Example 3: Search for claims from specific clinic ===")
results = semantic_search("KLINIK AZYAN")
for i, doc in enumerate(results['documents'][0]):
    print(f"\nResult {i+1}:")
    print(doc)

# Example 4: Search for claims with specific patient characteristics
print("\n=== Example 4: Search for claims with specific patient details ===")
results = semantic_search("male patient age above 40")
for i, doc in enumerate(results['documents'][0]):
    print(f"\nResult {i+1}:")
    print(doc)

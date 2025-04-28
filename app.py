import chromadb
from chromadb.utils import embedding_functions
import json
import re
from datetime import datetime

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="./chroma_claims")

# Use the same embedding function as before
embedding_function = embedding_functions.DefaultEmbeddingFunction()

# Get the collection
collection = chroma_client.get_collection(
    name="claims_collection",
    embedding_function=embedding_function
)

def process_query(query):
    """Process various types of queries about claims data"""
    query = query.lower()
    
    # Check if it's a query about claim status
    if 'status' in query:
        status_pattern = r'status ["\']?([^"\'\.]+)["\']?'
        match = re.search(status_pattern, query.lower())
        if match:
            status = match.group(1).upper()
            results = collection.query(
                query_texts=[f"claims with status {status}"],
                where={"claim_status": status},
                n_results=1000
            )
            return {
                "type": "status_count",
                "status": status,
                "count": len(results['ids'][0])
            }
    
    # Check if it's a query about patient gender
    elif any(word in query for word in ['male', 'female', 'gender']):
        gender = 'M' if 'male' in query else 'F' if 'female' in query else None
        if gender:
            results = collection.query(
                query_texts=[f"{gender.lower()} patients"],
                where={"patient_gender": gender},
                n_results=1000
            )
            return {
                "type": "gender_count",
                "gender": "Male" if gender == 'M' else "Female",
                "count": len(results['ids'][0])
            }
    
    # Check if it's a query about insurance amounts by year
    elif any(word in query for word in ['amount', 'insured', 'summary']):
        year = extract_year_from_query(query)
        if year:
            results = collection.query(
                query_texts=[f"claims from year {year}"],
                n_results=1000
            )
            
            # Process the results
            monthly_stats = {}
            for doc in results['metadatas'][0]:
                date = datetime.strptime(doc['date'], '%Y-%m-%d')
                if date.year == year:
                    month = date.month
                    amount = float(doc['amount_insured'])
                    if month not in monthly_stats:
                        monthly_stats[month] = 0.0
                    monthly_stats[month] += amount
            
            # Format the response
            response = [
                {
                    "year": year,
                    "month": month,
                    "amount_insured": round(amount, 2)
                }
                for month, amount in sorted(monthly_stats.items())
            ]
            return response
    
    # Default to semantic search
    results = collection.query(
        query_texts=[query],
        n_results=5
    )
    
    return {
        "type": "semantic_search",
        "results": [
            {
                "description": doc,
                "metadata": meta
            }
            for doc, meta in zip(results['documents'][0], results['metadatas'][0])
        ]
    }

def extract_year_from_query(query):
    """Extract year from the query text"""
    year_pattern = r'\b(20\d{2})\b'
    match = re.search(year_pattern, query)
    return int(match.group(1)) if match else None

while True:
    print("\n\n--------------------------------------")
    question = input("Ask your question (q to quit): ")
    print("\n\n")
    if question == "q":
        break

    # Process the query and get results
    results = process_query(question)
    
    # Format and display the results based on type
    if isinstance(results, list):  # Monthly statistics
        print(json.dumps(results, indent=2))
    elif results.get('type') == 'status_count':
        print(f"Number of claims with status '{results['status']}': {results['count']}")
    elif results.get('type') == 'gender_count':
        print(f"Number of {results['gender']} patients: {results['count']}")
    elif results.get('type') == 'semantic_search':
        print("Search results:")
        for i, result in enumerate(results['results'], 1):
            print(f"\nResult {i}:")
            print(result['description'])
            print("\nDetails:")
            print(json.dumps(result['metadata'], indent=2))

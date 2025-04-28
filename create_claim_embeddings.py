import pandas as pd
import chromadb
from chromadb.utils import embedding_functions
import os
import json

# Read the Excel file
df = pd.read_excel('Client_24011_Claim_Data.xlsx')

# Convert date to proper format
df['Date'] = pd.to_datetime(df['Date Incurred (YYYYMMDD)'], format='%Y%m%d')

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_claims")

# Delete existing collection if it exists
try:
    chroma_client.delete_collection(name="claims_collection")
except:
    pass

# Use default embedding function (all-MiniLM-L6-v2)
embedding_function = embedding_functions.DefaultEmbeddingFunction()

# Create new collection
collection = chroma_client.create_collection(
    name="claims_collection",
    embedding_function=embedding_function
)

# Process each row
for idx, row in df.iterrows():
    # Create a structured document that's easy to parse
    document = {
        'department_code': str(row['Department Code']),
        'category': str(row['Category']),
        'staff_id': str(row['StaffID']),
        'date': row['Date'].strftime('%Y-%m-%d'),
        'amount_insured': float(row['AmtInsured']),
        'claim_status': str(row['Claim Status']),
        'type_of_claims': str(row['TypeOfClaims']),
        'patient_gender': str(row['PatientGender']),
        'patient_age': int(row['PatientAge']),
        'relationship': str(row['Rel']),
        'medical_provider': str(row['MedicalProviders']),
        'diagnosis': str(row['Diagnosis']),
        'mc_days': str(row['MCDays']),
        'long_term_medical': str(row['Long Term Medical'])
    }
    
    # Create a natural language description for better semantic search
    description = f"Claim from {document['medical_provider']} for a {document['patient_age']} year old {document['patient_gender'].lower()} patient "
    description += f"with diagnosis of {document['diagnosis']}. "
    description += f"Amount insured: {document['amount_insured']}, Status: {document['claim_status']}, "
    description += f"Type: {document['type_of_claims']}, Date: {document['date']}"
    
    # Add the document to the collection
    collection.add(
        documents=[description],
        metadatas=[document],  # Store all fields in metadata for filtering
        ids=[f"claim_{idx}"]
    )

print("Embeddings created and stored successfully!")

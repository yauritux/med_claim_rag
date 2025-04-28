# Medical Claims Analysis System

A Python-based system for analyzing health insurance claims data using vector embeddings and semantic search capabilities. This system allows users to query claims data using natural language and get structured responses.

## Features

- **Semantic Search**: Search through claims using natural language queries
- **Statistical Analysis**: Get monthly summaries of insured amounts
- **Filtering Capabilities**: Filter claims by status, patient demographics, and more
- **Vector Database**: Utilizes ChromaDB for efficient similarity search and data retrieval

## Project Structure

```
med_claim_rag/
├── app.py                      # Main application interface
├── create_claim_embeddings.py  # Script to create vector embeddings
├── query_claims.py            # Example queries implementation
├── Client_24011_Claim_Data.xlsx # Source data file
└── chroma_claims/             # ChromaDB vector database directory
```

## Requirements

- Python 3.11+
- pipenv (Python package manager)

## Installation

1. Clone the repository

2. Install pipenv if you haven't already:
```bash
pip install pipenv
```

3. Install project dependencies:
```bash
pipenv install
```

This will install all required packages including:
- ChromaDB (for vector database)
- Pandas (for data manipulation)
- ONNX Runtime (for embeddings)
- OpenPyXL (for Excel file handling)

## Usage

1. Activate the virtual environment:
```bash
pipenv shell
```

2. Create the vector embeddings:
```bash
python create_claim_embeddings.py
```

3. Run the interactive query interface:
```bash
python app.py
```

Note: Always make sure you're in the pipenv shell before running any commands. You can check if you're in the correct environment by looking for `(med_claim_rag)` in your terminal prompt.

3. Example queries you can try:
   - "Can you give me summary of amount insured within year 2024?"
   - "Give me number of invoices with status 'PENDING'"
   - "Give me number of male patients"
   - "Show me claims from KLINIK AZYAN"

## Data Fields

The system processes the following claim data fields:
- Department Code
- Category
- Staff ID
- Date Incurred
- Amount Insured
- Claim Status
- Type of Claims
- Patient Gender
- Patient Age
- Relationship
- Medical Providers
- Diagnosis
- MC Days
- Long Term Medical

## Query Types

1. **Statistical Queries**
   - Monthly insurance amounts by year
   - Patient demographics statistics
   - Claim status counts

2. **Semantic Search Queries**
   - Search by medical provider
   - Search by diagnosis
   - Search by claim type
   - Search by patient characteristics

## Output Formats

The system provides responses in two main formats:

1. **JSON Format** (for statistical queries):
```json
[
  {
    "year": 2024,
    "month": 1,
    "amount_insured": 5571973.38
  }
]
```

2. **Structured Text** (for semantic searches):
   - Detailed claim information
   - Relevant metadata
   - Search result rankings

## Contributing

Feel free to submit issues and enhancement requests.

## License

This project is just for learning purposes. However, the code can be leveraged for other purposes.

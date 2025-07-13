# Investor Strategy

This file defines the investor strategy for picking stocks.

## Action

Generate a list of 5 stocks based on the following criteria: 
- Companies with a market capitalization over $1 billion.
- P/E ratio below 25.
- Consistent revenue growth over the last 2 years.
- Strong competitive advantage.
- Positive news sentiment in the last month.

Make sure the above checklist is met for each of the stocks, otherwise find another criteria is met.

Use web search to find the necessary financial data and news sentiment. For each stock, provide its current value, analyst's estimated price, and a brief summary explaining why it's a good pick. 
Sort them from good to best.

Output ONLY the JSON array, with no additional text or formatting outside the JSON.

## Output format

Output a JSON array of 5 stock objects. Each object MUST have the following keys and value types:
- `company_name`: string (e.g., "Apple (AAPL)")
- `current_value`: string (e.g., "$150.25")
- `analyst_estimated_price`: string (e.g., "$170.00")
- `summary`: string

Example JSON structure:
```json
[
    {
        "company_name": "Stock A (STA)",
        "current_value": "$150.25",
        "analyst_estimated_price": "$170.00",
        "summary": "Stock A is a leader in its industry with strong growth potential."
    }
]
```
# IBKR Screener Notification System

## Plan
1. Fetch data of stocks with specific criteria.
   1.1. Authenticate with IBRK.
   1.2. Apply selection criteria.
     1.2.1. Up 10%+ on the day
     1.2.2. 5x relative volume
     1.2.3. Price range $5-$20
     1.2.4. Low float, less than 10 million available shares.
     1.2.5. Breaking news
2. Get it through filters to categorize it, if needed.
3. Send a notification to a mobile app (telegram/slack).


## Outcome
* Not all filters are available in IBKR API, ex RV, so we might need to use other APIs or web scraping to get the required data.
* It's complicated and requires manual authentication with IBKR Gateway to inquire iserver data.
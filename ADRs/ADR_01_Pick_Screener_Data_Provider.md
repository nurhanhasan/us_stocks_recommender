# Architecture Decision Record 01 - Pick Screener Data Provider

## Date

2025-12-22

## Status

<!-- What is the status, such as proposed, accepted, rejected, deprecated, superseded, etc.? -->

Proposed: 2025-12-17

Accepted: 2025-12-22


## Context

<!-- What is the issue that we're seeing that is motivating this decision or change? -->

* We need to create a stock scanner based on certain criteria as follows,
  1. Change since last close
  2. Relative volume
  3. Price range
  4. Float
  5. Breaking news


* So, we need to pick a data provider. This provider need to have some characteristics,
1. Free or freemium subscription with reasonable rate-limits.
2. Reliable. Data is in the real-time.
3. Provide required data, preferably all of, at least, basic 5 criteria.
4. Ease of use.


* Potential provider list:
Y is yes, N is now and H is hesitant.

  - IBRK Web APIs
    1. [Y] Free
    2. [Y] Reliable
    3. [N] Enough (No Relative Volume, float or breaking news)
    4. [N] Easy (Non-straightforward authentication. Horrible API documentation)


  - Alpha Vantage
    1. [Y] Free (Free data is delayed)
    2. [N] Reliable (No RV, Breaking newsfeed is weak)
    3. [H] Enough (It has float, Insider Transactions)
    4. [ ] Easy


  - Alpaca
    1. [H] Free
    2. [ ] Reliable
    3. [N] Enough
    4. [ ] Easy


  - finnhub.io
    1. [Y] Free
    2. [H] Reliable (Breaking newsfeed is weak)
    3. [N] Enough (No free float)
    4. [Y] Easy


  - Massive
    1. [Y] Free
    2. [N] Reliable (Stock data and Breaking newsfeed are weak)
    3. [N] Enough
    4. [Y] Easy


  - Marketaux (News API)
    1. [ ] Free
    2. [N] Reliable (Breaking newsfeed is weak)
    3. [ ] Enough
    4. [ ] Easy


  - Benzinga (News API)
    1. [Y] Free
    2. [N] Reliable (Breaking newsfeed is weak)
    3. [N] Enough
    4. [ ] Easy


  - finviz.com
    1. [N] Free
    2. [Y] Reliable
    3. [Y] Enough
    4. [N] Easy (Need to find/create scrapper)


  - TradingView.com
    1. [N] Free (No public official APIs)
    2. [ ] Reliable
    3. [ ] Enough
    4. [ ] Easy


  - Stock Analysis
    1. [N] Free (No official APIs)
    2. [ ] Reliable
    3. [ ] Enough
    4. [ ] Easy


  - twelvedata
    1. [N] Free (Freemium sub is limited)
    2. [H] Reliable (No news, and RV and top-gainers are for premium subs)
    3. [H] Enough
    4. [ ] Easy


  - FMP financialmodelingprep.com
    1. [N] Free (Freemium sub is limited)
    2. [ ] Reliable (News, screeners, ... are for premium subs)
    3. [ ] Enough
    4. [ ] Easy

  - Scrappers
    - finviz
      -  https://github.com/oscar0812/pyfinviz/tree/main
      -  https://github.com/andr3w321/finvizlite
      -  https://github.com/xang1234/Finviz-Scraper/tree/master
      -  https://github.com/eg13/finviz-screener-scraper


## Decision

<!-- What is the change that we're proposing and/or doing? -->

* After trying all the solutions above—for both stock data and news, including IBKR, Alpha Vantage, Alpaca, Finnhub, .... I’ve decided to go with a Finviz scraper as the most complete solution.


## Consequences

<!-- What becomes easier or more difficult to do because of this change? -->

* Using only Finviz data provides all the required filters in one place, making things easier.
* However, this may not be entirely consistent, as Finviz could change its layout, which would break the script.
* Finviz sometimes returns zeros for change and relative volume, which may cause missed opportunities and leave the data outdated.
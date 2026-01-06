# U.S. Stock Recommendation and Execution System

- [U.S. Stock Recommendation and Execution System](#us-stock-recommendation-and-execution-system)
  - [Goal](#goal)
    - [Breakdown steps](#breakdown-steps)
  - [Repo Structure](#repo-structure)
    - [Services](#services)
    - [Supporting directories](#supporting-directories)
  - [Backlog/Possible Ideas](#backlogpossible-ideas)


## Goal
* The ultimate goal is to get recommendations/validation of stocks that meet certain criteria, with forecasted entry and exit points.

### Breakdown steps
- [x] Stock Screener to filter stocks based on criteria.
- [x] Notification system to alert user with potential stocks.
- [ ] Machine Learning model for stock prediction and validation.
- [ ] Integration with brokerage API for trade execution.


## Repo Structure

This project follows a monorepo structure hosting multiple independent services. Each component is designed as an independent service.

### Services
- **IBKR**: Gateway service for Interactive Brokers (IBKR) Client Portal.
- **n8n**: Workflow automation service for scheduling and notifications.
- **pyfinviz**: Core scraping and screening logic service.

### Supporting directories
- **ADRs**: Architecture Decision Records.
- **ideas**: Experimentation area for scripts, prototypes and testing new algorithms, validating approaches, or working with mock data.


## Backlog/Possible Ideas
* Auto trading?!
* Trader Advisor?!
* LLM trained on stock data and different trading patterns, If available. If not, create one?!

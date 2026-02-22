---
## Overview

description: Accessing and analyzing global financial and economic data.
---

# /fetch-external-data Workflow

This workflow handles the ingestion and analysis of external data from APIs like World Bank or yfinance.

**Version:** 1.0.0
**Owner:** IntelligenceSpecialist
**Skill Set:** `fetch-external-data`, `data-analysis`

## Trigger Conditions

This workflow is activated when:
- External financial or economic data is required for analysis.
- Real-time news updates are needed for a project domain.

**Trigger Examples:**
- "Fetch the latest GDP data for G7 countries."
- "Gather recent news about semiconductor supply chains."

// turbo-all

1. **Select Intelligence Source**
   - Financial (yfinance/Finnhub)
   - Economic (World Bank/FRED)
   - News (NewsAPI)

2. **Execute Retrieval**
   - For Financial: Use `FinancialConnector` in the **Financial Intel** tab.
   - For Economic: Use `EconomicConnector` (Integration pending UI update).

3. **Contextual Analysis**
   - correlate the fetched data with internal project datasets if applicable.
   - Generate summary reports using the `viz_manager`.


## Trigger Conditions

- User request
- Manual activation


## Phases

1. Initial Analysis
2. Implementation
3. Verification


## Decision Points

- Is the requirement clear?
- Are the tests passing?


## Example Session

User: Run the workflow
Agent: Initiating workflow steps...

# GraSPP-25S-climatechange
## Research question
- Are public statements about climate change taken into place and providing actual results in their inventory?
  - For GHG conscious countries like EU, they are publishing statements constantly and the nuance could be stronger
  - For developing economies, they are less proactive about including GHG related contents in the statement, but there may be also a possibility for them to include statement when it comes to natural disasters. If they react to these disasters with some kind of climate change words, we could say they are reacting indirectly.

## Thesis statement
- See the relationship between GHG emissions and frequency of GHG related words in the public statements for each country among world's top 10 GHG emitters.
- Target Countries
    - China, United States, India, Russia, Brazil, Indonesia, Japan, Iran, Saudi Arabia, and Canada
    - EU27 is also included as a reference
    - * Analyses are to be held in countries with data availability in public statements
- From 2014-2023, as Paris Agreement was taken in place in 2015.

## Data source and notebooks
- GHG inventory
    - EDGAR - GHG emissions of all world countries 2024 report (https://edgar.jrc.ec.europa.eu/report_2024)
        - Notebook path: notebooks/edgar_ghg_inventory.ipynb
    - Total GHG emissions for India ( https://ourworldindata.org/grapher/total-ghg-emissions.csv?v=1&csvType=full&useColumnShortNames=true)
        - Notebook path: notebooks/India_GHG_data.ipynb

- Public statements (Disaster)
    - EMDAT (Disaster data) (https://public.emdat.be/)
    - Notebook path: notebooks/20250525_Disaster_Data.ipynb

- Climate policy explorer data
    - Data source: https://climate-policy-explorer.shinyapps.io/climate-policies-dashboard/download/
        - Data is used to count the number of implemented policy actions by country and sector
    - Notebook path: notebooks/EffectiveClimatePolicy.ipynb

- Government Press Releases
    - Notebook path: WIP
    - EU (https://ec.europa.eu/commission/presscorner/home/en?dotyp=&keywords=GHG&commissioner=)
    - USA (https://www.whitehouse.gov/news/?s=greenhouse ; https://bidenwhitehouse.archives.gov/briefing-room/)
    - Japan (https://www.kantei.go.jp/jp/103/statement/index.html, prime minister's briefing)
    - China (https://www.gov.cn/toutiao/liebiao/, newsroom of the people's government)
    - India (https://www.pib.gov.in/allRel.aspx#)

## Key GHG related words
- Greenhouse Gas
- GHG
- Net-zero
- Carbon neutral

## Members
- SELVARAJU Akshaya
- Sandra
- Naing
- KOBAYASHI Daiju
- SUGIOKA Arata
- MO Zuanbin

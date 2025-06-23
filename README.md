# GraSPP-25S-climatechange
## Research question
- Are public statements about climate change taken into place and providing actual results in their inventory?
  - For GHG conscious countries like EU, they are publishing statements constantly and the nuance could be stronger
  - For developing economies, they are less proactive about including GHG related contents in the statement, but there may be also a possibility for them to include statement when it comes to natural disasters. If they react to these disasters with some kind of climate change words, we could say they are reacting indirectly.
 
  - https://univtokyo-my.sharepoint.com/:p:/r/personal/1246641011_utac_u-tokyo_ac_jp/_layouts/15/Doc.aspx?sourcedoc=%7BA54FC781-5F69-484E-87A2-4D65426CCBB7%7D&file=Data%20Science%20-%20Climate%20Change.pptx&action=edit&mobileredirect=true&DefaultItemOpen=1 

## Thesis statement
- See the relationship between GHG emissions and frequency of GHG related words in the public statements for each country among world's top 10 GHG emitters.
- Target Countries
    - China, United States, India, Russia, Brazil, Indonesia, Japan, Iran, Saudi Arabia, and Canada
    - EU27 is also included as a reference
    - * Analyses are to be held in countries with data availability in public statements
- From 2014-2023, as Paris Agreement was taken in place in 2015.
- **Main result includes United States and Japan data because of a data availability issue**

## Data source and notebooks
- GHG inventory - **Used for the main and extra analysis**
    - EDGAR - GHG emissions of all world countries 2024 report (https://edgar.jrc.ec.europa.eu/report_2024)
        - Notebook path: notebooks/edgar_ghg_inventory.ipynb
    - Total GHG emissions for India ( https://ourworldindata.org/grapher/total-ghg-emissions.csv?v=1&csvType=full&useColumnShortNames=true)
        - Notebook path: notebooks/India_GHG_data.ipynb

- Manifesto data - **Used for the main analysis**
    - https://manifesto-project.wzb.eu/datasets
 
- Public statements (Disaster) - **Used for the extra analysis**
    - EMDAT (Disaster data) (https://public.emdat.be/)
    - Notebook path: notebooks/20250525_Disaster_Data.ipynb

- NDC data
    - US
        - data/raw/United States 2035 NDC.pdf
        - data/raw/United States NDC April 21 2021 Final.pdf
    - EU
        - data/raw/ES-2023-10-17 EU submission NDC update.pdf
    - Notebook path: notebooks/ndc_data_word_count.ipynb

- Climate policy explorer data
    - Data source: https://climate-policy-explorer.shinyapps.io/climate-policies-dashboard/download/
        - Data is used to count the number of implemented policy actions by country and sector
    - Notebook path: notebooks/EffectiveClimatePolicy.ipynb

- Government Press Releases
    - Sample notebook path: notebooks/selenium_sample.ipynb -> To be discussed on Thursday
    - EU (https://ec.europa.eu/commission/presscorner/home/en?dotyp=&keywords=GHG&commissioner=)
    - USA (https://www.whitehouse.gov/news/?s=greenhouse ; https://bidenwhitehouse.archives.gov/briefing-room/)
    - Japan (https://www.kantei.go.jp/jp/103/statement/index.html, prime minister's briefing)
    - China (https://www.gov.cn/toutiao/liebiao/, newsroom of the people's government)
    - India (https://www.pib.gov.in/allRel.aspx#)

## Analysis and notebooks
- Scraping and word counting
    - Manifesto data: notebooks/manifesto_data_retrieval.ipynb **Used for the main result**
    - NDC data: notebooks/ndc_data_word_count.ipynb - US and EU, one year only
- Main analysis (GHG emission vs word counts for US and Japan)
    - notebooks/20250622_Regression_LLM_Scrape.ipynb
    - (Old analysis including China) notebooks/20250614_Regression.ipynb
- Extra analysis (GHG emission vs number of disasters)
    - notebooks/20250525_Disaster_Data.ipynb 

## Key GHG related words
- Greenhouse Gas
- GHG
- Net-zero
- Carbon neutral

## Members and Contributions 
- SELVARAJU Akshaya (powerpoint and GHG data analysis)
- Sandra (NDC text analysis)
- Naing (Disaster data analysis and regression)
- KOBAYASHI Daiju
- SUGIOKA Arata (GHG and text data analysis)
- MO Zuanbin (China data analysis)

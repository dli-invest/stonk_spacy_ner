import spacy
import pandas as pd
from utils import DIVIDEND_LABEL, IGNORE_LABEL, stop_terms, cse_pattern, tsx_pattern

# rewrite this to load based on patternl files.
# https://spacy.io/usage/rule-based-matching#entityruler-files
def init_nlp(exchange_data_path: str = "https://raw.githubusercontent.com/dli-invest/fin_news_nlp/main/nlp_articles/core/data/exchanges.tsv", indicies_data_path: str = "https://raw.githubusercontent.com/dli-invest/fin_news_nlp/main/nlp_articles/core/data/indicies.tsv"):
    SPLIT_COMPANY_INTO_WORDS = False
    BEAR_MARKET_ADJUSTMENT = True
    nlp = spacy.load("en_core_web_sm")
    ticker_df = pd.read_csv(
                "https://raw.githubusercontent.com/dli-invest/eod_tickers/main/data/us.csv"
            )
    ticker_df = ticker_df.dropna(subset=['Code', 'Name'])
    ticker_df = ticker_df[~ticker_df.Name.str.contains("Wall Street", na=False)]
    # remove exact matches
    ticker_df = ticker_df[~ticker_df['Name'].isin(['Wall Street'])]
    # remove bad symbols
    ticker_df = ticker_df[~ticker_df['Code'].isin(['ET'])]
    symbols = ticker_df.Code.tolist()
    companies = ticker_df.Name.tolist()

    ex_df = pd.read_csv(exchange_data_path, sep="\t")

    ind_df = pd.read_csv(indicies_data_path, sep="\t")
    indexes = ind_df.IndexName.tolist()
    index_symbols = ind_df.IndexSymbol.tolist()

    exchanges = ex_df.ISOMIC.tolist()+ ex_df["Google Prefix"].tolist()
    descriptions = ex_df.Description.tolist()

    # split stops into other arrays
    stops = stop_terms

    terms_to_add = ["b2b", "venture", "growth"]
    # want my cool stuff here
    # nlp = spacy.blank("en")
    ruler = nlp.add_pipe("entity_ruler")
    patterns = []

    first_words_added = []
    endings = [".TO", ".V", ".CN", ".HK"]
    #List of Entities and Patterns
    for symbol in symbols:
        if len(symbol) > 1:
            patterns.append({"label": "STOCK", "pattern": symbol})
            patterns.append({"label": "STOCK", "pattern": f"${symbol}"})
            for ending in endings:
                patterns.append({"label": "STOCK", "pattern": symbol+f".{ending}"})



    for company in companies:
        if company not in stops and len(company) > 1:
            patterns.append({"label": "COMPANY", "pattern": company})
            if SPLIT_COMPANY_INTO_WORDS:
                words = company.split()
                if len(words) >= 1:
                    new = " ".join(words)
                    if new not in first_words_added and new.isnumeric() == False:
                        patterns.append({"label": "COMPANY", "pattern": new})
                    # add first word to list as well
                    first_word = words[0]
                    # ignore the numbers
                    if (
                        first_word.isnumeric() == False
                        and first_word.lower() not in stops
                        and first_word not in first_words_added
                    ):
                        first_words_added.append(first_word)
                        patterns.append({"label": "COMPANY", "pattern": words[0]})

    for index in indexes:
        patterns.append({"label": "INDEX", "pattern": index})
        versions = []
        words = index.split()
        caps = []
        for word in words:
            word = word.lower().capitalize()
            caps.append(word)
        versions.append(" ".join(caps))
        versions.append(words[0])
        versions.append(caps[0])
        versions.append(" ".join(caps[:2]))
        versions.append(" ".join(words[:2]))
        for version in versions:
            if version != "NYSE":
                patterns.append({"label": "INDEX", "pattern": version})

    for symbol in index_symbols:
        patterns.append({"label": "INDEX", "pattern": symbol})    


    for d in descriptions:
        patterns.append({"label": "STOCK_EXCHANGE", "pattern": d})
    for e in exchanges:
        patterns.append({"label": "STOCK_EXCHANGE", "pattern": e})

    # could use holmes for this kind of stuff instead, not at the moment tho.
    for crit in ["acquisition", "buyout", "takeover"]:
        pass
         # patterns.append({"label": "CRITICAL", "pattern": crit})

    for term in ["COP", "BIDEN", "recession", "depression", "FED", "Quarter", "Earnings"]:
        patterns.append({"label": "THINGS", "pattern": term})

    for country in ["USA", "US", "United States", "U.S.", "U.S.A.", "CANADA", "CHINA"]:
        patterns.append({"label": "COUNTRY", "pattern": country})
    # might be of interest 

    for ec in ["ENVIRONMENT", "INTEREST", "RATES", "TAXPAYERS", "TRUMP", "SUPPLY"]:
        patterns.append({"label": "MAYBE", "pattern": ec})
    
    DIVIDEND_PATTERNS = [
        {
            "label": DIVIDEND_LABEL,
            "pattern": [{"LOWER": "special"}, {"LOWER": "dividend"}]
        },
        {
            "label": DIVIDEND_LABEL,
            "pattern": [{"LOWER": "cash"}, {"LOWER": "dividend"}]
        },
        {
            "label": DIVIDEND_LABEL,
            "pattern":  [{"LOWER": "regular"}, {"LOWER": "dividend"}]
        },
        {
            "label": DIVIDEND_LABEL,
            "pattern": [{"LOWER": "annual"}, {"LOWER": "dividend"}]
        }
    ]
    for pattern in DIVIDEND_PATTERNS:
        patterns.append(pattern)

    FINANCIAL_REPORTS_LABEL = "EARNINGS"
    # financial_reports patterns
    financial_reports = [
        # takes care of first quarter to fourth quarter
        # annual earnings
        {
            "label": FINANCIAL_REPORTS_LABEL,
            "pattern":  [{"LEMMA": {"IN": ["first", "second", "third", "fourth"]}}, {"LOWER": "quarter"}],
        }, 
        {
            "label": FINANCIAL_REPORTS_LABEL,
            "pattern":  [{"LOWER": "annual"}, {"LOWER": {"IN": {"earning", "earnings", "report"}}}],
        },
        {
            "label": FINANCIAL_REPORTS_LABEL,
            "pattern":  [{"LOWER": "quarterly"}, {"LOWER": {"IN": {"earning", "earnings", "report"}}}],
        }
    ]

    # remove terms next time

    patterns.append({
        "label": "COMPANY",
        "pattern": cse_pattern,
    })
    patterns.append({
        "label": "COMPANY",
        "pattern": tsx_pattern,
    })

    # ignore investor conference
    # can be useful in bull markets, but not in bear markets
    if BEAR_MARKET_ADJUSTMENT:
        patterns.append({
            "label": IGNORE_LABEL,
            "pattern": [{"LOWER": "investor"}, {"LOWER": "conference"}]
        })

    # search for MOU
    patterns.append({
        "label": "NEWS",
        "pattern": [{"LOWER": "mou"}]
    })
    ruler.add_patterns(patterns)
    return nlp


# my thoughts being, lets only do us tickers for now, us stonks are more common
# cad stocks can come later if its important
new_nlp = init_nlp()
new_nlp.to_disk("output/stonk_pipeline")
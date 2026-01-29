"""
Stock universe definitions with real ticker lists.
"""

# S&P 500 companies (top 100 most liquid for practical scanning)
SP500_TICKERS = [
    # Technology
    "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "NVDA", "META", "TSLA", "AVGO", "ORCL",
    "ADBE", "CRM", "CSCO", "ACN", "AMD", "INTC", "IBM", "INTU", "NOW", "TXN",
    "QCOM", "AMAT", "MU", "ADI", "LRCX", "KLAC", "SNPS", "CDNS", "PANW", "FTNT",
    "PLTR", "CRWD", "SNOW", "DDOG", "ZS", "NET", "OKTA", "MNDY", "S", "BILL",

    # Financial Services
    "JPM", "V", "MA", "BAC", "WFC", "MS", "GS", "BLK", "SPGI", "C",
    "SCHW", "AXP", "PNC", "USB", "TFC", "COF", "BK", "STT", "AMP", "ALL",
    "PGR", "CB", "TRV", "AFL", "MET", "PRU", "AIG", "HIG", "CINF", "L",

    # Healthcare
    "UNH", "JNJ", "LLY", "ABBV", "MRK", "TMO", "ABT", "DHR", "PFE", "BMY",
    "AMGN", "GILD", "CVS", "CI", "ELV", "VRTX", "REGN", "HCA", "ISRG", "ZTS",
    "MCK", "COR", "BSX", "MDT", "SYK", "BDX", "EW", "IDXX", "IQV", "RMD",

    # Consumer Discretionary
    "AMZN", "TSLA", "HD", "MCD", "NKE", "SBUX", "LOW", "TJX", "BKNG", "ABNB",
    "CMG", "MAR", "YUM", "ROST", "ORLY", "AZO", "DHI", "LEN", "DG", "DLTR",
    "ULTA", "BBY", "POOL", "TPR", "RL", "GRMN", "HLT", "MGM", "WYNN", "LVS",

    # Communication Services
    "GOOGL", "META", "NFLX", "DIS", "CMCSA", "T", "VZ", "TMUS", "CHTR", "EA",
    "TTWO", "MTCH", "PARA", "WBD", "FOXA", "FOX", "OMC", "IPG", "NWSA", "NWS",

    # Industrials
    "CAT", "BA", "GE", "RTX", "HON", "UPS", "LMT", "DE", "UNP", "ADP",
    "MMM", "GD", "NOC", "ETN", "ITW", "CSX", "WM", "EMR", "NSC", "FDX",
    "PCAR", "JCI", "TT", "CMI", "PH", "ROK", "CARR", "OTIS", "IR", "FAST",

    # Consumer Staples
    "PG", "KO", "PEP", "COST", "WMT", "PM", "MO", "MDLZ", "CL", "KMB",
    "GIS", "HSY", "K", "CPB", "CAG", "SJM", "MKC", "TSN", "HRL", "CHD",
    "CLX", "STZ", "TAP", "BF.B", "KDP", "MNST", "KR", "SYY", "DG", "DLTR",

    # Energy
    "XOM", "CVX", "COP", "SLB", "EOG", "MPC", "PSX", "VLO", "OXY", "HAL",
    "BKR", "WMB", "KMI", "OKE", "DVN", "FANG", "HES", "MRO", "APA", "CTRA",

    # Real Estate
    "AMT", "PLD", "CCI", "EQIX", "PSA", "SPG", "DLR", "WELL", "AVB", "EQR",
    "VICI", "VTR", "O", "SBAC", "WY", "ARE", "INVH", "MAA", "ESS", "UDR",

    # Materials
    "LIN", "APD", "SHW", "ECL", "DD", "NEM", "FCX", "NUE", "DOW", "ALB",
    "VMC", "MLM", "CTVA", "PPG", "IFF", "EMN", "CE", "FMC", "CF", "MOS",

    # Utilities
    "NEE", "DUK", "SO", "D", "AEP", "EXC", "SRE", "XEL", "WEC", "ES",
    "PEG", "ED", "EIX", "AWK", "FE", "ETR", "PPL", "DTE", "AEE", "CMS",
]

# Technology sector (comprehensive)
TECH_TICKERS = [
    # Mega-cap Tech
    "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "NVDA", "META", "TSLA", "AVGO", "ORCL",

    # Software
    "CRM", "ADBE", "NOW", "INTU", "PANW", "WDAY", "SNOW", "DDOG", "ZS", "CRWD",
    "TEAM", "HUBS", "SHOP", "SQ", "PYPL", "COIN", "RBLX", "U", "DOCN", "NET",
    "GTLB", "MDB", "ESTC", "OKTA", "ZI", "MNDY", "BILL", "S", "PCTY", "VEEV",

    # Semiconductors
    "NVDA", "AMD", "INTC", "QCOM", "AVGO", "TXN", "ADI", "AMAT", "MU", "LRCX",
    "KLAC", "SNPS", "CDNS", "MCHP", "NXPI", "MRVL", "ON", "MPWR", "SWKS", "QRVO",

    # Hardware & Equipment
    "AAPL", "DELL", "HPQ", "NTAP", "PSTG", "WDC", "STX", "SMCI", "ARW", "KEYS",

    # Internet & E-commerce
    "AMZN", "GOOGL", "META", "NFLX", "UBER", "ABNB", "DASH", "LYFT", "PINS", "SNAP",
    "ETSY", "EBAY", "BKNG", "EXPE", "TRIP", "CHWY", "W", "RH", "CVNA", "CPNG",

    # Cybersecurity
    "PANW", "CRWD", "ZS", "FTNT", "NET", "OKTA", "S", "CYBR", "TENB", "VRNS",
]

# Energy sector
ENERGY_TICKERS = [
    # Integrated Oil & Gas
    "XOM", "CVX", "COP", "TTE", "SHEL", "BP", "EQNR", "E", "IMO", "SU",

    # Exploration & Production
    "EOG", "OXY", "DVN", "FANG", "HES", "MRO", "APA", "CTRA", "OVV", "PR",
    "MTDR", "AR", "SM", "MGY", "RRC", "NOG", "CPE", "CRC", "ESTE", "VTLE",

    # Oil Services
    "SLB", "HAL", "BKR", "FTI", "NOV", "HP", "CHX", "LBRT", "PTEN", "NEX",

    # Refining & Marketing
    "MPC", "PSX", "VLO", "HFC", "DK", "CIVI", "PBF", "DINO", "CVI", "PARR",

    # Midstream
    "WMB", "KMI", "OKE", "EPD", "ET", "MPLX", "PAA", "WES", "HESM", "ENLC",

    # Renewables
    "NEE", "AES", "VST", "CWEN", "NOVA", "RUN", "ENPH", "SEDG", "FSLR", "SPWR",
]

# Healthcare sector
HEALTHCARE_TICKERS = [
    # Pharma - Large Cap
    "UNH", "JNJ", "LLY", "ABBV", "MRK", "PFE", "TMO", "ABT", "DHR", "BMY",
    "AMGN", "GILD", "VRTX", "REGN", "BIIB", "MRNA", "BNTX", "ALNY", "SGEN", "TECH",

    # Biotech
    "AMGN", "GILD", "VRTX", "REGN", "BIIB", "MRNA", "ALNY", "SGEN", "BMRN", "INCY",
    "EXEL", "NBIX", "IONS", "SRPT", "UTHR", "RARE", "FOLD", "BGNE", "ARVN", "KRYS",

    # Medical Devices
    "ISRG", "ABT", "SYK", "BSX", "MDT", "BDX", "EW", "ZBH", "BAX", "DXCM",
    "HOLX", "ALGN", "PODD", "TNDM", "NVCR", "NVST", "OMCL", "GMED", "STAA", "IRTC",

    # Healthcare Services
    "UNH", "CVS", "CI", "ELV", "HCA", "CNC", "ANTM", "HUM", "MOH", "THC",

    # Diagnostics & Research
    "TMO", "DHR", "IQV", "IDXX", "A", "DGX", "QGEN", "BIO", "TECH", "MEDP",
]

# Financial sector
FINANCE_TICKERS = [
    # Banks - Large Cap
    "JPM", "BAC", "WFC", "C", "GS", "MS", "USB", "PNC", "TFC", "SCHW",

    # Regional Banks
    "KEY", "CFG", "FITB", "HBAN", "RF", "MTB", "CMA", "ZION", "WTFC", "EWBC",
    "FHN", "SNV", "ONB", "UBSI", "BANR", "FULT", "WAFD", "CADE", "FFIN", "SFNC",

    # Investment Banks & Brokers
    "GS", "MS", "SCHW", "IBKR", "MKTX", "SF", "LAZ", "PJT", "EVR", "MC",

    # Payment Processors
    "V", "MA", "PYPL", "SQ", "FISV", "FIS", "AXP", "DFS", "COF", "ALLY",

    # Asset Management
    "BLK", "BX", "KKR", "APO", "ARES", "TROW", "BEN", "IVZ", "NTRS", "AMG",

    # Insurance
    "PGR", "CB", "TRV", "ALL", "AFL", "MET", "PRU", "AIG", "HIG", "WRB",
]

# Consumer sector (discretionary + staples)
CONSUMER_TICKERS = [
    # Retail
    "AMZN", "WMT", "COST", "HD", "TGT", "LOW", "TJX", "ROST", "DG", "DLTR",
    "BBY", "FIVE", "OLLI", "BIG", "PSMT", "LE", "UPBD", "DKS", "HIBB", "ANF",

    # Restaurants & Food Service
    "MCD", "SBUX", "CMG", "YUM", "QSR", "DRI", "DPZ", "TXRH", "WEN", "JACK",
    "PZZA", "BLMN", "EAT", "CAKE", "CHUY", "FWRG", "BJRI", "DENN", "WING", "CBRL",

    # Automotive
    "TSLA", "F", "GM", "RIVN", "LCID", "STLA", "HMC", "TM", "RACE", "PAG",

    # Consumer Packaged Goods
    "PG", "KO", "PEP", "PM", "MO", "CL", "KMB", "GIS", "K", "CPB",

    # Apparel & Footwear
    "NKE", "LULU", "TJX", "ROST", "ULTA", "RL", "PVH", "UAA", "CROX", "DECK",
]

# Defensive stocks (utilities, consumer staples, healthcare)
DEFENSIVE_TICKERS = [
    # Utilities
    "NEE", "DUK", "SO", "D", "AEP", "EXC", "SRE", "XEL", "WEC", "ES",
    "PEG", "ED", "EIX", "AWK", "FE", "ETR", "PPL", "DTE", "AEE", "CMS",

    # Consumer Staples
    "PG", "KO", "PEP", "COST", "WMT", "PM", "MO", "MDLZ", "CL", "KMB",
    "GIS", "K", "CPB", "CAG", "SJM", "MKC", "CHD", "CLX", "KR", "SYY",

    # Healthcare
    "JNJ", "UNH", "ABBV", "MRK", "PFE", "LLY", "TMO", "ABT", "DHR", "CVS",
]

# Growth stocks (high-growth tech and consumer)
GROWTH_TICKERS = [
    "NVDA", "META", "GOOGL", "AMZN", "TSLA", "AVGO", "AMD", "SNOW", "CRWD", "PANW",
    "DDOG", "ZS", "NET", "PLTR", "SHOP", "SQ", "COIN", "RBLX", "ABNB", "UBER",
    "DASH", "RIVN", "LCID", "ENPH", "SEDG", "FSLR", "PLUG", "BE", "CHPT", "BLNK",
    "MELI", "SE", "NU", "CPNG", "GRAB", "BABA", "JD", "PDD", "NIO", "XPEV",
]

# Map universe names to ticker lists
UNIVERSE_MAP = {
    "sp500": SP500_TICKERS,
    "tech": TECH_TICKERS,
    "energy": ENERGY_TICKERS,
    "healthcare": HEALTHCARE_TICKERS,
    "finance": FINANCE_TICKERS,
    "consumer": CONSUMER_TICKERS,
    "defensive": DEFENSIVE_TICKERS,
    "growth": GROWTH_TICKERS,
}

def get_universe_tickers(universe_name: str) -> list:
    """
    Get ticker list for a named universe.

    Args:
        universe_name: Name of the universe (sp500, tech, energy, etc.)

    Returns:
        List of ticker symbols
    """
    return UNIVERSE_MAP.get(universe_name.lower(), SP500_TICKERS[:10])  # Default to top 10 S&P 500

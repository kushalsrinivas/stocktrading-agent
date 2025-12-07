"""
Fundamental analysis helper for NSE/BSE tickers using yfinance data and
Moneycontrol headlines. Produces a Markdown report.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple
from urllib.parse import urlparse, urljoin

import pandas as pd
import requests
import yfinance as yf
from bs4 import BeautifulSoup

DEFAULT_EXCHANGE = "NSE"
EXCHANGE_SUFFIX = {"NSE": ".NS", "BSE": ".BO"}
MONEYCONTROL_SUGGEST_URL = (
    "https://www.moneycontrol.com/mccode/common/autosuggesion.php"
)
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0 Safari/537.36"
    )
}


def append_exchange(symbol: str, exchange: str) -> str:
    suffix = EXCHANGE_SUFFIX.get(exchange.upper(), "")
    return symbol if symbol.endswith(suffix) else f"{symbol}{suffix}"


def fmt_currency(value: Optional[float], currency: str = "INR") -> str:
    if value is None or pd.isna(value):
        return "N/A"
    abs_val = abs(value)
    unit = ""
    divisor = 1
    if abs_val >= 1_000_000_000_000:
        unit, divisor = "T", 1_000_000_000_000
    elif abs_val >= 1_000_000_000:
        unit, divisor = "B", 1_000_000_000
    elif abs_val >= 1_000_000:
        unit, divisor = "M", 1_000_000
    formatted = f"{value / divisor:,.2f}"
    prefix = "₹" if currency.upper() in {"INR", "IN"} else f"{currency} "
    return f"{prefix}{formatted}{unit}"


def fmt_number(value: Optional[float]) -> str:
    if value is None or pd.isna(value):
        return "N/A"
    return f"{value:,.2f}"


def fmt_pct(value: Optional[float]) -> str:
    if value is None or pd.isna(value):
        return "N/A"
    return f"{value*100:.2f}%"


def safe_div(numerator: Optional[float], denominator: Optional[float]) -> Optional[float]:
    if numerator is None or denominator in (None, 0):
        return None
    return numerator / denominator


def pick_row(df: pd.DataFrame, candidates: Iterable[str]) -> Optional[pd.Series]:
    if df is None or df.empty:
        return None
    lowered = {str(idx).lower(): idx for idx in df.index}
    for name in candidates:
        target = name.lower()
        for key, original in lowered.items():
            if target == key or target.replace(" ", "") == key.replace(" ", ""):
                return df.loc[original]
    return None


def extract_series(df: pd.DataFrame, candidates: Iterable[str]) -> pd.Series:
    row = pick_row(df, candidates)
    if row is None:
        return pd.Series(dtype=float)
    series = pd.to_numeric(row, errors="coerce").dropna()
    try:
        return series.sort_index()
    except Exception:
        return series


def latest_value(df: pd.DataFrame, candidates: Iterable[str]) -> Optional[float]:
    series = extract_series(df, candidates)
    if series.empty:
        return None
    return series.iloc[-1]


def cagr_from_series(series: pd.Series) -> Optional[float]:
    if series is None or series.empty or len(series) < 2:
        return None
    try:
        start = series.iloc[0]
        end = series.iloc[-1]
        periods = len(series) - 1
        if start <= 0 or periods <= 0:
            return None
        return (end / start) ** (1 / periods) - 1
    except Exception:
        return None


def fetch_moneycontrol_news(
    query: str, limit: int = 8
) -> List[Dict[str, str]]:
    params = {
        "classic": "true",
        "query": query,
        "type": "1",
        "format": "json",
        "count": 5,
    }
    try:
        search_resp = requests.get(
            MONEYCONTROL_SUGGEST_URL, params=params, headers=HEADERS, timeout=10
        )
        search_resp.raise_for_status()
    except Exception:
        return []

    try:
        suggestions = search_resp.json()
    except Exception:
        try:
            suggestions = json.loads(search_resp.text)
        except Exception:
            return []

    if not isinstance(suggestions, list) or not suggestions:
        return []

    first = suggestions[0]
    link = first.get("link_src") or first.get("url") or first.get("link")
    if not link:
        return []

    parsed = urlparse(link)
    slug_parts = [part for part in parsed.path.split("/") if part]
    if len(slug_parts) < 2:
        return []
    slug = slug_parts[-2]
    code = slug_parts[-1]
    news_url = f"https://www.moneycontrol.com/company-article/{slug}/news/{code}"

    try:
        news_resp = requests.get(news_url, headers=HEADERS, timeout=10)
        news_resp.raise_for_status()
    except Exception:
        return []

    soup = BeautifulSoup(news_resp.text, "html.parser")
    headlines: List[Dict[str, str]] = []
    for anchor in soup.find_all("a", href=True):
        text = anchor.get_text(strip=True)
        href = anchor["href"]
        if not text or len(text) < 30:
            continue
        if "news" not in href:
            continue
        full_url = href if href.startswith("http") else urljoin(news_url, href)
        headlines.append({"title": text, "url": full_url})
        if len(headlines) >= limit:
            break
    return headlines


def build_report(
    symbol: str,
    exchange: str,
    info: Dict,
    fast_info: Dict,
    income_df: pd.DataFrame,
    quarterly_income_df: pd.DataFrame,
    balance_df: pd.DataFrame,
    cashflow_df: pd.DataFrame,
    history: pd.DataFrame,
    analyst_targets: Optional[object],
    news_items: List[Dict[str, str]],
) -> str:
    currency = fast_info.get("currency", "INR") if fast_info else "INR"
    market_cap = info.get("marketCap")
    enterprise_value = info.get("enterpriseValue")
    ebitda = info.get("ebitda") or latest_value(income_df, ["EBITDA"])
    revenue_series = extract_series(income_df, ["Total Revenue", "TotalRevenue"])
    revenue = revenue_series.iloc[-1] if not revenue_series.empty else None
    gross_profit = latest_value(income_df, ["Gross Profit", "GrossProfit"])
    operating_income = latest_value(
        income_df, ["Operating Income", "OperatingIncome"]
    )
    net_income = latest_value(income_df, ["Net Income", "NetIncome"])
    cash = latest_value(balance_df, ["Cash", "Cash And Cash Equivalents"])
    total_assets = latest_value(balance_df, ["Total Assets", "TotalAssets"])
    total_liab = latest_value(
        balance_df, ["Total Liab", "Total Liabilities", "TotalLiab"]
    )
    total_equity = latest_value(
        balance_df, ["Total Stockholder Equity", "TotalEquity"]
    )
    current_assets = latest_value(
        balance_df, ["Total Current Assets", "Current Assets"]
    )
    current_liab = latest_value(
        balance_df, ["Total Current Liabilities", "Current Liabilities"]
    )
    total_debt = latest_value(
        balance_df, ["Total Debt", "Short Long Term Debt"]
    )
    free_cash_flow = latest_value(
        cashflow_df, ["Free Cash Flow", "FreeCashFlow"]
    )
    operating_cf = latest_value(
        cashflow_df,
        ["Total Cash From Operating Activities", "Operating Cash Flow"],
    )
    revenue_cagr = cagr_from_series(revenue_series.tail(4))

    # Margins
    gross_margin = safe_div(gross_profit, revenue)
    operating_margin = safe_div(operating_income, revenue)
    net_margin = safe_div(net_income, revenue)

    # Balance sheet metrics
    roe = safe_div(net_income, total_equity)
    roa = safe_div(net_income, total_assets)
    debt_to_equity = safe_div(total_debt, total_equity)
    current_ratio = safe_div(current_assets, current_liab)
    fcf_yield = safe_div(free_cash_flow, market_cap)

    # Valuation
    trailing_pe = info.get("trailingPE")
    forward_pe = info.get("forwardPE")
    pb = info.get("priceToBook")
    ev_to_ebitda = safe_div(enterprise_value, ebitda)

    # Price context
    last_price = fast_info.get("lastPrice") if fast_info else None
    year_high = fast_info.get("yearHigh") if fast_info else None
    year_low = fast_info.get("yearLow") if fast_info else None

    md: List[str] = []
    md.append(f"# Fundamental Analysis: {symbol} ({exchange.upper()})")
    if info.get("longName"):
        md.append(f"**Company:** {info.get('longName')}")
    if info.get("sector") or info.get("industry"):
        md.append(
            f"**Sector/Industry:** {info.get('sector', 'N/A')} / "
            f"{info.get('industry', 'N/A')}"
        )
    md.append("")

    md.append("## Snapshot")
    md.append(
        f"- Market Cap: {fmt_currency(market_cap, currency)}  "
        f"- Enterprise Value: {fmt_currency(enterprise_value, currency)}"
    )
    md.append(
        f"- Price: {fmt_currency(last_price, currency)}  "
        f"- 52W High/Low: {fmt_currency(year_high, currency)} / "
        f"{fmt_currency(year_low, currency)}"
    )
    md.append(
        f"- Beta: {fmt_number(info.get('beta'))}  "
        f"- Dividend Yield: {fmt_pct(info.get('dividendYield'))}"
    )
    md.append("")

    md.append("## Valuation")
    md.append(
        f"- Trailing P/E: {fmt_number(trailing_pe)}; "
        f"Forward P/E: {fmt_number(forward_pe)}"
    )
    md.append(f"- P/B: {fmt_number(pb)}; EV/EBITDA: {fmt_number(ev_to_ebitda)}")
    md.append(f"- FCF Yield: {fmt_pct(fcf_yield)}")
    md.append("")

    md.append("## Profitability & Margins")
    md.append(f"- Revenue (latest): {fmt_currency(revenue, currency)}")
    md.append(f"- Gross Margin: {fmt_pct(gross_margin)}")
    md.append(f"- Operating Margin: {fmt_pct(operating_margin)}")
    md.append(f"- Net Margin: {fmt_pct(net_margin)}")
    md.append(
        f"- ROE: {fmt_pct(roe)}; ROA: {fmt_pct(roa)}; "
        f"Revenue CAGR (≈3-4y): {fmt_pct(revenue_cagr)}"
    )
    md.append("")

    md.append("## Balance Sheet & Liquidity")
    md.append(
        f"- Total Assets: {fmt_currency(total_assets, currency)}; "
        f"Total Liabilities: {fmt_currency(total_liab, currency)}; "
        f"Total Equity: {fmt_currency(total_equity, currency)}"
    )
    md.append(
        f"- Total Debt: {fmt_currency(total_debt, currency)}; "
        f"Debt/Equity: {fmt_number(debt_to_equity)}"
    )
    md.append(f"- Current Ratio: {fmt_number(current_ratio)}")
    md.append("")

    md.append("## Cash Flow")
    md.append(
        f"- Operating Cash Flow: {fmt_currency(operating_cf, currency)}; "
        f"Free Cash Flow: {fmt_currency(free_cash_flow, currency)}"
    )
    md.append("")

    analyst_df: Optional[pd.DataFrame] = None
    if analyst_targets is not None:
        if isinstance(analyst_targets, pd.DataFrame):
            analyst_df = analyst_targets
        elif isinstance(analyst_targets, dict):
            analyst_df = pd.DataFrame([analyst_targets])
    if analyst_df is not None and not analyst_df.empty:
        row = analyst_df.iloc[0].to_dict()
        md.append("## Analyst Targets (yfinance)")
        md.append(
            f"- Mean: {fmt_currency(row.get('targetMean'), currency)}; "
            f"Median: {fmt_currency(row.get('targetMedian'), currency)}; "
            f"High/Low: {fmt_currency(row.get('targetHigh'), currency)} / "
            f"{fmt_currency(row.get('targetLow'), currency)}"
        )
        if row.get("lastUpdated"):
            md.append(f"- Last Updated: {row.get('lastUpdated')}")
        md.append("")

    if not news_items:
        md.append("## Moneycontrol News")
        md.append("- No recent headlines found or request blocked.")
    else:
        md.append("## Moneycontrol News")
        for item in news_items:
            md.append(f"- [{item['title']}]({item['url']})")

    md.append("")
    md.append(
        f"_Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M %Z')}_"
    )
    return "\n".join(md)


def load_ticker(symbol: str, exchange: str) -> Tuple[str, yf.Ticker]:
    full_symbol = append_exchange(symbol, exchange)
    return full_symbol, yf.Ticker(full_symbol)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a Markdown fundamental analysis report."
    )
    parser.add_argument(
        "--symbol",
        required=True,
        help="Stock symbol without suffix (e.g., RELIANCE, TCS).",
    )
    parser.add_argument(
        "--exchange",
        default=DEFAULT_EXCHANGE,
        choices=list(EXCHANGE_SUFFIX.keys()),
        help="Exchange to query (adds the correct yfinance suffix).",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Optional output path for the Markdown file.",
    )
    parser.add_argument(
        "--max-news",
        type=int,
        default=8,
        help="Maximum Moneycontrol headlines to include.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    full_symbol, ticker = load_ticker(args.symbol, args.exchange)

    info = ticker.get_info() or {}
    fast_info = getattr(ticker, "fast_info", {}) or {}
    income_df = getattr(ticker, "income_stmt", pd.DataFrame())
    if income_df.empty:
        income_df = getattr(ticker, "financials", pd.DataFrame())
    quarterly_income_df = getattr(ticker, "quarterly_income_stmt", pd.DataFrame())
    if quarterly_income_df.empty:
        quarterly_income_df = getattr(ticker, "quarterly_financials", pd.DataFrame())
    balance_df = getattr(ticker, "balance_sheet", pd.DataFrame())
    cashflow_df = getattr(ticker, "cashflow", pd.DataFrame())
    if cashflow_df.empty:
        cashflow_df = getattr(ticker, "cash_flow", pd.DataFrame())
    history = ticker.history(period="1y")
    try:
        analyst_targets = ticker.get_analyst_price_targets()
    except Exception:
        analyst_targets = None

    news_query = info.get("longName") or args.symbol
    news_items = fetch_moneycontrol_news(news_query, limit=args.max_news)

    report = build_report(
        symbol=args.symbol.upper(),
        exchange=args.exchange.upper(),
        info=info,
        fast_info=fast_info,
        income_df=income_df,
        quarterly_income_df=quarterly_income_df,
        balance_df=balance_df,
        cashflow_df=cashflow_df,
        history=history,
        analyst_targets=analyst_targets,
        news_items=news_items,
    )

    output_path = (
        Path(args.output)
        if args.output
        else Path("reports") / f"fundamental_{args.symbol.upper()}.md"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print(f"Report written to {output_path.resolve()}")


if __name__ == "__main__":
    main()


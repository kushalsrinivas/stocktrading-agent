# NSE Stock Screener Filters for Trading Strategies

## Overview

This guide provides specific screener filters to identify NSE stocks suitable for each trading strategy. Use these filters on popular Indian stock screeners like:

- **Screener.in**
- **Tickertape**
- **ChartInk**
- **TradingView**
- **Moneycontrol**

---

## Universal Filters (Apply to All Strategies)

These filters ensure basic liquidity and quality:

### Liquidity & Volume Filters

```
Market Cap > ₹500 Crores
Average Daily Volume > 100,000 shares
Average Daily Turnover > ₹5 Crores
```

### Quality Filters

```
Delivery % > 40% (avoid high speculation stocks)
Listed for > 2 years
Not in GSM/ASM list (Stage 1-4)
```

### Price Filters

```
Stock Price > ₹20 (avoid penny stocks)
Stock Price < ₹5,000 (for better position sizing)
```

---

## Strategy-Specific Filters

### 1. Stochastic Breakout Strategy

**Best For**: Momentum stocks breaking out with volume

#### Screener Filters:

```
Technical:
- Stochastic %K < 30 (oversold) OR %K > 70 (overbought recently)
- ADX(14) > 20 (trending)
- Volume today > 1.5 × 20-day avg volume
- Price > 50-day EMA

Fundamental:
- Market Cap > ₹1,000 Crores
- Average Volume > 500,000 shares

Ideal Sectors:
- Technology
- Pharmaceuticals
- Banking
- Auto
```

#### Sample ChartInk Scan:

```
( {cash} (
[0] 1 day ago close > 1 day ago ema( close , 50 ) and
[0] 1 day ago adx(14) > 20 and
[0] 1 day ago stochastic %k(14,3,3) < 30 and
[0] volume > 1.5 * sma( volume, 20 ) and
[0] market cap > 1000
) )
```

---

### 2. VWAP Reversal Strategy

**Best For**: High-volume stocks for intraday mean reversion

#### Screener Filters:

```
Technical:
- High intraday volatility (ATR % > 2%)
- Strong average volume (> 1 million shares daily)
- RSI(14) < 40 or RSI(14) > 60 (for reversal setups)
- Price deviated from VWAP by 1-3%

Fundamental:
- Market Cap > ₹2,000 Crores
- Delivery % > 35%

Ideal Sectors:
- Banking & Finance
- IT Services
- FMCG
- Large Cap indices stocks
```

#### Recommended Stock Universe:

- Nifty 50 stocks
- Bank Nifty stocks
- High liquidity mid-caps

---

### 3. Supertrend Momentum Strategy

**Best For**: Strong trending stocks with momentum

#### Screener Filters:

```
Technical:
- Supertrend(10, 3) = Bullish
- MACD Line > Signal Line
- Price > 20-day EMA AND 20-day EMA > 50-day EMA
- ADX(14) > 25 (strong trend)
- ROC(10) > 2% (positive momentum)

Fundamental:
- Market Cap > ₹500 Crores
- Sales Growth (QoQ) > 10%
- Promoter Holding > 30%

Ideal Sectors:
- Trending sectors (check current market leaders)
- Infrastructure
- Capital Goods
- Metals (during bull runs)
```

#### Sample Screener.in Filter:

```
Market Capitalization > 500
AND Supertrend(10,3) = Bullish
AND MACD Line > MACD Signal
AND Close > EMA(20)
AND Average Volume > 100000
```

---

### 4. Keltner Squeeze Strategy

**Best For**: Stocks in consolidation ready to breakout

#### Screener Filters:

```
Technical:
- Bollinger Band Width < 20-day average BB Width (narrowing)
- Price range last 10 days < 5% (tight consolidation)
- ADX(14) < 25 BUT > 15 (weak trend, building energy)
- Volume last 5 days declining (calm before storm)
- Stock near 52-week high OR significant support

Fundamental:
- Market Cap > ₹1,000 Crores
- Debt to Equity < 1
- ROE > 12%

Ideal Candidates:
- Stocks consolidating after news/results
- Stocks in multi-month ranges
- Stocks at support/resistance levels
```

#### ChartInk Scan for Squeeze:

```
( {cash} (
[0] 1 day ago Bollinger band width < 1 day ago sma( Bollinger band width, 20 ) and
[0] 1 day ago adx(14) < 25 and
[0] 1 day ago adx(14) > 15 and
[0] ( 1 day ago high - 1 day ago low ) / 1 day ago close * 100 < 3 and
[0] market cap > 1000
) )
```

---

### 5. Williams %R Trend Strategy

**Best For**: Oversold/overbought reversals with trend confirmation

#### Screener Filters:

```
Technical:
- Williams %R < -80 (deeply oversold) OR > -20 (overbought)
- ADX(14) > 20 (trend present)
- Volume > 20-day average
- RSI(14) showing divergence (optional advanced filter)

Fundamental:
- Market Cap > ₹750 Crores
- Consistent earnings growth
- Low debt

Ideal Sectors:
- All liquid sectors
- Focus on cyclical stocks for reversals
```

---

## Sector-Wise Recommendations

### Best Sectors for Each Strategy

| Strategy                | Primary Sectors           | Secondary Sectors     |
| ----------------------- | ------------------------- | --------------------- |
| **Stochastic Breakout** | IT, Pharma, Banking       | Auto, Metals          |
| **VWAP Reversal**       | Banking, IT, FMCG         | Large Caps            |
| **Supertrend Momentum** | Infrastructure, Metals    | Capital Goods, Energy |
| **Keltner Squeeze**     | Mid-Caps in consolidation | All sectors           |
| **Williams Trend**      | Cyclicals, Banking        | Consumer Durables     |

---

## Pre-Screened Stock Lists for NSE

### High Liquidity Stocks (All Strategies)

```
Large Cap (Nifty 50):
RELIANCE, TCS, HDFCBANK, INFY, ICICIBANK, HINDUNILVR, ITC, SBIN,
BHARTIARTL, KOTAKBANK, LT, AXISBANK, BAJFINANCE, ASIANPAINT,
MARUTI, TITAN, SUNPHARMA, ULTRACEMCO, NESTLEIND, WIPRO

Mid Cap (High Volume):
BAJAJFINSV, ADANIPORTS, POWERGRID, NTPC, ONGC, TATAMOTORS,
INDUSINDBK, DIVISLAB, DRREDDY, CIPLA, GRASIM, HINDALCO,
JSWSTEEL, TATASTEEL, VEDL, GODREJCP
```

### Momentum Stocks (Supertrend, Stochastic)

```
Technology:
TCS, INFY, WIPRO, HCLTECH, TECHM, LTTS, COFORGE, MPHASIS

Pharmaceuticals:
SUNPHARMA, DRREDDY, CIPLA, DIVISLAB, AUROPHARMA, BIOCON

Auto & Auto Ancillary:
MARUTI, TATAMOTORS, M&M, BAJAJ-AUTO, HEROMOTOCO, EICHERMOT
```

### Mean Reversion Stocks (VWAP, RSI+BB)

```
Banking:
HDFCBANK, ICICIBANK, KOTAKBANK, AXISBANK, SBIN, INDUSINDBK

FMCG:
HINDUNILVR, ITC, NESTLEIND, BRITANNIA, DABUR, MARICO

IT Services:
TCS, INFY, WIPRO, HCLTECH
```

### Breakout Candidates (Keltner Squeeze)

```
Check these sectors for consolidating stocks:
- Infrastructure: L&T, ADANIPORTS, DLF
- Capital Goods: BHEL, BEL, HAL
- Metals: TATASTEEL, JSWSTEEL, HINDALCO, VEDL
- Mid-Caps: Use screener to find consolidating patterns
```

---

## How to Use These Filters

### Step 1: Choose Your Screener Platform

**For Beginners**: Screener.in or Tickertape

- Easy to use interface
- Pre-built filters
- Fundamental data available

**For Advanced**: ChartInk

- Custom technical scans
- Real-time scanning
- More flexibility

**For Intraday**: TradingView or ChartInk

- Real-time data
- Advanced charting
- Alert capabilities

### Step 2: Apply Universal Filters First

1. Set minimum market cap (₹500 Cr+)
2. Set minimum volume (100,000+ shares)
3. Exclude penny stocks (<₹20)
4. Check delivery percentage (>40%)

### Step 3: Apply Strategy-Specific Filters

1. Choose your strategy
2. Apply technical filters from above
3. Add fundamental filters if long-term
4. Note down the tickers

### Step 4: Create Your CSV

Format:

```csv
Symbol,Name,MarketCap,Sector,Strategy,Priority
RELIANCE.NS,Reliance Industries,15.5L Cr,Oil & Gas,Supertrend,High
TCS.NS,TCS,13.2L Cr,IT,VWAP Reversal,High
HDFCBANK.NS,HDFC Bank,11.8L Cr,Banking,VWAP Reversal,High
```

---

## Sample Screener Setups

### On Screener.in

**For Momentum Strategies:**

```
Market Capitalization > 1000
AND Price > EMA(20)
AND RSI > 50
AND MACD Line > MACD Signal
AND Volume > 100000
AND Delivery Percentage > 40
```

**For Mean Reversion:**

```
Market Capitalization > 2000
AND RSI < 40
AND Price < EMA(20)
AND Volume > 500000
AND Delivery Percentage > 45
AND Bollinger Band Position < 20
```

### On ChartInk (Technical Focus)

**Stochastic Breakout Scan:**

```
( {cash} (
[0] 1 day ago close > 1 day ago ema( close , 50 ) and
[0] 1 day ago stochastic %k(14,3,3) < 30 and
[0] 1 day ago adx(14) > 20 and
[0] volume > 1.5 * sma( volume, 20 ) and
[0] close > 20 and
[0] market cap > 1000
) )
```

**Consolidation Breakout Scan:**

```
( {cash} (
[0] 1 day ago close = 1 day ago highest( close, 20 ) and
[0] 1 day ago adx(14) < 25 and
[0] volume > 2 * sma( volume, 20 ) and
[0] market cap > 500
) )
```

---

## Recommended CSV Structure

Create a CSV file named `nse_strategy_stocks.csv`:

```csv
Symbol,Name,Sector,MarketCap_Cr,AvgVolume,Strategy1,Strategy2,Strategy3,Priority,Notes
RELIANCE.NS,Reliance Industries,Oil & Gas,1550000,8500000,Supertrend,Stochastic,Williams,High,High liquidity leader
TCS.NS,TCS,IT,1320000,2500000,VWAP,Supertrend,Williams,High,Stable large cap
HDFCBANK.NS,HDFC Bank,Banking,1180000,5200000,VWAP,Williams,RSI+BB,High,Banking sector leader
INFY.NS,Infosys,IT,725000,4800000,VWAP,Supertrend,Stochastic,High,IT momentum
ICICIBANK.NS,ICICI Bank,Banking,680000,7500000,VWAP,Williams,RSI+BB,High,High volume banking
BHARTIARTL.NS,Bharti Airtel,Telecom,630000,3200000,Supertrend,Stochastic,Williams,Medium,Telecom leader
ITC.NS,ITC,FMCG,520000,6800000,VWAP,Williams,Mean Reversion,High,FMCG stable
SBIN.NS,SBI,Banking,480000,12000000,VWAP,Williams,Stochastic,High,Highest volume bank
LT.NS,L&T,Infrastructure,465000,1200000,Supertrend,Keltner,Momentum,High,Infra play
AXISBANK.NS,Axis Bank,Banking,325000,6500000,VWAP,Williams,Stochastic,Medium,Banking
TATAMOTORS.NS,Tata Motors,Auto,310000,9500000,Supertrend,Stochastic,Momentum,Medium,Auto sector
BAJFINANCE.NS,Bajaj Finance,NBFC,485000,800000,Supertrend,Williams,Momentum,High,NBFC leader
MARUTI.NS,Maruti Suzuki,Auto,345000,650000,Supertrend,Keltner,Stochastic,Medium,Auto leader
TITAN.NS,Titan,Consumer,280000,420000,Supertrend,VWAP,Williams,Medium,Consumer play
WIPRO.NS,Wipro,IT,265000,3800000,VWAP,Supertrend,Mean Reversion,Medium,IT services
SUNPHARMA.NS,Sun Pharma,Pharma,260000,2100000,Stochastic,Supertrend,Keltner,Medium,Pharma leader
ULTRACEMCO.NS,UltraTech Cement,Cement,255000,180000,Supertrend,Keltner,Momentum,Low,Cement leader
KOTAKBANK.NS,Kotak Bank,Banking,340000,1800000,VWAP,Williams,Mean Reversion,High,Private bank
ASIANPAINT.NS,Asian Paints,Paints,270000,520000,VWAP,Keltner,Mean Reversion,Medium,Paint leader
HINDUNILVR.NS,HUL,FMCG,590000,1200000,VWAP,Mean Reversion,Williams,High,FMCG stable
```

---

## Advanced Filtering Tips

### 1. **Sector Rotation Strategy**

- Check which sectors are leading (Nifty Sectoral Indices)
- Apply momentum strategies to leading sectors
- Apply mean reversion to lagging quality stocks

### 2. **Result Season Plays**

- Before results: Use consolidation/squeeze strategies
- After results: Use momentum/breakout strategies
- Avoid: Stocks with upcoming results (high uncertainty)

### 3. **Market Condition Filters**

**Bull Market:**

```
Focus on: Supertrend, Stochastic Breakout, Williams (uptrend)
Avoid: Excessive mean reversion (trend may continue)
```

**Bear Market:**

```
Focus on: VWAP Reversal, Williams (oversold), Mean Reversion
Avoid: Momentum strategies (whipsaws)
```

**Range-Bound Market:**

```
Focus on: VWAP, Keltner Squeeze, Mean Reversion
Avoid: Trend-following strategies
```

### 4. **Time Frame Considerations**

**Intraday (Use only liquid stocks):**

- VWAP Reversal: Nifty 50 stocks only
- Volume > 5 million shares daily
- Tight spreads (<0.1%)

**Swing (2-10 days):**

- Stochastic Breakout: Mid to large caps
- Supertrend Momentum: Any trending stock
- Keltner Squeeze: Consolidating stocks

**Positional (weeks to months):**

- All strategies work
- Focus on fundamental quality too
- Add fundamental filters

---

## Creating Your Master CSV

### Template Structure:

```csv
Symbol,Name,Sector,SubSector,MarketCap_Cr,Price,AvgVolume,Delivery%,Strategy1,Strategy2,Liquidity,TimeFrame,Priority
```

### Priority Levels:

- **High**: Trade these first, best fit
- **Medium**: Good candidates, secondary focus
- **Low**: Watch list, backup options

### Liquidity Levels:

- **Very High**: Nifty 50 stocks, >5M daily volume
- **High**: >1M daily volume
- **Medium**: >500K daily volume
- **Low**: >100K daily volume

---

## Next Steps

1. **Open your preferred screener** (Screener.in, ChartInk, etc.)
2. **Apply universal filters** to get quality stocks
3. **Apply strategy-specific filters** for each strategy
4. **Download results as CSV**
5. **Merge all CSVs** into master list
6. **Tag each stock** with suitable strategies
7. **Prioritize** based on liquidity and quality
8. **Backtest** top 50 stocks with your strategies
9. **Create watchlists** for each strategy
10. **Monitor daily** and execute when signals appear

---

## Important Notes

⚠️ **Disclaimer**: These filters are for screening purposes only. Always:

- Backtest before live trading
- Use proper risk management
- Don't trade all strategies simultaneously
- Focus on 2-3 strategies initially
- Monitor market conditions

✅ **Best Practices**:

- Update your CSV weekly
- Remove stocks with declining volume
- Add newly listed liquid stocks
- Rotate based on sector performance
- Keep separate lists for different timeframes

---

**Ready to Start?** Use the sample CSV above and modify based on your screener results! 🚀

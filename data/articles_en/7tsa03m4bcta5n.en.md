---
title: "Pythonで解き明かす株式投資の未来：PER/PBRバンド分析による銘柄の「真の価値」可視化戦略 (English)"
emoji: "🤖"
type: "tech"
topics: []
published: false
---

# Unlocking the Future of Stock Investing with Python: A Strategy to Visualize a Stock's 'True Value' through PER/PBR Band Analysis

Are you being forced into emotional decisions amidst the uncertain fluctuations of the stock market? For our readers at TechTrend Watch, especially developers who value data and logic, you must surely wish to interpret the market with a more scientific and data-driven approach. In this article, we will provide a detailed explanation of a method for drawing PER/PBR bands, leveraging Python and J-Quants data to objectively and intuitively visualize a stock's "undervaluation." This analysis technique will serve as a powerful compass, enabling you to make sound investment decisions without being swayed by market noise.

## Why is PER/PBR Band Analysis Important Now?

In traditional stock analysis, there's a tendency to evaluate indicators like PER (Price-to-Earnings Ratio) and PBR (Price-to-Book Ratio) in isolation, leading to "undervalued" or "overvalued" judgments. However, this approach often lacks a multi-faceted perspective. For instance, even with the same PER of 10x, its meaning can differ significantly depending on the company's historical levels or the average for its industry. This is where "PER/PBR band" analysis truly shines. It's an innovative tool that visually captures the historical PER/PBR levels at which a stock's price has traded, allowing for an intuitive judgment of a stock's "historical undervaluation" based on where the current price sits within that band.

Without incorporating this band analysis, investors risk being continuously swayed by short-term market noise. In modern investment strategies, making decisions based on data – facts – rather than emotions has become indispensable.

<div class="expert-opinion">
<h3>TechTrend Watch's Recommendation: Data-Driven Investment Strategies for Navigating Uncertain Times</h3>
<p>The reason TechTrend Watch strongly recommends this PER/PBR band analysis lies in its 'high reproducibility.' A common challenge many individual investors face is the inability to make 'confident decisions' amidst information overload. However, by handling high-quality official data like J-Quants with Python and building your own band analysis, you can objectively grasp the divergence between a company's intrinsic value and its stock price, without being tossed around by the market's random walk.</p>
<p>This is not merely technical analysis. It re-evaluates a company's fundamentals (PER/PBR) over a time axis and visualizes the 'waves of expectation' woven by market sentiment. Particularly, many stocks in the Japanese market tend to have their potential underestimated. This band analysis will truly serve as a compass for discovering such 'hidden gem' stocks and building assets from a long-term perspective. Python's flexibility, allowing for free customization, can indeed become the strongest weapon for developers in establishing a 'competitive advantage' that is never achievable with existing brokerage tools.</p>
</div>

## J-Quants × Python: A Technical Deep Dive

The core of this analysis involves data acquisition from the J-Quants API and processing/visualization with Python. The main architecture is as follows:

1.  **Data Acquisition via J-Quants API**: First, historical stock price data for the target stock, along with financial data (such as EPS and BPS) required to calculate PER and PBR, are retrieved from the J-Quants API. As this is official data, its reliability is extremely high.
2.  **PER/PBR Calculation**: Daily PER/PBR values are calculated based on the acquired stock prices and financial data. This process requires precise data handling.
3.  **Band Calculation**: The band width is calculated using the historical maximum, minimum, or standard deviation of PER/PBR over a specific period (e.g., the past 5 years). Multiple calculation methods exist, allowing for tuning according to one's own strategy.
4.  **Visualization**: Powerful Python visualization libraries like `matplotlib` and `plotly` are used to plot the PER/PBR bands on a stock price chart. This allows for an immediate understanding of where the current stock price stands within the band.

```python
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib # Supports Japanese display
# from jquantsapi import JQuantsapi # J-Quants API client requires separate installation and authentication

# Create dummy data (actual data would be obtained from J-Quants)
dates = pd.to_datetime(pd.date_range(start='2020-01-01', periods=200, freq='D'))
stock_prices = pd.Series(5000 + 1000 * (0.5 * pd.np.sin(pd.np.arange(200)/10) + pd.np.random.rand(200)*0.2), index=dates)
per_values = pd.Series(10 + 5 * (0.5 * pd.np.sin(pd.np.arange(200)/10) + pd.np.random.rand(200)*0.1), index=dates)

# PER band calculation (e.g., band using moving average and standard deviation of PER over the past N days)
window = 60 # 60-day moving average window
per_mean = per_values.rolling(window=window).mean()
per_std = per_values.rolling(window=window).std()
per_upper_band = per_mean + 1.5 * per_std
per_lower_band = per_mean - 1.5 * per_std

# Visualization
plt.figure(figsize=(12, 6))
plt.plot(stock_prices.index, stock_prices, label='Stock Price', color='blue')

# When converting PER bands to stock prices for display, conversion logic based on financial data like EPS is required.
# Example: Back-calculating stock price bands from PER bands (assuming constant EPS)
# if 'eps_values' in locals(): # If EPS data exists
#     eps = eps_values.reindex(dates, method='ffill') # Align EPS to stock price index
#     plt.plot(dates, per_upper_band * eps, label='PER Upper Band', color='red', linestyle='--')
#     plt.plot(dates, per_lower_band * eps, label='PER Lower Band', color='green', linestyle='--')

plt.title('Stock Price and PER Band (Simple Version)')
plt.xlabel('Date')
plt.ylabel('Stock Price')
plt.grid(True)
plt.legend()
plt.show()
```

## Comparison with Existing Tools: The 'Overwhelming Freedom' Python Offers

Analysis tools provided by brokerage firms and commercially available investment software do offer features similar to PER/PBR bands. However, these tools inherently come with the limitations of "off-the-shelf products." The periods that can be set and the band calculation logic are often fixed, making it frequently difficult to fully align them with one's own investment strategy.

On the other hand, leveraging Python completely transforms this situation. By extracting raw data from J-Quants, you can flexibly set the band calculation period **to match your own investment strategy.** You can also change the standard deviation multiplier, or apply concepts from moving averages and Bollinger Bands to draw more complex bands. This overwhelming freedom is the biggest reason to choose Python, allowing you to pursue a "competitive advantage" that is hard to find with standard analysis tools.

## Pitfalls to Be Aware Of and Setup Tips

### 1. PER/PBR Considerations: Accounting for Industry and Growth Stage

PER/PBR bands are powerful analytical tools, but they are not a panacea. For example, growth-stage companies tend to have high PERs due to future growth expectations, and companies in mature industries may not necessarily be "undervalued" even with a low PER. Furthermore, the appropriate PER levels differ significantly between IT companies and manufacturing firms. It is crucial to not only observe band fluctuations but also to deeply understand the industry characteristics and growth stage of the stock in question.

### 2. Strict Management of J-Quants API Keys

Authentication is required to use the J-Quants API. API keys are sensitive information, and we strongly recommend managing them as environment variables to prevent leakage. Directly writing them into public repositories like GitHub is absolutely not recommended for security reasons.

### 3. Data Freshness and Update Frequency

Stock prices and financial data are constantly changing. Especially for stock prices, if they are not acquired daily and reflected in the analysis, real-time value judgment becomes difficult. It is advisable to set up a system to automatically update data by building a script, ensuring that analysis is always performed with the latest information.

### Environment Setup Tips

*   **Python**: Latest version (3.8 or higher recommended)
*   **Key Libraries**: `pandas`, `matplotlib`, `numpy`, `japanize-matplotlib` (for Japanese display)
*   **J-Quants Client**: `jquantsapi` (installable via pip)

We recommend starting by setting up this environment and running the sample code provided in this article.

## Frequently Asked Questions (FAQ)

### Q1: What kind of stocks are PER/PBR bands effective for?
**A1**: They are particularly effective for companies that have consistently recorded relatively stable profits in the past and whose PBR is not extremely low (i.e., not in a continuous loss-making state). For emerging growth companies or highly cyclical stocks with volatile earnings, the bands may not function as effectively.

### Q2: Can similar analysis be performed using data other than J-Quants?
**A2**: Yes, absolutely. If you can obtain stock price and financial data from sources like Yahoo! Finance, various brokerage APIs, or through web scraping, you can build a similar analysis. However, considering data reliability and the effort involved in acquisition, J-Quants is an excellent choice.

### Q3: How should the band width and period be set?
**A3**: This depends on the analyst's investment strategy. The period should be adjusted, for example, a few months for short-term trading or several years for long-term investment. The band width (e.g., 1.5 times, 2 times the standard deviation) also requires trial and error, tailored to the stock's volatility and your own risk tolerance.

### Q4: Is it okay to make investment decisions based solely on this analysis?
**A4**: No, making investment decisions based on a single indicator alone is highly risky. PER/PBR bands are merely one powerful tool for measuring "undervaluation." It is crucial to combine them with a multi-faceted perspective, including the company's business model, competitive advantages, future prospects, financial health, and overall market trends.

## TechTrend Watch's Final Conclusion: Seize the Future with Data!

How was that? We hope you've understood just how powerful PER/PBR band analysis is when leveraged with Python and J-Quants. In the often emotion-driven world of investment, there are few tools that offer such objective and visual support for decision-making. Especially for us developers, the freedom to build and customize logic with our own hands must be the most appealing aspect.

Investment is an area of personal responsibility, but if you can dramatically enhance the quality of that responsibility with data, we strongly urge you to consider adopting this approach. We expect you to master this analysis technique and steadily advance your asset building through wise and bold data-driven investment decisions. The future market will be carved out by your own insights and execution.

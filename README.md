# DeFi_Data_Logger

## Premise
In the decentralized world of cryptocurrencies, there has been a push to decentralize financial systems and instruments, the DeFi (Decentralized Finance) wave. For example, the equivalent to the Forex in crypto used to be a site like Coinbase, a centralized exchange for cryptocurrencies. The DeFi equivalent to the Forex is a Decentralized Exchange (or DEX for short). DEXs particularly caught my attention because they work using liquidity pools, where users can provide liquidity for a pair of assets, and the ratio between those two assets determines the current exchange rate between them. This means that the DEX relies on arbitrage to maintain price with the rest of the market. For example, if the price of BTC in USD falls in the rest of the market then the only way for a DEX to track this price change is if people buy BTC in the outside markets and sell it on the DEX, increasing the number of BTC for every dollar, or equivalently said, decreasing the USD required to buy BTC on the DEX until the price matches outside markets. This is interesting because the system requires arbitragers to work, and the arbitragers earn money along the way.


## The Problem
This sounds great –– free money, right? But there are so many different cryptocurrencies, with so many pairs -- finding arbitrage that is worth the transaction fees takes forever, and often for only a couple % in returns for every arbitrage. Is it really worth all that time?

## The Solution
Of course not! That's what bots are for! To tackle this problem, I wrote a bot that uses Selenium to scrape the top 100 DEXs, by Volume, check the exchange rate between 10 currency pairs, and logs the price to a SQL database. The number of exchanges (100) and number of currecncy pairs (10) were pared down to prioritize only the currencies with high volume –– lower volume currencies don't have very large arbitrage opportunities. This information is stored in a sql database and kept track of over time for future reference. It provides data to check the arbitrage bots accuracy, to test future changes on, and to analyze and find trends from in the future.

This code is up and running on a local server (which I unfortunately don't have access to at the moment), along with a separate discord bot (which is unfortunately not in this repo, but will be very soon!) that processes the data in realtime and sends messages whenever profitable arbitrage opportunities are found. This bot has resulted in a 327% ROI to date!

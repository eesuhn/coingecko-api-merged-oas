- [coingecko.json](https://raw.githubusercontent.com/eesuhn/coingecko-api-merged-oas/refs/heads/main/app/docs/coingecko.json)
- [selected-coingecko.json](https://raw.githubusercontent.com/eesuhn/coingecko-api-merged-oas/refs/heads/main/app/docs/selected-coingecko.json)

### List of Selected Endpoints for `selected-coingecko.json`

```sh
# General
"/key",                            # 💼 API Usage
"/simple/price",                   # Coin Price by IDs and Symbols
"/simple/token_price/{id}",        # Coin Price by Token Addresses
"/coins/list",                     # Coins List (ID Map)
"/coins/{id}",                     # Coin Data by ID
"/coins/{id}/market_chart/range",  # Coin Historical Chart Data within Time Range by ID
"/coins/{id}/ohlc/range",          # 💼 Coin OHLC Chart within Time Range by ID
"/coins/categories",               # Coins Categories List with Market Data

# Onchain
"/onchain/simple/networks/{network}/token_price/{addresses}",  # Token Price by Token Addresses
"/onchain/networks",                                           # Supported Networks List (ID Map)
"/onchain/networks/{network}/trending_pools",                  # Trending Pools by Network
"/onchain/networks/{network}/pools/multi/{addresses}",         # Multiple Pools Data by Pool Addresses
"/onchain/networks/{network}/pools",                           # Top Pools by Network
"/onchain/pools/megafilter",                                   # 🔥 Megafilter for Pools
"/onchain/networks/{network}/tokens/multi/{addresses}"         # Tokens Data by Token Addresses
```

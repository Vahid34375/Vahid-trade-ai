
import requests

def get_market_data(symbol="bitcoin"):
    url = f"https://api.coingecko.com/api/v3/simple/price"

    params = {
        "ids": symbol,
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=15
        )
        response.raise_for_status()
        return response.json()

    except requests.RequestException as error:
        return {"error": str(error)}

def build_message(wallets: list[str]) -> list[str]:
    urls_wallets = []
    BASE_URL_PROFILE = "https://polymarket.com/ru/profile/"
    if wallets:
        for wallet in wallets:
            if isinstance(wallet, str):
                urls_wallets.append(BASE_URL_PROFILE + wallet)
    return urls_wallets

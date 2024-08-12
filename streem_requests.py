from streemer.request_handler import RequestsHandler, RequestResultQuiet, RequestResultPrinter, CsvRequestResultPrinter
from streemer.env import Env


def test_market_prices():
    rh = RequestsHandler(
        env = Env('prod_api'),
        rrh = RequestResultQuiet(),
    )

    rh.authenticate()

    route = '/v2/market_prices'

    params = {
        "end_date":"2024-02-17",
        "country":"FR",
        "type":"negative_imbalance",
        "start_date":"2024-01-01"
    }

    response = rh.get(route, params=params)

    return response


def test_get_revenues():
    rh = RequestsHandler(
        env = Env('prod_api'),
        rrh = RequestResultPrinter(),
    )

    rh.authenticate()

    route = '/v2/revenues'
    params = {
        "start_date": "2024-01-01",
        "end_date": "2024-01-31",
    }

    response = rh.get(route, params=params)

    return response


def test_get_exchange_rates():
    rh = RequestsHandler(
        env = Env('prod_api'),
        rrh = RequestResultPrinter(),
    )

    rh.authenticate()

    route = '/v2/exchange_rates'
    params = {
        "start_date": "2024-01-01",
        "end_date": "2024-01-31",
    }

    response = rh.get(route, params=params)

    return response


def test_api_telereleve():
    rh = RequestsHandler(
        env = Env('prod_api'),
        rrh = RequestResultPrinter(),
    )

    rh.authenticate()

    installation = 'XXX'

    route = f'/v2/installations/{installation}/call'

    response = rh.get(route)  # should be ok
    response = rh.get(route)  # should fail due to rate limit

    return response


if __name__ == '__main__':
    r = test_api_telereleve()
from bot.betfairlightweight.filters import (
    streaming_market_filter,
    streaming_market_data_filter,
)
import bot.betfairlightweight as betfairlightweight

username = "adamjeremiah"
password = "we1$4b0y"
appKey = "OCWWOxNeROp7JOvx"

# create trading instance
trading = betfairlightweight.APIClient(username, password, app_key=appKey, certs="C:\\Users\\a-d-a\\PycharmProjects\\bettingTool\\bot\\certs")

# login
trading.login()

betfair_socket = trading.streaming.create_stream(
    unique_id=2,
    description='Test Market Socket',
)

market_filter = streaming_market_filter(
    event_type_ids=['7'],
    country_codes=['IE'],
    market_types=['WIN'],
)
market_data_filter = streaming_market_data_filter(
    fields=['EX_ALL_OFFERS', 'EX_MARKET_DEF'],
    ladder_levels=3
)

betfair_socket.subscribe_to_markets(
    unique_id=12345,
    market_filter=market_filter,
    market_data_filter=market_data_filter,
)
betfair_socket.start(async=False)
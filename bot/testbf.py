from bot.bf import Betfair
import json



username = "adamjeremiah"
password = "we1$4b0y"
appKey = "OCWWOxNeROp7JOvx"

bf = Betfair(username, password, appKey)
bf.login()
bf.user_details()

bf.get_market_ids()

catalogues = list(map(lambda x: list(json.loads(x.json()).values())[:-1], bf.get_catalogue(max_results=100)))
bf.get_catalogue()[0].json()
market_ids = list(map(lambda x: x[0], catalogues))
markets = list(map(lambda x: x.json(), bf.get_markets(market_ids)))
print(markets)
#print(catalogues)
#for c in catalogues:
#    print(list(json.loads(c.json()).values()))
#market_ids = (map(lambda x: marketId, catalogues))
#print(list(market_ids))
#ids = (list(map(lambda x: x.market_id, catalogues)))
#market = bf.get_markets(ids)[0]


#print(market.runners[0].json())
#columns = list(someitem)

#print(columns)
#market_ids = list(map(lambda x: x.market_id, catalogues))
#
# for market in bf.get_markets(market_ids):
#     for runner in market.runners:
#         print(map(lambda x, y: {'BACK_PRICE_{}'.format(y):x.price,
#                                'BACK_SIZE_{}'.format(y):x.size},runner.ex.available_to_back, range(100)))
#         #print(backs)
#         #for back in runner.ex.available_to_back:
#
#         print("MARKET_ID: {}; "
#               "STATUS: {}; "
#               "LAST_MATCHED_TIME: {}; "
#               "TOTAL_MATCHED: {}; "
#               "TOTAL_AVAILABLE: {}; "
#               "SELECTION_ID: {}; "
#               "LAST_PRICE_TRADED: {}; "
#               "TOTAL_MATCHED: {}; "
#               ""
#               .format(market.market_id,
#                       market.status,
#                       market.last_match_time,
#                       market.total_matched,
#                       market.total_available,
#                       runner.selection_id,
#                       runner.last_price_traded,
#                       runner.total_matched))
#

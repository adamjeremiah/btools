import betfairlightweight as betfairlightweight
from betfairlightweight import filters

username = ""
password = ""
appKey = ""

# create trading instance
trading = betfairlightweight.APIClient(username, password, app_key=appKey, certs="C:\\Users\\a-d-a\\PycharmProjects\\bettingTool\\bot\\certs")

# login
trading.login()

# make event type request to find horse racing event type


# returns one result
print(horse_racing_event_type_id)

for event_type in horse_racing_event_type_id:
    # prints id, name and market count
    print(
        event_type.event_type.id, event_type.event_type.name, event_type.market_count
    )
    horse_racing_id = event_type.event_type.id

    # list all horse racing market catalogues

    print('%s market catalogues returned' % len(market_catalogues))

        # market book request
        market_books = trading.betting.list_market_book(
            market_ids=[market_catalogue.market_id],
            price_projection=filters.price_projection(
                price_data=filters.price_data(
                    ex_all_offers=True
                )
            )
        )

        for market_book in market_books:
            # prints market id, inplay?, status and total matched
            print(
                market_book.market_id, market_book.inplay, market_book.status, market_book.total_matched
            )

            for runner in market_book.runners:
                # prints selection id, status and total matched
                print(
                    runner.selection_id, runner.status, runner.total_matched
                )

                available_to_back = runner.ex.available_to_back
                available_to_lay = runner.ex.available_to_lay
                print("ATB: {}, ATL: {}".format(
                    available_to_back, available_to_lay
                ))
            #for atb in available_to_back:
             #   print(atb.json())
                 #   print(atb.json())
                    #print(atb.price, atb.datetime_created, atb.size, atb.json())

# logout
trading.logout()
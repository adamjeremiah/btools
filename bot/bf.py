import betfairlightweight as betfairlightweight
from betfairlightweight import filters


class Betfair:

    def __init__(self, username, password, appKey):
        self.bf = betfairlightweight.APIClient(username, password, app_key=appKey,
                                               certs="bot\certs")

    def login(self):
        self.bf.login()

    def user_details(self):
        return self.bf.account.get_account_details().json()

    def um(self):
        self.bf.logout()

    def horse_racing_id(self):
        return "7"
        #return self.bf.betting.list_event_types(
        #    filter=filters.market_filter(
        #        text_query='Horse Racing'
        #    )
        #)[0].event_type.id

    def get_catalogue(self, event_ids=None, max_results=100, countries=None, types=None, projections=None):
        if types is None:
            types = ['WIN']
        if countries is None:
            countries = ['GB']
        if event_ids is None:
            event_ids = ['7']
        if projections is None:
            projections = ['EVENT', 'MARKET_START_TIME', 'RUNNER_DESCRIPTION']

        return self.bf.betting.list_market_catalogue(
            filter=filters.market_filter(
                event_type_ids=event_ids,  # filter on just horse racing
                market_countries=countries,  # filter on just GB countries
                market_type_codes=types,  # filter on just WIN market types
            ),
            market_projection=projections,
            # runner description required
            max_results=max_results
        )

    def get_markets(self, market_ids):
        return self.bf.betting.list_market_book(
            market_ids=market_ids,
            price_projection=filters.price_projection(

                price_data=filters.price_data(
                    ex_all_offers=True,
                    ex_traded=True

                )
            )
        )

    @staticmethod
    def get_market_ids(self, catalogues):
        return list(map(lambda x: x[0], catalogues))


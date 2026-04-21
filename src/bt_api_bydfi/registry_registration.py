from bt_api_base.balance_utils import simple_balance_handler as _bydfi_balance_handler
from bt_api_bydfi.containers.exchanges.bydfi_exchange_data import BYDFiExchangeDataSpot
from bt_api_bydfi.feeds.spot import BYDFiRequestDataSpot
from bt_api_base.registry import ExchangeRegistry


def register_bydfi():
    ExchangeRegistry.register_feed("BYDFI___SPOT", BYDFiRequestDataSpot)
    ExchangeRegistry.register_exchange_data("BYDFI___SPOT", BYDFiExchangeDataSpot)
    ExchangeRegistry.register_balance_handler("BYDFI___SPOT", _bydfi_balance_handler)


register_bydfi()
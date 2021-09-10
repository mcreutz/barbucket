class Encoder():
    """Encode and decode exchange names between different formats."""

    def __init__(self) -> None:
        pass

    # def remove_special_chars(input_string):
    #     special_chars = ["'"]
    #     result = input_string
    #     for char in special_chars:
    #         result = result.replace(char, '')
    #     return result

    # Known exchanges:
    # 'ISLAND'          # NASDAQ / Island
    # 'NASDAQ'          # NASDAQ / Island
    # 'NYSE'            # NYSE
    # 'NYSE ARCA'       # Archipelago
    # 'AMEX'            # American Stock Exchange
    # 'BATS'            # Better Alternative Trading System

    # 'VSE'             # Vancouver Stock Exchange

    # 'FWB'             # Frankfurter Wertpapierbörse
    # 'IBIS'            # XETRA
    # 'SWB'             # Stuttgarter Wertpapierbörse

    # 'LSE'             # London Stock Exchange
    # 'LSEETF'          # London Stock Exchange: ETF

    # 'SBF'             # Euronext France

    # 'ENEXT.BE'        #
    # 'AEB'             #

    @staticmethod
    def encode_exchange_tv(exchange: str) -> str:
        """Encode from Barbucket-notation to TV-notation"""

        exchange_codes = {
            'NASDAQ': "NASDAQ",     # NASDAQ / Island
            'ARCA': "NYSE ARCA",    # Archipelago
            'IBIS': "XETR"}         # XETRA
        if exchange in exchange_codes.keys():
            return exchange_codes[exchange]
        else:
            return exchange

    @staticmethod
    def decode_exchange_tv(exchange: str) -> str:
        """Decode from IB-notation to Barbucket-notation"""

        exchange_codes = {
            'ISLAND': "NASDAQ",     # NASDAQ / Island
            'NYSE ARCA': "ARCA",    # Archipelago
            'XETR': "IBIS"}         # XETRA
        if exchange in exchange_codes.keys():
            return exchange_codes[exchange]
        else:
            return exchange

    @staticmethod
    def encode_exchange_ib(exchange: str) -> str:
        """Encode from Barbucket-notation to IB-notation"""

        exchange_codes = {
            'NASDAQ': "ISLAND",     # NASDAQ / Island
            'ARCA': "NYSE ARCA"}    # Archipelago
        if exchange in exchange_codes.keys():
            return exchange_codes[exchange]
        else:
            return exchange

    @staticmethod
    def decode_exchange_ib(exchange: str) -> str:
        """Decode from IB-notation to Barbucket-notation"""

        exchange_codes = {
            'ISLAND': "NASDAQ",     # NASDAQ / Island
            'NYSE ARCA': "ARCA"}    # Archipelago
        if exchange in exchange_codes.keys():
            return exchange_codes[exchange]
        else:
            return exchange

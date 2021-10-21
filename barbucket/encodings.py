from enum import Enum


class Api(Enum):
    IB = 1
    TV = 2


class Encoding(Enum):
    """Doc"""

    @classmethod
    def encode(cls, name: str, to_api: Api) -> str:
        """Encode from Barbucket notation to specific api notation"""

        for element in cls:
            if element.name == name:
                return element.value[to_api]
        raise AttributeError(f"Attribute '{name}' not found.")

    @classmethod
    def decode(cls, name: str, from_api: Api) -> str:
        """Decode from specific api notation to Barbucket notation"""

        for element in cls:
            if element.value[from_api] == name:
                return element.name
        raise AttributeError(f"Attribute '{name}' not found.")


class Exchange(Encoding):
    AEB = {Api.IB: 'AEB', Api.TV: ''}
    AMEX = {Api.IB: 'AMEX', Api.TV: 'AMEX'}
    ARCA = {Api.IB: 'ARCA', Api.TV: 'NYSE ARCA'}
    ATH = {Api.IB: 'ATH', Api.TV: ''}
    BATS = {Api.IB: 'BATS', Api.TV: ''}
    BM = {Api.IB: 'BM', Api.TV: ''}
    BVL = {Api.IB: 'BVL', Api.TV: ''}
    BVME = {Api.IB: 'BVME', Api.TV: ''}
    BVME_ETF = {Api.IB: 'BVME.ETF', Api.TV: ''}
    EBS = {Api.IB: 'EBS', Api.TV: ''}
    ENEXT_BE = {Api.IB: 'ENEXT.BE', Api.TV: ''}
    FWB = {Api.IB: 'FWB', Api.TV: 'FWB'}
    GETTEX = {Api.IB: 'GETTEX', Api.TV: ''}
    HEX = {Api.IB: 'HEX', Api.TV: ''}
    IBIS = {Api.IB: 'IBIS', Api.TV: 'XETR'}
    IBIS2 = {Api.IB: 'IBIS2', Api.TV: ''}
    ISED = {Api.IB: 'ISED', Api.TV: ''}
    LSE = {Api.IB: 'LSE', Api.TV: ''}
    LSEETF = {Api.IB: 'LSEETF', Api.TV: ''}
    NASDAQ = {Api.IB: 'ISLAND', Api.TV: 'NASDAQ'}
    NYSE = {Api.IB: 'NYSE', Api.TV: 'NYSE'}
    SBF = {Api.IB: 'SBF', Api.TV: ''}
    SWB = {Api.IB: 'SWB', Api.TV: ''}
    VSE = {Api.IB: 'VSE', Api.TV: ''}

    @classmethod
    def decode(cls, name: str, from_api: Api) -> str:
        """Decode from specific api notation to Barbucket notation"""

        # IB inconsistently uses the names 'island' and 'nasdaq'
        if (from_api == Api.IB) and (name == 'NASDAQ'):
            name = 'ISLAND'
        return super().decode(name=name, from_api=from_api)


class ContractType(Encoding):
    COMMON_STOCK = {Api.IB: 'COMMON', Api.TV: ''}
    ETF = {Api.IB: 'ETF', Api.TV: ''}
    ETC = {Api.IB: 'ETC', Api.TV: ''}
    ETN = {Api.IB: 'ETN', Api.TV: ''}
    ETP = {Api.IB: 'ETP', Api.TV: ''}
    ADR = {Api.IB: 'ADR', Api.TV: ''}
    BOND = {Api.IB: 'BOND', Api.TV: ''}
    CLOSED_END_FUND = {Api.IB: 'CLOSED_END_FUND', Api.TV: ''}
    CONV_PREFERRED = {Api.IB: 'CONVPREFERRED', Api.TV: ''}
    DUTCH_CERT = {Api.IB: 'DUTCH CERT', Api.TV: ''}
    FUND_OF_FUNDS = {Api.IB: 'FUND OF FUNDS', Api.TV: ''}
    GDR = {Api.IB: 'GDR', Api.TV: ''}
    GERMAN_CERT = {Api.IB: 'GERMAN CERT', Api.TV: ''}
    LDT_PART = {Api.IB: 'LDT PART', Api.TV: ''}
    MLP = {Api.IB: 'MLP', Api.TV: ''}
    NY_REG_SHRS = {Api.IB: 'NY REG SHRS', Api.TV: ''}
    OPEN_END_FUND = {Api.IB: 'OPEN-END FUND', Api.TV: ''}
    PREFERENCE = {Api.IB: 'PREFERENCE', Api.TV: ''}
    PREFERRED = {Api.IB: 'PREFERRED', Api.TV: ''}
    REIT = {Api.IB: 'REIT', Api.TV: ''}
    RIGHT = {Api.IB: 'RIGHT', Api.TV: ''}
    ROYALTY_TRUST = {Api.IB: 'ROYALTY TRST', Api.TV: ''}
    SAVINGS_SHARE = {Api.IB: 'SAVINGS SHARE', Api.TV: ''}
    TRACKING_STOCK = {Api.IB: 'TRACKING STK', Api.TV: ''}
    UNIT = {Api.IB: 'UNIT', Api.TV: ''}
    US_DOMESTIC = {Api.IB: 'US DOMESTIC', Api.TV: ''}
import logging
from typing import Any, List

import enlighten

from .mediator import Mediator
from .base_component import BaseComponent
from .encoder import Encoder
from .signal_handler import SignalHandler
from .custom_exceptions import (
    QueryReturnedNoResultError,
    QueryReturnedMultipleResultsError,
    TwsSystemicError,
    TwsContractRelatedError)

logger = logging.getLogger(__name__)


class IbDetailsProcessor(BaseComponent):
    """Downloading of contract details from IB TWS and storing to db"""

    def __init__(self, mediator: Mediator = None) -> None:
        self.mediator: Mediator = mediator
        self.__contracts: List[Any] = None
        self.__details: Any = None
        self.__pbar: Any = None
        self.__signal_handler = SignalHandler()

        # Setup progress bar
        manager = enlighten.get_manager()
        self.__pbar = manager.counter(
            total=0,
            desc="Contracts", unit="contracts")

    def update_ib_contract_details(self) -> None:
        """Download and store all missing contract details entries from IB TWS."""

        self.__get_contracts()
        self.__pbar.total = len(self.__contracts)
        self.__connect_tws()
        try:
            for contract in self.__contracts:
                if self.__check_abort_conditions():
                    break  # todo: should be an exception to handle it better
                try:
                    self.__get_contract_details_from_tws(contract)
                    self.__validate_details()
                except TwsContractRelatedError as e:
                    self.__handle_tws_contract_related_error(e)
                except QueryReturnedNoResultError as e:
                    self.__handle_no_result_error(e)
                except QueryReturnedMultipleResultsError as e:
                    self.__handle_multiple_results_error(e)
                else:
                    self.__decode_exchange_names()
                    self.__insert_ib_details_into_db(contract)
                finally:
                    self.__pbar.update(inc=1)
        except TwsSystemicError as e:
            self.__handle_tws_systemic_error(e)
        finally:
            self.__disconnect_tws()

    def __get_contracts(self) -> None:
        """Get contracts from db, where IB details are missing"""

        columns = [
            'contract_id', 'contract_type_from_listing', 'broker_symbol',
            'exchange', 'currency']
        filters = {'primary_exchange': "NULL"}
        parameters = {'filters': filters, 'return_columns': columns}
        self.__contracts = self.mediator.notify("get_contracts", parameters)
        logger.debug(f"Found {len(self.__contracts)} contracts with missing "
                     f"IB details in master listing.")

    def __connect_tws(self) -> None:
        """Connect to TWS app"""
        self.mediator.notify("connect_to_tws")

    def __disconnect_tws(self) -> None:
        """Disconnect from TWS app"""
        self.mediator.notify("disconnect_from_tws")

    def __check_abort_conditions(self) -> bool:
        """Check conditions to abort operation."""

        if (self.__signal_handler.exit_requested()
                or self.mediator.notify("tws_has_error")):
            return True
        else:
            return False

    def __get_contract_details_from_tws(self, contract: Any) -> None:
        """Download contract details over TWS."""

        parameters = {
            'contract_type_from_listing': contract['contract_type_from_listing'],
            'broker_symbol': contract['broker_symbol'],
            'exchange': contract['exchange'],
            'currency': contract['currency']}
        self.__details = self.mediator.notify(
            "download_contract_details_from_tws", parameters)

    def __validate_details(self) -> None:
        if len(self.__details) == 0:
            raise QueryReturnedNoResultError
        elif len(self.__details) > 1:
            raise QueryReturnedMultipleResultsError
        else:
            self.__details = self.__details[0]

    def __decode_exchange_names(self) -> None:
        """Decode exchange names"""
        self.__details.contract.exchange = Encoder.decode_exchange_ib(
            self.__details.contract.exchange)
        self.__details.contract.primaryExchange = Encoder.decode_exchange_ib(
            self.__details.contract.primaryExchange)

    def __insert_ib_details_into_db(self, contract: Any) -> None:
        """Insert contract details into db"""
        self.mediator.notify("insert_ib_details", {
            'contract_id': contract['contract_id'],
            'contract_type_from_details': self.__details['contract_type_from_details'],
            'primary_exchange': self.__details['primary_exchange'],
            'industry': self.__details['industry'],
            'category': self.__details['category'],
            'subcategory': self.__details['subcategory)']})

    def __handle_tws_contract_related_error(self, e):
        logger.warning(
            f"Contract-related problem in TWS detected: {e.req_id}, "
            f"{e.contract}, {e.error_code}, {e.error_string}")
        self.mediator.notify(
            "show_cli_message",
            {'message': (
                f"Details request {e.req_id} for contract {e.contract} "
                f"returned error {e.error_code}: {e.error_string}")})

    def __handle_tws_systemic_error(self, e):
        logger.error(
            f"Systemic problem in TWS connection detected: {e.req_id}, "
            f"{e.contract}, {e.error_code}, {e.error_string}")
        self.mediator.notify(
            "show_cli_message",
            {'message': (
                f"Details request {e.req_id} for contract{e.contract} "
                f"returned error {e.error_code}: {e.error_string}")})

    def __handle_no_result_error(self, e):
        logger.warning(f"__handle_no_result_error")
        self.mediator.notify(
            "show_cli_message",
            {'message': "__handle_no_result_error"})

    def __handle_multiple_results_error(self, e):
        logger.warning(f"__handle_multiple_results_error")
        self.mediator.notify(
            "show_cli_message",
            {'message': "__handle_multiple_results_error"})

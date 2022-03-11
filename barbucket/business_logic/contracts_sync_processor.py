import logging

from sqlalchemy.orm import Session

from barbucket.datasource_connectors.ib_exchange_listing_reader import IbExchangeListingReader
from barbucket.persistence.data_managers import ContractsDbManager
from barbucket.domain_model.data_classes import Contract
from barbucket.domain_model.types import ContractType, Exchange
from barbucket.util.custom_exceptions import ExitSignalDetectedError


_logger = logging.getLogger(__name__)


class ContractSyncProcessor():
    def __init__(self,
                 listing_reader: IbExchangeListingReader,
                 contracts_db_manager: ContractsDbManager,
                 orm_session: Session) -> None:
        self._listing_reader = listing_reader
        self._contracts_db_manager = contracts_db_manager
        self._orm_session = orm_session

    def sync_contracts_to_listing(self, exchange: Exchange) -> None:

        # Get contracts
        try:
            web_contracts = self._listing_reader.read_ib_exchange_listing(
                exchange=exchange)
        except ExitSignalDetectedError as e:
            _logger.info(e.message)
            return
        contract_filters = (
            Contract.contract_type == ContractType.STOCK.name,
            Contract.exchange == exchange.name)
        db_contracts = self._contracts_db_manager.get_by_filters(
            filters=contract_filters)

        # Find removed contracts
        removed_contracts = []
        for contract in db_contracts:
            if contract not in web_contracts:
                self._orm_session.delete(contract)
                removed_contracts.append(contract)

        # Find addded contracts
        added_contracts = []
        for contract in web_contracts:
            if contract not in db_contracts:
                self._orm_session.add(contract)
                added_contracts.append(contract)

        # Execute
        if True:  # User acknowledge
            self._orm_session.commit()
        else:
            self._orm_session.rollback()
        self._orm_session.close()

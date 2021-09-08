import logging

import click

from .base_component import BaseComponent
from .mediator import Mediator


class CommandLineInterface(BaseComponent):
    """Docstring"""

    def __init__(self, mediator: Mediator = None) -> None:
        self.mediator = mediator

    # Initial group. This method is called to run the cli.
    @click.group()
    def cli(self) -> None:
        pass

    # Group database
    @cli.group()
    def database(self) -> None:
        """Local database commands"""

    @database.command()
    @click.confirmation_option(prompt="Are you sure you want to archive the current database?")
    def archive(self) -> None:
        """Archive the local database"""
        logging.info(f"User requested to archive the datebase cia the cli.")
        self.mediator.notify("archive_database")
        click.echo("Successfully archived database.")

    # Group contracts
    @cli.group()
    def contracts(self) -> None:
        """Contracts commands"""

    @contracts.command()
    @click.option("-t", "--type", "contract_type", required=True, type=str)
    @click.option("-e", "--exchange", "exchange", required=True, type=str)
    def sync_listing(self, contract_type: str, exchange: str) -> None:
        """Sync master listing to IB exchange listing"""
        logging.info(f"User requested to sync '{contract_type}' contracts on "
                     f"'{exchange}' to master listing via the cli.")
        self.mediator.notify(
            "sync_contracts_to_listing",
            {'ctype': contract_type.upper(),
             'exchange': exchange.upper()})
        click.echo(f"Master listing synced for {contract_type.upper()} on "
                   f"{exchange.upper()}.")

    @contracts.command()
    def download_ib_details(self) -> None:
        """Fetch details for all contracts from IB TWS"""
        logging.info(f"User requested to download details from TWS via the cli"
                     f".")
        self.mediator.notify("update_ib_contract_details")
        click.echo("Updated IB details for master listings.")

    @contracts.command()
    def read_tv_details(self) -> None:
        """Read details for all contracts from TV files"""
        logging.info(f"User requested to read and store details from tv files "
                     f"via the cli.")
        self.mediator.notify("read_tv_data")
        click.echo(f"Finished reading TV files.")

    # Group quotes
    @cli.group()
    def quotes(self) -> None:
        """Quotes commands"""

    @quotes.command()
    @click.option("-u", "--universe", "universe", required=True, type=str)
    def fetch(self, universe: str) -> None:
        """Fetch quotes from IB TWS"""
        logging.info(f"User requested to download quotes from TWS for "
                     f"universe '{universe}' via the cli.")
        self.mediator.notify(
            "download_historical_quotes",
            {'universe': universe})
        click.echo(f"Finished downloading historical data for universe "
                   f"'{universe}'")

    # Group universes
    @cli.group()
    def universes(self) -> None:
        """Universes commands"""

    @universes.command()
    @click.option("-n", "--name", "name", required=True, type=str)
    @click.option("-c", "--contract_ids", "contract_ids", required=True, type=str)
    def create(self, name: str, contract_ids: str) -> None:
        """Create new universe"""
        logging.info(f"User requested to create universe '{name}' with "
                     f"{len(contract_ids)} members via the cli.")
        con_list = [int(n) for n in contract_ids.split(",")]
        self.mediator.notify(
            "create_universe",
            {'name': name, 'contract_ids': con_list})
        click.echo(f"Created universe '{name}' with {len(contract_ids)} "
                   f"members.")

    @universes.command()
    def list(self) -> None:
        """List all universes"""
        logging.info(f"User requestet to list all universes via the cli.")
        universes = self.mediator.notify("get_universes")
        click.echo(universes)

    @universes.command()
    @click.option("-n", "--name", "name", required=True, type=str)
    def members(self, name: str) -> None:
        """List universes members"""
        logging.info(f"User requestet to list the members for universe "
                     f"'{name}' via the cli.")
        members = self.mediator.notify(
            "get_universe_members",
            {'universe': name})
        click.echo(members)

    @universes.command()
    @click.option("-n", "--name", "name", required=True, type=str)
    @click.confirmation_option(prompt="Are you sure you want to delete this universe?")
    def delete(self, name: str) -> None:
        """Delete universe"""
        logging.info(f"User requestet to delete universe '{name}' via the "
                     f"cli.")
        self.mediator.notify(
            "delete_universe",
            {'universe': name})
        click.echo(f"Deleted universe '{name}'.")

    def exiter_message(self) -> None:
        click.echo("Ctrl-C detected, gracefully stopping operation. Press "
                   f"again to stop immediately.")
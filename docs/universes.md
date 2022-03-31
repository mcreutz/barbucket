# Universes
To conveniently handle the contracts, you can group them to universes.

## Listing all existing universes
```console
$ barbucket universes list
````

## Creating a new universe
```console
$ barbucket universes create --name my_universe --contract_ids 1,2,3
```
`--name` Name of the universe to create<br>
`--contract_ids` The ``contracts_ids`` are automatically assigned to the contracts by the software on their creation and need to be obtained manually from the database.

## Getting all members of a universe
```console
$ barbucket universes members --name my_universe
```
`--name` Name of the universe to get the members for

## Deleting a universe
```console
$ barbucket universes delete --name my_universe
```
`--name` Name of the universe to delete
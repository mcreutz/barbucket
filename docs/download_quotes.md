# Quotes downloading
To download historical quotes, IB's TWS needs to be running and API access enabled. Then execute

```console
$ barbucket quotes fetch --universe my_universe
```
`--universe` Name of the universe to download quotes for

## Restrictions
- Right now, only daily quotes are supported
- End-date will always be today
- Duration will be 15 years or shorter, if youngest existing quote is newer
- IB is enforcing strict speedlimits, so downloading quotes on IB for many contracts will need some time.

## Configuration
Some adjustments to the process can be changed in the `config.ini` at
`{your_local_user_directory}/.barbucket/config.ini`
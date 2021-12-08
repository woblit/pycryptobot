import ast
import json
import os.path
import re
import sys
import yaml
from yaml.constructor import ConstructorError
from yaml.scanner import ScannerError

from .default_parser import isCurrencyValid, defaultConfigParse
from models.exchange.Granularity import Granularity

def isMarketValid(market) -> bool:
    p = re.compile(r"^[0-9A-Z]{1,10}\-[1-9A-Z]{2,5}$")
    return p.match(market) is not None

def parseMarket(market):
    if not isMarketValid(market):
        raise ValueError(f'Selected market is invalid: {market}')

    base_currency, quote_currency = market.split('-', 2)
    return market, base_currency, quote_currency

def merge_config_and_args(exchange_config, args):
    new_config = {}
    if "config" in exchange_config and exchange_config["config"] is not None:
        new_config = {**exchange_config["config"]}
    for (key, value) in args.items():
        if value is not None and value is not False:
            new_config[key] = value
    return new_config

def parser(app, strategy_config, args={}):
    #print('Strategy Specific Config Configuration parse')

    if not app:
        raise Exception('No app is passed')

    strategy_config_file = strategy_config["config_file"]

    if isinstance(strategy_config, dict):
        if os.path.isfile(strategy_config_file):
            try:
                with open(strategy_config_file, "r", encoding="utf8") as stream:
                    try:
                        strategy_custom_config = yaml.safe_load(stream)
                    except:
                        try:
                            stream.seek(0)
                            strategy_custom_config = json.load(stream)
                        except json.decoder.JSONDecodeError as err:
                            sys.tracebacklimit = 0
                            raise ValueError(f"Invalid Strategy Config File: {str(err)}")

            except (ScannerError, ConstructorError) as err:
                sys.tracebacklimit = 0
                raise ValueError(
                    f"Invalid config: cannot parse config file: {str(err)}"
                )

            except (IOError, FileNotFoundError) as err:
                sys.tracebacklimit = 0
                raise ValueError(f"Invalid config: cannot open config file: {str(err)}")

            except ValueError as err:
                sys.tracebacklimit = 0
                raise ValueError(f"Invalid config: {str(err)}")

            except:
                raise
    else:
        strategy_config = {}

    #print(strategy_custom_config[strategy_config["exchange"]])

    config = merge_config_and_args(strategy_custom_config[strategy_config["exchange"]],args)

    defaultConfigParse(app, config)

    app.strategy_module_config = strategy_custom_config[strategy_config["exchange"]]["config"]
    #print (app.strategy_module_config)


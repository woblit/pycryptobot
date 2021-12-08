from datetime import datetime
from pandas import DataFrame
from models.PyCryptoBot import PyCryptoBot
from models.AppState import AppState
from models.helper.LogHelper import Logger
import sys
import importlib
from  models.helper.ModuleHelper import CanImportModule,ImportModule


class StrategyBase:
    def __init__(
        self,
        app: PyCryptoBot = None,
        state: AppState = AppState,
        df: DataFrame = DataFrame,
        iterations: int = 0,
    ) -> None:
        if not isinstance(df, DataFrame):
            raise TypeError("'df' not a Pandas dataframe")

        if len(df) == 0:
            raise ValueError("'df' is empty")

        self._action = "WAIT"
        self.app = app
        self.state = state
        self._df = df
        self._df_last = app.getInterval(df, iterations)

        self.strategy = ImportModule(app.strategy_config["module"], app.strategy_config["module_class"])

    def isBuySignal(
         self, app, price, now: datetime = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
     ) -> bool:
       
        return self.strategy.isBuySignal(self, app, price, now)

    def isSellSignal(self) -> bool:

        return self.strategy.isSellSignal(self)

    def isSellTrigger(
         self,
         app,
         price: float = 0.0,
         price_exit: float = 0.0,
         margin: float = 0.0,
         change_pcnt_high: float = 0.0,
         obv_pc: float = 0.0,
         macdltsignal: bool = False,
     ) -> bool:
        
        return self.strategy.isSellTrigger(self,app,price,margin,change_pcnt_high,obv_pc,macdltsignal)

    def isWaitTrigger(self, app, margin: float = 0.0, goldencross: bool = False):

        return self.strategy.isWaitTrigger(self,app,margin,goldencross)

    def getAction(self, app, price, dt):
        if self.isBuySignal(app, price, dt):
            return "BUY"
        elif self.isSellSignal():
            return "SELL"
        else:
            return "WAIT"

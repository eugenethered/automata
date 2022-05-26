from typing import Optional

from exchange.InstrumentExchangesHolder import InstrumentExchangesHolder
from exchangerepo.repository.ExchangeRateRepository import ExchangeRateRepository
from exchangerepo.repository.InstrumentExchangeRepository import InstrumentExchangeRepository
from oracle.resolve.PredictionResolver import PredictionResolver
from positionrepo.repository.PositionRepository import PositionRepository
from tradestrategy.TradeStrategizor import TradeStrategizor

from automata.exception.AutomataRequirementMissingException import AutomataRequirementMissingException


class Automata:

    def __init__(self, options):
        self.options = options
        # repositories
        self.position_repository: Optional[PositionRepository] = None
        self.instrument_exchange_repository: Optional[InstrumentExchangeRepository] = None
        self.exchange_rate_repository: Optional[ExchangeRateRepository] = None
        # required dependencies
        self.prediction_resolver: PredictionResolver = Optional[None]
        self.trade_strategizor: TradeStrategizor = Optional[None]
        # data
        self.instrument_exchanges_holder: InstrumentExchangesHolder = Optional[None]
        # control init
        self.__init_in_sequence()

    def __init_in_sequence(self):
        self.init_repositories()
        self.init_prediction_resolver()
        self.init_trade_strategizor()
        self.pre_load_data()

    def init_repositories(self):
        self.position_repository = PositionRepository(self.options)
        self.instrument_exchange_repository = InstrumentExchangeRepository(self.options)
        self.exchange_rate_repository = ExchangeRateRepository(self.options)

    def init_prediction_resolver(self):
        if self.prediction_resolver is None:
            raise AutomataRequirementMissingException('Prediction Resolver is required! Implement "init_prediction_resolver"')

    def init_trade_strategizor(self):
        if self.trade_strategizor is None:
            raise AutomataRequirementMissingException('Trade Strategizor is required! Implement "init_trade_strategizor"')

    def pre_load_data(self):
        self.instrument_exchanges_holder = self.instrument_exchange_repository.retrieve()

    def run(self):
        position = self.position_repository.retrieve()

        instant = position.instant
        instrument = position.instrument
        exchanged_from = position.exchanged_from

        instrument_exchanges = self.instrument_exchanges_holder.get(instrument)
        exchange_rates = self.exchange_rate_repository.retrieve_multiple(instrument_exchanges, instrument, instant)

        prediction = self.prediction_resolver.resolve(instrument, exchange_rates, exchanged_from, instant)

        self.trade_strategizor.trade(position, prediction)

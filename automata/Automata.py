from exchangerepo.repository.ExchangeRateRepository import ExchangeRateRepository
from oracle.resolve.PredictionResolver import PredictionResolver
from positionrepo.repository.PositionRepository import PositionRepository
from tradestrategy.TradeStrategizor import TradeStrategizor

from automata.exception.AutomataRequirementMissingException import AutomataRequirementMissingException


class Automata:

    def __init__(self, options):
        self.options = options
        # repositories
        self.position_repository: PositionRepository = None
        self.exchange_rate_repository: ExchangeRateRepository = None
        # required dependencies
        self.prediction_resolver: PredictionResolver = None
        self.trade_strategizor: TradeStrategizor = None
        self.__init_in_sequence()

    def __init_in_sequence(self):
        self.init_repositories()
        self.init_prediction_resolver()
        self.init_trade_strategizor()

    def init_repositories(self):
        self.position_repository = PositionRepository(self.options)
        self.exchange_rate_repository = ExchangeRateRepository(self.options)

    def init_prediction_resolver(self):
        if self.prediction_resolver is None:
            raise AutomataRequirementMissingException('Prediction Resolver is required! Implement "init_prediction_resolver"')

    def init_trade_strategizor(self):
        if self.trade_strategizor is None:
            raise AutomataRequirementMissingException('Trade Strategizor is required! Implement "init_trade_strategizor"')

    def run(self):
        position = self.position_repository.retrieve()

        # todo: time frame now

        # todo: need exchangeable (instruments) + time frame
        exchange_rates = self.exchange_rate_repository.retrieve_multiple()

        prediction = self.prediction_resolver.resolve(position.instrument, exchange_rates)

        self.trade_strategizor.trade(position, prediction)

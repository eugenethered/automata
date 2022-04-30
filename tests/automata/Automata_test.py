import unittest

from cache.holder.RedisCacheHolder import RedisCacheHolder
from oracle.Oracle import Oracle
from oracle.resolve.PredictionResolver import PredictionResolver

from automata.Automata import Automata
from automata.exception.AutomataRequirementMissingException import AutomataRequirementMissingException


class AutomataTestCase(unittest.TestCase):

    def setUp(self):
        self.options = {
            'REDIS_SERVER_ADDRESS': '192.168.1.90',
            'REDIS_SERVER_PORT': 6379,
            'POSITION_KEY': 'test:position',
            'TIMESERIES_KEY': 'test-time-series:exchange-rate:{}'
        }
        self.cache = RedisCacheHolder(self.options)

    def test_should_raise_error_when_prediction_resolver_missing(self):
        with self.assertRaises(AutomataRequirementMissingException) as rm:
            Automata(self.options)
        self.assertEqual('Prediction Resolver is required! Implement "init_prediction_resolver"', str(rm.exception))

    def test_should_raise_error_when_trade_strategy_processor_missing(self):
        with self.assertRaises(AutomataRequirementMissingException) as rm:
            class SimpleAutomata(Automata):
                def init_prediction_resolver(self):
                    simple_oracles = [Oracle()]
                    self.prediction_resolver = PredictionResolver(simple_oracles)
            SimpleAutomata(self.options)
        self.assertEqual('Trade Strategy Processor is required! Implement "init_trade_strategy_processor"', str(rm.exception))


if __name__ == '__main__':
    unittest.main()

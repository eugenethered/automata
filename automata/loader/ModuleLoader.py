import importlib
import logging
from typing import TypeVar

from automata.exception.AutomataRequirementMissingException import AutomataRequirementMissingException

T = TypeVar('T')


class ModuleLoader:

    def __init__(self, module_reference):
        self.log = logging.getLogger(__name__)
        self.module_reference = module_reference

    def load_module(self, module_reference) -> T:
        try:
            module = importlib.import_module(module_reference)
            print(module)
            return module
        except ModuleNotFoundError as error:
            self.log.warning(f'Unable to load module {error.msg}')
            raise AutomataRequirementMissingException(error.msg)

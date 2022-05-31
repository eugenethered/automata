from automata.loader.ModuleLoader import ModuleLoader


class OracleModuleLoader(ModuleLoader):

    def __init__(self, module_reference):
        super().__init__(module_reference)

    def initialize_oracles(self):
        oracles = []
        oracle_references = self.module_reference.split(',')
        for oracle_reference in oracle_references:
            oracle = self.load_module(oracle_reference)
            oracles.append(oracle)
        return oracles

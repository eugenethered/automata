import logging
import time

from cache.holder.RedisCacheHolder import RedisCacheHolder

from automata.Automata import Automata

if __name__ == '__main__':

    options = {
        'REDIS_SERVER_ADDRESS': '192.168.1.90',
        'REDIS_SERVER_PORT': 6379,
        'MARKET': '[--WHICH-MARKET--]',
        'PROCESS_KEY': '{}:process:status:{}',
        'PROCESS_RUN_PROFILE_KEY': '{}:process:run-profile:{}'
    }

    logging.basicConfig(level=logging.DEBUG)

    RedisCacheHolder(options)

    start_time = time.perf_counter()

    conductor = Automata(options)
    conductor.run()

    end_time = time.perf_counter()
    print(f"Completed in {end_time - start_time:0.4f} seconds")

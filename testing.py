from collector import DataCollector
import time

inputs = list(range(0, 505, 5))

collect = DataCollector(iterations=5, trigger='b', data_type='out', period=1000)

collect.collect_data(time_per_sample='160e-9', phases=inputs)
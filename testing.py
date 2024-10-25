from collector import DataCollector
import time

inputs = [0]

collect = DataCollector(iterations=5, trigger='a', data_name='rising_falling', period=1000)

collect.collect_single(time_per_sample=41e-6, label='out_comp')

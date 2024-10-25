from collector import DataCollector
import time

inputs = [0,5]

<<<<<<< HEAD
collect = DataCollector(iterations=5, trigger='b', data_type='R2=10K_R1=10K', period=1000)
=======
collect = DataCollector(iterations=5, trigger='b', data_type='out', period=1000)
>>>>>>> 4e411aa5c2c5d211717e09f37d30ad40a5811aa1

collect.collect_data(time_per_sample=160e-9, phases=inputs)
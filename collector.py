from PLL_Lib import Arduino, Picoscope
from typing import List
import csv
import numpy as np
import time
import os

class DataCollector:
    def __init__(self, period, phase, iterations):
        """
        Takes input period & phase (processed as microseconds).
        Iteration count for averaging passed as int.
        """
        assert isinstance(iterations, int)

        self.period = period
        self.phase = phase
        self.iterations = iterations

        self.map = {
            10e-9: '10ns',
            20e-9: '20ns',
            40e-9: '40ns',
            80e-9: '80ns',
            160e-9: '160ns',
            1e-6: '1micro_s',
            3e-6: '3micro_s',
            5e-6: '5micro_s',
            1e-5: '10micro_s',
            2e-5: '20micro_s',
            4.1e-5: '41micro_s',
            8.2e-5: '82micro_s',
            1.64e-4: '164micro_s',
            3.28e-4: '328micro_s',
            1e-3: '1ms',
            3e-3: '3ms',
            5e-3: '5ms',
            1e-2: '10ms'
        }

    def collect_data(self, time_per_sample: float) -> None:
        """
        For loops for <iterations> to collect voltages & time data.
        Each loop of the Picoscope reading takes ~1000 readings.
        Readings are spaced by <time_per_sample>.
        Each call of <get_trace> collects a vector of the data.
        """
        # check there are at least 50 samples per cycle
        assert self.period / time_per_sample >= 50
        # check there are at least 10 samples per phase length
        if self.phase != 0:
            assert self.phase / time_per_sample >= 10

        # eg inputs:
        # period = 100micro_s, phase = 10micro_s, time_per_sample = 1e-6

        with Arduino() as arduino:
            if time_per_sample not in self.map:
                time_per_sample = '5micro_s'
            else:
                time_per_sample = self.map[time_per_sample]

            with Picoscope(time_per_sample=time_per_sample, probe_10x=True, trigger_channel='a') as scope:
                # function takes input period and passes the half_period to arduino
                # eg inputs:
                # period = 100, phase = 10
                # channel1 on -> 10micro_s -> channel2 on
                # -> 40micro_s -> channel1 off -> 10micro_s
                # -> channel2 off -> 40micro_s

                s = f'{self.period / 2},{self.phase}#'
                arduino.send_code(s)

                time.sleep(1)

                _, voltage_ref, _ = scope.wait_for_key('s', 'Press to start')
                
                voltages_a = np.zeros((self.iterations, voltage_ref.size), dtype=float)
                voltages_b = np.zeros_like(voltages_a, dtype=float)

                for i in range(self.iterations):
                    _, v_a, v_b = scope.get_trace(f'Caputring trace {i}...')
                    voltages_a[i] = v_a
                    voltages_b[i] = v_b
        
            dir_path = f'out_{self.period}_{self.phase}'
            os.mkdir(dir_path)
            os.chdir(dir_path)

            for i in range(self.iterations):
                with open(f'iteration={i+1}.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['V_A', 'V_B'])

                    for j in range(voltages_a.shape[1]):
                        a = voltages_a[i, j]
                        b = voltages_b[i, j]
                        writer.writerow([1 if a>=2 else 0, 1 if b>=2 else 0])

            os.chdir(os.path.dirname(os.path.abspath(__file__)))






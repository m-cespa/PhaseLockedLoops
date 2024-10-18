from PLL_Lib import Arduino, Picoscope
from typing import List
import csv
import numpy as np

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
        # period = 100, phase = 10, time_per_sample = 1e-6

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

                _, voltage_ref, _ = scope.wait_for_key('s', 'Press to start')
                
                times = np.zeros((self.iterations, voltage_ref.size))
                voltages_a = np.zeros_like(times)
                voltages_b = np.zeros_like(times)

                for i in range(self.iterations):
                    t, v_a, v_b = scope.get_trace(f'Caputring trace {i}...')
                    times[i] = t
                    voltages_a[i] = v_a
                    voltages_b[i] = v_b
        
        with open(f'out_{self.period}_{self.phase}.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Iteration', 'Times', 'V_A', 'V_B'])
            for i in range(self.iterations):
                writer.writerow([i+1, times[i], voltages_a[i], voltages_b[i]])






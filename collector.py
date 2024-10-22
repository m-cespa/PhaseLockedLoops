from PLL_Lib import Arduino, Picoscope
from typing import List, Tuple
import csv
import numpy as np
import time
import os

class DataCollector:
    def __init__(self, iterations: int, trigger: str, data_type: str, period: float):
        """
        Initializes the DataCollector with specified parameters.
        :param iterations: Number of iterations for averaging.
        :param trigger: Trigger channel for the Picoscope.
        :param data_type: Type of data being collected, used for folder naming.
        """
        assert isinstance(iterations, int)

        self.iterations = iterations
        self.trigger = trigger
        self.data_type = data_type
        self.period = period

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

    def send_code(self, phase: float) -> None:
        with Arduino() as arduino:
            s = f'{self.period / 2},{phase}#'
            arduino.send_code(s)

    def collect_data(self, time_per_sample: float, phases: List[float]) -> None:
        """
        Collects voltage and time data from the Picoscope for the specified iterations and inputs.
        :param time_per_sample: Time per sample for the Picoscope.
        :param inputs: List of tuples containing period and phase values.
        """
        if time_per_sample not in self.map:
            time_per_sample = '5micro_s'
        else:
            time_per_sample = self.map[time_per_sample]

        with Picoscope(time_per_sample=time_per_sample, probe_10x=True, trigger_channel=self.trigger) as scope:
            _, voltage_ref, _ = scope.wait_for_key('s', 'Press to start')

            n = len(phases)
            # Create the base directory for saving data
            base_dir = os.path.abspath(f"{self.data_type}_period={self.period}")
            os.makedirs(base_dir, exist_ok=True)

            for i in range(n):
                phase = phases[i]
                dir_path = os.path.join(base_dir, f'{self.data_type}_{self.period}_{phase}')
                os.makedirs(dir_path, exist_ok=True)

                self.send_code(phase)

                time.sleep(1)

                # Initialize arrays to hold voltage readings
                voltages_a = np.zeros((self.iterations, voltage_ref.shape[0]))
                voltages_b = np.zeros_like(voltages_a)

                for j in range(self.iterations):
                    _, v_a, v_b = scope.get_trace(f'Capturing trace {j + 1} for input {i + 1}...')
                    voltages_a[j] = v_a
                    voltages_b[j] = v_b

                # Write the data to CSV files
                for k in range(self.iterations):
                    with open(os.path.join(dir_path, f'iteration={k + 1}.csv'), 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(['V_A', 'V_B'])

                        for l in range(voltages_a.shape[1]):
                            a = voltages_a[k, l]
                            b = voltages_b[k, l]
                            writer.writerow([1 if a >= 2 else 0, 1 if b >= 2 else 0])
                time.sleep(1)

            # Change back to the original directory (optional)
            os.chdir(os.path.dirname(os.path.abspath(__file__)))






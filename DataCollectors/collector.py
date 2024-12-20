from PLL_Lib import Arduino, Picoscope
from typing import List, Tuple
import csv
import numpy as np
import time
import os

class DataCollector:
    def __init__(self, iterations: int, trigger: str, data_name: str, period: float):
        """
        Initializes the DataCollector with specified parameters.
        :param iterations: Number of iterations for averaging.
        :param trigger: Trigger channel for the Picoscope.
        :param data_type: Type of data being collected, used for folder naming.
        """
        assert isinstance(iterations, int)

        self.iterations = iterations
        self.trigger = trigger
        self.data_name = data_name
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

    def gen_code(self, phase: float) -> str:
        s = f'{self.period / 2},{phase}#'
        return s
    
    def collect_single(self, time_per_sample: float, label: str) -> None:
        """
        Collects voltage data and saves it to a CSV file.
        """
        if time_per_sample not in self.map:
            t = '5micro_s'
        else:
            t = self.map[time_per_sample]

        print(f'\nTime_per_sample = {t}\n')

        with Picoscope(time_per_sample=t, probe_10x=True, trigger_channel=self.trigger) as scope:
            _, voltage_ref, _ = scope.wait_for_key('s', 'Press to start')

            _, v_a, v_b = scope.get_trace('Capturing data...\n')

            # Specify the filename directly
            file_path = f"{self.data_name}_{label}.csv"
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['OUT', 'IN'])  # Header for the single column

                # Write each value of voltages_a into the column
                for i in range (v_a.shape[0]):
                    val_a = v_a[i]
                    val_b = v_b[i]

                    if val_a > 4:
                        val_a = 2
                    elif val_a > 1.5:
                        val_a = 1
                    else:
                        val_a = 0

                    writer.writerow([val_a, 1 if val_b > 4 else 0])

    def collect_data(self, time_per_sample: float, phases: List[float]) -> None:
        """
        Collects voltage and time data from the Picoscope for the specified iterations and inputs.
        :param time_per_sample: Time per sample for the Picoscope.
        :param inputs: List of tuples containing period and phase values.
        """
        if time_per_sample not in self.map:
            t = '5micro_s'
        else:
            t = self.map[time_per_sample]

        print(f'\nTime_per_sample = {t}\n')

        with Arduino() as arduino:

            with Picoscope(time_per_sample=t, probe_10x=True, trigger_channel=self.trigger) as scope:
                _, voltage_ref, _ = scope.wait_for_key('s', 'Press to start')

                n = len(phases)
                # Create the base directory for saving data
                base_dir = os.path.abspath(f"{self.data_name}_period={self.period}")
                os.makedirs(base_dir, exist_ok=True)

                for i in range(n):
                    phase = phases[i]
                    dir_path = os.path.join(base_dir, f'{self.data_name}_{self.period}_{phase}')
                    os.makedirs(dir_path, exist_ok=True)

                    arduino.send_code(self.gen_code(phase))

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
                                writer.writerow([a, 1 if b >= 4 else 0])
                    time.sleep(1)

                # Change back to the original directory (optional)
                os.chdir(os.path.dirname(os.path.abspath(__file__)))







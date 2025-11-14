import nidaqmx
from nidaqmx.constants import TerminalConfiguration

with nidaqmx.Task() as task:
    # Add an analog input voltage channel (e.g., ai0 on device 'Dev1')
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0",
                                         terminal_config=TerminalConfiguration.DIFF,
                                         min_val=-10.0,
                                         max_val=10.0)

    # Read a single sample
    data = task.read()
    print(f"Acquired voltage: {data} V")
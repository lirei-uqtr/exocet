import nidaqmx
from nidaqmx.constants import TerminalConfiguration, AcquisitionType
import pandas as pd
from questdb.ingress import Sender, IngressError
import time
import datetime

# DAQ Configuration
DEVICE = "Dev1"
CHANNELS = "ai0:3"  # Read from 4 channels, ai0 through ai3
SAMPLING_RATE = 10  # Hz

# QuestDB Configuration
QUESTDB_HOST = 'localhost'
QUESTDB_PORT = 9009
TABLE_NAME = 'daq_measurements'

def main():
    try:
        with nidaqmx.Task() as task:
            # Add four analog input voltage channels
            task.ai_channels.add_ai_voltage_chan(
                f"{DEVICE}/{CHANNELS}",
                terminal_config=TerminalConfiguration.DIFF,
                min_val=-10.0,
                max_val=10.0)

            # Configure sampling clock for continuous acquisition
            task.timing.cfg_samp_clk_timing(
                SAMPLING_RATE,
                sample_mode=AcquisitionType.CONTINUOUS,
                samps_per_chan=SAMPLING_RATE * 5)  # 5 second buffer

            print(f"Starting data acquisition from {DEVICE}/{CHANNELS}...")
            print("Press Ctrl+C to stop.")

            conf = f'http::addr={QUESTDB_HOST}:9000;'
            with Sender.from_conf(conf) as sender:
                while True:
                    try:
                        # Read a single sample from each channel
                        data = task.read()
                        
                        # Get current timestamp
                        timestamp = datetime.datetime.now(datetime.timezone.utc)

                        # Create a DataFrame
                        df_data = []
                        for i, voltage in enumerate(data):
                            df_data.append({
                                'timestamp': timestamp,
                                'channel_id': f'ai{i}',
                                'voltage': voltage
                            })
                        
                        df = pd.DataFrame(df_data)

                        # Ingest into QuestDB
                        sender.dataframe(
                            df,
                            table_name=TABLE_NAME,
                            symbols=['channel_id'],
                            at='timestamp')
                        
                        print(f"Ingested {len(df)} rows into QuestDB.")
                        
                        # Wait for the next acquisition cycle
                        time.sleep(1)

                    except IngressError as e:
                        print(f"QuestDB Ingress Error: {e}")
                    except nidaqmx.errors.DaqError as e:
                        print(f"NI DAQmx Error: {e}")
                        # Stop and restart the task on buffer overflow or other errors
                        task.stop()
                        task.start()


    except KeyboardInterrupt:
        print("\nStopping data acquisition.")
    except nidaqmx.errors.DaqError as e:
        print(f"Fatal NI DAQmx Error: {e}")
    finally:
        print("Script finished.")

if __name__ == '__main__':
    main()
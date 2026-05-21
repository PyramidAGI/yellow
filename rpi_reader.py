# On a real Pi with gpiozero installed it reads from MCP3008 channel 0.
# On any other machine it simulates random values.
# Every 5 seconds it logs a cluster to log2.csv.
import time
import template_program

template_program.CONST = 2  # logs to log2.csv

try:
    from gpiozero import MCP3008
    def read_channel(ch):
        return MCP3008(channel=ch).value  # 0.0 to 1.0
except Exception:
    import random
    def read_channel(ch):
        return round(random.uniform(0.0, 1.0), 4)  # simulated on non-Pi hardware

CHANNEL = 0
THRESHOLD = 0.5
INTERVAL = 5  # seconds between readings

def main():
    print(f"Reading analogue channel {CHANNEL} every {INTERVAL}s. Logging to log2.csv. Ctrl+C to stop.")
    while True:
        value = read_channel(CHANNEL)
        voltage = round(value * 3.3, 4)
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%S")
        template_program.log(
            f"analogue channel {CHANNEL} reading",
            [f"channel {CHANNEL};{value};{voltage};{timestamp};;{value};{THRESHOLD};"]
        )
        print(f"[{timestamp}] ch{CHANNEL} = {value} ({voltage}V)")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()

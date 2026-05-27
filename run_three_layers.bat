:: Three-layer architecture: sensor -> transformation -> causal diagram
:: bus.py must run last — it passes messages between node logs.
python rpi_reader.py
python transformation.py
python top.py
python bus.py

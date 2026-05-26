:: Add one line per Python program you want to run.
:: Each program should import template_program.py for logging and LLM problem solving.
:: bus.py must run last — it passes messages between node logs after all other programs have written.
python rpi_reader.py
python bus.py

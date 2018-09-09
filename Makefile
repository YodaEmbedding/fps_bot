.PHONY: all clean run

all: run

clean:
	find . -name '*.pyc'       -exec rm    --force {} +
	find . -name '__pycache__' -exec rm -r --force {} +

run:
	cd fps_bot && python3 fps_bot.py

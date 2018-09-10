.PHONY: all clean run test

all: run

clean:
	find . -name '*.pyc'       -exec rm    --force {} +
	find . -name '__pycache__' -exec rm -r --force {} +

run:
	mkdir -p log/
	cd fps_bot && python3 fps_bot.py

test:
	pytest test/

# Makefile for a Flask application

# Default target executed when no arguments are given to make.
default: run

# Target to create a virtual environment and install dependencies
setup:
	@echo "Creating virtual environment..."
	 virtualenv myenv
#	python3 -m venv myenv
	@echo "Virtual environment created."

# Target to activate the virtual environment
env:
	@echo "Activating virtual environment..."
	source  myenv/bin/activate

# Target to install Python packages
install: setup
	@echo "Installing dependencies..."
	. myenv/bin/activate; pip3 install -r requirements.txt

# Target to run the Flask application
run: install
	@echo "Checking and freeing port 5000 if necessary..."
	@fuser -k 5000/tcp || true
	@echo "Running Flask application..."
	. myenv/bin/activate && FLASK_APP=main.py FLASK_ENV=development flask run --host=127.0.0.1 --port=5000

# Target to clean the project
clean:
	@echo "Cleaning up..."
	rm -rf myenv
	@echo "Clean up done."

.PHONY: default setup env install run clean

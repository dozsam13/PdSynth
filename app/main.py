import tkinter as tk
from pattern import Pattern
from viewmodel import ViewModel
from view import View
from pd_client import PdClient

import logging
import json


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def read_patterns():
	with open('app/patterns.json', 'r') as file:
		data = json.load(file)
	patterns = []
	for pattern_data in data:
		pattern = Pattern()
		pattern.data = pattern_data
		patterns.append(pattern)
	return patterns


def main():
	engine_client = PdClient()
	view = View()
	ptns = read_patterns()
	viewmodel = ViewModel(engine_client, view.root, ptns)

	view.build(viewmodel)
	

if __name__ == "__main__":
	main()


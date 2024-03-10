# Book Scanning Optimization

The Book Scanning problem is from HashCode competition (2020), and the goal of the present project is to solve it using different metaheuristics optimization methods while providing an interactive UI for method, parameters and dataset selection.

## Requirements
The project is developed in Python 3.10, and the following packages are required in order to run the program. Make sure to install them in your environment.

```
import copy
import tracemalloc
import time
import uuid
import tkinter
import io
import sys
import threading
import operator
import csv
import seaborn
import matplotlib
import random
import numpy
```

## User Interface
To run the interactive interface, run the ```app.py``` script.

## Code Changes From Previous Delivery
- Implemented Frequency Based Long Term Memory for TS.
- Changed initial solution to be 50% greedy-originated individuals and 50% random individuals in GA.
- Added a method to save and plot the generation score log to see the population evolution in GA.
- Corrected the 'if log' structure of SA to print even if the solution is not improved in the current iteration.

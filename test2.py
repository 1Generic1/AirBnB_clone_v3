#!/usr/bin/python3
""" Test delete feature
"""
from models.engine.file_storage import FileStorage
from models.state import State

fs = FileStorage()

# Create two State instances
state1 = State()
state2 = State()

# Add the State instances to the storage
fs.new(state1)
fs.new(state2)
fs.save()

# All States
all_states = fs.all(State)
print("All States: {}".format(len(all_states.keys())))
for state_key in all_states.keys():
    print(all_states[state_key])


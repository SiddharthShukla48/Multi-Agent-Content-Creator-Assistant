#!/usr/bin/env python3

# Show the problem in crew_definitions.py and task_definitions.py
import os

print("=== CHECKING TASK DEFINITIONS ===")
task_path = os.path.join("tasks", "task_definitions.py")
with open(task_path, "r") as f:
    content = f.read()
    print(content)

print("\n=== CHECKING CREW DEFINITIONS ===")
crew_path = os.path.join("crews", "crew_definitions.py")
with open(crew_path, "r") as f:
    content = f.read()
    print(content)

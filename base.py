#!/usr/bin/env python3

class TasksCommand:
    TASKS_FILE = "tasks.txt"
    COMPLETED_TASKS_FILE = "completed.txt"

    current_items = {}
    completed_items = []

    def read_current(self):
        try:
            file = open(self.TASKS_FILE, "r")
            for line in file.readlines():
                item = line[:-1].split(" ")
                self.current_items[int(item[0])] = " ".join(item[1:])
            file.close()
        except Exception:
            pass

    def read_completed(self):
        try:
            file = open(self.COMPLETED_TASKS_FILE, "r")
            self.completed_items = file.readlines()
            file.close()
        except Exception:
            pass

    def write_current(self):
        with open(self.TASKS_FILE, "w+") as f:
            f.truncate(0)
            for key in sorted(self.current_items.keys()):
                f.write(f"{key} {self.current_items[key]}\n")

    def write_completed(self):
        with open(self.COMPLETED_TASKS_FILE, "w+") as f:
            f.truncate(0)
            for item in self.completed_items:
                f.write(f"{item}\n")

    def run(self, command, args):
        self.read_current()
        self.read_completed()
        if command == "add":
            self.add(args)
        elif command == "done":
            self.done(args)
        elif command == "delete":
            self.delete(args)
        elif command == "ls":
            self.ls()
        elif command == "report":
            self.report()
        elif command == "help":
            self.help()

    def help(self):
        print(
            """Usage :-
$ python tasks.py add 2 hello world # Add a new item with priority 2 and text "hello world" to the list
$ python tasks.py ls # Show incomplete priority list items sorted by priority in ascending order
$ python tasks.py del PRIORITY_NUMBER # Delete the incomplete item with the given priority number
$ python tasks.py done PRIORITY_NUMBER # Mark the incomplete item with the given PRIORITY_NUMBER as complete
$ python tasks.py help # Show usage
$ python tasks.py report # Statistics"""
        )

    def check_priority_exists(self, priority):
        # Following LBYL as errors can happen in each loop
        if priority in self.current_items:
            # Shift keys to the right
            keys_to_shift = sorted([k for k in self.current_items.keys() if k >= priority], reverse=True)
            for k in keys_to_shift:
                self.current_items[k + 1] = self.current_items[k]

    def add(self, args):
        priority = int(args[0])
        if priority == 0:
            print("Error, priority cannot be zero")
        task = args[1]
        self.read_current()
        self.check_priority_exists(priority)
        self.current_items[priority] = task
        self.write_current()
        print(f'Added task: "{task}" with priority {priority}')

    def done(self, args):
        priority = int(args[0])
        self.read_current()
        # Following EAFP here
        try:
            self.completed_items.append(self.current_items.pop(priority))
            self.write_current()
            self.write_completed()
            print("Marked item as done.")
        except KeyError:
            print(f"Error: no incomplete item with priority {priority} exists.")

    def delete(self, args):
        priority = int(args[0])
        self.read_current()
        # Following EAFP here
        try:
            self.current_items.pop(priority)
            print(f"Deleted item with priority {priority}")
            self.write_current()
        except KeyError:
            print(f"Error: item with priority {priority} does not exist. Nothing deleted.")

    def ls(self):
        self.read_current()
        for index, (key, value) in enumerate(self.current_items.items()):
            print(f"{index + 1}. {value} [{key}]")

    def report(self):
        self.read_current()
        self.read_completed()
        print(f"Pending : {len(self.current_items.keys())}")
        self.ls()
        print()
        print(f"Completed : {len(self.completed_items)}")
        for index, item in enumerate(self.completed_items):
            print(f"{index + 1}. {item}")


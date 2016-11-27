#  -*- coding: utf-8 -*-
import csv
import re

class Formatter:
    def __init__(self, url):
        self.url = url
        
    def format(self, task, total):
        output = '<html><body><h1>Work</h1><table>';
        for task in sorted(tasks):
            output += self._row(self._link(task), tasks[task])
        output += self._row('Total', total)
        return output
    
    def _link(self, task):
        return '<a href="' + self.url + task + '" target="_blank">' + task + '</a>'
    
    def _row(self, task, time):
        return '<tr><td>' + task + '</td><td>' + time + '</td></tr>'

class Calculator:
    def calculate(self, tasks):
        for task in tasks:
            tasks[task] = self._calculate(tasks[task])
        total = self._calculate(tasks.values())
        return {'tasks': tasks, 'total': total}
    
    def _calculate(self, times):
        seconds = 0
        for time in times:
            parts = [int(s) for s in time.split(':')]
            seconds += (parts[0] * 60 + parts[1]) * 60
        total, seconds = divmod(seconds, 60)
        hour, minute = divmod(total, 60)
        return "%d:%02d" % (hour, minute)
    
class TaskNameFormatter:
    def format(self, task):
        matches = re.search(r'^dev\-[0-9]+', task)
        if matches is not None:
            return matches.group(0)
        else:
            return 'Other'
        
class Reader:
    def __init__(self, namer, taskRowNumber, timeRowNumber):
        self.namer = namer
        self.taskRowNumber = taskRowNumber
        self.timeRowNumber = timeRowNumber
    
    def read(self, filepath):
        tasks = {'Other': []}
        with open(filepath, 'r', encoding='utf-8', errors='replace') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                task = self.namer.format(row[self.taskRowNumber])
                time = row[self.timeRowNumber]
                if task not in tasks:
                    tasks[task] = [time]
                else:
                    tasks[task] = tasks[task] + [time]
        return tasks

class Writer:
    def write(self, filepath, output):
        file = open(filepath, 'w')
        file.write(output)
        file.close()

namer = TaskNameFormatter()
reader = Reader(namer, 5, 4)
calculator = Calculator()
writer = Writer()

tasks = reader.read('work.csv')
result = calculator.calculate(tasks)
formatter = Formatter('https://youtrack.dev.comet.estate/issue/')
output = formatter.format(result['tasks'], result['total']) 
writer.write('work.html', output)

print('Totally: %s tasks calculated with total time: %s' % (str(len(result['tasks'])), str(result['total'])))

# This assumes that trigger and target have matching values, i.e. they have the
# same number of lines, and each line in trigger corresponds to the same index
# line in target.

with open('trigger.txt', 'r') as fp:
    triggers = fp.readlines()

with open('target.txt', 'r') as fp:
    targets = fp.readlines()

diffs = []
for i in range(len(targets)):
    target = float(targets[i].split(':')[0])
    trigger = float(triggers[i].split(':')[0])
    diffs.append(target - trigger)

print(sum(diffs) / len(diffs))

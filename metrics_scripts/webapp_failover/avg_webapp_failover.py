with open('failover_times.txt', 'r') as fp:
    times = []
    for line in fp.readlines():
        times.append(float(line.split(':')[0]))

    diffs = []
    for i in range(0, len(times), 2):
        start = times[i]
        end = times[i + 1]
        diffs.append(end - start)

print('end - start = diff')
for i in range(0, len(times), 2):
    print('%.3f - %.3f = %.3f' % (times[i+1], times[i], diffs[i//2]))

print('average: %f seconds' % (sum(diffs) / len(diffs)))

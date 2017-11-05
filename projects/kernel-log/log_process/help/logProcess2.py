import re
import plot
import sys

filename=sys.argv[1]
timestamp_start=float(sys.argv[2])
timestamp_end=float(sys.argv[3])

file_object = open(filename)
stat_timeline = []
cost_timeline = []
res = {}
per ={}
raw_log = []
line = "Cats are smarter than dogs"
for raw_data in file_object.readlines():
    data = str.strip(raw_data)
    task_and_pid = re.search('[\S ]+-\d+',data).group()
    timestamp = re.search('\d+\.\d{6}',data).group()
    sched = re.search('sched_\S+',data).group()
    sched_stat = re.search('sched_stat_\S+', data)
    if sched_stat is not None:
        stat_timeline.append(sched_stat.group())
        runtime_or_delay = 0
        if 'runtime' in sched_stat.group():
        #     runtime_or_delay = re.search('runtime=\d+',data).group()
            runtime_or_delay = re.search('runtime=(\d+)',data).group(1)
        else:
            runtime_or_delay = re.search('delay=(\d+)', data).group(1)
        # print(runtime_or_delay)
        sched_stat_cost = runtime_or_delay
        # print(sched_stat_cost)
        cost_timeline.append(float(sched_stat_cost))
# for i in range(len(stat_timeline)):
# print(stat_timeline[i],cost_timeline[i])
# print(stat_timeline)
# print(cost_timeline)
# print(len(stat_timeline))
comb_stat =[]
comb_cost =[]
for i in range(len(stat_timeline)):
    if i == 0:
        start_stat = stat_timeline[0]
        comb_stat.append (start_stat)
        comb_cost.append (cost_timeline[0])
    else:
        if stat_timeline[i] == stat_timeline[i-1]:
            comb_cost[len(comb_cost)-1] +=  cost_timeline[i]
        else:
            comb_stat.append(start_stat)
            comb_cost.append(cost_timeline[i])
for key in set(stat_timeline):
    res[key] = 0;
    for index in range(len(stat_timeline)):
        if stat_timeline[index] == key:
            res[key] += cost_timeline[index]
print(res)
sum = 0
for i in res.keys():
    sum += res[i]
for key in res:
    per[key] = (res[key]) / sum
print(per)
plot.plot(stat_timeline,cost_timeline)

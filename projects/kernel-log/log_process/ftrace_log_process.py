import re
import plot
# 给定log文件
file_object = open('test_case')
# 查看进程名
process_id = 'ping-10105'
# 查看时间段
timestamp_start = 0
timestamp_end = 50000
# 初始化时间线上的状态与耗时统计
stat_timeline = []
cost_timeline = []
# 汇总数据
res = {}
per ={}
# 原始数据
raw_log = []
line = "Cats are smarter than dogs"

for raw_data in file_object.readlines():
    # print(raw_data)
    # 去除首尾空行
    data = str.strip(raw_data)
    # print(data)
    # print(data)
    # \S+\s*\S*-\d+
    # \S+\s*\S+-\d+
    task_and_pid = re.search('[\S ]+-\d+',data).group()
    timestamp = re.search('\d+\.\d{6}',data).group()
    sched = re.search('sched_\S+',data).group()
    # 是状态信息
    sched_stat = re.search('sched_stat_\S+', data)
    if sched_stat is not None:
        # print(sched_stat.group())
        # 加入状态信息到状态时间线
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
#     print(stat_timeline[i],cost_timeline[i])

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
        # 与之前状态相同
        if stat_timeline[i] == stat_timeline[i-1]:
            comb_cost[len(comb_cost)-1] +=  cost_timeline[i]
        # 与之前状态不同
        else:
            comb_stat.append(start_stat)
            comb_cost.append(cost_timeline[i])


# 拿出数据再统计
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


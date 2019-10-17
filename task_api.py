from Deadline.Scripting import RepositoryUtils, JobUtils
from datetime import datetime
from os import mkdir, walk, remove, rename
from io import open
from time import time, ctime

t = time()
while True:
    with open('task_api.cfg') as input_cfg:
        for cfg in input_cfg:
            config = cfg.split()
            if 1 < len(config):
                if 'fldr' == config[0]:
                    fldr = config[1]
                if 'core' == config[0]:
                    core = float(config[1])
                if 'ticks_null' == config[0]:
                    ticks_null = int(config[1])

    suph_slave = {}
    with open(fldr + 'suph_dl.csv') as input_suph:
        next(input_suph)
        for suph in input_suph:
            data = suph.replace(',', ' ').split()
            if 1 < len(data):
                suph_slave[data[0]] = float(data[1])

    with open(fldr + 'ch_group.txt') as input_ch:
        ch_group = {
            group.strip().lower() for group in input_ch if group.strip()}

    all_group = set()
    all_slave = set()
    all_job = []
    report_users = {}
    for job in (tuple(RepositoryUtils.GetJobs(True)) +
                tuple(RepositoryUtils.GetDeletedJobs())):
        all_group.add(job.JobGroup.lower())
        task_job = RepositoryUtils.GetJobTasks(job, True)
        ticks = 0.0
        for task in task_job:
            slave = task.TaskSlaveName.lower()
            all_slave.add(slave)
            if slave in suph_slave:
                suph = suph_slave[slave]
            else:
                suph = core
            if 0 < task.TaskRenderTime.Ticks < ticks_null:
                ticks += task.TaskRenderTime.Ticks * suph
        su = round(ticks // 360000 / 100000, 8)
        stats = JobUtils.CalculateJobStatistics(job, task_job)
        ch = round(
            stats.TotalTaskRenderTime.Ticks * core // 360000 / 100000, 8)
        ch = max(ch, 0.0)
        username = job.JobUserName.lower()
        if username and username not in report_users:
            report_users[username] = []
        if username and 1900 <= job.JobCompletedDateTime.Year:
            time_end = datetime(
                job.JobCompletedDateTime.Year,
                job.JobCompletedDateTime.Month,
                job.JobCompletedDateTime.Day,
                job.JobCompletedDateTime.Hour,
                job.JobCompletedDateTime.Minute,
                job.JobCompletedDateTime.Second,
            ).isoformat()
            report_users[username].append((
                time_end,
                job.JobId.lower(),
                job.JobName,
                str(job.JobPriority),
                job.JobGroup.lower(),
                str(ch),
                str(su),
            ))
            all_job.append('\t'.join((
                time_end,
                username,
                str(max(stats.TotalTaskRenderTime.Ticks, 0)),
            )) + '\n')

    try:
        mkdir(fldr + 'temp')
        mkdir(fldr + 'users')
    except EnvironmentError:
        pass

    for username in report_users:
        filename = fldr + 'temp/dl_' + username + '.csv'
        
        try:
            with open(filename, 'w', encoding='utf_8') as output_user:
                output_user.write(
                    u'time\tid\tname\tpriority\tgroup\tcore_hour\tSU\n')
                su_total = 0
                for data in sorted(report_users[username]):
                    output_user.write('\t'.join(data) + '\n')
                    if data[-3] in ch_group:
                        su_total += float(data[-2])
                    else:
                        su_total += float(data[-1])
                output_user.write(
                    u'SU_total\t' + str(round(su_total, 8)) + '\n')
        except EnvironmentError:
            pass
    
    try:
        with open(
            fldr + 'temp/filtered.log', 'w', encoding='utf_8') as output_all:
            output_all.writelines(sorted(all_job))
    except EnvironmentError:
        pass
    
    try:
        with open(
            fldr + 'temp/group.log', 'w', encoding='utf_8') as output_group:
            output_group.write('\n'.join(sorted(all_group)))
    except EnvironmentError:
        pass
    
    try:
        with open(
            fldr + 'temp/slave.log', 'w', encoding='utf_8') as output_slave:
            output_slave.write('\n'.join(sorted(all_slave)))
    except EnvironmentError:
        pass
    
    try:
        temp = sorted(next(walk(fldr + 'temp'))[2])
    except StopIteration:
        pass
    for filename in temp:
        if '.csv' == filename[-4:]:
            dst = fldr + 'users/' + filename
        else:
            dst = fldr + filename
        try:
            remove(dst)
        except EnvironmentError:
            pass
        try:
            rename(fldr + 'temp/' + filename, dst)
        except EnvironmentError:
            pass

    print '\r\t\t\t\t\t\t{} {}     '.format(round(time() - t, 3), ctime()),

def __main__():
    return None

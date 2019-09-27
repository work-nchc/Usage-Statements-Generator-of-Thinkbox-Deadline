# The Usage Statements Generator of Thinkbox Deadline from NCHC

Ported from [Union-Log-Deadline](https://github.com/work-nchc/Union-Log-Deadline)

---
task_api.py and task_api.cfg should be placed in:

```
C:\Program Files\Thinkbox\Deadline10\bin
```

suph_dl.csv and ch_group.txt should be placed in the IO directory [fldr] specified in task_api.cfg.  Also configure the default SU per hour in task_api.cfg, the SU per hour for each slave in suph_dl.csv, and the groups using core hour as usage in ch_group.txt, one group per line, first.

---
Routine Reporting:

```
& 'C:\Program Files\Thinkbox\Deadline10\bin\deadlinecommand.exe' ExecuteScriptNoGui .\task_api.py
```

Usage statement of each user will present in directory [fldr]/users, updated in real-time, listing completed time, id, name, priority, group, core hour, and SU of each job.  There will also be group.log, slave.log, and filtered.log, for one-off usage table generating, in [fldr].  The execution time will be printed on the standard output.

---
2019-09-27 by 1803031@narlabs.org.tw

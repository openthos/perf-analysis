#1.irqsoff
1.1简介  
该追踪器记录最长关中断时间以及最长关中断发生时内核调用栈信息。在实时系统中，大都尽量减小关中断时间(因为中断具有最高优先级，关中断期间实时任务必然不能执行)，在很多实时性评测benchmark中，都将关中断时间做为一个很重要的指标。我们会着重分析irqsoff中的log
1.2样例
```
# tracer: irqsoff
#
# irqsoff latency trace v1.1.5 on 4.4.27-rt37
# --------------------------------------------------------------------
# latency: 253 us, #180/180, CPU#0 | (M:preempt VP:0, KP:0, SP:0 HP:0 #P:8)
#    -----------------
#    | task: swapper/0-0 (uid:0 nice:0 policy:0 rt_prio:0)
#    -----------------
#  => started at: apic_timer_interrupt
#  => ended at:   restore_regs_and_iret
#
#
#                   _--------=> CPU#              
#                  / _-------=> irqs-off          
#                 | / _------=> need-resched      
#                 || / _-----=> need-resched_lazy 
#                 ||| / _----=> hardirq/softirq   
#                 |||| / _---=> preempt-depth     
#                 ||||| / _--=> preempt-lazy-depth
#                 |||||| / _-=> migrate-disable   
#                 ||||||| /     delay             
#  cmd     pid    |||||||| time  |   caller       
#     \   /      ||||||||  \   |   /            
  <idle>-0       0d...1..    1us : trace_hardirqs_off_thunk <-apic_timer_interrupt
  <idle>-0       0d...1..    2us : smp_apic_timer_interrupt <-apic_timer_interrupt
  <idle>-0       0d...1..    4us : irq_enter <-smp_apic_timer_interrupt
  <idle>-0       0d...1..    5us : rcu_irq_enter <-irq_enter
  <idle>-0       0d...1..    7us : rcu_eqs_exit_common.isra.43 <-rcu_irq_enter
  <idle>-0       0d...1..   10us : tick_irq_enter <-irq_enter
  <idle>-0       0d...1..   12us : tick_check_oneshot_broadcast_this_cpu <-tick_irq_enter
  <idle>-0       0d...1..   14us+: ktime_get <-tick_irq_enter
  <idle>-0       0d...1..   26us : tick_nohz_stop_idle <-tick_irq_enter
  <idle>-0       0d...1..   28us : update_ts_time_stats <-tick_nohz_stop_idle
  <idle>-0       0d...1..   29us : nr_iowait_cpu <-update_ts_time_stats
  <idle>-0       0d...1..   31us : touch_softlockup_watchdog <-sched_clock_idle_wakeup_event
  <idle>-0       0d...1..   32us : preempt_count_add <-irq_enter
  <idle>-0       0d..h1..   33us : exit_idle <-smp_apic_timer_interrupt
  <idle>-0       0d..h1..   34us : atomic_notifier_call_chain <-exit_idle
  <idle>-0       0d..h1..   35us : __rcu_read_lock <-atomic_notifier_call_chain
  <idle>-0       0d..h1..   37us : notifier_call_chain <-atomic_notifier_call_chain
  <idle>-0       0d..h1..   39us : __rcu_read_unlock <-atomic_notifier_call_chain
  <idle>-0       0d..h1..   40us : local_apic_timer_interrupt <-smp_apic_timer_interrupt
  <idle>-0       0d..h1..   42us : hrtimer_interrupt <-local_apic_timer_interrupt
  <idle>-0       0d..h1..   43us : _raw_spin_lock <-hrtimer_interrupt
  <idle>-0       0d..h1..   44us : preempt_count_add <-_raw_spin_lock
  <idle>-0       0d..h2..   45us : ktime_get_update_offsets_now <-hrtimer_interrupt
  <idle>-0       0d..h2..   47us : __hrtimer_run_queues <-hrtimer_interrupt
  <idle>-0       0d..h2..   49us : __remove_hrtimer <-__hrtimer_run_queues
  <idle>-0       0d..h2..   51us : preempt_count_sub <-__hrtimer_run_queues
  <idle>-0       0d..h1..   52us : tick_sched_timer <-__hrtimer_run_queues
  <idle>-0       0d..h1..   53us : ktime_get <-tick_sched_timer
  <idle>-0       0d..h1..   54us : tick_sched_do_timer <-tick_sched_timer
  <idle>-0       0d..h1..   56us : tick_do_update_jiffies64 <-tick_sched_do_timer
  <idle>-0       0d..h1..   57us : _raw_spin_lock <-tick_do_update_jiffies64
  <idle>-0       0d..h1..   58us : preempt_count_add <-_raw_spin_lock
  <idle>-0       0d..h2..   59us : preempt_count_add <-tick_do_update_jiffies64
  <idle>-0       0d..h3..   60us : do_timer <-tick_do_update_jiffies64
  <idle>-0       0d..h3..   62us : calc_global_load <-do_timer
  <idle>-0       0d..h3..   63us : preempt_count_sub <-tick_do_update_jiffies64
  <idle>-0       0d..h2..   64us : preempt_count_sub <-tick_do_update_jiffies64
  <idle>-0       0d..h1..   66us : update_wall_time <-tick_do_update_jiffies64
  <idle>-0       0d..h1..   67us : _raw_spin_lock_irqsave <-update_wall_time
  <idle>-0       0d..h1..   69us : preempt_count_add <-_raw_spin_lock_irqsave
  <idle>-0       0d..h2..   71us : ntp_tick_length <-update_wall_time
  <idle>-0       0d..h2..   73us : ntp_tick_length <-update_wall_time
  <idle>-0       0d..h2..   74us : ntp_tick_length <-update_wall_time
  <idle>-0       0d..h2..   75us : preempt_count_add <-update_wall_time
  <idle>-0       0d..h3..   77us : timekeeping_update <-update_wall_time
  <idle>-0       0d..h3..   78us : ntp_get_next_leap <-timekeeping_update
  <idle>-0       0d..h3..   79us : update_vsyscall <-timekeeping_update
  <idle>-0       0d..h3..   81us : raw_notifier_call_chain <-timekeeping_update
  <idle>-0       0d..h3..   83us : notifier_call_chain <-raw_notifier_call_chain
  <idle>-0       0d..h3..   84us : pvclock_gtod_notify <-notifier_call_chain
  <idle>-0       0d..h3..   86us : preempt_count_add <-pvclock_gtod_notify
  <idle>-0       0d..h4..   87us : preempt_count_sub <-pvclock_gtod_notify
  <idle>-0       0d..h3..   88us : update_fast_timekeeper <-timekeeping_update
  <idle>-0       0d..h3..   89us : update_fast_timekeeper <-timekeeping_update
  <idle>-0       0d..h3..   90us : preempt_count_sub <-update_wall_time
  <idle>-0       0d..h2..   91us : _raw_spin_unlock_irqrestore <-update_wall_time
  <idle>-0       0d..h2..   92us : preempt_count_sub <-_raw_spin_unlock_irqrestore
  <idle>-0       0d..h1..   94us : tick_sched_handle.isra.13 <-tick_sched_timer
  <idle>-0       0d..h1..   95us : update_process_times <-tick_sched_handle.isra.13
  <idle>-0       0d..h1..   96us : account_process_tick <-update_process_times
  <idle>-0       0d..h1..   97us : account_idle_time <-account_process_tick
  <idle>-0       0d..h1..   99us : scheduler_tick <-update_process_times
  <idle>-0       0d..h1..  100us : _raw_spin_lock <-scheduler_tick
  <idle>-0       0d..h1..  102us : preempt_count_add <-_raw_spin_lock
  <idle>-0       0d..h2..  103us : update_rq_clock.part.82 <-scheduler_tick
  <idle>-0       0d..h2..  104us : task_tick_idle <-scheduler_tick
  <idle>-0       0d..h2..  105us : update_cpu_load_active <-scheduler_tick
  <idle>-0       0d..h2..  106us : __update_cpu_load <-update_cpu_load_active
  <idle>-0       0d..h2..  107us : sched_avg_update <-__update_cpu_load
  <idle>-0       0d..h2..  108us : calc_global_load_tick <-scheduler_tick
  <idle>-0       0d..h2..  109us : preempt_count_sub <-scheduler_tick
  <idle>-0       0d..h1..  110us : trigger_load_balance <-scheduler_tick
  <idle>-0       0d..h1..  111us : raise_softirq <-trigger_load_balance
  <idle>-0       0d..h1..  112us : raise_softirq_irqoff <-raise_softirq
  <idle>-0       0d..h1..  113us : do_raise_softirq_irqoff <-raise_softirq_irqoff
  <idle>-0       0d..h1..  116us : hrtimer_run_queues <-update_process_times
  <idle>-0       0d..h1..  117us : raise_softirq <-update_process_times
  <idle>-0       0d..h1..  118us : raise_softirq_irqoff <-raise_softirq
  <idle>-0       0d..h1..  119us : do_raise_softirq_irqoff <-raise_softirq_irqoff
  <idle>-0       0d..h1..  121us : rcu_check_callbacks <-update_process_times
  <idle>-0       0d..h1..  122us : rcu_sched_qs <-rcu_check_callbacks
  <idle>-0       0d..h1..  123us : rcu_bh_qs <-rcu_check_callbacks
  <idle>-0       0d..h1..  125us : rcu_preempt_qs <-rcu_bh_qs
  <idle>-0       0d..h1..  127us : rcu_preempt_qs <-rcu_check_callbacks
  <idle>-0       0d..h1..  129us : cpu_needs_another_gp <-rcu_check_callbacks
  <idle>-0       0d..h1..  131us : invoke_rcu_core <-rcu_check_callbacks
  <idle>-0       0d..h1..  133us : wake_up_process <-invoke_rcu_core
  <idle>-0       0d..h1..  135us : try_to_wake_up <-wake_up_process
  <idle>-0       0d..h1..  137us : _raw_spin_lock_irqsave <-try_to_wake_up
  <idle>-0       0d..h1..  138us : preempt_count_add <-_raw_spin_lock_irqsave
  <idle>-0       0d..h2..  139us : task_waking_fair <-try_to_wake_up
  <idle>-0       0d..h2..  141us : _raw_spin_lock <-try_to_wake_up
  <idle>-0       0d..h2..  141us : preempt_count_add <-_raw_spin_lock
  <idle>-0       0d..h3..  142us : ttwu_do_activate.constprop.94 <-try_to_wake_up
  <idle>-0       0d..h3..  144us : activate_task <-ttwu_do_activate.constprop.94
  <idle>-0       0d..h3..  145us : update_rq_clock.part.82 <-activate_task
  <idle>-0       0d..h3..  147us : enqueue_task_fair <-activate_task
  <idle>-0       0d..h3..  148us : enqueue_entity <-enqueue_task_fair
  <idle>-0       0d..h3..  149us : update_curr <-enqueue_entity
  <idle>-0       0d..h3..  151us : __compute_runnable_contrib <-enqueue_entity
  <idle>-0       0d..h3..  152us : account_entity_enqueue <-enqueue_entity
  <idle>-0       0d..h3..  154us : update_cfs_shares <-enqueue_entity
  <idle>-0       0d..h3..  156us : __enqueue_entity <-enqueue_entity
  <idle>-0       0d..h3..  158us : hrtick_update <-enqueue_task_fair
  <idle>-0       0d..h3..  159us : ttwu_do_wakeup <-ttwu_do_activate.constprop.94
  <idle>-0       0d..h3..  160us : check_preempt_curr <-ttwu_do_wakeup
  <idle>-0       0d..h3..  162us : resched_curr <-check_preempt_curr
  <idle>-0       0dN.h3..  163us : preempt_count_sub <-__raw_spin_unlock
  <idle>-0       0dN.h2..  164us : _raw_spin_unlock_irqrestore <-try_to_wake_up
  <idle>-0       0dN.h2..  166us : preempt_count_sub <-_raw_spin_unlock_irqrestore
  <idle>-0       0dN.h1..  167us : run_posix_cpu_timers <-update_process_times
  <idle>-0       0dN.h1..  168us : profile_tick <-tick_sched_handle.isra.13
  <idle>-0       0dN.h1..  170us : hrtimer_forward <-tick_sched_timer
  <idle>-0       0dN.h1..  171us : _raw_spin_lock <-__hrtimer_run_queues
  <idle>-0       0dN.h1..  173us : preempt_count_add <-_raw_spin_lock
  <idle>-0       0dN.h2..  174us : enqueue_hrtimer <-__hrtimer_run_queues
  <idle>-0       0dN.h2..  176us : __hrtimer_get_next_event <-hrtimer_interrupt
  <idle>-0       0dN.h2..  178us : preempt_count_sub <-hrtimer_interrupt
  <idle>-0       0dN.h1..  179us : tick_program_event <-hrtimer_interrupt
  <idle>-0       0dN.h1..  180us : clockevents_program_event <-tick_program_event
  <idle>-0       0dN.h1..  181us : ktime_get <-clockevents_program_event
  <idle>-0       0dN.h1..  182us : lapic_next_deadline <-clockevents_program_event
  <idle>-0       0dN.h1..  183us : irq_exit <-smp_apic_timer_interrupt
  <idle>-0       0dN.h1..  185us : preempt_count_sub <-irq_exit
  <idle>-0       0dN..1..  185us : wakeup_softirqd <-irq_exit
  <idle>-0       0dN..1..  186us : wake_up_process <-wakeup_softirqd
  <idle>-0       0dN..1..  187us : try_to_wake_up <-wake_up_process
  <idle>-0       0dN..1..  188us : _raw_spin_lock_irqsave <-try_to_wake_up
  <idle>-0       0dN..1..  190us : preempt_count_add <-_raw_spin_lock_irqsave
  <idle>-0       0dN..2..  191us : task_waking_fair <-try_to_wake_up
  <idle>-0       0dN..2..  193us : _raw_spin_lock <-try_to_wake_up
  <idle>-0       0dN..2..  194us : preempt_count_add <-_raw_spin_lock
  <idle>-0       0dN..3..  195us : ttwu_do_activate.constprop.94 <-try_to_wake_up
  <idle>-0       0dN..3..  196us : activate_task <-ttwu_do_activate.constprop.94
  <idle>-0       0dN..3..  197us : update_rq_clock.part.82 <-activate_task
  <idle>-0       0dN..3..  198us : enqueue_task_fair <-activate_task
  <idle>-0       0dN..3..  201us : enqueue_entity <-enqueue_task_fair
  <idle>-0       0dN..3..  202us : update_curr <-enqueue_entity
  <idle>-0       0dN..3..  203us : account_entity_enqueue <-enqueue_entity
  <idle>-0       0dN..3..  205us : update_cfs_shares <-enqueue_entity
  <idle>-0       0dN..3..  207us : __enqueue_entity <-enqueue_entity
  <idle>-0       0dN..3..  208us : hrtick_update <-enqueue_task_fair
  <idle>-0       0dN..3..  209us : ttwu_do_wakeup <-ttwu_do_activate.constprop.94
  <idle>-0       0dN..3..  210us : check_preempt_curr <-ttwu_do_wakeup
  <idle>-0       0dN..3..  211us : resched_curr <-check_preempt_curr
  <idle>-0       0dN..3..  213us : preempt_count_sub <-__raw_spin_unlock
  <idle>-0       0dN..2..  214us : _raw_spin_unlock_irqrestore <-try_to_wake_up
  <idle>-0       0dN..2..  216us : preempt_count_sub <-_raw_spin_unlock_irqrestore
  <idle>-0       0dN..1..  217us : wakeup_timer_softirqd <-irq_exit
  <idle>-0       0dN..1..  219us : wake_up_process <-wakeup_timer_softirqd
  <idle>-0       0dN..1..  220us : try_to_wake_up <-wake_up_process
  <idle>-0       0dN..1..  221us : _raw_spin_lock_irqsave <-try_to_wake_up
  <idle>-0       0dN..1..  223us : preempt_count_add <-_raw_spin_lock_irqsave
  <idle>-0       0dN..2..  224us : _raw_spin_lock <-try_to_wake_up
  <idle>-0       0dN..2..  225us : preempt_count_add <-_raw_spin_lock
  <idle>-0       0dN..3..  227us : ttwu_do_activate.constprop.94 <-try_to_wake_up
  <idle>-0       0dN..3..  227us : activate_task <-ttwu_do_activate.constprop.94
  <idle>-0       0dN..3..  228us : update_rq_clock.part.82 <-activate_task
  <idle>-0       0dN..3..  230us : enqueue_task_rt <-activate_task
  <idle>-0       0dN..3..  231us : dequeue_rt_stack <-enqueue_task_rt
  <idle>-0       0dN..3..  232us : dequeue_top_rt_rq <-dequeue_rt_stack
  <idle>-0       0dN..3..  233us : cpupri_set <-enqueue_task_rt
  <idle>-0       0dN..3..  234us : update_rt_migration <-enqueue_task_rt
  <idle>-0       0dN..3..  235us : _raw_spin_lock <-enqueue_task_rt
  <idle>-0       0dN..3..  236us : preempt_count_add <-_raw_spin_lock
  <idle>-0       0dN..4..  237us : preempt_count_sub <-enqueue_task_rt
  <idle>-0       0dN..3..  238us : enqueue_top_rt_rq <-enqueue_task_rt
  <idle>-0       0dN..3..  240us : ttwu_do_wakeup <-ttwu_do_activate.constprop.94
  <idle>-0       0dN..3..  240us : check_preempt_curr <-ttwu_do_wakeup
  <idle>-0       0dN..3..  241us : resched_curr <-check_preempt_curr
  <idle>-0       0dN..3..  243us : task_woken_rt <-ttwu_do_wakeup
  <idle>-0       0dN..3..  244us : preempt_count_sub <-__raw_spin_unlock
  <idle>-0       0dN..2..  246us : _raw_spin_unlock_irqrestore <-try_to_wake_up
  <idle>-0       0dN..2..  247us : preempt_count_sub <-_raw_spin_unlock_irqrestore
  <idle>-0       0dN..1..  249us : idle_cpu <-irq_exit
  <idle>-0       0dN..1..  250us : rcu_irq_exit <-irq_exit
  <idle>-0       0dN..1..  251us : rcu_eqs_enter_common <-rcu_irq_exit
  <idle>-0       0dN..1..  253us : trace_hardirqs_on_thunk <-restore_regs_and_iret
  <idle>-0       0dN..1..  254us+: trace_hardirqs_on_caller <-restore_regs_and_iret
  <idle>-0       0dN..1..  321us : <stack trace>
 => trace_hardirqs_on_thunk
 => cpuidle_enter
 => call_cpuidle
 => cpu_startup_entry
 => rest_init
 => start_kernel
 => x86_64_start_reservations
 => x86_64_start_kernel
```
此外这个最大关中断时间是可以通过tracing_max_latency获取的
在系统的另一个时刻，再次查看trace信息，此时出现了一个更大的关中断时间。
```
# tracer: irqsoff
#
# irqsoff latency trace v1.1.5 on 4.4.27-rt37
# --------------------------------------------------------------------
# latency: 323 us, #268/268, CPU#0 | (M:preempt VP:0, KP:0, SP:0 HP:0 #P:8)
#    -----------------
#    | task: swapper/0-0 (uid:0 nice:0 policy:0 rt_prio:0)
#    -----------------
#  => started at: apic_timer_interrupt
#  => ended at:   restore_regs_and_iret
#
#
#                   _--------=> CPU#              
#                  / _-------=> irqs-off          
#                 | / _------=> need-resched      
#                 || / _-----=> need-resched_lazy 
#                 ||| / _----=> hardirq/softirq   
#                 |||| / _---=> preempt-depth     
#                 ||||| / _--=> preempt-lazy-depth
#                 |||||| / _-=> migrate-disable   
#                 ||||||| /     delay             
#  cmd     pid    |||||||| time  |   caller       
#     \   /      ||||||||  \   |   /            
  <idle>-0       0d...1..    0us : trace_hardirqs_off_thunk <-apic_timer_interrupt
  <idle>-0       0d...1..    1us : smp_apic_timer_interrupt <-apic_timer_interrupt
  <idle>-0       0d...1..    3us : irq_enter <-smp_apic_timer_interrupt
  <idle>-0       0d...1..    4us : rcu_irq_enter <-irq_enter
  <idle>-0       0d...1..    5us : rcu_eqs_exit_common.isra.43 <-rcu_irq_enter
  <idle>-0       0d...1..    6us : tick_irq_enter <-irq_enter
  <idle>-0       0d...1..    8us : tick_check_oneshot_broadcast_this_cpu <-tick_irq_enter
  <idle>-0       0d...1..   10us : ktime_get <-tick_irq_enter
  <idle>-0       0d...1..   11us : tick_nohz_stop_idle <-tick_irq_enter
  <idle>-0       0d...1..   12us+: update_ts_time_stats <-tick_nohz_stop_idle
  <idle>-0       0d...1..   24us : nr_iowait_cpu <-update_ts_time_stats
  <idle>-0       0d...1..   25us : touch_softlockup_watchdog <-sched_clock_idle_wakeup_event
  <idle>-0       0d...1..   26us : preempt_count_add <-irq_enter
  <idle>-0       0d..h1..   27us : exit_idle <-smp_apic_timer_interrupt
  <idle>-0       0d..h1..   28us : atomic_notifier_call_chain <-exit_idle
  <idle>-0       0d..h1..   29us : __rcu_read_lock <-atomic_notifier_call_chain
  <idle>-0       0d..h1..   30us : notifier_call_chain <-atomic_notifier_call_chain
  <idle>-0       0d..h1..   31us : __rcu_read_unlock <-atomic_notifier_call_chain
  <idle>-0       0d..h1..   32us : local_apic_timer_interrupt <-smp_apic_timer_interrupt
  <idle>-0       0d..h1..   33us : hrtimer_interrupt <-local_apic_timer_interrupt
  <idle>-0       0d..h1..   34us : _raw_spin_lock <-hrtimer_interrupt
  <idle>-0       0d..h1..   34us : preempt_count_add <-_raw_spin_lock
  <idle>-0       0d..h2..   35us : ktime_get_update_offsets_now <-hrtimer_interrupt
  <idle>-0       0d..h2..   36us : __hrtimer_run_queues <-hrtimer_interrupt
  <idle>-0       0d..h2..   37us : __remove_hrtimer <-__hrtimer_run_queues
  <idle>-0       0d..h2..   39us : preempt_count_sub <-__hrtimer_run_queues
  <idle>-0       0d..h1..   40us : tick_sched_timer <-__hrtimer_run_queues
  <idle>-0       0d..h1..   40us : ktime_get <-tick_sched_timer
  <idle>-0       0d..h1..   41us : tick_sched_do_timer <-tick_sched_timer
  <idle>-0       0d..h1..   43us : tick_do_update_jiffies64 <-tick_sched_do_timer
  <idle>-0       0d..h1..   44us : _raw_spin_lock <-tick_do_update_jiffies64
  <idle>-0       0d..h1..   44us : preempt_count_add <-_raw_spin_lock
  <idle>-0       0d..h2..   45us : preempt_count_add <-tick_do_update_jiffies64
  <idle>-0       0d..h3..   45us : do_timer <-tick_do_update_jiffies64
  <idle>-0       0d..h3..   46us : calc_global_load <-do_timer
  <idle>-0       0d..h3..   48us : preempt_count_sub <-tick_do_update_jiffies64
  <idle>-0       0d..h2..   49us : preempt_count_sub <-tick_do_update_jiffies64
  <idle>-0       0d..h1..   50us : update_wall_time <-tick_do_update_jiffies64
  <idle>-0       0d..h1..   51us : _raw_spin_lock_irqsave <-update_wall_time
  <idle>-0       0d..h1..   52us : preempt_count_add <-_raw_spin_lock_irqsave
  <idle>-0       0d..h2..   53us : ntp_tick_length <-update_wall_time
  <idle>-0       0d..h2..   54us : ntp_tick_length <-update_wall_time
  <idle>-0       0d..h2..   55us : ntp_tick_length <-update_wall_time
  <idle>-0       0d..h2..   56us : preempt_count_add <-update_wall_time
  <idle>-0       0d..h3..   57us : timekeeping_update <-update_wall_time
  <idle>-0       0d..h3..   58us : ntp_get_next_leap <-timekeeping_update
  <idle>-0       0d..h3..   59us : update_vsyscall <-timekeeping_update
  <idle>-0       0d..h3..   59us : raw_notifier_call_chain <-timekeeping_update
  <idle>-0       0d..h3..   60us : notifier_call_chain <-raw_notifier_call_chain
  <idle>-0       0d..h3..   62us : pvclock_gtod_notify <-notifier_call_chain
  <idle>-0       0d..h3..   62us : preempt_count_add <-pvclock_gtod_notify
  <idle>-0       0d..h4..   63us : preempt_count_sub <-pvclock_gtod_notify
  <idle>-0       0d..h3..   64us : update_fast_timekeeper <-timekeeping_update
  <idle>-0       0d..h3..   65us : update_fast_timekeeper <-timekeeping_update
  <idle>-0       0d..h3..   66us : preempt_count_sub <-update_wall_time
  <idle>-0       0d..h2..   67us : _raw_spin_unlock_irqrestore <-update_wall_time
  <idle>-0       0d..h2..   67us : preempt_count_sub <-_raw_spin_unlock_irqrestore
  <idle>-0       0d..h1..   69us : tick_sched_handle.isra.13 <-tick_sched_timer
  <idle>-0       0d..h1..   69us : update_process_times <-tick_sched_handle.isra.13
  <idle>-0       0d..h1..   70us : account_process_tick <-update_process_times
  <idle>-0       0d..h1..   71us : account_idle_time <-account_process_tick
  <idle>-0       0d..h1..   72us : scheduler_tick <-update_process_times
  <idle>-0       0d..h1..   73us : _raw_spin_lock <-scheduler_tick
  <idle>-0       0d..h1..   74us : preempt_count_add <-_raw_spin_lock
  <idle>-0       0d..h2..   75us : update_rq_clock.part.82 <-scheduler_tick
  <idle>-0       0d..h2..   77us : task_tick_idle <-scheduler_tick
  <idle>-0       0d..h2..   78us : update_cpu_load_active <-scheduler_tick
  <idle>-0       0d..h2..   78us : __update_cpu_load <-update_cpu_load_active
  <idle>-0       0d..h2..   79us : sched_avg_update <-__update_cpu_load
  <idle>-0       0d..h2..   80us : calc_global_load_tick <-scheduler_tick
  <idle>-0       0d..h2..   81us : preempt_count_sub <-scheduler_tick
  <idle>-0       0d..h1..   82us : trigger_load_balance <-scheduler_tick
  <idle>-0       0d..h1..   83us : raise_softirq <-trigger_load_balance
  <idle>-0       0d..h1..   84us : raise_softirq_irqoff <-raise_softirq
  <idle>-0       0d..h1..   85us : do_raise_softirq_irqoff <-raise_softirq_irqoff
  <idle>-0       0d..h1..   86us : hrtimer_run_queues <-update_process_times
  <idle>-0       0d..h1..   87us : raise_softirq <-update_process_times
  <idle>-0       0d..h1..   88us : raise_softirq_irqoff <-raise_softirq
  <idle>-0       0d..h1..   89us : do_raise_softirq_irqoff <-raise_softirq_irqoff
  <idle>-0       0d..h1..   90us : rcu_check_callbacks <-update_process_times
  <idle>-0       0d..h1..   91us : rcu_sched_qs <-rcu_check_callbacks
  <idle>-0       0d..h1..   92us : rcu_bh_qs <-rcu_check_callbacks
  <idle>-0       0d..h1..   93us : rcu_preempt_qs <-rcu_bh_qs
  <idle>-0       0d..h1..   94us : rcu_preempt_qs <-rcu_check_callbacks
  <idle>-0       0d..h1..   95us : invoke_rcu_core <-rcu_check_callbacks
  <idle>-0       0d..h1..   96us : wake_up_process <-invoke_rcu_core
  <idle>-0       0d..h1..   97us : try_to_wake_up <-wake_up_process
  <idle>-0       0d..h1..   98us : _raw_spin_lock_irqsave <-try_to_wake_up
  <idle>-0       0d..h1..   99us : preempt_count_add <-_raw_spin_lock_irqsave
  <idle>-0       0d..h2..  100us : task_waking_fair <-try_to_wake_up
  <idle>-0       0d..h2..  101us : _raw_spin_lock <-try_to_wake_up
  <idle>-0       0d..h2..  102us : preempt_count_add <-_raw_spin_lock
  <idle>-0       0d..h3..  103us : ttwu_do_activate.constprop.94 <-try_to_wake_up
  <idle>-0       0d..h3..  104us : activate_task <-ttwu_do_activate.constprop.94
  <idle>-0       0d..h3..  105us : update_rq_clock.part.82 <-activate_task
  <idle>-0       0d..h3..  106us : enqueue_task_fair <-activate_task
  <idle>-0       0d..h3..  106us : enqueue_entity <-enqueue_task_fair
  <idle>-0       0d..h3..  107us : update_curr <-enqueue_entity
  <idle>-0       0d..h3..  108us : __compute_runnable_contrib <-enqueue_entity
  <idle>-0       0d..h3..  110us : account_entity_enqueue <-enqueue_entity
  <idle>-0       0d..h3..  111us : update_cfs_shares <-enqueue_entity
  <idle>-0       0d..h3..  111us : __enqueue_entity <-enqueue_entity
  <idle>-0       0d..h3..  112us : hrtick_update <-enqueue_task_fair
  <idle>-0       0d..h3..  113us : ttwu_do_wakeup <-ttwu_do_activate.constprop.94
  <idle>-0       0d..h3..  114us : check_preempt_curr <-ttwu_do_wakeup
  <idle>-0       0d..h3..  115us : resched_curr <-check_preempt_curr
  <idle>-0       0dN.h3..  117us : preempt_count_sub <-__raw_spin_unlock
  <idle>-0       0dN.h2..  118us : _raw_spin_unlock_irqrestore <-try_to_wake_up
  <idle>-0       0dN.h2..  119us : preempt_count_sub <-_raw_spin_unlock_irqrestore
  <idle>-0       0dN.h1..  120us : run_posix_cpu_timers <-update_process_times
  <idle>-0       0dN.h1..  121us : profile_tick <-tick_sched_handle.isra.13
  <idle>-0       0dN.h1..  122us : hrtimer_forward <-tick_sched_timer
  <idle>-0       0dN.h1..  123us : _raw_spin_lock <-__hrtimer_run_queues
  <idle>-0       0dN.h1..  124us : preempt_count_add <-_raw_spin_lock
  <idle>-0       0dN.h2..  125us : enqueue_hrtimer <-__hrtimer_run_queues
  <idle>-0       0dN.h2..  127us : __remove_hrtimer <-__hrtimer_run_queues
  <idle>-0       0dN.h2..  128us : preempt_count_sub <-__hrtimer_run_queues
  <idle>-0       0dN.h1..  129us : hrtimer_wakeup <-__hrtimer_run_queues
  <idle>-0       0dN.h1..  130us : wake_up_process <-hrtimer_wakeup
  <idle>-0       0dN.h1..  131us : try_to_wake_up <-wake_up_process
  <idle>-0       0dN.h1..  131us : _raw_spin_lock_irqsave <-try_to_wake_up
  <idle>-0       0dN.h1..  132us : preempt_count_add <-_raw_spin_lock_irqsave
  <idle>-0       0dN.h2..  134us : task_waking_fair <-try_to_wake_up
  <idle>-0       0dN.h2..  135us : select_task_rq_fair <-try_to_wake_up
  <idle>-0       0dN.h2..  136us : __rcu_read_lock <-select_task_rq_fair
  <idle>-0       0dN.h2..  137us : select_idle_sibling <-select_task_rq_fair
  <idle>-0       0dN.h2..  139us : idle_cpu <-select_idle_sibling
  <idle>-0       0dN.h2..  140us : idle_cpu <-select_idle_sibling
  <idle>-0       0dN.h2..  142us : idle_cpu <-select_idle_sibling
  <idle>-0       0dN.h2..  143us : idle_cpu <-select_idle_sibling
  <idle>-0       0dN.h2..  144us : idle_cpu <-select_idle_sibling
  <idle>-0       0dN.h2..  145us : __rcu_read_unlock <-select_task_rq_fair
  <idle>-0       0dN.h2..  146us : _raw_spin_lock <-try_to_wake_up
  <idle>-0       0dN.h2..  147us : preempt_count_add <-_raw_spin_lock
  <idle>-0       0dN.h3..  149us : ttwu_do_activate.constprop.94 <-try_to_wake_up
  <idle>-0       0dN.h3..  149us : activate_task <-ttwu_do_activate.constprop.94
  <idle>-0       0dN.h3..  151us : update_rq_clock.part.82 <-activate_task
  <idle>-0       0dN.h3..  152us : enqueue_task_fair <-activate_task
  <idle>-0       0dN.h3..  153us : enqueue_entity <-enqueue_task_fair
  <idle>-0       0dN.h3..  154us : update_curr <-enqueue_entity
  <idle>-0       0dN.h3..  156us : __compute_runnable_contrib <-enqueue_entity
  <idle>-0       0dN.h3..  157us : account_entity_enqueue <-enqueue_entity
  <idle>-0       0dN.h3..  158us : update_cfs_shares <-enqueue_entity
  <idle>-0       0dN.h3..  159us : __enqueue_entity <-enqueue_entity
  <idle>-0       0dN.h3..  161us : enqueue_entity <-enqueue_task_fair
  <idle>-0       0dN.h3..  162us : update_curr <-enqueue_entity
  <idle>-0       0dN.h3..  163us : account_entity_enqueue <-enqueue_entity
  <idle>-0       0dN.h3..  164us : update_cfs_shares <-enqueue_entity
  <idle>-0       0dN.h3..  165us : __enqueue_entity <-enqueue_entity
  <idle>-0       0dN.h3..  167us : hrtick_update <-enqueue_task_fair
  <idle>-0       0dN.h3..  168us : ttwu_do_wakeup <-ttwu_do_activate.constprop.94
  <idle>-0       0dN.h3..  169us : check_preempt_curr <-ttwu_do_wakeup
  <idle>-0       0dN.h3..  169us : resched_curr <-check_preempt_curr
  <idle>-0       0dN.h3..  170us : preempt_count_sub <-__raw_spin_unlock
  <idle>-0       0dN.h2..  173us : _raw_spin_unlock_irqrestore <-try_to_wake_up
  <idle>-0       0dN.h2..  174us : preempt_count_sub <-_raw_spin_unlock_irqrestore
  <idle>-0       0dN.h1..  176us : _raw_spin_lock <-__hrtimer_run_queues
  <idle>-0       0dN.h1..  177us : preempt_count_add <-_raw_spin_lock
  <idle>-0       0dN.h2..  178us : __remove_hrtimer <-__hrtimer_run_queues
  <idle>-0       0dN.h2..  180us : preempt_count_sub <-__hrtimer_run_queues
  <idle>-0       0dN.h1..  181us : hrtimer_wakeup <-__hrtimer_run_queues
  <idle>-0       0dN.h1..  182us : wake_up_process <-hrtimer_wakeup
  <idle>-0       0dN.h1..  184us : try_to_wake_up <-wake_up_process
  <idle>-0       0dN.h1..  185us : _raw_spin_lock_irqsave <-try_to_wake_up
  <idle>-0       0dN.h1..  187us : preempt_count_add <-_raw_spin_lock_irqsave
  <idle>-0       0dN.h2..  189us : task_waking_fair <-try_to_wake_up
  <idle>-0       0dN.h2..  190us : select_task_rq_fair <-try_to_wake_up
  <idle>-0       0dN.h2..  191us : __rcu_read_lock <-select_task_rq_fair
  <idle>-0       0dN.h2..  192us : select_idle_sibling <-select_task_rq_fair
  <idle>-0       0dN.h2..  194us : idle_cpu <-select_idle_sibling
  <idle>-0       0dN.h2..  196us : idle_cpu <-select_idle_sibling
  <idle>-0       0dN.h2..  197us : idle_cpu <-select_idle_sibling
  <idle>-0       0dN.h2..  198us : idle_cpu <-select_idle_sibling
  <idle>-0       0dN.h2..  199us : idle_cpu <-select_idle_sibling
  <idle>-0       0dN.h2..  201us : idle_cpu <-select_idle_sibling
  <idle>-0       0dN.h2..  202us : __rcu_read_unlock <-select_task_rq_fair
  <idle>-0       0dN.h2..  203us : _raw_spin_lock <-try_to_wake_up
  <idle>-0       0dN.h2..  204us : preempt_count_add <-_raw_spin_lock
  <idle>-0       0dN.h3..  205us : native_queued_spin_lock_slowpath <-_raw_spin_lock
  <idle>-0       0dN.h3..  212us : ttwu_do_activate.constprop.94 <-try_to_wake_up
  <idle>-0       0dN.h3..  213us : activate_task <-ttwu_do_activate.constprop.94
  <idle>-0       0dN.h3..  214us : update_rq_clock.part.82 <-activate_task
  <idle>-0       0dN.h3..  215us : enqueue_task_fair <-activate_task
  <idle>-0       0dN.h3..  216us : enqueue_entity <-enqueue_task_fair
  <idle>-0       0dN.h3..  218us : update_curr <-enqueue_entity
  <idle>-0       0dN.h3..  219us : __compute_runnable_contrib <-enqueue_entity
  <idle>-0       0dN.h3..  221us : account_entity_enqueue <-enqueue_entity
  <idle>-0       0dN.h3..  222us : update_cfs_shares <-enqueue_entity
  <idle>-0       0dN.h3..  225us : __enqueue_entity <-enqueue_entity
  <idle>-0       0dN.h3..  226us : enqueue_entity <-enqueue_task_fair
  <idle>-0       0dN.h3..  227us : update_curr <-enqueue_entity
  <idle>-0       0dN.h3..  230us : account_entity_enqueue <-enqueue_entity
  <idle>-0       0dN.h3..  231us : update_cfs_shares <-enqueue_entity
  <idle>-0       0dN.h3..  233us : __enqueue_entity <-enqueue_entity
  <idle>-0       0dN.h3..  236us : hrtick_update <-enqueue_task_fair
  <idle>-0       0dN.h3..  237us : ttwu_do_wakeup <-ttwu_do_activate.constprop.94
  <idle>-0       0dN.h3..  239us : check_preempt_curr <-ttwu_do_wakeup
  <idle>-0       0dN.h3..  240us : resched_curr <-check_preempt_curr
  <idle>-0       0dN.h3..  243us : preempt_count_sub <-__raw_spin_unlock
  <idle>-0       0dN.h2..  245us : _raw_spin_unlock_irqrestore <-try_to_wake_up
  <idle>-0       0dN.h2..  247us : preempt_count_sub <-_raw_spin_unlock_irqrestore
  <idle>-0       0dN.h1..  248us : _raw_spin_lock <-__hrtimer_run_queues
  <idle>-0       0dN.h1..  250us : preempt_count_add <-_raw_spin_lock
  <idle>-0       0dN.h2..  251us : __hrtimer_get_next_event <-hrtimer_interrupt
  <idle>-0       0dN.h2..  253us : preempt_count_sub <-hrtimer_interrupt
  <idle>-0       0dN.h1..  255us : tick_program_event <-hrtimer_interrupt
  <idle>-0       0dN.h1..  256us : clockevents_program_event <-tick_program_event
  <idle>-0       0dN.h1..  257us : ktime_get <-clockevents_program_event
  <idle>-0       0dN.h1..  258us : lapic_next_deadline <-clockevents_program_event
  <idle>-0       0dN.h1..  259us : irq_exit <-smp_apic_timer_interrupt
  <idle>-0       0dN.h1..  261us : preempt_count_sub <-irq_exit
  <idle>-0       0dN..1..  263us : wakeup_softirqd <-irq_exit
  <idle>-0       0dN..1..  264us : wake_up_process <-wakeup_softirqd
  <idle>-0       0dN..1..  265us : try_to_wake_up <-wake_up_process
  <idle>-0       0dN..1..  266us : _raw_spin_lock_irqsave <-try_to_wake_up
  <idle>-0       0dN..1..  267us : preempt_count_add <-_raw_spin_lock_irqsave
  <idle>-0       0dN..2..  268us : task_waking_fair <-try_to_wake_up
  <idle>-0       0dN..2..  269us : _raw_spin_lock <-try_to_wake_up
  <idle>-0       0dN..2..  270us : preempt_count_add <-_raw_spin_lock
  <idle>-0       0dN..3..  271us : native_queued_spin_lock_slowpath <-_raw_spin_lock
  <idle>-0       0dN..3..  274us : ttwu_do_activate.constprop.94 <-try_to_wake_up
  <idle>-0       0dN..3..  275us : activate_task <-ttwu_do_activate.constprop.94
  <idle>-0       0dN..3..  276us : update_rq_clock.part.82 <-activate_task
  <idle>-0       0dN..3..  277us : enqueue_task_fair <-activate_task
  <idle>-0       0dN..3..  279us : enqueue_entity <-enqueue_task_fair
  <idle>-0       0dN..3..  280us : update_curr <-enqueue_entity
  <idle>-0       0dN..3..  281us : account_entity_enqueue <-enqueue_entity
  <idle>-0       0dN..3..  282us : update_cfs_shares <-enqueue_entity
  <idle>-0       0dN..3..  284us : __enqueue_entity <-enqueue_entity
  <idle>-0       0dN..3..  285us : hrtick_update <-enqueue_task_fair
  <idle>-0       0dN..3..  286us : ttwu_do_wakeup <-ttwu_do_activate.constprop.94
  <idle>-0       0dN..3..  287us : check_preempt_curr <-ttwu_do_wakeup
  <idle>-0       0dN..3..  288us : resched_curr <-check_preempt_curr
  <idle>-0       0dN..3..  290us : preempt_count_sub <-__raw_spin_unlock
  <idle>-0       0dN..2..  291us : _raw_spin_unlock_irqrestore <-try_to_wake_up
  <idle>-0       0dN..2..  291us : preempt_count_sub <-_raw_spin_unlock_irqrestore
  <idle>-0       0dN..1..  293us : wakeup_timer_softirqd <-irq_exit
  <idle>-0       0dN..1..  295us : wake_up_process <-wakeup_timer_softirqd
  <idle>-0       0dN..1..  296us : try_to_wake_up <-wake_up_process
  <idle>-0       0dN..1..  297us : _raw_spin_lock_irqsave <-try_to_wake_up
  <idle>-0       0dN..1..  298us : preempt_count_add <-_raw_spin_lock_irqsave
  <idle>-0       0dN..2..  299us : _raw_spin_lock <-try_to_wake_up
  <idle>-0       0dN..2..  300us : preempt_count_add <-_raw_spin_lock
  <idle>-0       0dN..3..  301us : ttwu_do_activate.constprop.94 <-try_to_wake_up
  <idle>-0       0dN..3..  302us : activate_task <-ttwu_do_activate.constprop.94
  <idle>-0       0dN..3..  303us : update_rq_clock.part.82 <-activate_task
  <idle>-0       0dN..3..  304us : enqueue_task_rt <-activate_task
  <idle>-0       0dN..3..  305us : dequeue_rt_stack <-enqueue_task_rt
  <idle>-0       0dN..3..  306us : dequeue_top_rt_rq <-dequeue_rt_stack
  <idle>-0       0dN..3..  307us : cpupri_set <-enqueue_task_rt
  <idle>-0       0dN..3..  308us : update_rt_migration <-enqueue_task_rt
  <idle>-0       0dN..3..  309us : _raw_spin_lock <-enqueue_task_rt
  <idle>-0       0dN..3..  310us : preempt_count_add <-_raw_spin_lock
  <idle>-0       0dN..4..  311us : preempt_count_sub <-enqueue_task_rt
  <idle>-0       0dN..3..  312us : enqueue_top_rt_rq <-enqueue_task_rt
  <idle>-0       0dN..3..  313us : ttwu_do_wakeup <-ttwu_do_activate.constprop.94
  <idle>-0       0dN..3..  314us : check_preempt_curr <-ttwu_do_wakeup
  <idle>-0       0dN..3..  314us : resched_curr <-check_preempt_curr
  <idle>-0       0dN..3..  316us : task_woken_rt <-ttwu_do_wakeup
  <idle>-0       0dN..3..  317us : preempt_count_sub <-__raw_spin_unlock
  <idle>-0       0dN..2..  318us : _raw_spin_unlock_irqrestore <-try_to_wake_up
  <idle>-0       0dN..2..  319us : preempt_count_sub <-_raw_spin_unlock_irqrestore
  <idle>-0       0dN..1..  320us : idle_cpu <-irq_exit
  <idle>-0       0dN..1..  321us : rcu_irq_exit <-irq_exit
  <idle>-0       0dN..1..  321us : rcu_eqs_enter_common <-rcu_irq_exit
  <idle>-0       0dN..1..  322us : trace_hardirqs_on_thunk <-restore_regs_and_iret
  <idle>-0       0dN..1..  324us+: trace_hardirqs_on_caller <-restore_regs_and_iret
  <idle>-0       0dN..1..  383us : <stack trace>
 => trace_hardirqs_on_thunk
 => cpuidle_enter
 => call_cpuidle
 => cpu_startup_entry
 => rest_init
 => start_kernel
 => x86_64_start_reservations
 => x86_64_start_kernel
```
现在的问题是这样的，从栈上来看，调用的入口和出口都是一样的，但是其关中断的时间是不一样的，时间不同有两种可能性：一种执行路径完全一致，但是由于硬件上原因可能同一个函数的执行时间不同;另一种可能性就是执行路径都是不同的。通过对log的分析，排除了第一种可能性（当然同一个函数的执行时间在不同时刻也是可能不同的，为简化问题先忽略这点）。那么如何从这两段log中分析出问题来呢？
我分别找了内核栈中两个不同的调用片段  
来自log1
```
  <idle>-0       0d..h1..   90us : rcu_check_callbacks <-update_process_times
  <idle>-0       0d..h1..   91us : rcu_sched_qs <-rcu_check_callbacks
  <idle>-0       0d..h1..   92us : rcu_bh_qs <-rcu_check_callbacks
  <idle>-0       0d..h1..   93us : rcu_preempt_qs <-rcu_bh_qs
  <idle>-0       0d..h1..   94us : rcu_preempt_qs <-rcu_check_callbacks
  <idle>-0       0d..h1..   95us : invoke_rcu_core <-rcu_check_callbacks
```
来自log2
```
  <idle>-0       0d..h1..  121us : rcu_check_callbacks <-update_process_times
  <idle>-0       0d..h1..  122us : rcu_sched_qs <-rcu_check_callbacks
  <idle>-0       0d..h1..  123us : rcu_bh_qs <-rcu_check_callbacks
  <idle>-0       0d..h1..  125us : rcu_preempt_qs <-rcu_bh_qs
  <idle>-0       0d..h1..  127us : rcu_preempt_qs <-rcu_check_callbacks
  <idle>-0       0d..h1..  129us : cpu_needs_another_gp <-rcu_check_callbacks
  <idle>-0       0d..h1..  131us : invoke_rcu_core <-rcu_check_callbacks
```
通过对比发现 log2多执行了一条程序 好了 问题到这该怎么进一步分析？这种分析感觉是不够的。那么下一步是要继续深入到函数内部读代码分析？

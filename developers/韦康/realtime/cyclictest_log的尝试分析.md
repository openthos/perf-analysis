#关于对cyclictest测延时抖动的尝试性分析
##说明
关于延时的抖动很多时候将原因归结为以下几个方面，内存的换入与换出（内存的不确定性），cache命中的不确定性，以及多进程调度的不确定性。

上周跟踪cyclictest产生了一些log，当时没有合理的方法来分析这些log（额，当然了。。。现在也是不知道的！）。不过这周尝试去分析这段log中的一部分，也许能解释延时抖动的部分原因（单纯从这段log分析延时抖动的原因是很有局限性的）。

在分析中并没有尝试去分析整个log，而是挑选了schedule()这个函数去分析，所以分析是很有局限的。该schedule()的触发时机是在nanosleep使得该进程进入休眠状态时触发的。需要解释的是这里的schedule函数是休眠时触发的，它产生的延时应该不能算作对该进程的影响，应当成对下一个被选中进程的影响。但是这并不妨碍我们对延时抖动原因的分析。


##分析
log 1.这是一段出现频率最高的schedule()函数整体的调用流程情况，所以我将该schedule函数的调用作为分析的基准。下面会又几段调用关系出现轻微变化的schedule()流程。我们需要先大致统计一下这个schedule花费了多少个us（这里不是10053.32 us），可以大致将各个函数的花费累加起来（不超过30个us）。
```
 7)               |        schedule() {
 7)   0.059 us    |          preempt_count_add();
 7)               |          rcu_note_context_switch() {
 7)   0.055 us    |            rcu_sched_qs();
 7)   0.059 us    |            rcu_preempt_qs();
 7)   1.211 us    |          }
 7)               |          _raw_spin_lock_irq() {
 7)   0.055 us    |            preempt_count_add();
 7)   0.552 us    |          }
 7)               |          deactivate_task() {
 7)   0.081 us    |            update_rq_clock.part.82();
 7)               |            dequeue_task_fair() {
 7)               |              dequeue_entity() {
 7)               |                update_curr() {
 7)   0.053 us    |                  update_min_vruntime();
 7)               |                  cpuacct_charge() {
 7)   0.047 us    |                    __rcu_read_lock();
 7)   0.047 us    |                    __rcu_read_unlock();
 7)   1.014 us    |                  }
 7)   2.050 us    |                }
 7)   0.056 us    |                clear_buddies();
 7)   0.079 us    |                account_entity_dequeue();
 7)   0.054 us    |                update_min_vruntime();
 7)               |                update_cfs_shares() {
 7)               |                  update_curr() {
 7)   0.059 us    |                    __calc_delta();
 7)   0.058 us    |                    update_min_vruntime();
 7)   1.081 us    |                  }
 7)   0.072 us    |                  account_entity_dequeue();
 7)   0.077 us    |                  account_entity_enqueue();
 7)   2.641 us    |                }
 7)   7.196 us    |              }
 7)               |              dequeue_entity() {
 7)   0.066 us    |                update_curr();
 7)   0.053 us    |                clear_buddies();
 7)   0.064 us    |                account_entity_dequeue();
 7)   0.054 us    |                update_min_vruntime();
 7)   0.059 us    |                update_cfs_shares();
 7)   2.554 us    |              }
 7)   0.048 us    |              hrtick_update();
 7) + 11.156 us   |            }
 7) + 12.187 us   |          }
 7)               |          pick_next_task_fair() {
 7)   0.050 us    |            __rcu_read_lock();
 7)   0.051 us    |            __msecs_to_jiffies();
 7)   0.054 us    |            __rcu_read_unlock();
 7)   1.525 us    |          }
 7)               |          pick_next_task_idle() {
 7)               |            put_prev_task_fair() {
 7)   0.061 us    |              put_prev_entity();
 7)   0.054 us    |              put_prev_entity();
 7)   1.041 us    |            }
 7)   1.554 us    |          }
 7)               |          finish_task_switch() {
 7)               |            _raw_spin_unlock_irq() {
 7)   0.078 us    |              preempt_count_sub();
 7)   0.606 us    |            }
 7)   1.140 us    |          }
 7)   0.055 us    |          preempt_count_sub();
 7) * 10053.32 us |        }
```
log 2.这是一段在schedule()出现了时钟中断的log
```
 7)               |        schedule() {
 7)   0.059 us    |          preempt_count_add();
 7)               |          rcu_note_context_switch() {
 7)   0.063 us    |            rcu_sched_qs();
 7)   0.057 us    |            rcu_preempt_qs();
 7)   1.040 us    |          }
 7)               |          _raw_spin_lock_irq() {
 7)   0.053 us    |            preempt_count_add();
 7)   0.554 us    |          }
 7)               |          deactivate_task() {
 7)   0.078 us    |            update_rq_clock.part.82();
 7)               |            dequeue_task_fair() {
 7)               |              dequeue_entity() {
 7)               |                update_curr() {
 7)   0.053 us    |                  update_min_vruntime();
 7)               |                  cpuacct_charge() {
 7)   0.050 us    |                    __rcu_read_lock();
 7)   0.053 us    |                    __rcu_read_unlock();
 7)   1.049 us    |                  }
 7)   2.088 us    |                }
 7)   0.052 us    |                clear_buddies();
 7)   0.131 us    |                account_entity_dequeue();
 7)   0.058 us    |                update_min_vruntime();
 7)               |                update_cfs_shares() {
 7)               |                  update_curr() {
 7)   0.080 us    |                    __calc_delta();
 7)   0.056 us    |                    update_min_vruntime();
 7)   1.128 us    |                  }
 7)   0.067 us    |                  account_entity_dequeue();
 7)   0.066 us    |                  account_entity_enqueue();
 7)   2.664 us    |                }
 7)   7.539 us    |              }
 7)               |              dequeue_entity() {
 7)   0.057 us    |                update_curr();
 7)   0.052 us    |                clear_buddies();
 7)   0.058 us    |                account_entity_dequeue();
 7)   0.051 us    |                update_min_vruntime();
 7)   0.052 us    |                update_cfs_shares();
 7)   2.502 us    |              }
 7)   0.050 us    |              hrtick_update();
 7) + 11.456 us   |            }
 7) + 12.472 us   |          }
 7)               |          pick_next_task_fair() {
 7)   0.047 us    |            __rcu_read_lock();
 7)   0.053 us    |            __msecs_to_jiffies();
 7)   0.056 us    |            __rcu_read_unlock();
 7)   1.524 us    |          }
 7)               |          pick_next_task_idle() {
 7)               |            put_prev_task_fair() {
 7)   0.060 us    |              put_prev_entity();
 7)   0.059 us    |              put_prev_entity();
 7)   1.038 us    |            }
 7)   1.546 us    |          }
 7)               |          finish_task_switch() {
 7)               |            _raw_spin_unlock_irq() {
 7)   0.079 us    |              preempt_count_sub();
 7)   0.591 us    |            }
 7)   ==========> |
 7)               |            smp_apic_timer_interrupt() {
 7)               |              irq_enter() {
 7)   0.088 us    |                rcu_irq_enter();
 7)   0.050 us    |                preempt_count_add();
 7)   1.077 us    |              }
 7)   0.076 us    |              exit_idle();
 7)               |              local_apic_timer_interrupt() {
 7)               |                hrtimer_interrupt() {
 7)               |                  _raw_spin_lock() {
 7)   0.063 us    |                    preempt_count_add();
 7)   0.574 us    |                  }
 7)   0.151 us    |                  ktime_get_update_offsets_now();
 7)               |                  __hrtimer_run_queues() {
 7)   0.120 us    |                    __remove_hrtimer();
 7)   0.057 us    |                    preempt_count_sub();
 7)               |                    tick_sched_timer() {
 7)   0.077 us    |                      ktime_get();
 7)   0.056 us    |                      tick_sched_do_timer();
 7)               |                      tick_sched_handle.isra.13() {
 7)               |                        update_process_times() {
 7)               |                          account_process_tick() {
 7)               |                            account_system_time() {
 7)   0.052 us    |                              in_serving_softirq();
 7)               |                              cpuacct_account_field() {
 7)   0.054 us    |                                __rcu_read_lock();
 7)   0.063 us    |                                __rcu_read_unlock();
 7)   0.977 us    |                              }
 7)               |                              acct_account_cputime() {
 7)               |                                __acct_update_integrals() {
 7)   0.054 us    |                                  jiffies_to_timeval();
 7)   0.636 us    |                                }
 7)   1.141 us    |                              }
 7)   3.693 us    |                            }
 7)   4.241 us    |                          }
 7)               |                          scheduler_tick() {
 7)               |                            _raw_spin_lock() {
 7)   0.062 us    |                              preempt_count_add();
 7)   0.636 us    |                            }
 7)   0.079 us    |                            update_rq_clock.part.82();
 7)               |                            task_tick_fair() {
 7)               |                              update_curr() {
 7)   0.057 us    |                                update_min_vruntime();
 7)               |                                cpuacct_charge() {
 7)   0.057 us    |                                  __rcu_read_lock();
 7)   0.064 us    |                                  __rcu_read_unlock();
 7)   1.164 us    |                                }
 7)   2.206 us    |                              }
 7)               |                              update_cfs_shares() {
 7)               |                                update_curr() {
 7)   0.071 us    |                                  __calc_delta();
 7)   0.055 us    |                                  update_min_vruntime();
 7)   1.108 us    |                                }
 7)   0.069 us    |                                account_entity_dequeue();
 7)   0.072 us    |                                account_entity_enqueue();
 7)   2.757 us    |                              }
 7)   0.130 us    |                              hrtimer_active();
 7)   0.073 us    |                              update_curr();
 7)   0.081 us    |                              update_cfs_shares();
 7)   0.046 us    |                              hrtimer_active();
 7)   8.443 us    |                            }
 7)               |                            update_cpu_load_active() {
 7)               |                              __update_cpu_load() {
 7)   0.067 us    |                                sched_avg_update();
 7)   0.596 us    |                              }
 7)   1.107 us    |                            }
 7)   0.059 us    |                            calc_global_load_tick();
 7)   0.061 us    |                            preempt_count_sub();
 7)               |                            trigger_load_balance() {
 7)               |                              raise_softirq() {
 7)               |                                raise_softirq_irqoff() {
 7)   0.092 us    |                                  do_raise_softirq_irqoff();
 7)   0.590 us    |                                }
 7)   1.114 us    |                              }
 7)   0.054 us    |                              __rcu_read_lock();
 7)   0.057 us    |                              __rcu_read_unlock();
 7)   2.864 us    |                            }
 7) + 16.731 us   |                          }
 7)   0.056 us    |                          hrtimer_run_queues();
 7)               |                          raise_softirq() {
 7)               |                            raise_softirq_irqoff() {
 7)   0.087 us    |                              do_raise_softirq_irqoff();
 7)   0.565 us    |                            }
 7)   1.077 us    |                          }
 7)               |                          rcu_check_callbacks() {
 7)               |                            rcu_bh_qs() {
 7)   0.058 us    |                              rcu_preempt_qs();
 7)   0.575 us    |                            }
 7)   0.065 us    |                            rcu_preempt_qs();
 7)               |                            invoke_rcu_core() {
 7)               |                              wake_up_process() {
 7)               |                                try_to_wake_up() {
 7)               |                                  _raw_spin_lock_irqsave() {
 7)   0.049 us    |                                    preempt_count_add();
 7)   0.541 us    |                                  }
 7)   0.069 us    |                                  task_waking_fair();
 7)               |                                  _raw_spin_lock() {
 7)   0.049 us    |                                    preempt_count_add();
 7)   0.548 us    |                                  }
 7)               |                                  ttwu_do_activate.constprop.94() {
 7)               |                                    activate_task() {
 7)   0.074 us    |                                      update_rq_clock.part.82();
 7)               |                                      enqueue_task_fair() {
 7)               |                                        enqueue_entity() {
 7)               |                                          update_curr() {
 7)   0.068 us    |                                            __calc_delta();
 7)   0.054 us    |                                            update_min_vruntime();
 7)   1.053 us    |                                          }
 7)   0.067 us    |                                          account_entity_enqueue();
 7)   0.053 us    |                                          update_cfs_shares();
 7)   0.066 us    |                                          __enqueue_entity();
 7)   3.146 us    |                                        }
 7)   0.051 us    |                                        hrtick_update();
 7)   4.172 us    |                                      }
 7)   5.195 us    |                                    }
 7)               |                                    ttwu_do_wakeup() {
 7)               |                                      check_preempt_curr() {
 7)               |                                        check_preempt_wakeup() {
 7)   0.065 us    |                                          update_curr();
 7)   0.051 us    |                                          wakeup_preempt_entity.isra.54();
 7)   0.075 us    |                                          set_next_buddy();
 7)   0.067 us    |                                          resched_curr_lazy();
 7)   2.224 us    |                                        }
 7)   2.805 us    |                                      }
 7)   3.441 us    |                                    }
 7)   9.611 us    |                                  }
 7)   0.102 us    |                                  preempt_count_sub();
 7)               |                                  _raw_spin_unlock_irqrestore() {
 7)   0.071 us    |                                    preempt_count_sub();
 7)   0.673 us    |                                  }
 7) + 14.526 us   |                                }
 7) + 15.060 us   |                              }
 7) + 15.687 us   |                            }
 7) + 17.891 us   |                          }
 7)   0.145 us    |                          run_posix_cpu_timers();
 7) + 43.023 us   |                        }
 7)   0.087 us    |                        profile_tick();
 7) + 44.463 us   |                      }
 7)   0.083 us    |                      hrtimer_forward();
 7) + 46.717 us   |                    }
 7)               |                    _raw_spin_lock() {
 7)   0.066 us    |                      preempt_count_add();
 7)   0.632 us    |                    }
 7)   0.116 us    |                    enqueue_hrtimer();
 7) + 50.548 us   |                  }
 7)   0.086 us    |                  __hrtimer_get_next_event();
 7)   0.067 us    |                  preempt_count_sub();
 7)               |                  tick_program_event() {
 7)               |                    clockevents_program_event() {
 7)   0.097 us    |                      ktime_get();
 7)   0.166 us    |                      lapic_next_deadline();
 7)   1.318 us    |                    }
 7)   1.913 us    |                  }
 7) + 56.424 us   |                }
 7) + 56.988 us   |              }
 7)               |              irq_exit() {
 7)   0.073 us    |                preempt_count_sub();
 7)               |                wakeup_softirqd() {
 7)               |                  wake_up_process() {
 7)               |                    try_to_wake_up() {
 7)               |                      _raw_spin_lock_irqsave() {
 7)   0.069 us    |                        preempt_count_add();
 7)   0.653 us    |                      }
 7)   0.077 us    |                      task_waking_fair();
 7)               |                      _raw_spin_lock() {
 7)   0.068 us    |                        preempt_count_add();
 7)   0.620 us    |                      }
 7)               |                      ttwu_do_activate.constprop.94() {
 7)               |                        activate_task() {
 7)   0.107 us    |                          update_rq_clock.part.82();
 7)               |                          enqueue_task_fair() {
 7)               |                            enqueue_entity() {
 7)               |                              update_curr() {
 7)   0.067 us    |                                __calc_delta();
 7)   0.077 us    |                                update_min_vruntime();
 7)   1.213 us    |                              }
 7)   0.074 us    |                              account_entity_enqueue();
 7)   0.064 us    |                              update_cfs_shares();
 7)   0.087 us    |                              __enqueue_entity();
 7)   3.551 us    |                            }
 7)   0.066 us    |                            hrtick_update();
 7)   4.694 us    |                          }
 7)   5.857 us    |                        }
 7)               |                        ttwu_do_wakeup() {
 7)               |                          check_preempt_curr() {
 7)               |                            check_preempt_wakeup() {
 7)   0.080 us    |                              update_curr();
 7)   0.065 us    |                              wakeup_preempt_entity.isra.54();
 7)   0.069 us    |                              set_next_buddy();
 7)   0.079 us    |                              resched_curr_lazy();
 7)   2.304 us    |                            }
 7)   2.868 us    |                          }
 7)   3.470 us    |                        }
 7) + 10.349 us   |                      }
 7)   0.079 us    |                      preempt_count_sub();
 7)               |                      _raw_spin_unlock_irqrestore() {
 7)   0.070 us    |                        preempt_count_sub();
 7)   0.825 us    |                      }
 7) + 15.692 us   |                    }
 7) + 16.283 us   |                  }
 7) + 16.889 us   |                }
 7)               |                wakeup_timer_softirqd() {
 7)               |                  wake_up_process() {
 7)               |                    try_to_wake_up() {
 7)               |                      _raw_spin_lock_irqsave() {
 7)   0.070 us    |                        preempt_count_add();
 7)   0.622 us    |                      }
 7)               |                      _raw_spin_lock() {
 7)   0.069 us    |                        preempt_count_add();
 7)   0.611 us    |                      }
 7)               |                      ttwu_do_activate.constprop.94() {
 7)               |                        activate_task() {
 7)   0.098 us    |                          update_rq_clock.part.82();
 7)               |                          enqueue_task_rt() {
 7)               |                            dequeue_rt_stack() {
 7)   0.078 us    |                              dequeue_top_rt_rq();
 7)   0.670 us    |                            }
 7)   0.156 us    |                            cpupri_set();
 7)   0.066 us    |                            update_rt_migration();
 7)               |                            _raw_spin_lock() {
 7)   0.067 us    |                              preempt_count_add();
 7)   0.620 us    |                            }
 7)   0.136 us    |                            preempt_count_sub();
 7)   0.070 us    |                            enqueue_top_rt_rq();
 7)   4.761 us    |                          }
 7)   5.907 us    |                        }
 7)               |                        ttwu_do_wakeup() {
 7)               |                          check_preempt_curr() {
 7)   0.103 us    |                            resched_curr();
 7)   0.696 us    |                          }
 7)   0.066 us    |                          task_woken_rt();
 7)   1.873 us    |                        }
 7)   8.813 us    |                      }
 7)   0.065 us    |                      preempt_count_sub();
 7)               |                      _raw_spin_unlock_irqrestore() {
 7)   0.069 us    |                        preempt_count_sub();
 7)   0.618 us    |                      }
 7) + 13.280 us   |                    }
 7) + 13.826 us   |                  }
 7) + 14.417 us   |                }
 7)   0.065 us    |                idle_cpu();
 7)   0.118 us    |                rcu_irq_exit();
 7) + 34.319 us   |              }
 7) + 94.401 us   |            }
 7)   <========== |
 7) + 96.326 us   |          }
 7)               |          preempt_count_sub() {
 7)               |            rcu_note_context_switch() {
 7)   0.080 us    |              rcu_sched_qs();
 7)   0.078 us    |              rcu_preempt_qs();
 7)   1.259 us    |            }
 7)               |            _raw_spin_lock_irq() {
 7)   0.066 us    |              preempt_count_add();
 7)   0.637 us    |            }
 7)   0.073 us    |            pick_next_task_stop();
 7)   0.080 us    |            pick_next_task_dl();
 7)               |            pick_next_task_rt() {
 7)               |              put_prev_task_fair() {
 7)               |                put_prev_entity() {
 7)               |                  update_curr() {
 7)   0.075 us    |                    update_min_vruntime();
 7)               |                    cpuacct_charge() {
 7)   0.069 us    |                      __rcu_read_lock();
 7)   0.083 us    |                      __rcu_read_unlock();
 7)   1.216 us    |                    }
 7)   2.553 us    |                  }
 7)   0.080 us    |                  __enqueue_entity();
 7)   3.853 us    |                }
 7)               |                put_prev_entity() {
 7)               |                  update_curr() {
 7)   0.067 us    |                    __calc_delta();
 7)   0.080 us    |                    update_min_vruntime();
 7)   1.222 us    |                  }
 7)   0.136 us    |                  __enqueue_entity();
 7)   2.428 us    |                }
 7)   7.341 us    |              }
 7)   7.972 us    |            }
 7)               |            finish_task_switch() {
 7)               |              _raw_spin_unlock_irq() {
 7)   0.079 us    |                preempt_count_sub();
 7)   0.584 us    |              }
 7)   1.131 us    |            }
 7)   0.082 us    |          }
 7) * 10177.15 us |        }
```
在这段log里发生了一次时钟中断，该时钟中断打断了正常schedule的执行流程，在该例子中整个时钟中断的耗时在96.326us，这对这段调度来说影响是极大的（超过了调度本身所花费的代价）。所以在调度时时钟中断的发生是产生延时抖动的一个重要原因。此外一点是在上次利用irqsoff追踪器对进行追踪器时发现，最大的关中断时间就是由时钟中断引起的，并且并非所有的时钟中断器函数的执行轨迹都相同。因此在调度时产生了不可避免的时钟中断是一定会造成延时抖动的。

log 3.这是一段cpu产生切换时的schedule()情况
```
 7)               |        schedule() {
 7)   0.058 us    |          preempt_count_add();
 7)               |          rcu_note_context_switch() {
 7)   0.060 us    |            rcu_sched_qs();
 7)   0.061 us    |            rcu_preempt_qs();
 7)   1.034 us    |          }
 7)               |          _raw_spin_lock_irq() {
 7)   0.054 us    |            preempt_count_add();
 7)   0.525 us    |          }
 7)               |          deactivate_task() {
 7)   0.082 us    |            update_rq_clock.part.82();
 7)               |            dequeue_task_fair() {
 7)               |              dequeue_entity() {
 7)               |                update_curr() {
 7)   0.052 us    |                  update_min_vruntime();
 7)               |                  cpuacct_charge() {
 7)   0.050 us    |                    __rcu_read_lock();
 7)   0.050 us    |                    __rcu_read_unlock();
 7)   1.015 us    |                  }
 7)   2.032 us    |                }
 7)   0.050 us    |                __compute_runnable_contrib();
 7)   0.055 us    |                clear_buddies();
 7)   0.071 us    |                account_entity_dequeue();
 7)   0.050 us    |                update_min_vruntime();
 7)               |                update_cfs_shares() {
 7)               |                  update_curr() {
 7)   0.078 us    |                    __calc_delta();
 7)   0.052 us    |                    update_min_vruntime();
 7)   1.067 us    |                  }
 7)   0.065 us    |                  account_entity_dequeue();
 7)   0.065 us    |                  account_entity_enqueue();
 7)   2.623 us    |                }
 7)   7.800 us    |              }
 7)               |              dequeue_entity() {
 7)   0.063 us    |                update_curr();
 7)   0.052 us    |                __compute_runnable_contrib();
 7)   0.052 us    |                clear_buddies();
 7)   0.055 us    |                account_entity_dequeue();
 7)   0.054 us    |                update_min_vruntime();
 7)   0.070 us    |                update_cfs_shares();
 7)   2.994 us    |              }
 7)   0.047 us    |              hrtick_update();
 7) + 12.236 us   |            }
 7) + 13.256 us   |          }
 7)               |          pick_next_task_fair() {
 7)   0.050 us    |            __rcu_read_lock();
 7)   0.054 us    |            __msecs_to_jiffies();
 7)   0.051 us    |            __rcu_read_unlock();
 7)   1.517 us    |          }
 7)               |          pick_next_task_idle() {
 7)               |            put_prev_task_fair() {
 7)   0.061 us    |              put_prev_entity();
 7)   0.058 us    |              put_prev_entity();
 7)   1.005 us    |            }
 7)   1.495 us    |          }
 1)   2.554 us    |      }  
```
我们分析该段进程会发现该部分的执行轨迹同1中的执行轨迹也是有着些许差别的。首先一个很明显的差别就是log 1中存在了这样一段函数：
```
 7)               |          finish_task_switch() {
 7)               |            _raw_spin_unlock_irq() {
 7)   0.078 us    |              preempt_count_sub();
 7)   0.606 us    |            }
 7)   1.140 us    |          }
 7)   0.055 us    |          preempt_count_sub();
```
该部分函数主要完成进程切换后的清理工作，但是在log 3中确没有这样一段，仔细观察下面的cpu id我们会发现其cpu id发生了变化。这一点是我不是很懂，但是可以确定的是在cpu发生了迁移的时候也会产生延时的抖动。

log 4: 可以注意到这段log的执行轨迹同log 1也是有着显著差别的。
```
 1)               |        schedule() {
 1)   0.059 us    |          preempt_count_add();
 1)               |          rcu_note_context_switch() {
 1)   0.059 us    |            rcu_sched_qs();
 1)   0.056 us    |            rcu_preempt_qs();
 1)   1.013 us    |          }
 1)               |          _raw_spin_lock_irq() {
 1)   0.064 us    |            preempt_count_add();
 1)   0.561 us    |          }
 1)               |          deactivate_task() {
 1)   0.078 us    |            update_rq_clock.part.82();
 1)               |            dequeue_task_fair() {
 1)               |              dequeue_entity() {
 1)               |                update_curr() {
 1)   0.054 us    |                  update_min_vruntime();
 1)               |                  cpuacct_charge() {
 1)   0.050 us    |                    __rcu_read_lock();
 1)   0.051 us    |                    __rcu_read_unlock();
 1)   1.103 us    |                  }
 1)   2.225 us    |                }
 1)   0.053 us    |                clear_buddies();
 1)   0.127 us    |                account_entity_dequeue();
 1)   0.054 us    |                update_min_vruntime();
 1)               |                update_cfs_shares() {
 1)               |                  update_curr() {
 1)   0.073 us    |                    __calc_delta();
 1)   0.052 us    |                    update_min_vruntime();
 1)   1.252 us    |                  }
 1)   0.062 us    |                  account_entity_dequeue();
 1)   0.064 us    |                  account_entity_enqueue();
 1)   2.784 us    |                }
 1)   7.557 us    |              }
 1)               |              dequeue_entity() {
 1)   0.062 us    |                update_curr();
 1)   0.049 us    |                __compute_runnable_contrib();
 1)   0.050 us    |                clear_buddies();
 1)   0.063 us    |                account_entity_dequeue();
 1)   0.050 us    |                update_min_vruntime();
 1)   0.078 us    |                update_cfs_shares();
 1)   3.098 us    |              }
 1)   0.051 us    |              hrtick_update();
 1) + 12.123 us   |            }
 1) + 13.137 us   |          }
 1)               |          pick_next_task_fair() {
 1)   0.056 us    |            preempt_count_sub();
 1)               |            update_blocked_averages() {
 1)               |              _raw_spin_lock_irqsave() {
 1)   0.064 us    |                preempt_count_add();
 1)   0.535 us    |              }
 1)               |              update_rq_clock() {
 1)   0.073 us    |                update_rq_clock.part.82();
 1)   0.541 us    |              }
 1)   0.052 us    |              __compute_runnable_contrib();
 1)   0.048 us    |              __compute_runnable_contrib();
 1)   0.049 us    |              __compute_runnable_contrib();
 1)   0.050 us    |              __compute_runnable_contrib();
 1)   0.050 us    |              __compute_runnable_contrib();
 1)   0.049 us    |              __compute_runnable_contrib();
 1)   0.051 us    |              __compute_runnable_contrib();
 1)   0.050 us    |              __compute_runnable_contrib();
 1)   0.049 us    |              __compute_runnable_contrib();
 1)   0.050 us    |              __compute_runnable_contrib();
 1)   0.049 us    |              __compute_runnable_contrib();
 1)   0.051 us    |              __compute_runnable_contrib();
 1)   0.051 us    |              __compute_runnable_contrib();
 1)   0.050 us    |              __compute_runnable_contrib();
 1)   0.050 us    |              __compute_runnable_contrib();
 1)   0.052 us    |              __compute_runnable_contrib();
 1)   0.050 us    |              __compute_runnable_contrib();
 1)   0.050 us    |              __compute_runnable_contrib();
 1)   0.052 us    |              __compute_runnable_contrib();
 1)   0.052 us    |              __compute_runnable_contrib();
 1)   0.050 us    |              __compute_runnable_contrib();
 1)   0.052 us    |              __compute_runnable_contrib();
 1)   0.049 us    |              __compute_runnable_contrib();
 1)   0.050 us    |              __compute_runnable_contrib();
 1)   0.050 us    |              __compute_runnable_contrib();
 1)   0.051 us    |              __compute_runnable_contrib();
 1)   0.051 us    |              __compute_runnable_contrib();
 1)   0.052 us    |              __compute_runnable_contrib();
 1)   0.050 us    |              __compute_runnable_contrib();
 1)   0.049 us    |              __compute_runnable_contrib();
 1)   0.048 us    |              __compute_runnable_contrib();
 1)   0.052 us    |              __compute_runnable_contrib();
 1)   0.053 us    |              __compute_runnable_contrib();
 1)   0.051 us    |              __compute_runnable_contrib();
 1)               |              _raw_spin_unlock_irqrestore() {
 1)   0.054 us    |                preempt_count_sub();
 1)   0.564 us    |              }
 1) + 20.884 us   |            }
 1)   0.051 us    |            __rcu_read_lock();
 1)               |            load_balance() {
 1)               |              find_busiest_group() {
 1)   0.070 us    |                idle_cpu();
 1)   0.073 us    |                idle_cpu();
 1)   1.507 us    |              }
 1)   2.100 us    |            }
 1)   0.053 us    |            __msecs_to_jiffies();
 1)               |            load_balance() {
 1)               |              find_busiest_group() {
 1)   0.053 us    |                idle_cpu();
 1)   0.063 us    |                idle_cpu();
 1)   0.055 us    |                idle_cpu();
 1)   0.074 us    |                idle_cpu();
 1)   0.059 us    |                idle_cpu();
 1)   0.101 us    |                idle_cpu();
 1)   0.078 us    |                idle_cpu();
 1)   0.052 us    |                idle_cpu();
 1)   4.803 us    |              }
 1)   5.511 us    |            }
 1)   0.051 us    |            __msecs_to_jiffies();
 1)   0.049 us    |            __rcu_read_unlock();
 1)               |            _raw_spin_lock() {
 1)   0.052 us    |              preempt_count_add();
 1)   0.522 us    |            }
 1) + 33.373 us   |          }
 1)               |          pick_next_task_idle() {
 1)               |            put_prev_task_fair() {
 1)   0.065 us    |              put_prev_entity();
 1)   0.057 us    |              put_prev_entity();
 1)   1.040 us    |            }
 1)   1.530 us    |          }
 1)               |          finish_task_switch() {
 1)               |            _raw_spin_unlock_irq() {
 1)   0.078 us    |              preempt_count_sub();
 1)   0.711 us    |            }
 1)   1.350 us    |          }
 1)   0.057 us    |          preempt_count_sub();
 1) * 10054.71 us |        }
 ```
 
延时抖动的原因有很多，这些因素也并非一定独立发生，仅仅时钟中断和cpu迁移可能叠加就会造成较大的影响。
（待续待修改）
##实时优化

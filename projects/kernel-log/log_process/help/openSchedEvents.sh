#clean trace record
echo 0 > /sys/kernel/debug/tracing/trace
#resize buffer
echo 102400 > /sys/kernel/debug/tracing/buffer_size_kb
#enable sched events
echo nop > /sys/kernel/debug/tracing/current_tracer
echo 1 > /sys/kernel/debug/tracing/events/sched/enable
#enable trace
echo 1 > /sys/kernel/debug/tracing/tracing_on


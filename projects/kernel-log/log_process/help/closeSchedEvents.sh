#close trace
echo 0 > /sys/kernel/debug/tracing/tracing_on
#save record
cat /sys/kernel/debug/tracing/trace > $1.full_log
#save selected pid record
cat /sys/kernel/debug/tracing/trace | grep comm=$1 > $1.select_log
cat /sys/kernel/debug/tracing/trace | grep comm=$2 > $2.select_log
#clean trace recode
echo 0 > /sys/kernel/debug/tracing/trace


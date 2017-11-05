#说明
这是一个测试延时的小程序，大体的思想和cyclictest是一样的，让一个时钟定时，比较其唤醒运行时真实时间与实际时间的差别。目前实现的比较简单，能传入三个参数(优先级，测试次数，休眠时间us)。恩，然后好像和cyclictest的测的结果有差距。。。额。
#源码
```
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <pthread.h>


#define USEC_PER_SEC 1000000
#define NSEC_PER_SEC 1000000000
#define MAXSIZE 100000

static int min_latency=100000;
static int max_latency=-1;
static int latency[MAXSIZE]={0};


static int loop=1000;
static int interval_value=100;
static int prior=30;



static inline int64_t calcdiff(struct timespec t1,struct timespec t2){
   int64_t diff;
   diff = USEC_PER_SEC * (long long)((int) t1.tv_sec - (int) t2.tv_sec);
   diff += ((int) t1.tv_nsec - (int) t2.tv_nsec) / 1000;
   return diff;
}

static inline int64_t calcdiff_ns(struct timespec t1,struct timespec t2){
   int64_t diff;
   diff = NSEC_PER_SEC * (int64_t)((int) t1.tv_sec - (int) t2.tv_sec);
   diff += ((int) t1.tv_nsec - (int) t2.tv_nsec);
   return diff;
}


void* latency_get(void *arg)
{
    int64_t diff;
    int count = -1;
    struct timespec interval,now,next;

    // setup interval 
    interval.tv_sec = interval_value / USEC_PER_SEC;
    interval.tv_nsec =(interval_value % USEC_PER_SEC) * 1000;


    clock_gettime(CLOCK_MONOTONIC,&now);
    next = now;
    next.tv_sec += interval.tv_sec;
    next.tv_nsec += interval.tv_nsec;

    while(count<loop)
    {
        count++;
        if (nanosleep(&interval,NULL) == -1 )
        {
          exit(1);
        }

        clock_gettime(CLOCK_REALTIME,&now);
        //caculate diff
        diff = calcdiff(now,next);
        //reset
        next = now;
        next.tv_sec += interval.tv_sec;
        next.tv_nsec += interval.tv_nsec;

        if(count ==0 ) continue;  //the first time 
        if(diff > max_latency && diff <= MAXSIZE) max_latency=diff;
        if(diff < min_latency && diff <= MAXSIZE) min_latency=diff;
        if(diff >= MAXSIZE)  printf("the error %d\n",diff);
        else latency[diff]++;
    }
}


void threadCreat(int prior_v,int loop_v,int interval_v){
    pthread_t pthd;
    int ret;
    pthread_attr_t attr;
    struct sched_param param;

    prior=prior_v;
    loop=loop_v;
    interval_value=interval_v;

    pthread_attr_init(&attr);
    pthread_attr_setschedpolicy(&attr,SCHED_RR); //SCHED_RR
    param.sched_priority = prior;

    pthread_attr_setschedparam(&attr,&param);
    ret = pthread_create(&pthd, NULL, latency_get, NULL);

    if(ret !=0 ){
      printf("thread creat failed\n");
      exit(1);
    }
    pthread_join(pthd,&ret);
}

void print_LatencyInfo(){
    int i=0;
    printf("latency(us)\tnum\n");
    for(i=0;i<=max_latency;i++)
    if(latency[i]!=0) printf("%d\t\t%d\n",i,latency[i]);
}


int main(int agrc,char *argv[]){
    int i_prior=atoi(argv[1]);
    int i_loop =atoi(argv[2]);
    int i_interval=atoi(argv[3]);
    threadCreat(i_prior,i_loop,i_interval);
    print_LatencyInfo();
    return 0;
}
```
#使用与结果
```
这里的第一个参数为优先级(不要超过90) 第二个参数为测试次数 第三个参数为休眠时间
root@thu-Lenovo-IdeaPad-Y580:/home/thu/FTest/Test# ./latencyThread 50 1000 100
latency(us)    num
43        1
44        1
45        1
46        1
47        1
48        1
49        1
51        1
57        23
58        43
59        17
60        800
61        30
62        23
63        9
64        4
65        4
66        7
67        4
68        3
69        2
72        1
73        1
74        3
75        2
76        1
80        1
81        1
87        1
90        1
93        1
94        1
95        1
96        1
97        2
100       2
104       1
106       1
128       1
```
#图形化显示
将结果保存到latency.dat 中可以利用gnuplot进行画图
```
gnuplot> set ylabel 'jobs'
gnuplot> set xlabel 'latency(us)'
gnuplot> set title 'latency distribution'
gnuplot> plot 'latency.dat'
```
![latency.png](https://github.com/openthos/research-analysis/blob/master/developers/%E9%9F%A6%E5%BA%B7/realtime/latency.png "")

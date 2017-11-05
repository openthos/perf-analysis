#The Worst-Case Execution Time Problem（摘录）
##只读了survey中前面的一部分内容，觉得WCET分析是比较麻烦的（会涉及到代码静态分析，暂时会放弃WCET这部分内容）
##介绍
The determination of upper bounds on execution times, commonly called Worst-Case Execution
Times (WCETs), is a necessary step in the development and validation process for hard real-time systems. This problem is hard if the underlying processor architecture has components such as
caches, pipelines, branch prediction, and other speculative components
##存在的挑战
与最坏执行时间相关的问题  
- Data-Dependent Control Flow  
  
  The task to be analyzed attains its WCET on one (or sometimes several) of its possible    execution paths. If the input and the initial state leading to the execution of this worst-case path were known, the problem would be easy to solve
  
  A first problem that has to be solved is the construction of the control-flow
graph and call graph of the task from a source or a machine-code version of the
task
  
  A phase called Control-Flow Analysis (CFA) determines information about the
possible flow of control through the task to increase the precision of the subsequent
analyzes. Control flow analysis may attempt to exclude infeasible paths, determine  execution frequencies of paths or the relation between execution frequencies of
different paths or subpaths etc. Control-Flow Analysis has previously been called
High-level Analysis
 
- Context Dependence of Execution Times  
   
   Early approaches to the timing analysis problem assumed context independence of the timing behavior; the execution times for individual instructions were independent from the execution history and could be found in the manual of the processor
   
   A phase called Processor-Behavior Analysis gathers information on the processor
behavior for the given task, in particular the behavior of the components that influence the execution times, such as memory, caches, pipelines, and branch prediction.It determines upper bounds on the execution times of instructions or basic blocks.Processor-Behavior Analysis has previously been called Low-level Analysis
   
- Timing Anomalies  
  
##基本策略  
 - 静态分析方法(对于有硬实时要求的一般采用该种方法)  
 
 These methods do not rely on executing code on real hardware
or on a simulator. They rather take the task code itself, maybe together with
some annotations, analyze the set of possible control flow paths through the task,
combine control flow with some (abstract) model of the hardware architecture, and
obtain upper bounds for this combination. 

 - 基于测量的方法（这种方法类似与概率估计，一般用于自估）
   
 These methods execute the task or task parts on
the given hardware or a simulator for some set of inputs. They then take the
measured times and derive the maximal and minimal observed execution times, or their distribution or combine the measured times of code snippets to results for the whole task.

##最坏执行时间分析步骤
- Static Program Analysis 
 
  Static program analysis is a generic method to
  determine properties of the dynamic behavior of a given task without actually
  executing the task
  
  Therefore, sound approximations are used; they have to be
correct, but may not necessarily be complete
    
- Measurement  
   
  Measurements can be used in different ways. End-to-end
  measurements of a subset of all possible executions produce estimates, not bounds
  
  
  They may give the developer a feeling about the execution
time in common cases and the likelihood of the occurrence of the worst case. Measurement can also be applied to code snippets after which the results are combined
to estimates for the whole program in similar ways as used in static methods

- Simulation  
  
  Simulation is a standard technique to estimate the execution
time for tasks on hardware architectures

- Abstract Processor Models   

  Processor-behavior analysis needs a model of
the architecture. This need not be a concrete model implementing all of the functionality of the target hardware. A simplified model that is conservative with respect to the timing behavior is sufficient
  
- Integer Linear Programming
  
  
- Annotation

- Frontend  

- Visualization of Results

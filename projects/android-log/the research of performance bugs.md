# the research of performance bugs

### 1. performance bugs

* software bug
  * an error or mistake in a program or system that causes it to crash, behave in unintended ways, or produce incorrect results. 

* performance bug
  * a type of software bug that causes execution times to be longer than they could be, and fixing the bug 
can significantly speed up software without altering its functionality . 

### 2. characteristics of the Android platform that impact performance

* Single Threaded System

  * When an application is launched, the Linux kernel creates a new process for it, with a single thread for execution . By default, application components will run on this single thread, which is the only thread from which the UI can be manipulated,and where user interaction events can be handled.
* Display Refresh Rate and VSync

  * Each Android device has a certain device and display refresh rate, at which operations and executions are synced to ensure that graphics are rendered correctly and not displayed or updated before they have finished rendering . The standard refresh rate is about 60 frames per seconds, or 16.667 ms per frame. The display sends a signal called VSync every time it is ready to update, at which point the system will search for any changes to the UI that will need updating.
* UI Components and UI Rendering

  * On Android, the GUI consists of objects called views, which extend the View class, a class that implements logic for how the view is rendered and displayed on the screen. A view is a graphical object that controls a certain area of the screen, and can respond to user interaction. A view can either be a widget, or it can be a layout: a container for other views. Layouts, which extend both the ViewGroup class and the View class, implement logic as to how its children are displayed and ordered. Layouts can be nested in other layouts, in which case they act both as views relative to their parent layout, and as layouts relative to their child views.
  * When an activity receives focus, it is requested to draw its view hierarchy, starting　from the root node [16]. Drawing the layout has two passes: the measuring pass　and the layout pass, both of which are top-down traversals of the view hierarchy. In　the measure pass, each view calculates and stores its preferred measurements, with　respect to any constraints set by its parent. In the layout pass, each ViewGroup　positions its child views using its preferred or imposed measurements, and then all　views are drawn to the screen according to their drawing logic.　When an application needs to update its UI, it will invalidate the view that needs to　update [6]. The invalidation propagates through the view hierarchy to compute the　region of the screen that needs to be redrawn, known as the “dirty region”. How the　hierarchy is redrawn depends on whether or not drawing is hardware accelerated.　The software based drawing model invalidates the view hierarchy and then redraws　any view that intersects with the dirty region, whether or not those views have actually changed. The hardware accelerated drawing model records drawing commands　in display lists. When a view is invalidated, only the display list of that view is　invalidated. The system then draws from the display lists, and if a display list has　not been invalidated, it will simply be redrawn without any additional computation.
* Mobile CPU

  * Mobile devices have different CPUs used for different tasks: they have low-powered, efficient CPUs that are used for most tasks to save energy, and high performance CPUs that are only used for heavy graphics rendering in e.g. games, or videos. Running the high performance CPU for an extended period of time will cause battery drain, and the device will heat up.
* Device Performance

  * Applications are run as users on the Linux kernel, which share the available resources of the device, including for instance memory and CPU . This means that the performance of an application can impact the performance of the whole device. For instance, an application that uses a lot of memory can cause other applications that are running in the background to be killed in order to free up memory. This can make the entire device appear slow and non-performant to the user when switching applications, because recreating an application takes more time than just restarting or resuming it.
* Platform Fragmentation

  * Android is a very fragmented ecosystem, and there are many devices that are still being sold and used that are running older versions of Android.There have been numerous updates in the newer versions that improve performance.To ensure that an application can be performant for as many users as possible, developers need to ensure that applications can run smoothly on older devices and older versions of Android as well.

### 3. Performance Bug Patterns for Android Applications

* Blocking the UI Thread(network access,storage access,database access,bitmap processing)

  * As applications by default have a single thread that is responsible for the UI, any operation that is not responsible for UI updates or handling user input is run on the main thread can be considered a blocking operation.
  * To avoid this, all blocking operations should be performed outside of the UI thread.
* Dropped Frames and Frame Rates

  * Android applications have 16.667 ms to update the UI to meet the 60 fps refresh rate of the device. If a frame takes longer than that to render, that frame is “dropped”, meaning the system will not update the UI.
* Complex View Hierarchies

  * rendering UI components is a process involving many parts of the system, and UI computations are prone to get very heavy. A complex or poorly implemented UI is likely to lead to poor performance. Updating a deep and complicated view hierarchy will increase the computation needed for the CPU and GPU when updating and rendering display lists, since there is more measuring, layouting, and drawing needed than for a simpler, more shallow view hierarchy
* Overdraw

  * the system updates the UI by drawing each view of the view hierarchy,starting with the root view. The system will draw views on top of each other, ordering children views in front of their parents. This could potentially lead to drawing opaque views on top of other opaque views, effectively drawing the pixels multiple times. This is known as overdraw, and causes unnecessary computation and drawing operations, which can be especially bad for performance during animations
* Garbage Collection

  * The Garbage Collector removes allocated memory that is no longer being referenced, which clears up memory. GC runs are expensive, especially on older devices.The difference is due to the newer versions using an “ahead-of-time” runtime compiler called ART (Android RunTime), while the older versions uses a “just-in-time” runtime called Dalvik, and these perform GC runs differently. GC runs can be triggered by allocating a lot of temporary objects at the same time, in a loop for instance. They can also be triggered by memory leaks, which is when unused objects are still referenced somewhere in the system, meaning it will not be deallocated by the GC. Memory leaks mean that there is less memory to use, which will likely increase the rate of GC runs.
* frequent, heavyweight callbacks, especially callbacks invoked by user interaction orchanges in the activity lifecycle

  * Yepang Liu, Chang Xu, and Shing-Chi Cheung. Characterizing and detecting　performance bugs for smartphone applications. In ICSE’14, pages 1013–1024,2014.
  
### 4. Other General Performance Bug Patterns

——Guoliang Jin, Linhai Song, Xiaoming Shi, Joel Scherpelz, and Shan Lu. Understanding and detecting real-world performance bugs. 
In PLDI’12, pages 77–88,2012.
* inefficient call sequences

* functions doing unnecessary work

* synchronisation issues,which has been found to occur even if there isjust one or two threads running

### 5. references

- A Recipe for Responsiveness,Strategies for Improving Performance in Android Applications

(https://github.com/openthos/research-analysis/blob/master/projects/android-log/paper/FULLTEXT01.pdf)
  

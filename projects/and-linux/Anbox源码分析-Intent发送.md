# 1 Anbox简介

Anbox项目地址：https://github.com/anbox/anbox 。

Anbox能够在桌面Linux系统中运行Android应用程序。它利用了LXC等技术，通过构造Android系统兼容层，实现Android应用程序在桌面Linux系统中的运行。

# 2 研究目的

希望阅读Anbox项目源码，看它是怎么处理Intent，从而在我的Binder客户端程序中处理Intent，包括发送和接收Intent等。

# 3 工具介绍

在源码阅读过程中，我常用自己编写的一个名为`myfind`的脚本，来查找当前文件夹下的所有包含关键字的文件。
``` shell
deep@deep-virtual-machine:~$ cat /usr/local/bin/myfind 
 find -type f | xargs grep -n $1 2> /dev/null
```
它主要利用find获取当前目录下的所有文件，然后利用xargs将每行结果，即每个文件名作为grep的参数，让grep读取该文件查找关键字。
`2> /dev/null`错误输出重定向是为了不输出报错，因为当grep读取到文件夹的时候会报错，影响结果观看。

# 4 研究过程

过程较为繁琐，可跳过直接看结果。

在本文中`方法`和`函数`两个词语的意思相同，都是编程语言里的`method`，没有区别。

## 4.1 Anbox在哪打开/dev/binder文件的

搜索发现 src/anbox/cmds/session_manager.cpp 文件里有相关代码。
``` c++
251     container::Configuration container_configuration;
252     if (!standalone_) {
253       container_configuration.bind_mounts = {
254         {qemu_pipe_connector->socket_file(), "/dev/qemu_pipe"},
255         {bridge_connector->socket_file(), "/dev/anbox_bridge"},
256         {audio_server->socket_file(), "/dev/anbox_audio"},
257         {SystemConfiguration::instance().input_device_dir(), "/dev/input"},
258         {"/dev/binder", "/dev/binder"},
259         {"/dev/ashmem", "/dev/ashmem"},
260         {"/dev/fuse", "/dev/fuse"},
261       };
```
可以看到它把binder文件路径给配置到container_configuration里了。
``` c++
176     container_ = lxc_container_new("default", container_config_dir.c_str());
```
调用这个配置的地方是`lxc_container_new`函数。但是搜不到`lxc_container_new`这个函数，查了资料这个应该是LXC的内置函数。

并且bind_mounts 这块是设置容器里的文件挂载的，跟程序逻辑好像没什么关系。所以查这块代码没什么用。

## 4.2 Anbox在哪里用到了Intent

查找Intent
``` shell
myfind "Intent"
./src/anbox/bridge/android_api_stub.h:1526: void launch(const android::Intent &intent,
./src/anbox/bridge/android_api_stub.cpp:1506:void AndroidApiStub::launch(const android::Intent &intent,
./src/anbox/protobuf/anbox_bridge.proto:156:message Intent {
./src/anbox/dbus/skeleton/application_manager.h:1323: void launch(const android::Intent &intent,
./src/anbox/dbus/skeleton/application_manager.cpp:1565: android::Intent intent;
./src/anbox/dbus/stub/application_manager.h:1372: void launch(const android::Intent &intent,
./src/anbox/dbus/stub/application_manager.cpp:1892:void ApplicationManager::launch(const android::Intent &intent,
./src/anbox/application/manager.h:1024: virtual void launch(const android::Intent &intent,
./src/anbox/application/database.h:993: android::Intent launch_intent;
./src/anbox/cmds/launch.h:1142: android::Intent intent_;
./src/anbox/cmds/session_manager.cpp:3318: android::Intent launch_intent;
./tests/anbox/android/intent_tests.cpp:736:TEST(Intent, IsValid) {
./tests/anbox/application/restricted_manager_tests.cpp:847: MOCK_METHOD3(launch, void(const anbox::android::Intent&,
./android/camera/EmulatedFakeCamera2.cpp:85921: uint8_t controlIntent = 0;
./android/appmgr/src/org/anbox/appmgr/AppsLoader.java:1732: PackageIntentReceiver mPackageObserver;
```
打开 src/anbox/bridge/android_api_stub.cpp 文件。
``` c++
 42 void AndroidApiStub::set_rpc_channel(
 43     const std::shared_ptr<rpc::Channel> &channel) {
 44   channel_ = channel;
 45 }
 
 53 void AndroidApiStub::launch(const android::Intent &intent,
 54                             const graphics::Rect &launch_bounds,
 55                             const wm::Stack::Id &stack) {

 90   if (!intent.action.empty()) launch_intent->set_action(intent.action);

105   channel_->call_method(
106       "launch_application", &message, c->response.get(),
107       google::protobuf::NewCallback(this, &AndroidApiStub::application_launched,
108                                     c.get()));
```
Intent在`launch()`函数里有使用，最后调用了`channel_->call_method`。channel是在set_rpc_channel()里传入的。

接着搜索了`set_rpc_channel`函数定义在哪。
``` shell
myfind set_rpc_channel
./src/anbox/cmds/session_manager.cpp:233: android_api_stub->set_rpc_channel(rpc_channel);
```
打开`session_manager.cpp`文件。
``` c++
226               auto pending_calls = std::make_shared<rpc::PendingCallCache>();
227               auto rpc_channel =
228                   std::make_shared<rpc::Channel>(pending_calls, sender);
```
`std::make_shared`这个是C++智能指针的模板函数，指向的就是`rpc::Channel`。

打开`Channel`类定义文件`src/anbox/rpc/channel.cpp`。
``` c++
 30 Channel::Channel(const std::shared_ptr<PendingCallCache> &pending_calls,
 31                  const std::shared_ptr<network::MessageSender> &sender)
 32     : pending_calls_(pending_calls), sender_(sender) {}
 
 36 void Channel::call_method(std::string const &method_name,
 37                           google::protobuf::MessageLite const *parameters,
 38                           google::protobuf::MessageLite *response,
 39                           google::protobuf::Closure *complete) {
 40   auto const &invocation = invocation_for(method_name, parameters);
 41   pending_calls_->save_completion_details(invocation, response, complete);
 42   send_message(MessageType::invocation, invocation);
 43 }
```

## 4.3 Anbox中的send_message()

可以看到，我们下面要找 `send_message`函数，仍然在这个文件。
```
 73 void Channel::send_message(const std::uint8_t &type,
 74                            google::protobuf::MessageLite const &message) {

 88     sender_->send(reinterpret_cast<const char *>(send_buffer.data()),
 89                   send_buffer.size());

 94 }
```
调用了`sender_`发送，是构造时传入的，在第31、32行。
`const std::shared_ptr<network::MessageSender> &sender`。
可以看到我们要查找`MessageSender`类。
通过`myfind class\ MessageSender | less`查找，打开`src/anbox/network/message_sender.h`文件。
```
 28  public:
 29   virtual void send(char const* data, size_t length) = 0;
```
奇怪的是它没有对应的cpp文件,说明这个是虚函数，在子类里面进行实现。

所以接着查找。
``` shell
myfind public\ MessageSender | less #我的这个myfind脚本还有点问题，遇到空格不能加入进$1去
./android/service/local_socket_connection.h:28:class LocalSocketConnection : public network::MessageSender {
./src/anbox/network/socket_messenger.h:30:class SocketMessenger : public MessageSender, public MessageReceiver {
```
看了这几个文件，看了只有`LocalSocketConnection`实现了`send`函数。

打开`android/service/local_socket_connection.cpp`文件。
``` c++
 35 namespace anbox {
 36 LocalSocketConnection::LocalSocketConnection(const std::string &path) :
 37     fd_(Fd::invalid) {

 45     fd_ = Fd{socket(AF_UNIX, SOCK_STREAM, 0)};

 60 void LocalSocketConnection::send(char const* data, size_t length) {

 63     while(bytes_written < length) {
 64         ssize_t const result = ::send(fd_,
 65                                       data + bytes_written,
 66                                       length - bytes_written,
 67                                       MSG_NOSIGNAL);

 76     }
 77 }
```
这里面的`::send`应该就是系统自带的send，因为有四个参数。
这个`fd_`是一个unix socket。
也就是这里的intent发送通过`rpc_channel -> sender_ -> ::send(`。
这里面是发送方，没有与Android有任何直接接触，Android的binder是个字符设备文件，不是unix socket。
那么在接收方肯定要与Android内部的Binder机制接触了。

## 4.4 Anbox的unix socket接收方

这里做了很多无用功，没有意义，因此不再写出。

最后找到接收处理函数是通过`launch_application`关键字。
这个关键字在`src/anbox/bridge/android_api_stub.cpp`文件的106行传入`channel_->call_method`函数。

打开`android/service/message_processor.cpp`文件。
``` c++
 39 void MessageProcessor::dispatch(rpc::Invocation const& invocation) {
 40   if (invocation.method_name() == "launch_application")
 41     invoke(this, platform_api_.get(), &AndroidApiSkeleton::launch_application, invocation);
```
这里的逻辑是：当方法名等于`launch_application`然后进入`invoke`调用。

这个方法名确实在src/anbox/bridge/android_api_stub.cpp的106行发出的，应该直接找这个关键字就行了，我还找了半天。
这里的 invoke 方法只是个远程调用的包装，以protobuf形式发送数据，我们不用去看了。
这个`AndroidApiSkeleton::launch_application`应该是业务上要调用的方法。

该方法定义在`android/service/android_api_skeleton.cpp`
``` c++
 66 void AndroidApiSkeleton::launch_application(anbox::protobuf::bridge::LaunchApplication const *request,
 67                                 anbox::protobuf::rpc::Void *response,
 68                                 google::protobuf::Closure *done) {
 69     (void) response;
 70
 71     auto intent = request->intent();
 72
 73     std::vector<std::string> argv = {
 74         "/system/bin/am",
 75         "start",
 76     };
```
发现最后竟然还是用Android自带的am命令执行intent。

# 5 研究结果

## 5.1 Anbox里的Intent发送的函数调用过程

Anbox里的Intent发送的函数调用过程如图所示：

![Anbox中Intent发送过程](https://github.com/HsingPeng/research-analysis/raw/patch-1/projects/and-linux/image/Anbox%E4%B8%ADIntent%E5%8F%91%E9%80%81%E8%BF%87%E7%A8%8B.png)

## 5.2 Anbox如何发送Intent

通过阅读Anbox源码了解到，它里面虽然描述了一个intent结构，但是这不是Android里的Intent，它最终是通过Android自带的am命令发送intent。没有看到我想要看的东西。


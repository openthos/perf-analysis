Intel SGX SDK for linux

/opt/intel/sgxpsw/aesm/aesm_service

There is no need to load the launch enclave directly.  The SGX Platform Software (PSW) handles that for you when the "Intel SGX AESM" service loads during Windows boot.  If you are having trouble loading your built enclave with sgx_create_enclave(), check that you have installed the PSW  and the "Intel SGX AESM" service is running.  


包括PSW(platform software)
每一个Intel 的SDK 所支持的Enclave程序都包括：
Enclave definition Language(EDL) file 描述enclave 信任和不信任的函数和类型。
Enclave configuration file: 包括enclve的元数据。
Signing key file 用来sign 一个enclave来产生signature 结构体。
应用程序和enclave的源代码。
makefile 生成edger routines，构建application 和enclave，sign enclave。
linker 脚本，将不必要的符号隐藏起来。

enclave 将需要的linux中所有的共享库静态链接在一起。

SDK 提供以下几个工具：
Edger8r Tool
生成untrusted components 和enclave之间的接口
Enclave Signing Tool
生成enclave 的metadata，包括enclave signature ，将这些元数据添加到enclave image中。

Edger8r Tool:
Edger8r 通过读取EDL file，生成untruested 和enclave的交互接口。Edger8r 一般生成4个文件：
demo_t.h  prototype declarations for trusted proxies and bridges.
demo_t.c
demo_u.h  prototype declarations for untrusted proxies and bridges.
demo_u.c

Enclave Signing Tool
Enclave 的signing时生成signature stucture 的一部分。一旦一个enclave file被sign后，他的Code, data, signature 等再被修改就都能被检测到。

Enclave Debugger

Enclave Memory Measurement Tool
sgx_emmt
这个工具在运行时检测Enclave 的受保护内存的使用。

CPUSVN Configuration Tool
这个时给模拟器使用的工具，以模拟CPU 的升级降级。


一般来说，开发一个enclave包括以下几个步骤：
1. 在EDL 文件中定义untrusted 和 enclave 之间的交互接口。
2. 实现应用程序和enclave的函数
3. 构建应用程序和encalve。
4. 运行和调试应用程序
5. 发布。

如何编写一个enclave 函数：
从应用程序的角度来看，ECALL 像是任何一个函数调用。Encalve 函数是有着一些限制的明文的C/C++ 函数。
Enclave function 可以依赖于特定的C/C++ runtime 库， STL，synchronization 和一些其他的SDK中的可信赖的库。这些可信库是专门为enclave 内运行所设计的。
注意以下三点：
1. Enclave function不能使用所有的32-bits或64-bits指令。
2. 只能运行在ring3，其他模式将会导致错误
3. Function calls在enclave中是可能的，如果这个被调用的函数是静态链接到enclave中的。Linux 的shared library不被支持。（Sign 阶段就会发生错误）
如果要调用外部函数，要使用OCALL 。

Calling Functions inside an Enclave
ECALL

Calling Functions outside the Enclave
有时候Enclave 需要调用一些在外部的函数来获得操作系统的支持，如system call，I/O 等。这些函数被成为OCALL。Encalve image 的加载过程就和Shared library的过程是类似的， Aplications的函数地址空间和Enclave是共享的，所以Encalve可以间接调用创建这个enclave 的application内的函数。然而，直接调用是不可以的，会导致一个运行时异常。
这个wrapper function 将参数从受保护的区域复制到不受保存的区域。OCall将参数拷贝到untrusted stack上，如果参数太多，可能会造成stack overrun。
当一个指针在EDL 文件中指明了特殊的attributes时，他指向的内存区域才会被拷贝。

样例：
1. 在EDL 文件中添加一个foo 函数：
```
// foo.edl
enclave {
  untrusted {
    [cdecl] void foo(int param);
  };
};
```
2. 在Enclave 中写一个可信的，用户友好的wrapper。
```c
// enclave's trusted code
#include "foo_t.h"
void ocall_foo(int param)
{
  // it is necessary to check the return value of foo()
  if (foo(param) != SGX_SUCCESS)
  abort();
}
```
3. 在不可信区写一个foo
```c
// untrusted code
void foo(int param)
{
  // the implementation of foo
}
```

之后，sgx_edger8r 会生成一个不可信的bridge 函数，自动调用不可信的foo。这两者都是Application而非Encalve。
Library deployment for enclave
1. Trusted library也是Intel SGX 解决方案的一部分。通常经历了更加严格的评估和review
2. trusted library 是为了特定目的开发的，因此不应该包括sgx 不支持的指令
3. Trusted library 的api也许也是enclave interface的一部分，因此也需要edl file。
4. Trusted library 也可能需要调用外部函数。

Avoiding Name Collisions
一个应用程序可能有好几个enclaves，每个enclave是一个独立的计算单元，以so文件的形式展示。因此，Encalve也需要提供了一个独一无二的interface 来避免名字冲突。sgx_edger8r 能够避免OCALL 函数的名字冲突，因为他预先考虑了enclave 名字和不可信的bridge funcation 的名字。但是，ISV 必须保证ECALL 函数没有名字冲突。
同时，两个Encalve 可能会导入同一个trusted library。为了避免这一点，ISV需要：
1. 在sgx_edger8r 时，提供--use-prefix选项
2. 给所有的Ecall 在他们的不可信代码部分加上encalve 名字。

将Encalve 和库链接：
动态库：
enclave shared object 不能依赖于任何动态链接库，如果库文件中有任何的unresolved 依赖，sign 过程会失败。
静态库：
只要静态库没有什么依赖，就可以链接。

为了方便阅读源代码，将Intel SDK 所提供的库放在下方：
Trusted library
libsgx_trts.a             Intel(R) SGX internals
libsgx_trts_sim.a
libsgx_stdc.a             Standard C library (math, string, and so on.)
libsgx_tsetjmp.a          Provides setjmp and longjmp functions to be used to perform non-local jumps.
libsgx_tstdcxx.a        Standard C++ libraries, STL
libsgx_tservice.a       Data seal/unseal (encryption), trusted Architectural Enclaves support, Elliptic Curve Diffie Hellman (EC DH) library, and so on
libsgx_tservice_sim.a
libsgx_tcrypro.a Cryptographic library
libsgx_tkey_exchange.a Trusted key exchange library

Untrusted library
libsgx_urts.so  Provides functionality for applications to manage enclaves
libsgx_urts_sim.so
libsgx_uae_service.so   Provides both enclaves and untrusted applications access to services provided by the AEs
libsgx_uae_service_sim.so
libsgx_ukey_exchange.a  Untrusted key exchange library


Enclave Configuration file
这个文件用来提供给sign过程中，创建enclave 的signature 和metadata。

Loading and unloading enclave
Enclave 源代码最后被编译成一个shared object。为了使用这个enclave，这个so文件将会被加载到保护内存区域，通过create_enclave。第一次加载enclave时，loader 会从LE 中拿到一个launch token，user 可以将launch token保存在一个文件中，下次加载时就可以直接使用。sgx_destroy_enclave 可以unload 一个enclave。

Handling Power Events
Application 需要能够处理任何的电源的变化，如sleep。

Enclave Definition Language Syntax：
Edl 文件的模板：
```c
enclave {
  //Include files
  //Import other edl files
  //Data structure declarations to be used as parameters of the
  //function prototypes in edl
  trusted {
    //Include header files if any
    //Will be includedd in enclave_t.h
    //Trusted function prototypes
  };
  untrusted {
    //Include header files if any
    //Will be included in enclave_u.hhead
    //Untrusted function prototypes
  };
};

```

```c
enclave {
  // An EDL file can optionally import functions from
  // other EDL files
  from “other/file.edl” import foo, bar; // selective importing
  from “another/file.edl” import *;
  // import all functions
  // Include C headers, these headers will be included in the
  // generated files for both trusted and untrusted routines
  include "string.h"
  include "mytypes.h"
  // Type definitions (struct, union, enum), optional
  struct mysecret {
    int key;
    const char* text;
  };
  enum boolean { FALSE = 0, TRUE = 1 };
  // Export functions (ECALLs), optional for library EDLs
  trusted {
    //Include header files if any
    //Will be included in enclave_t.h
    //Trusted function prototypes
    public void set_secret([in] struct mysecret* psecret);
    void some_private_func(enum boolean b); // private ECALL
    (non-root ECALL).
  };
  // Import functions (OCALLs), optional
  untrusted {
    //Include header files if any
    //Will be included in enclave_u.h
    //Will be inserted in untrusted header file
    “untrusted.h”
    //Untrusted function prototypes
    // This OCALL is not allowed to make another ECALL.
    void ocall_print();
    // This OCALL can make an ECALL to function
    // “some_private_func”.
    int another_ocall([in] struct mysecret* psecret)
    allow(some_private_func);
  };
};
```


## SampleEnclave
这个Sample code 的主要目的是：
1. 如何初始化和摧毁一个enclave
2. 创建ECALL 和OCALL
这一点，可以看看生成的函数是如何操作的。
3. 在enclave 中调用trusted libraries。


```
/* Initialize the enclave:
 *   Step 1: try to retrieve the launch token saved by last transaction
 *   Step 2: call sgx_create_enclave to initialize an enclave instance
 *   Step 3: save the launch token if it is updated
*/
```

sgx_create_enclave
```c
extern "C" sgx_status_t sgx_create_enclave(const char *file_name, const int debug,
    sgx_launch_token_t *launch_token, int *launch_token_updated,
    sgx_enclave_id_t *enclave_id, sgx_misc_attribute_t *misc_attr)
```

enclave is the file of enclave, token 是从文件中读取的上一次保存的token(如果有)。
将enclave 打开后调用_create_enclave
```c
ret = _create_enclave(!!debug, fd, file, NULL, launch_token, launch_token_updated, enclave_id, misc_attr);
```
在这时候，会将之前从文件中读取的token用来验证是否可用。
最终会调用到__create_enclave

## Attestation
### Local Attestation
创建DH key 交换的过程：
这个过程和普通的DKE 交换相比，多了互相report 和 verifer 的过程。
create_session函数
1. Enclave 1 调用sgx_dh_init_session，作为一个session的发起者
2. Ocall 向 untrusted 请求帮助，发送请求给enclave 2
3. untrusted 调用ECALL 到Enclave2
4. Enclave 2 调用 sgx_dh_init_session 来初始化自己作为session 的responer（session_request）
5. Enclave 2 生成DH message 1 （ga || TARGETINFO）
6. DH message 1 发给Enclave 1 ，通过Ocall 和Ecall
7. Enclave 处理Messgae 1，生成DH message 2 gb||[Report Enclave 1(h(ga || gb))]SMK.
8. DH message 2 发送给 Enclave 2， 通过Ocall 和Ecall
9. Enclave 2 处理Message 2 并生成Message 3，并将Message 通过Untrusted code 发送给Enclave 1.
10. Enclave 2 处理Message 3[ReportEnclave2(h(gb || ga)) || Optional Payload]SMK. ，建立session
11. 接下来的消息就在AEK 的保护下进行

### 如何进行私密的通信
test_message_exchange
marshal_message_exchange_request 函数将secret_data拷贝到 Marshalled_inp_buff 函数中。
send_request_receive_response函数将 Marshalled_inp_buff 用之前session 得到的AEK加密。并向Enclave 2 发送请求。

### 如何执行Enclave 到Enclave 的函数调用
test_enclave_to_enclave_call

### Remote Attestation
Intel SGX 中 Remote Attestation 包括App 的enclave 和 Intel 提供的 QE 和Provisioning Enclave，以及带SGX 功能的CPU。
Intel Sample Code 中的Remote Attestation 包含了一个application enclave 如何给一个远端程序验证，以及他们之间如何建立加密链接。

## How to seal Data
function provided by SDK
```c
/*sealing the plaintext to ciphertext. The ciphertext can be delivered
        outside of enclave.*/
ret = sgx_seal_data(0, NULL,sizeof(data2seal),(uint8_t*)&data2seal,
        sealed_log_size, (sgx_sealed_data_t*)sealed_log);

extern "C" sgx_status_t sgx_seal_data(const uint32_t additional_MACtext_length,
                                      const uint8_t *p_additional_MACtext, const uint32_t text2encrypt_length,
                                      const uint8_t *p_text2encrypt, const uint32_t sealed_data_size,
                                      sgx_sealed_data_t *p_sealed_data)
```
Get seal key
1. ereport and other operation to generate key_request struct
2. Use this key_request to generate key by egetkey
sgx_rijndael128GCM_encrypt
AES-GCM 算法


### Replay protect  policy

# SGX SDK platform analysis
Intel SGX 的SDK是开放源代码的，尽管如此，SGX中对于软件的运行依然有很多的限制。

Intel SGX Platform 的主要逻辑封装在AESMLogic类中，其中该逻辑的的启动函数如下：

ae_error_t AESMLogic::service_start()
其主要启动逻辑如下：
1. 注册Intel EPID
2. 启动实例化的CLEClass类，调用其函数load_enclave().这个LE就是Launch Enclave
3. 开启另外两个线程 thread_to_load_qe 和thread_to_init_pse, 分别对应QuotingEnclave 和Provisioning Enclave
4. 启动white_list thread.

需要区分的是，只有几个platform enclave运行在SGX的Enclave中，其他的代码都运行在普通模式下。

接下来介绍的LE的启动流程
1. CLEClass依然是在普通模式下运行的。其首先从预先编写好的静态结构体中找到LE的production sig structure 和 二进制文件，之后调用sgx_create_le 函数，讲LE加载进SGX中。此处的LE使用的是Intel 预先签名好的LE。
2. sgx_create_le 调用_create_enclave，创建enclave。
3. 在load成功后，读取whitelist，该whitelist存放在磁盘上，加密。之后启动的whitelist会尝试通过互联网更新whitelist。

对于对应的数据的文件名可以部分参考如下：
persistent_storage_table.cpp
``` c
static const persistent_storage_info_t psinfos[]={
    {FT_ENCLAVE_NAME, AESM_LOCATION_EXE_FOLDER, AESM_FILE_ACCESS_PATH_ONLY, "le"},//LE_ENCLAVE_FID
    {FT_ENCLAVE_NAME, AESM_LOCATION_EXE_FOLDER, AESM_FILE_ACCESS_PATH_ONLY, "qe"},//QE_ENCLAVE_FID

#ifdef DBG_LOG
    {FT_PERSISTENT_STORAGE, AESM_LOCATION_DATA, AESM_FILE_ACCESS_ALL, "internal_log.txt"}, //AESM_DBG_LOG_FID
    {FT_PERSISTENT_STORAGE, AESM_LOCATION_DATA, AESM_FILE_ACCESS_ALL, "internal_log_cfg.xml"}, //AESM_DBG_LOG_CFG_FID
#endif
#ifdef _PROFILE_
    {FT_PERSISTENT_STORAGE, AESM_LOCATION_DATA, AESM_FILE_ACCESS_ALL, "perf_time.csv"}, //AESM_PERF_DATA_FID
#endif
    {FT_PERSISTENT_STORAGE, AESM_LOCATION_DATA, AESM_FILE_ACCESS_ALL, "white_list_cert.bin"},//AESM_WHITE_LIST_CERT_FID
    {FT_PERSISTENT_STORAGE, AESM_LOCATION_DATA, AESM_FILE_ACCESS_ALL, "white_list_cert_to_be_verify.bin"},//AESM_WHITE_LIST_CERT_TO_BE_VERIFY_FID

```
（LE在debug模式下无法再加载其他的enclave）
production signed 的 enclave 不能在debug 模式下运行

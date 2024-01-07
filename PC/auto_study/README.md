# PC端（由autoGUI开发）
可实现截图后发送到指定微信群
## 安装PaddleOCR

pip install paddlepaddle
pip install paddleocr

安装后出现报错

OMP: Error #15: Initializing libiomp5md.dll, but found libiomp5md.dll already initialized.
OMP: Hint This means that multiple copies of the OpenMP runtime have been linked into the program. That is dangerous, since it can degrade performance or cause incorrect results. The best thing to do is to ensure that only a single OpenMP runtime is linked into the process, e.g. by avoiding static linking of the OpenMP runtime in any library. As an unsafe, unsupported, undocumented workaround you can set the environment variable KMP_DUPLICATE_LIB_OK=TRUE to allow the program to continue to execute, but that may cause crashes or silently produce incorrect results. For more information, please see http://www.intel.com/software/products/support/.

删除E:\Anaconda\ProgramFiles\Library\bin\libiomp5md.dll

备份到E:\Anaconda\back_up\libiomp5md.dll



## 安装tesseract-ocr

（英语识别率高，中文识别率不高）

识别率太低，后处理操作很复杂，不好，虽然快

[Tesseract-OCR 下载安装和使用_tesseract-ocr下载_半濠春水的博客-CSDN博客](https://blog.csdn.net/weixin_51571728/article/details/120384909?ops_request_misc=%7B%22request%5Fid%22%3A%22169521206216800222870375%22%2C%22scm%22%3A%2220140713.130102334..%22%7D&request_id=169521206216800222870375&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_positive~default-1-120384909-null-null.142^v94^chatsearchT3_1&utm_term=Tesseract&spm=1018.2226.3001.4187)
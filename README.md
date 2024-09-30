# FuzzingJSPath
不建议用自动挡，访问暴露路径的多线程问题未解决。
有子路径的，一定要加最后的/

Recursively search for the paths of JS leaks. It is not recommended to use automatic mode, as the multithreading issues when accessing exposed paths have not been resolved. For sub-paths, be sure to add a trailing '/' symbol.

usage：
python3 FuzzingJS-manual.py|FuzzingJS-auto.py -u http://x.x.x.x

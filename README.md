# TensorFlow 第三方依赖库版本分析脚本

一个简单的Python脚本，用于获取TensorFlow在构建或运行过程中，所依赖的第三方库的版本信息，如：cuda、cudnn、bazel等。

```
$ python .\tf_dep.py --help
usage: tf_dep.py [-h] repo

positional arguments:
  repo        tensorflow repo path, current only supported github and local filesystem

optional arguments:
  -h, --help  show this help message and exit
```

## TODO

- [ ] 从Github上拉取TensorFlow版本信息
- [ ] 获取TensorFlow构建阶段需要的GCC的版本信息

## 快速开始

### 获取Github上特定版本的TensorFlow的第三方库依赖信息
```
$ python ./tf_dep.py github:tensorflow/tensorflow/v2.0.0

               bazel: 0.26.1
           bazel_max: 0.26.1
           bazel_min: 0.24.1
                cuda: 10
        cuda_compute: 3.5,7.0
               cudnn: 7
           tensor_rt: 5
```

`github:tensorflow/tensorflow/v2.0.0` 是由三部分构成：
- `github:` 表示从Github上拉取第三方库版本信息
- `tensorflow/tensorflow` Github上的TensorFlow仓库的位置，可以是官方的`tensorflow/tensorflow`，也可以是其他`fork`版本`xxx/tensorflow`
- `v2.0.0` TensorFlow版本号，即Github上的tag

国内使用该脚本访问Github，或许需要添加代理设置

Windows PowerShell
```powershell
$env:HTTP_PROXY='http://127.0.0.1:10809'
$env:HTTPS_PROXY='http://127.0.0.1:10809'
```

Windows CMD
```cmd
set HTTP_PROXY=http://127.0.0.1:10809
set HTTPS_PROXY=http://127.0.0.1:10809
```

Linux Shell
```sh
export HTTP_PROXY='http://127.0.0.1:10809'
export HTTPS_PROXY='http://127.0.0.1:10809'
```

### 获取本地TensorFlow仓库的依赖信息

```
$ python ./tf_dep.py ~/projects/tensorflow
```

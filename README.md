# 使用

请在 `cookies.txt` 中用以下格式存放 cookie

``` plain
UM_distinctid __client_id _uid
UM_distinctid __client_id _uid
·
·
·
```

在代码中可以指定图片的左上角坐标，修改 `base_x` 与 `base_y` 即可

## 关于图片

请首先使用 `parse.py` 将图片转换为 `.out`

然后修改 `paint.py` 中的文件名就好了

请使用 `python3`，并确保安装以下的库

``` plain
requests
colorama
matplotlib
```

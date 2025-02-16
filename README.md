# PythonScript

自用的 python 脚本，链接到环境变量作为终端命令使用

## 用例

替换 `...` 为本地路径并将下面环境变量放入终端环境变量（例如：.zshenv）中

```shell
SCRIPT_PYTHON=".../.venv/bin/python3"
PY_SCRIPT_PATH=".../script"

alias manga-chap-add='$SCRIPT_PYTHON $PY_SCRIPT_PATH/manga_chap_add.py'
alias fix-cbz-image='$SCRIPT_PYTHON $PY_SCRIPT_PATH/fix_cbz_image.py'
alias check-ppcat='$SCRIPT_PYTHON $PY_SCRIPT_PATH/check_ppcat.py'
alias ass-subset='$SCRIPT_PYTHON $PY_SCRIPT_PATH/mkv_ass_subset.py'
```

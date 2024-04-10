# 安装出现版本冲突
```
pip install scikit-image opencv-python open3d imageio
```
Installing collected packages: pure-eval, ptyprocess, pickleshare, fastjsonschema, dash-table, dash-html-components, dash-core-components, backcall, widgetsnbextension, traitlets, six, rpds-py, pyyaml, pyparsing, pygments, prompt-toolkit, pkgutil-resolve-name, pexpect, parso, networkx, nest-asyncio, kiwisolver, jupyterlab-widgets, itsdangerous, executing, cycler, configargparse, blinker, attrs, retrying, referencing, matplotlib-inline, jupyter-core, jedi, Flask, comm, asttokens, stack-data, matplotlib, jsonschema-specifications, dash, jsonschema, ipython, nbformat, ipywidgets, open3d
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
lyft-dataset-sdk 0.0.8 requires Shapely>=1.6.4.post2, which is not installed.
nuscenes-devkit 1.1.11 requires Shapely<2.0.0, which is not installed.
pycocotools 2.0.1 requires cython>=0.27.3, which is not installed.
ultralytics 8.0.96 requires psutil, which is not installed.
nuscenes-devkit 1.1.11 requires matplotlib<3.6.0, but you have matplotlib 3.7.5 which is incompatible.
Successfully installed Flask-3.0.3 asttokens-2.4.1 attrs-23.2.0 backcall-0.2.0 blinker-1.7.0 comm-0.2.2 configargparse-1.7 cycler-0.12.1 dash-2.16.1 dash-core-components-2.0.0 dash-html-components-2.0.0 dash-table-5.0.0 executing-2.0.1 fastjsonschema-2.19.1 ipython-8.12.3 ipywidgets-8.1.2 itsdangerous-2.1.2 jedi-0.19.1 jsonschema-4.21.1 jsonschema-specifications-2023.12.1 jupyter-core-5.7.2 jupyterlab-widgets-3.0.10 kiwisolver-1.4.5 matplotlib-3.7.5 matplotlib-inline-0.1.6 nbformat-5.10.4 nest-asyncio-1.6.0 networkx-3.1 open3d-0.18.0 parso-0.8.4 pexpect-4.9.0 pickleshare-0.7.5 pkgutil-resolve-name-1.3.10 prompt-toolkit-3.0.43 ptyprocess-0.7.0 pure-eval-0.2.2 pygments-2.17.2 pyparsing-3.1.2 pyyaml-6.0.1 referencing-0.34.0 retrying-1.3.4 rpds-py-0.18.0 six-1.16.0 stack-data-0.6.3 traitlets-5.14.2 widgetsnbextension-4.0.10

# 下载数据
- train 

python download_data.py --out_dir={pwd} --id scene0191_00
python download_data.py --out_dir={pwd} --id scene0191_01
python download_data.py --out_dir={pwd} --id scene0191_02

- test

python download_data.py --out_dir={pwd} --id scene0707_00
python download_data.py --out_dir={pwd} --id scene0708_00
python download_data.py --out_dir={pwd} --id scene0709_00

- val

python download_data.py --out_dir={pwd} --id scene0568_00
python download_data.py --out_dir={pwd} --id scene0568_01
python download_data.py --out_dir={pwd} --id scene0568_02


python download_data.py --out_dir={pwd} --id scene0568_01
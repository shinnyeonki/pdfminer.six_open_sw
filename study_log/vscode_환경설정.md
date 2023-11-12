# vs code 환경설정을 일정하게 만들어 보자

아래의 코드를 실행하면 현제 PYTHONPATH를 확인할 수 있다.
* PYTHONPATH는 파이썬이 모듈을 찾는 경로를 저장한 리스트이다.
```python
import sys
print(sys.path)
```

## 하려고 하는 것
* test 코드를 만들어 기능 개발을 하는데 사용하고 싶다. 하지만 아래의 프로젝트 루트 폴더에 새로운 파일을 만드면 import 가 되지만 새로 만든 폴더에 코드를 만들면 import 가 되지 않는다.
```shell
.
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── MANIFEST.in
├── Makefile
├── README.md
├── README.md.original
├── cmaprsrc
├── docs
├── mypy.ini
├── noxfile.py
├── open_sw
├── pdfminer
├── samples
├── setup.py
├── study_log
├── tests
└── tools

9 directories, 10 files
```

그래서 다음과 같은 방법으로 개발환경을 구성한다  
* PYTHONPATH에 프로젝트 루트를 추가한다. -> .vscode/setting.json 을 만들어 프로젝트 루트 폴더를 pythonPath를 추가한다.
* open_sw 폴더(모든 test 코드를 활용할 폴더)를 만든다
* .gitignore에 .vscode와 open_sw를 추가하여 git에 올라가지 않도록 한다 (.gitignore 과 open_sw는 추가해 두었으니 .gitignore 은 수정하지 않아도 된다.)
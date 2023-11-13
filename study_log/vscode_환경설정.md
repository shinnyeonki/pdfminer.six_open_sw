# vs code 환경설정을 일정하게 만들어 보자

## 하려고 하는 것
test 코드를 만들어 기능 개발을 하는데 사용하고 싶다.  
하지만 아래의 프로젝트 루트 폴더에 새로운 파일을 만드면 import 가 되지만 새로 만든 폴더에 코드를 만들면 import 가 되지 않는다.
이후 기능 추가를 위해 외부 모듈을 사용할텐데 이때 외부의 pip 와 겹치는 모듈이 있으면 충돌이 일어난다.(venv)

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
* venv 구성을 하여 충돌을 방지한다


## 실제 실행
.vscode 폴더를 만들고 내부에 settings.json 파일을 만든다.

```json
{
    "terminal.intergrated.env.windows": {
        "PYTHONPATH": "${workspaceFolder}"
    },
    "terminal.integrated.env.osx": {
        "PYTHONPATH": "${workspaceFolder}"
    },
    "terminal.integrated.env.linux": {
        "PYTHONPATH": "${workspaceFolder}"
    }
}
```
위와 같이 json 파일을 만들면 된다

이후 open_sw 폴더를 만든후 여기서 test 코드를 작성하면 된다

---
venv 구성은 다음과 같이 한다

초기 가상환경 생성(처음만 하면 된다)
```shell
python -m venv .venv
```

venv 활성화(가상환경을 사용할때마다 실행해야 한다)
```shell
source .venv/scripts/activate
```

venv 비활성화(가상환경에서 벗어날때 실행한다)
```shell
deactivate
```







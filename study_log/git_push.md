# git push 할 때 비밀번호 입력 귀찮음

*통신방식을 https에서 ssh로 변경하면 비밀번호 입력 없이 push 가능
하지만 ssh 프로토콜의 경우 ssh key를 등록해야 한다

* ~/.ssh 폴더에 id_rsa, id_rsa.pub 파일이 있는지 확인
* cat ~/.ssh/id_rsa.pub 명령어로 ssh key를 확인할 수 있다
* git hub에 ssh key를 등록해야 한다
* github.com -> settings -> SSH and GPG keys -> New SSH key
* title은 임의로 입력하고 key에 id_rsa.pub 파일의 내용을 복사 붙여넣기 한다
* 이제 git push 할 때 비밀번호 입력 없이 push 가능하다

---
## 상세설명
git bash && terminal 에서 아래 명령어를 입력하면 ssh key를 생성할 수 있다
```shell
ssh-keygen
```
![img](https://lh5.googleusercontent.com/JsYp-j1MK6oGs7dTDy2rbtfHGOPnD1aKXOKEWefCtmhnXu1w7fpAiJlNVTXavnuF9YUgxtEJL5AyBpJ9YHLUXCuguW6eYB6XWHUxKEwMRiN-zxBg48OvD33d-LIyuFEtunepcuQ)


```shell
cat ~/.ssh/id_rsa.pub
```
내용을 복사하여 github.com -> settings -> SSH and GPG keys -> New SSH key 에 붙여넣기 한다
title은 임의로 입력하면 된다


다음과 같이 등록이 되었다면 ssh key 등록이 완료된 것이다
![img](https://lh6.googleusercontent.com/PDrUIi-9uI8ia_CyqJx0wgJSPezDNcQuRyZ48uDu3Tq9x_BzIxCAYv4xEAIpxoy_VSP2gjKklrjPmTvZEvCaaNCNRljdLnrSnEVAvbs5jrICTJUjE_V1klV_jsBQo8RBw9Ffpng)



이제부터 프로젝트를 clone 할 떄 https가 아닌 ssh로 clone 하면 push 할 때 비밀번호 입력 없이 push 할 수 있다
![img](https://lh6.googleusercontent.com/-hgBUR4PTjaknkdCBBIbJwOOb5cOZJIFWY1YweYnM8aXUNcXnU2TEQ4ZYnYVCd-aS3GWljYME4Y9AN2vDnodaT8FERw7xMPaHzpKjJ9Jz5-7wFA4Ga1kpv6-epNayYulR_tCDuc)






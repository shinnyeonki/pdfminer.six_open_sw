pdf 문서의 텍스트 블록을 나타내며, 각 텍스트 블록은 하나 이상의 텍스트 라인(LTTextLine 객체)으로 구성된다는 것을 나타낸다.
텍스트 블록의 위치, 크기, 텍스트 내용 등의 정보를 저장하고 처리하는데 사용된다.


<__init__메소드>
 클래스의 객체가 생성될 때 호출되는 초기화 메소드. 상위 클래스인 LTTextContainer의 초기화메소드를 호출하고, index 속성을 -1로 설정

<__repr__메소드>
클래스의 객체를 문자열로 표현할 때 호출된다. 여기에서는 클래스 이름, 인덱스, 경계상자의 문자열 표현, 그리고 텍스트 내용을 포함한 문자열을 반환합니다.

<get_writing_mode메소드>
텍스트 블록의 쓰기 모드(예: 좌우 방향, 상하 방향 등)를 반환해야 하는데, 구현이 되지 않음 따라서 메소드 호출 시 NotImplementedError 발생


```
class LTTextBox(LTTextContainer[LTTextLine]):

    def __init__(self) -> None:

        LTTextContainer.__init__(self)

        self.index: int = -1

        return

  

    def __repr__(self) -> str:

        return "<%s(%s) %s %r>" % (

            self.__class__.__name__,

            self.index,

            bbox2str(self.bbox),

            self.get_text(),
    def get_writing_mode(self) -> str:

        raise NotImplementedError

        )
```
# SYUNotice
자동으로 삼육대 학사 및 단과별 홈페이지 공지를 크롤링하고 디스코드 웹훅으로 보냅니다.  
나중에 다른 방식으로 확장할 수 있도록 Sanic 프레임워크 기반으로 제작했습니다.

## 예시
![image](https://user-images.githubusercontent.com/61371424/221483113-a1a4492e-307b-461f-a81a-3acbe1f429b0.png)

## 셀프 호스팅 및 테스트 방법
1. 파이썬을 준비해주시고, `requirements.txt`를 통해 의존성을 설치합니다.
2. `config.example.py`를 `config.py`로 복사 또는 rename하고, 안의 내용을 채워줍니다.
3. `main.py`를 구동합니다.
4. 자신의 디스코드 서버의 채널 웹훅을 자동으로 생성된 `database.db`의 `discord_sub` 테이블에 넣어줍니다.
   - webhook: 웹훅 URL
   - sub: 구독할 목록; 컴마 등으로 구독할 공지를 작성해주세요. ID는 [파서 지원 목록](#파서-지원-목록)을 참고해주세요.
5. 이제 기다려줍니다.

## 파서 지원 목록
- [학사공지 (academic)](https://www.syu.ac.kr/academic/academic-notice/)
- [인공지능융합학부 (aice)](https://www.syu.ac.kr/aice/community/notice/)
- [건축학과 (arch)](https://www.syu.ac.kr/arch/community/notice/)
- [생활공지 (campus)](https://www.syu.ac.kr/university-square/notice/campus-notice/)
- [컴퓨터공학부 (cse)](https://www.syu.ac.kr/cse/community/notice/)
- [경영학과 (doba)](https://www.syu.ac.kr/doba/community/notice/)
- [행사공지 (event)](https://www.syu.ac.kr/university-square/notice/event/)
- [SW중심대학사업단 (swuniv)](https://www.syu.ac.kr/swuniv/community/notice/)
- [스미스학부대학 (teacher)](https://www.syu.ac.kr/teacher/community/notice/)

## 파서 추가 방법
1. `parsers` 디렉토리에 파이썬 파일을 하나 생성해주세요.
2. 다음 예시와 같이 내용을 추가해주세요.
   ```python
   from .base import BaseParser
   
   
   class ExampleParser(BaseParser):
       URL = "공지가 올라오는 페이지 URL"
       NAME = "공지가 올라오는 과의 이름"
   ```
   - 파싱에 문제가 있는 경우 기본 파서로는 크롤링이 불가능한 경우입니다. 이 경우 `parse` 메서드를 오버라이딩해 파서를 작성해주세요.
3. `__init__.py`의 `available_parsers` dict에 `"파서 ID": 파서 클래스` 형식으로 추가해주세요.

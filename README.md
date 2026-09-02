# DNS 이름 풀이 추적기

도메인이 IP 주소로 바뀌는 과정을 직접 확인하기 위해 만든 Python CLI 미니 프로젝트입니다. 루트 DNS 서버에 질의를 시작해, 응답에 포함된 다음 DNS 서버 정보로 다시 질의하며 최종 IPv4 주소를 찾습니다.

## 프로젝트 목표

평소에는 운영체제가 DNS 조회를 처리하지만, 그 내부에서 여러 DNS 서버를 거쳐 IP 주소를 찾는 과정을 직접 확인해 보고자 했습니다. 또한 직접 DNS 서버에 질의한 결과와 Windows 일반 조회 결과를 비교했습니다.

## 핵심 동작

- 루트 DNS 서버에 A 레코드 질의를 전송합니다.
- UDP 응답이 잘리면 `TC` 플래그를 확인해 TCP로 다시 질의합니다.
- 응답의 IPv4 정보를 이용해 다음 DNS 서버에 반복 질의합니다.
- 최종 IPv4 주소와 질의 경로를 출력합니다.
- Windows 일반 조회 결과를 함께 출력해 차이를 확인합니다.

## 조회 흐름

```text
루트 DNS 서버 → 다음 DNS 서버 → … → 도메인 IPv4 주소
```

## 실행 예시

```text
조회 도메인: www.example.com.

현재 서버: 198.41.0.4
다음 서버: 192.41.162.30

...

직접 조회한 도메인 IP: [...]
윈도우에서 조회한 도메인 IP: [...]
```

## 실행 방법

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## 사용 기술

- Python
- dnspython
- Windows DNS 캐시 및 `hosts` 파일 실습

## 범위

현재는 `www.example.com.`의 A 레코드와 IPv4 주소를 기준으로 동작합니다. AAAA·CNAME 레코드, 복잡한 오류 처리, DNS 캐시·재귀 DNS 리졸버 구현은 범위에서 제외했습니다. `hosts` 파일도 프로그램이 직접 수정하지 않습니다.

## 더 알아보기

- [블로그 첫 페이지 — DNS 용어, 도메인 구조, 이름 풀이 과정](https://app.notion.com/p/DNS_-3c9b3160e4c08066bac6ecdd934b9dd8)
- [블로그 1번 페이지 — 루트 DNS 서버 질의와 UDP/TCP 재질의](https://app.notion.com/p/1-Root-DNS-3cab3160e4c0801088bef336ae13ce34)
- [블로그 2번 페이지 — DNS 질의 함수 분리](https://app.notion.com/p/2-1-3cbb3160e4c0809fb3b9d407ffa67888)
- [블로그 3번 페이지 — 다음 DNS 서버로 반복 질의](https://app.notion.com/p/3-ipv4-3cbb3160e4c08087b3b1cf4bf0caa846)
- [블로그 4번 페이지 — 반복·종료 조건 정리](https://app.notion.com/p/4-2-3ccb3160e4c080e19b32d2fe3850908b)
- [블로그 5번 페이지 — 질의 경로 출력](https://app.notion.com/p/5-3cdb3160e4c0809fbc5cd29d29151740)
- [블로그 6번 페이지 — Windows DNS 캐시 TTL과 `hosts` 파일 확인](https://app.notion.com/p/6-hosts-cache-TTL-3ceb3160e4c08035ba8ee98bbc3b0d8d)

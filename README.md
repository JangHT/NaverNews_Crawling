# 네이버 뉴스기사 크롤링 코드 입니다

[프로세스 흐름]

페이지별(10개) title, body, date, company, url 정보를 긁어와 
dictionary 형태로 변환후 csv 파일로 저장한다

[수정 요구 사항]

1. csv 파일 저장시 body 부분에서 -, =, + 등으로 시작하면 연산기호로 생각하여 $?NAME으로 뜬다. 
    (단, txt 파일의 경우 원본 그대로 출력함)
2. body 크롤링시 cp949 에러 try except으로 수정하면 깔끔할듯
3. title, body, date, company, url 크롤링 수행중 하나라도 잘못되면 그부분 write 하지 않는 
   try except 부분 추가 필요

curl 'http://127.0.0.1:8080/rest/captcha/' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Accept-Language: en' \
  -H 'Cache-Control: no-cache' \
  -H 'Connection: keep-alive' \
  -H 'Cookie: language=en; welcomebanner_status=dismiss; cookieconsent_status=dismiss; continueCode=2bk8y9XlY4EnxLvwZaqm7dzrTVikBfejhBeSY6dP5ez6jorKOWBQDV3gJ1Np' \
  -H 'Pragma: no-cache' \
  -H 'Referer: http://127.0.0.1:8080/' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  --compressed


curl 'http://127.0.0.1:8080/api/Feedbacks/' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Accept-Language: en' \
  -H 'Cache-Control: no-cache' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json' \
  -H 'Cookie: language=en; welcomebanner_status=dismiss; cookieconsent_status=dismiss; continueCode=2bk8y9XlY4EnxLvwZaqm7dzrTVikBfejhBeSY6dP5ez6jorKOWBQDV3gJ1Np' \
  -H 'Origin: http://127.0.0.1:8080' \
  -H 'Pragma: no-cache' \
  -H 'Referer: http://127.0.0.1:8080/' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  --data-raw '{"captchaId":1,"captcha":"3","comment":"ttt (anonymous)","rating":0}' \
  --compressed
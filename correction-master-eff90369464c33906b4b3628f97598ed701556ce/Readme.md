## Correction 

### 说明
1. 此模组功能为纠错，輸入一問句，糾錯後返回

### API

```
GET <IP>:15901/correction/v1/<TEXT>
```

### Response
field | description 
------|------------
query | 輸入的問句
spellCheck | 糾錯完的結果
madeChange | 是否有糾錯
stateCode | 狀態碼，0代表成功，-1 代表過程有錯誤

```
{
  "query": "给我徐子摩",
  "spellCheck": "给我徐志摩",
  "madeChange": True,
  "stateCode": 0
}
```

### Health Check
```
GET <IP>:15901/correction/_health_check
```

### Test
```
pip3 install tox
tox -r -e test
```


### Limitation & Issue

1. 輸入的問句長度無限制
2. 問句有空白時無法處理

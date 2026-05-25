### **获取余额**

https://weixin.shandongtowngas.com.cn/nv1/vcc-cbs/charge/gasFeeBaseinfo?subsId=8ad88b839ae98c6a019cf3ee53921e22&sign=F7DEDACF1C38D33360AD5C8C1BA7A105&timestamp=1778030752518&orgId=8ad88b8582f48df601835f6235810065

Authorization Bearer d070115bda4843ff91ea42645948ba25

```json
{
    "feePayable": "0",
    "lastMeterReadingDate": "2026-05-06",
    "resultCode": "0",
    "availableBalance": "50.00"
}
```

### **查询用气记录**

https://weixin.shandongtowngas.com.cn/nv1/vcc-cbs/carelessWorkorder/gasConsumptionDataQuery?subsId=8ad88b839ae98c6a019cf3ee53921e22&timestamp=1778030732804&sign=194153F1C9AA56EA2AC94477597015A9

Authorization Bearer d070115bda4843ff91ea42645948ba25

```json
{
   "gasConsumptionTrendInfo":[
      {
         "lastYearFlag":"Y",
         "yrMonth":"202501",
         "gasSum":"0"
      },
      {
         "lastYearFlag":"Y",
         "yrMonth":"202502",
         "gasSum":"0"
      },
      {
         "lastYearFlag":"Y",
         "yrMonth":"202503",
         "gasSum":"0"
      },
      {
         "lastYearFlag":"Y",
         "yrMonth":"202504",
         "gasSum":"0"
      },
      {
         "lastYearFlag":"Y",
         "yrMonth":"202505",
         "gasSum":"0"
      },
      {
         "lastYearFlag":"Y",
         "yrMonth":"202506",
         "gasSum":"0"
      },
      {
         "lastYearFlag":"Y",
         "yrMonth":"202507",
         "gasSum":"0"
      },
      {
         "lastYearFlag":"Y",
         "yrMonth":"202508",
         "gasSum":"0"
      },
      {
         "lastYearFlag":"Y",
         "yrMonth":"202509",
         "gasSum":"0"
      },
      {
         "lastYearFlag":"Y",
         "yrMonth":"202510",
         "gasSum":"0"
      },
      {
         "lastYearFlag":"Y",
         "yrMonth":"202511",
         "gasSum":"0"
      },
      {
         "lastYearFlag":"Y",
         "yrMonth":"202512",
         "gasSum":"0"
      },
      {
         "lastYearFlag":"N",
         "yrMonth":"202601",
         "gasSum":"0"
      },
      {
         "lastYearFlag":"N",
         "yrMonth":"202602",
         "gasSum":"0"
      },
      {
         "lastYearFlag":"N",
         "yrMonth":"202603",
         "gasSum":"0"
      },
      {
         "lastYearFlag":"N",
         "yrMonth":"202604",
         "gasSum":"0"
      },
      {
         "lastYearFlag":"N",
         "yrMonth":"202605",
         "gasSum":"0"
      },
      {
         "lastYearFlag":"N",
         "yrMonth":"202606",
         "gasSum":"0"
      },
      {
         "lastYearFlag":"N",
         "yrMonth":"202607",
         "gasSum":"0"
      },
      {
         "lastYearFlag":"N",
         "yrMonth":"202608",
         "gasSum":"0"
      },
      {
         "lastYearFlag":"N",
         "yrMonth":"202609",
         "gasSum":"0"
      },
      {
         "lastYearFlag":"N",
         "yrMonth":"202610",
         "gasSum":"0"
      },
      {
         "lastYearFlag":"N",
         "yrMonth":"202611",
         "gasSum":"0"
      },
      {
         "lastYearFlag":"N",
         "yrMonth":"202612",
         "gasSum":"0"
      }
   ],
   "gasConsumptionInfo":[
      {
         "resTypeCategory":"0",
         "lastYearFlag":"N",
         "subsCode":"1970117677",
         "yrMonth":"202604",
         "meterCode":"183240102949",
         "money":"0",
         "gasSum":"0",
         "lastReading":"1",
         "currReading":"1",
         "readingDate":"2026-04-22",
         "rechargeDetails":null
      },
      {
         "resTypeCategory":"0",
         "lastYearFlag":"N",
         "subsCode":"1970117677",
         "yrMonth":"202603",
         "meterCode":"183240102949",
         "money":"0",
         "gasSum":"0",
         "lastReading":"1",
         "currReading":"1",
         "readingDate":"2026-03-24",
         "rechargeDetails":null
      }
   ],
   "resultCode":"0"
}
```

### **获取用气阶梯数据**

https://weixin.shandongtowngas.com.cn/nv1/vcc-cbs/charge/gasStepFee?subsId=8ad88b839ae98c6a019cf3ee53921e22&orgId=8ad88b8582f48df601835f636dca0067&timestamp=1778030732800&sign=6B08C04131729C7DC074F6AFB58EFC47

Authorization Bearer d070115bda4843ff91ea42645948ba25

```json
{
   "datas":{
      "buyamount":"0",
      "stepList":[
         {
            "priceModel":null,
            "modelSeq":"1",
            "minMount":null,
            "maxMount":"216",
            "mountTrate":null,
            "price":"3.5",
            "discFactor":null,
            "effDate":null,
            "expDate":null,
            "priceCode":null,
            "stepName":"一阶气价"
         },
         {
            "priceModel":null,
            "modelSeq":"2",
            "minMount":null,
            "maxMount":"360",
            "mountTrate":null,
            "price":"4.1",
            "discFactor":null,
            "effDate":null,
            "expDate":null,
            "priceCode":null,
            "stepName":"二阶气价"
         },
         {
            "priceModel":null,
            "modelSeq":"3",
            "minMount":null,
            "maxMount":"-1",
            "mountTrate":null,
            "price":"5",
            "discFactor":null,
            "effDate":null,
            "expDate":null,
            "priceCode":null,
            "stepName":"三阶气价"
         }
      ]
   },
   "resultCode":"0"
}
```

## 刷新令牌

https://weixin.shandongtowngas.com.cn/vcc-oauth/oauth/authorize2/refreshToken?refreshToken=eed9414e90de41b3ac8f0f5d282bfd88&sign=CB2615BE1BAE885441B3399C3863AE57&timestamp=1778076082856

```jsx
{
    "access_token": "da44e33ab79e41549f2114cfe3e84bc7",
    "refresh_token": "f5fbb171e90c4736b747b5c935b14b06",
    "expires_in": 7200,
    "scope": null
}
```

refresh_token只能用一次，每次调用这个接口会返回一个新的refresh_token
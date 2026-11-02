# 云碩資產管理官網 www.xcloudam.com

云碩資產管理股份有限公司（XCloud Asset Management Co., Ltd.）官網原始碼。單頁靜態網站：`index.html` ＋ `assets/`，無建置步驟、無後端。

- 主軸：銷售研華 MIC-743-AT（NVIDIA Jetson T5000／Thor）邊緣 AI 設備，搭配 x360 數位孿生維運、xESG 碳盤查、xMeetAI 會議記錄三套系統。
- 諮詢表單無後端，送出時組成信件開啟使用者的郵件程式（mailto）。
- 線上環境：Azure Static Web Apps `xcloudam`（資源群組 `xcloudam-Website`）。

## 本機預覽

```bash
python3 -m http.server 8765
```

## 部署

部署權杖不放在 repo 內，部署時以 Azure CLI 即時取得：

```bash
swa deploy . --deployment-token "$(az staticwebapp secrets list -n xcloudam -g xcloudam-Website --query properties.apiKey -o tsv)" --env production
```

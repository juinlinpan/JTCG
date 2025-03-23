# JTCG (Japanese Travel Chat Guide)

一個基於 AI 的日本旅遊諮詢聊天機器人系統。

## 專案架構

```
.
├── backend/
│   └── app/
│       ├── agents/         # AI 代理邏輯
│       ├── main.py        # FastAPI 後端服務
│       ├── schemas.py     # 資料模型定義
│       └── Dockerfile     # 後端容器設定
├── frontend/
│   ├── src/              # React 前端程式碼
│   ├── package.json      # 前端依賴配置
│   └── Dockerfile        # 前端容器設定
└── docker-compose.yml    # 容器編排配置
```

## 技術棧

- 後端：Python + FastAPI
- 前端：React + TypeScript
- 容器化：Docker + Docker Compose

## 開始使用

### 前置需求

- Docker
- Docker Compose

### 安裝與執行

1. 複製專案
```bash
git clone [repository-url]
cd JTCG
```

2. 啟動服務
```bash
docker-compose up --build
```

3. 訪問服務
- 前端界面：http://localhost:3000
- API 文檔：http://localhost:9527/docs

## API 端點

- `GET /messages/reset` - 重置對話
- `POST /messages` - 發送新訊息
- `GET /messages/get_messages` - 獲取對話歷史
- `GET /events` - Server-Sent Events (SSE) 端點，用於即時訊息推送

## 特色功能

- 即時對話：使用 SSE (Server-Sent Events) 實現即時訊息推送
- AI 驅動：使用先進的 AI 模型提供旅遊建議
- 對話記憶：保持上下文理解，提供連貫的對話體驗

## 開發注意事項

- 後端服務運行在 9527 端口
- 前端服務運行在 3000 端口
- 使用 Docker 網絡 "jtcg-network" 進行服務間通信
- SSE 連接需要保持長連接支持

## 授權

[授權說明]

# 流程圖設計文件 (FLOWCHART)：讀書筆記本系統

本文件根據產品需求 (PRD) 與系統架構 (ARCHITECTURE) 進行視覺化設計，說明使用者在網站中的操作路徑與系統內部的資料流動。

## 1. 使用者流程圖 (User Flow)

此流程圖展示使用者進入讀書筆記本系統後，能夠執行的所有主要操作，包含查看書單、新增書籍、以及針對特定書籍的編輯與心得撰寫等。

```mermaid
flowchart LR
    A([使用者開啟網頁]) --> B[首頁 - 書單列表]
    
    %% 書單操作
    B --> C{要執行什麼操作？}
    
    C -->|搜尋或篩選| D[輸入關鍵字 / 選擇分類]
    D --> B
    
    C -->|新增書籍| E[進入「新增書籍」表單頁面]
    E --> F[填寫書名、作者、分類]
    F -->|送出表單| B
    
    C -->|點擊書籍| G[進入「書籍詳情與心得」頁面]
    
    %% 詳情頁操作
    G --> H{要執行什麼操作？}
    
    H -->|撰寫/編輯心得| I[填寫心得與評分]
    I -->|儲存| G
    
    H -->|更新閱讀狀態| J[切換狀態: 未讀/閱讀中/已讀]
    J -->|儲存| G
    
    H -->|編輯基本資訊| L[修改書名、作者等]
    L -->|儲存| G
    
    H -->|刪除書籍| K[點擊刪除並確認]
    K -->|成功刪除| B
    
    H -->|返回列表| B
```

## 2. 系統序列圖 (Sequence Diagram)

此圖描述使用者「新增一本書籍並撰寫心得」的完整後端資料流與互動過程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Database Model
    participant DB as SQLite

    User->>Browser: 填寫「新增書籍」表單並送出
    Browser->>Flask: POST /books/new (帶入表單資料)
    Flask->>Model: 建立 Book 物件並驗證資料
    Model->>DB: INSERT INTO books (書名, 作者, 分類, 狀態...)
    DB-->>Model: 寫入成功
    Model-->>Flask: 回傳成功狀態
    Flask-->>Browser: HTTP 302 重新導向至首頁 (GET /)
    
    User->>Browser: 點擊剛新增的書籍
    Browser->>Flask: GET /books/{id}
    Flask->>DB: SELECT * FROM books WHERE id={id}
    DB-->>Flask: 回傳書籍資料
    Flask-->>Browser: 渲染並回傳 detail.html
    
    User->>Browser: 填寫讀書心得與評分並送出
    Browser->>Flask: POST /books/{id}/edit
    Flask->>DB: UPDATE books SET notes=..., rating=... WHERE id={id}
    DB-->>Flask: 更新成功
    Flask-->>Browser: 重新導向回書籍詳情頁
```

## 3. 功能清單對照表

以下為系統核心功能對應的 URL 路徑與 HTTP 方法初步規劃：

| 功能名稱 | URL 路徑 | HTTP 方法 | 說明 |
| --- | --- | --- | --- |
| 首頁 / 書單列表 | `/` | GET | 顯示所有書籍列表，可包含搜尋與篩選參數 |
| 顯示新增表單 | `/books/new` | GET | 呈現新增書籍的 HTML 表單頁面 |
| 處理新增書籍 | `/books/new` | POST | 接收表單資料，寫入資料庫後導向首頁 |
| 書籍詳情與心得 | `/books/<id>` | GET | 顯示特定書籍的詳細資料、閱讀狀態與心得 |
| 更新書籍資訊/心得 | `/books/<id>/edit` | POST | 接收更新的書籍資料、狀態、心得或評分 |
| 刪除書籍 | `/books/<id>/delete` | POST | 從資料庫刪除該書籍並導向首頁 |

> 註：為符合傳統 HTML 表單只支援 GET 與 POST 的限制，編輯與刪除操作將透過 POST 方法實作（或可於表單中使用隱藏欄位控制實際行為）。

# 路由設計文件 (ROUTES)：讀書筆記本系統

本文件基於產品需求 (PRD)、系統架構 (ARCHITECTURE) 與資料庫設計 (DB DESIGN) 進行路由與頁面的詳細規劃。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 首頁 / 書單列表 | GET | `/` 或 `/books` | `templates/index.html` | 顯示所有書籍列表 |
| 新增書籍頁面 | GET | `/books/new` | `templates/new_book.html` | 顯示新增書籍的表單 |
| 建立書籍 | POST | `/books` | — | 接收表單，存入 DB，重導向至首頁 |
| 書籍詳情與心得 | GET | `/books/<int:id>` | `templates/detail.html` | 顯示單筆書籍詳情、心得與評分 |
| 編輯書籍頁面 | GET | `/books/<int:id>/edit` | `templates/edit_book.html` | 顯示編輯書籍與心得的表單 |
| 更新書籍 | POST | `/books/<int:id>/update` | — | 接收表單，更新 DB，重導向至詳情頁 |
| 刪除書籍 | POST | `/books/<int:id>/delete` | — | 刪除指定書籍後重導向至首頁 |

## 2. 每個路由的詳細說明

### 首頁 / 書單列表 (`GET /` 或 `GET /books`)
- **輸入**：無（未來可擴充搜尋參數 `?q=關鍵字`）。
- **處理邏輯**：呼叫 `Book.get_all()` 取得所有書籍資料。
- **輸出**：渲染 `index.html`，傳入 `books` 變數。
- **錯誤處理**：無特殊錯誤，若無資料則在畫面上顯示提示。

### 新增書籍頁面 (`GET /books/new`)
- **輸入**：無。
- **處理邏輯**：準備顯示表單。
- **輸出**：渲染 `new_book.html`。

### 建立書籍 (`POST /books`)
- **輸入**：表單欄位 `title` (必填), `author`, `category`。
- **處理邏輯**：驗證 `title` 是否為空，若是則 flash 錯誤訊息並重新導向。通過後呼叫 `Book.create()` 寫入資料庫。
- **輸出**：重導向至首頁 `/`。

### 書籍詳情與心得 (`GET /books/<int:id>`)
- **輸入**：URL 參數 `id`。
- **處理邏輯**：呼叫 `Book.get_by_id(id)`，若找不到則回傳 404。
- **輸出**：渲染 `detail.html`，傳入 `book` 變數。
- **錯誤處理**：404 Not Found 頁面。

### 編輯書籍頁面 (`GET /books/<int:id>/edit`)
- **輸入**：URL 參數 `id`。
- **處理邏輯**：呼叫 `Book.get_by_id(id)` 取得目前資料以填入表單。
- **輸出**：渲染 `edit_book.html`，傳入 `book` 變數。
- **錯誤處理**：若找不到該書則回傳 404。

### 更新書籍 (`POST /books/<int:id>/update`)
- **輸入**：URL 參數 `id`，表單欄位 `title`, `author`, `category`, `status`, `rating`, `notes`。
- **處理邏輯**：取得書籍並驗證必填欄位。使用 `book.update()` 寫入資料庫。
- **輸出**：重導向至書籍詳情頁 `/books/<id>`。

### 刪除書籍 (`POST /books/<int:id>/delete`)
- **輸入**：URL 參數 `id`。
- **處理邏輯**：呼叫 `Book.get_by_id(id)` 取得書籍並執行 `book.delete()` 刪除資料。
- **輸出**：重導向至首頁 `/`。

## 3. Jinja2 模板清單

所有的 HTML 模板皆存放於 `app/templates/` 目錄下：

1. `base.html`：共用版型（包含 HTML `<head>`、導覽列 navbar 與頁尾 footer，以及引入共用 CSS）。
2. `index.html`：首頁（書單列表），繼承自 `base.html`。
3. `new_book.html`：新增書籍表單，繼承自 `base.html`。
4. `detail.html`：書籍詳情與心得展示頁，繼承自 `base.html`。
5. `edit_book.html`：編輯書籍與撰寫心得表單，繼承自 `base.html`。
6. `404.html`：找不到頁面時的錯誤提示（選用），繼承自 `base.html`。

## 4. 路由骨架程式碼

我們在 `app/routes/main.py` 中使用了 Flask Blueprint 建立了路由的骨架程式碼，並在 `app/routes/__init__.py` 中匯出，詳細實作邏輯將在下一階段補齊。

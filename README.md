
# 影片與字幕剪輯處理腳本

此Python腳本用於從影片中移除指定的時間段，並對應調整字幕時間。使用該腳本，您可以輕鬆剪輯影片並同步更新字幕，適用於需要批量處理影片和字幕的情況。

## 功能概述

- **影片處理**：使用 `moviepy` 庫剪輯影片，移除不需要的片段。
- **字幕處理**：使用 `pysrt` 庫同步調整字幕的時間軸，確保與剪輯後的影片對應。

## 先決條件

### 系統要求
- **Python 版本**：Python 3.x
- **依賴庫**：
  - `moviepy`
  - `pysrt`

### 安裝必要庫

使用以下命令安裝依賴庫：

```bash
pip install moviepy pysrt
```

## 使用方法

1. **準備影片與字幕文件**：

   將您的影片文件（例如 `DJI_0132.MP4`）和字幕文件（例如 `DJI_0132.srt`）放在對應的目錄下。

2. **定義輸入與輸出文件**：

   修改腳本中的 `FILE_NAME` 變數，以設置輸入文件的路徑和名稱：

   ```python
   FILE_NAME = "/home/ubuntu/大疆影片/0132/DJI_0132"
   ```

3. **定義移除的時間段**：

   在腳本中調整 `remove_intervals` 列表，根據需求指定要移除的時間段：

   ```python
   remove_intervals = [
       ('0:34', '0:47'),
       ('2:48', '2:51'),
       ('2:53', 'end'),
   ]
   ```

4. **運行腳本**：

   在終端中運行以下命令：

   ```bash
   python your_script_name.py
   ```

   **注意**：請將 `your_script_name.py` 替換為實際的腳本文件名。

5. **檢查輸出結果**：

   - **影片**：剪輯後的影片將保存為 `{FILE_NAME}_crop.mp4`。
   - **字幕**：同步調整後的字幕將保存為 `{FILE_NAME}_crop.srt`。

## 腳本邏輯

- **影片剪輯**：
  - 解析移除的時間段，計算要保留的片段，並使用 `moviepy` 進行剪輯與合併。

- **字幕調整**：
  - 讀取字幕，重新計算每段字幕的開始和結束時間，並保存為新的 `.srt` 文件。

## 注意事項

- **影片與字幕同步**：請確保提供的影片和字幕文件對應，否則可能導致不同步。
- **處理時間**：影片文件較大時，處理可能需要較長時間。
- **格式支持**：`moviepy` 支持多種影片格式，但建議使用常見格式如 MP4。

## 常見問題

### 1. 運行時出現錯誤

- **ImportError**：請確保安裝了所有依賴庫。
- **FileNotFoundError**：請確認影片和字幕文件路徑正確。

### 2. 輸出的影片或字幕有問題

- 檢查移除的時間段是否正確。
- 確保影片文件包含可解析的字幕軌。

## 版本資訊

- **版本**：1.0.0
- **日期**：2024 年 10 月 14 日
- **作者**：您的姓名

## 聯繫方式

如有任何問題或建議，請聯繫：

- **電子郵件**：your.email@example.com
- **GitHub**：https://github.com/your-github-profile

## 授權

此腳本基於 MIT 授權條款發布。詳情請參閱 [LICENSE](LICENSE) 文件。

---

**感謝您使用此腳本！希望它能幫助您輕鬆處理影片與字幕。**
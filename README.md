# 🎙️ FastAPI Audio Upload API

音声ファイルをアップロードし、文字起こしやスコアリングを行うための FastAPI アプリです。シンプルな HTML/JS フロントエンドから音声を送信し、JSON 形式で結果を受け取る構成になっています。

## 🚀 Features

* FastAPI による非同期音声ファイル受信
* `.wav` や `.mp3` などのバイナリファイルに対応
* 仮文字起こし・スコア返信（ダミー実装）
* CORS 設定済みでフロントエンドとの連携可能
* シンプルな HTML フロントエンド付き

---

## 🛠️ Setup

### ✅ 依存ライブラリのインストール

```bash
uv pip install fastapi uvicorn python-multipart
```

または `requirements.txt` がある場合：

```bash
uv pip install -r requirements.txt
```

### 🔄 サーバーの起動

```bash
uvicorn main:app --reload
```

デフォルトで [http://localhost:8000](http://localhost:8000) に立ち上がります。

---

## 🌐 API Usage

### `POST /upload/`

音声ファイルをアップロードします。

#### 🔸 リクエスト

* `Content-Type: multipart/form-data`
* パラメータ名: `file`
* ファイル: `.wav`, `.mp3`, `.ogg` など

```bash
curl -X POST http://localhost:8000/upload/ \
  -F "file=@your_audio.wav"
```

#### 🔹 レスポンス例（JSON）

```json
{
  "filename": "your_audio.wav",
  "transcription": "This is a dummy transcription.",
  "score": 87.3
}
```

---

## 🖥️ フロントエンドとの連携

`static/index.html` のような HTML ファイルで `<input type="file">` から送信可能です。JavaScript 側では以下のように fetch を使って送信します：

```js
const formData = new FormData();
formData.append("file", fileInput.files[0]);

fetch("http://localhost:8000/upload/", {
  method: "POST",
  body: formData
})
  .then(res => res.json())
  .then(json => {
    console.log("Response:", json);
  });
```

---

## 🔒 CORS 設定

ローカル開発では `localhost:3000` や `127.0.0.1` を許可しておくと便利です：

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📦 ディレクトリ構成（例）

```
project-root/
├── main.py
├── static/
│   └── index.html
└── temp_audio/
```

---

## 🧪 今後の展望

* Whisper 等による実音声文字起こし統合
* 発音評価スコアのリアル実装
* 音素・ピッチ・エネルギー情報の抽出可視化
* 音声アップロード時のユーザー識別・DB連携

---

## 📄 ライセンス

MIT License

---
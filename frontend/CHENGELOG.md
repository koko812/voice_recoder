````markdown
# 🔧 CHANGELOG-v0.1 **voice_recoder**  2025-06-08

---

## 1. 目的・背景

- **音声発音評価アプリのプロトタイプ**を素早く動かしたい  
- 最小構成として FastAPI + シンプル HTML/JS で  
  - 手元の音声ファイルをアップロードして  
  - 仮スコアと文字起こしを返す
- 研究室内サーバーでの運用を前提に **CORS/IP 制限・セキュリティ設計**を再確認

---

## 2. 主な変更点

| 種別 | 内容 |
|------|------|
| ✨ Add | `backend/main.py` 初版（/upload エンドポイント） |
| ✨ Add | `frontend/index.html`（ファイル選択＋fetch） |
| 🛠 Script | `init_voice_recoder.sh`（ディレクトリ自動生成） |
| ➕ Dependency | `uvicorn`, `python-multipart` を `uv` で追加 |
| ➕ Docs | セキュリティメモ / 技術メモ (2025-06-08_fastapi_file_upload_and_cors_basics.md) |

---

## 3. 設計変更の内容と理由

| 🟦 対象 | Before | After | 理由 |
|---------|--------|-------|------|
| **main.py** | なし | `/upload/` を `POST` + `UploadFile` で受信 | 最小のファイル受付 API を実装 |
| **CORS 設定** | `allow_origins=["*"]` | `allow_origins=["http://localhost:3000"]` (dev) | 本番では特定ドメインに絞る方針を確認 |
| **async/def** | ― | `async def upload_audio()` に統一 | 将来の非同期 DB/API 呼び出しに備え拡張性確保 |

---

## 4. 検討した別案・悩み

- **Flask(W​​SGI)** にする案 ⇢ 同時接続 & WebSocket 将来要件で却下  
- **同期 `def`** で始める ⇢ 拡張時に書き換え必須になるため `async` 採用  
- **フロントを React+Vite** ⇢ 学習コスト > 早期動作確認、まず素の HTML/JS に

---

## 5. 既存コードとの関係・依存箇所

- 影響範囲は `voice_recoder/` ディレクトリのみ  
- 外部ライブラリ依存：`fastapi`, `uvicorn`, `python-multipart`  
- 研究室 VPN 内以外にはまだ公開していないため互換性問題なし

---

## 6. 具体的な使い方 / CLI 実行例

```bash
# ① バックエンド
cd voice_recoder/backend
uv run uvicorn main:app --reload          # localhost:8000

# ② フロントエンド（静的サーバー）
cd ../frontend
python3 -m http.server 3000               # localhost:3000

# ③ ブラウザで http://localhost:3000 開き → ファイル選択 → アップロード
````

---

## 7. コメント・議論抜粋

> **User**: 「CORS を \* にすると危なくない？」
> **Assistant**: 「ブラウザ JS だけ守る壁。API 自体は認証や IP 制限が本丸です」

> **User**: 「非同期で 10k 問題クリアするのが FastAPI の強みか」
> **Assistant**: 「Yes、WSGI のスレッド地獄を回避できます」

---

## 8. 既知のバグ・限界

* ファイルサイズ上限・拡張子チェックなし
* 文字起こしはダミー固定文字列
* 認証なし：curl 直叩きで誰でも API 利用可能
* レート制限なし ⇒ DoS 耐性ゼロ

---

## 9. TODO リスト

* [ ] Whisper / faster-whisper を組込み実文字起こし
* [ ] `python-magic` で MIME 判定 → 拡張子偽装防御
* [ ] JWT or API-Key 認証を導入
* [ ] 本番ドメインで `allow_origins` をホワイトリスト化
* [ ] 最大ファイルサイズ・アップロード数制限
* [ ] WebSocket 版リアルタイム録音ストリーム（検討）

---

## 10. 感想・メモ

* **FastAPI × Uvicorn** の開発体験が非常に軽快。
* ブラウザ側の CORS エラーは **file://** 開きで嵌りがち —— 必ずローカル HTTP サーバーを使うこと。
* 今後は **セキュリティ層（認証・レートリミット）と音声処理層** を並行して強化予定。

```
```

# 🔧 CHANGELOG-v0.2 **voice\_recoder** 2025-06-08

---

## 1. 目的・背景

* 既存の素朴な `<script>` 直読み構成では

  * Spectrogram プラグインのバージョン整合が難しい
  * 非同期処理（アップロード⇄再生⇄文字起こし）がスパゲッティ化
* **Vite + ESM** 構成に刷新することで

  * モジュール管理とバンドルを一本化
  * WaveSurfer v7 の最新 API を正式に利用
  * 「音声再生をブロックしない文字起こし」UXを実現
* 研究室メンバーがすぐ触れるように **npm scripts & 最小雛形** を整備したい。

---

## 2. 主な変更点

| 種別          | ファイル                      | 内容                                  |
| ----------- | ------------------------- | ----------------------------------- |
| ✨ Add       | `frontend/vite.config.js` | Vite ルートを `frontend/` 直下に設定         |
| ✨ Add       | `frontend/src/main.js`    | WaveSurfer 初期化＋アップロード/再生ロジック        |
| ✨ Add       | `frontend/index.html`     | Waveform / Spectrogram 用コンテナ追加      |
| 🗑 Remove   | 旧 `frontend/index.html`   | CDN 直読み & v6/v7 混在コードを廃止            |
| 🔄 Change   | `backend/main.py`         | **CORS** を `"*"` に緩和（ローカル開発優先）      |
| 🛠 Refactor | JS ロジック                   | `postFile`, `fetchJSON` など小さなヘルパ関数化 |

---

## 3. 設計変更の内容と理由

| 🟦 対象              | Before                   | After                         | 理由                       |
| ------------------ | ------------------------ | ----------------------------- | ------------------------ |
| **フロントビルド**        | 素の HTML + `<script src>` | **Vite + ESM**                | プラグイン読込失敗を根絶／Hot-Reload  |
| **WaveSurfer 初期化** | イベントハンドラ内で都度生成           | `main.js` グローバルで 1インスタンス      | スコープ問題を排除／再生失敗バグを解消      |
| **非同期制御**          | `await` + `.then()` 混在   | すべて `await` or すべて `then` に統一 | 可読性向上／例外捕捉を一箇所に          |
| **再生ボタン制御**        | load 直後に有効化              | `wavesurfer.on('ready')` で有効化 | ready 前 play で無音になる問題を解消 |

---

## 4. 検討した別案・悩み

* **React + hooks** へ全面移行案
  → 学習コストと工数に対し今回は Vanilla + Vite が最速と判断
* **Next.js / Astro** など SSR 系
  → 静的 SPA で要件十分、将来の SSR 必要性が未定なため見送り
* **SSE / WebSocket** でリアルタイム文字起こし
  → まず非同期 fetch 版で体験を固め、後日置き換え予定。

---

## 5. 既存コードとの関係・依存箇所

* **バックエンド API パス** (`/upload/`, `/transcribe/`, `/temp_audio/…`) は変更なし。
* Python 側の依存ライブラリ追加なし（faster-whisperは既存）。
* 旧 `frontend/index.html` を参照しているリンクがある場合は 404 になる→要切替確認。

---

## 6. 具体的な使い方 / CLI 実行例

```bash
# backend
uvicorn backend.main:app --reload --workers 4

# frontend
cd frontend
npm install
npm run dev          # http://localhost:5173

# ブラウザ手順
# 1. ファイル選択 → アップロード
# 2. Waveform + Spectrogram が即描画
# 3. 再生ボタンで試聴しつつ、文字起こしが完了するとテキスト反映
```

---

## 7. コメント・議論抜粋

> **User**: 「ESM って何？ `<script src>` じゃダメ？」
> **Assistant**: 「v7 プラグインは ESM 専用。Vite で import するのが一番安定です。」

> **User**: 「再生ボタン押しても鳴らん！」
> **Assistant**: 「ready 前に play してました。`on('ready')` でボタンを有効化しましょう。」

---

## 8. 既知のバグ・限界

* 文字起こし fetch 中にリロードすると UI が中途半端なまま残る
* 大ファイル（> 20 MB）は upload 成功してもブラウザのデコードが遅延
* CORS を `*` にしているのは開発用。運用前に要制限。

---

## 9. TODO リスト

* [ ] Whisper segment を使い再生位置に字幕ハイライト
* [ ] `maxFileSize` & 拡張子バリデーション
* [ ] WebSocket 版リアルタイム文字起こし
* [ ] `vite build` 用の `nginx.conf` / S3 デプロイ手順
* [ ] GPU サーバー分離 ＋ Celery ジョブキュー

---

## 10. 感想・思ったこと

> Vite + WaveSurfer ESM の組み合わせは「最初のハマり所（プラグイン読込）」を越えると快適そのもの。
> **「アップロード直後に再生できる UX」** がスムーズにつくれたのが大きな成果。今後はバックエンドを並列化して、より重い解析もブロックフリーで回せる構成にしていきたい。

</br>
</br>
</br>
</br>
</br>

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

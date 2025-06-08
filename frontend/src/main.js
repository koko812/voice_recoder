/* ---------- 依存ライブラリ ---------- */
import WaveSurfer          from 'wavesurfer.js'
import SpectrogramPlugin   from 'wavesurfer.js/dist/plugins/spectrogram.esm.js'

/* ---------- DOM 取得 ---------- */
const $waveform        = document.querySelector('#waveform')
const $spectrogram     = document.querySelector('#spectrogram')
const $fileInput       = document.querySelector('#audioInput')
const $uploadBtn       = document.querySelector('#uploadBtn')
const $playBtn         = document.querySelector('#playBtn')
const $transcriptionTx = document.querySelector('#transcriptionText')

/* ---------- WaveSurfer インスタンス ---------- */
const wavesurfer = WaveSurfer.create({
  container      : $waveform,
  waveColor      : '#4F4A85',
  progressColor  : '#383351',
  height         : 100,
  plugins        : [
    SpectrogramPlugin.create({
      container : $spectrogram,
      labels    : true,
      fftSamples: 512,
      height    : 128,
    }),
  ],
})

wavesurfer.on('ready', () => {             // 再生位置を初期化
  $playBtn.disabled = false
})

wavesurfer.on('audioprocess', () => {      // 再生位置のリアルタイム表示
  document.querySelector('#currentTime').textContent =
    wavesurfer.getCurrentTime().toFixed(2)
})

wavesurfer.on('finish', () => {            // 終端で 0 に戻す
  wavesurfer.seekTo(0)
  document.querySelector('#currentTime').textContent = '0.00'
})

/* ---------- 再生 / 一時停止 ---------- */
$playBtn.addEventListener('click', () => wavesurfer.playPause())

/* ---------- アップロード & 文字起こし ---------- */
$uploadBtn.addEventListener('click', async () => {
  const file = $fileInput.files?.[0]
  if (!file) return alert('ファイルを選んでください')

  try {
    $playBtn.disabled            = true
    $transcriptionTx.textContent = '（文字起こし中...）'

    /* 1) アップロード */
    const { filename } = await postFile(file)
    const audioUrl     = `http://localhost:8000/temp_audio/${filename}`

    /* 2) 音声は即ロード（ready → 再生可能に）*/
    wavesurfer.load(audioUrl)

    /* 3) transcription は裏で取得 */
    const { transcription } = await fetchJSON(
      `http://localhost:8000/transcribe/${filename}`
    )
    $transcriptionTx.textContent = transcription

  } catch (err) {
    console.error(err)
    alert('アップロード / 文字起こしに失敗しました')
    $transcriptionTx.textContent = '（エラー）'
  }
})

/* ---------- 小さなヘルパ ---------- */
async function postFile(file) {
  const fd = new FormData()
  fd.append('file', file)
  const res = await fetch('http://localhost:8000/upload/', { method: 'POST', body: fd })
  if (!res.ok) throw new Error('upload failed')
  return res.json()
}

async function fetchJSON(url) {
  const res = await fetch(url)
  if (!res.ok) throw new Error(`${url} failed`)
  return res.json()
}

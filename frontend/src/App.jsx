import { useState, useRef } from 'react'
import Resolucao from './components/Resolucao'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
  const [texto, setTexto] = useState('')
  const [imagem, setImagem] = useState(null)
  const [preview, setPreview] = useState(null)
  const [resolucao, setResolucao] = useState(null)
  const [loading, setLoading] = useState(false)
  const [erro, setErro] = useState(null)
  const inputRef = useRef()

  const handleImagem = (e) => {
    const file = e.target.files[0]
    if (!file) return
    setImagem(file)
    setPreview(URL.createObjectURL(file))
  }

  const removerImagem = () => {
    setImagem(null)
    setPreview(null)
    inputRef.current.value = ''
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!texto.trim() && !imagem) return
    setLoading(true)
    setErro(null)
    setResolucao(null)

    const form = new FormData()
    if (texto.trim()) form.append('texto', texto)
    if (imagem) form.append('imagem', imagem)

    try {
      const res = await fetch(`${API_URL}/resolver`, { method: 'POST', body: form })
      if (!res.ok) throw new Error('Erro no servidor')
      const data = await res.json()
      setResolucao(data.resolucao)
    } catch {
      setErro('Não foi possível conectar ao servidor. Verifique se o backend está rodando.')
    } finally {
      setLoading(false)
    }
  }

  const limpar = () => {
    setTexto('')
    setResolucao(null)
    setErro(null)
    removerImagem()
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-icon">⚓</div>
        <h1>Resolvedor Naval</h1>
        <p>Cole ou fotografe sua questão e receba a resolução passo a passo</p>
      </header>

      <main className="app-main">
        <form className="questao-form" onSubmit={handleSubmit}>
          <textarea
            className="questao-input"
            placeholder="Cole aqui o enunciado da questão... (ex: Se log₂8 = x, quanto vale x?)"
            value={texto}
            onChange={(e) => setTexto(e.target.value)}
            rows={5}
            disabled={loading}
          />

          <div className="upload-area">
            {preview ? (
              <div className="preview-wrapper">
                <img src={preview} alt="Questão" className="imagem-preview" />
                <button type="button" className="btn-remover" onClick={removerImagem}>✕ Remover foto</button>
              </div>
            ) : (
              <label className="btn-upload">
                📷 Fotografar questão
                <input
                  ref={inputRef}
                  type="file"
                  accept="image/*"
                  capture="environment"
                  onChange={handleImagem}
                  hidden
                />
              </label>
            )}
          </div>

          <div className="form-actions">
            <button
              type="submit"
              className="btn-resolver"
              disabled={loading || (!texto.trim() && !imagem)}
            >
              {loading ? (
                <><span className="spinner-sm" /> Resolvendo...</>
              ) : '⚡ Resolver'}
            </button>
            {(resolucao || texto || imagem) && (
              <button type="button" className="btn-limpar" onClick={limpar}>
                🗑 Nova questão
              </button>
            )}
          </div>
        </form>

        {erro && <div className="alert erro">{erro}</div>}

        {loading && (
          <div className="loading-box">
            <div className="spinner" />
            <span>Analisando a questão...</span>
          </div>
        )}

        {resolucao && <Resolucao texto={resolucao} />}
      </main>

      <footer className="app-footer">
        <p>Powered by Claude AI · Colégio Naval · Todas as matérias</p>
      </footer>
    </div>
  )
}

export default App

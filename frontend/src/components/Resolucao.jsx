export default function Resolucao({ texto }) {
  // Converte markdown simples em HTML legível
  const linhas = texto.split('\n')

  return (
    <div className="resolucao-box">
      <div className="resolucao-header">📋 Resolução passo a passo</div>
      <div className="resolucao-corpo">
        {linhas.map((linha, i) => {
          if (linha.startsWith('### ')) return <h3 key={i}>{linha.slice(4)}</h3>
          if (linha.startsWith('## '))  return <h2 key={i}>{linha.slice(3)}</h2>
          if (linha.startsWith('# '))   return <h2 key={i}>{linha.slice(2)}</h2>
          if (linha.startsWith('**') && linha.endsWith('**')) {
            return <p key={i}><strong>{linha.slice(2, -2)}</strong></p>
          }
          if (linha.match(/^\d+\.\s/)) return <p key={i} className="passo">{linha}</p>
          if (linha.startsWith('- '))   return <p key={i} className="item">• {linha.slice(2)}</p>
          if (linha.trim() === '')      return <br key={i} />
          return <p key={i}>{linha}</p>
        })}
      </div>
    </div>
  )
}

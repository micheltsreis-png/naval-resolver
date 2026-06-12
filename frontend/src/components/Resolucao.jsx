import ReactMarkdown from 'react-markdown'
import remarkMath from 'remark-math'
import rehypeKatex from 'rehype-katex'
import 'katex/dist/katex.min.css'

export default function Resolucao({ texto }) {
  return (
    <div className="resolucao-box">
      <div className="resolucao-header">📋 Resolução passo a passo</div>
      <div className="resolucao-corpo markdown">
        <ReactMarkdown
          remarkPlugins={[remarkMath]}
          rehypePlugins={[rehypeKatex]}
        >
          {texto}
        </ReactMarkdown>
      </div>
    </div>
  )
}

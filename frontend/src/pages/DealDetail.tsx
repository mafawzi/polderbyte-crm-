import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import {
  getDeal, getActivities, createActivity,
  summarizeDeal, nextSteps, qualifyDeal
} from '../lib/api'

export default function DealDetail() {
  const { id } = useParams()
  const dealId = Number(id)

  const [deal, setDeal] = useState<any>(null)
  const [activities, setActivities] = useState<any[]>([])
  const [newNote, setNewNote] = useState('')
  const [noteType, setNoteType] = useState('note')
  const [summary, setSummary] = useState('')
  const [steps, setSteps] = useState('')
  const [qualifications, setQualifications] = useState<any[]>([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    getDeal(dealId).then(setDeal)
    getActivities(dealId).then(setActivities)
  }, [dealId])

  async function handleAddActivity(e: React.FormEvent) {
    e.preventDefault()
    if (!newNote.trim()) return
    const activity = await createActivity({ deal_id: dealId, type: noteType, content: newNote })
    setActivities([activity, ...activities])
    setNewNote('')
  }

  async function handleSummarize() {
    setLoading(true)
    const res = await summarizeDeal(dealId)
    setSummary(res.summary)
    setLoading(false)
  }

  async function handleNextSteps() {
    setLoading(true)
    const res = await nextSteps(dealId)
    setSteps(res.next_steps)
    setLoading(false)
  }

  async function handleQualify() {
    setLoading(true)
    const res = await qualifyDeal(dealId)
    setQualifications(res)
    setLoading(false)
  }

  if (!deal) return <div className="p-8">Loading...</div>

  return (
    <div className="p-8 grid grid-cols-3 gap-6">
      {/* Left: activity log */}
      <div className="col-span-2">
        <h1 className="text-2xl font-semibold">{deal.title}</h1>
        <p className="text-gray-500 mb-6">${deal.value.toLocaleString()} · {deal.stage}</p>

        <form onSubmit={handleAddActivity} className="bg-white rounded-lg p-4 shadow-sm mb-6">
          <select value={noteType} onChange={e => setNoteType(e.target.value)} className="border rounded px-2 py-1 mb-2 text-sm">
            <option value="note">Note</option>
            <option value="call">Call</option>
            <option value="email">Email</option>
            <option value="meeting">Meeting</option>
          </select>
          <textarea
            value={newNote}
            onChange={e => setNewNote(e.target.value)}
            placeholder="Log a call, email, meeting, or note..."
            className="w-full border rounded px-3 py-2 mb-2"
            rows={3}
          />
          <button type="submit" className="bg-black text-white px-4 py-2 rounded text-sm">
            Add Activity
          </button>
        </form>

        <div className="space-y-3">
          {activities.map(a => (
            <div key={a.id} className="bg-white rounded-lg p-4 shadow-sm">
              <div className="flex justify-between items-start">
                <span className="text-xs uppercase text-gray-400">{a.type}</span>
                <span className="text-xs text-gray-400">{new Date(a.created_at).toLocaleString()}</span>
              </div>
              <p className="mt-1 text-sm">{a.content}</p>
              {a.ai_summary && (
                <p className="mt-2 text-xs text-blue-600 bg-blue-50 rounded px-2 py-1">
                  AI: {a.ai_summary}
                </p>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Right: AI panel */}
      <div className="space-y-4">
        <div className="bg-white rounded-lg p-4 shadow-sm">
          <h2 className="font-medium mb-3">AI Assistant</h2>
          <div className="space-y-2">
            <button onClick={handleSummarize} disabled={loading} className="w-full text-sm bg-gray-100 rounded px-3 py-2 hover:bg-gray-200">
              Summarize Deal
            </button>
            <button onClick={handleNextSteps} disabled={loading} className="w-full text-sm bg-gray-100 rounded px-3 py-2 hover:bg-gray-200">
              Suggest Next Steps
            </button>
            <button onClick={handleQualify} disabled={loading} className="w-full text-sm bg-gray-100 rounded px-3 py-2 hover:bg-gray-200">
              Run BANT Qualification
            </button>
          </div>
        </div>

        {summary && (
          <div className="bg-white rounded-lg p-4 shadow-sm">
            <h3 className="font-medium text-sm mb-2">Summary</h3>
            <p className="text-sm text-gray-700">{summary}</p>
          </div>
        )}

        {steps && (
          <div className="bg-white rounded-lg p-4 shadow-sm">
            <h3 className="font-medium text-sm mb-2">Next Steps</h3>
            <p className="text-sm text-gray-700 whitespace-pre-line">{steps}</p>
          </div>
        )}

        {qualifications.length > 0 && (
          <div className="bg-white rounded-lg p-4 shadow-sm">
            <h3 className="font-medium text-sm mb-2">BANT Qualification</h3>
            {qualifications.map(q => (
              <div key={q.id} className="mb-2 text-sm">
                <div className="flex justify-between">
                  <span className="capitalize font-medium">{q.criterion}</span>
                  <span className={q.confirmed ? 'text-green-600' : 'text-gray-400'}>
                    {q.confirmed ? '✓' : '—'} {q.score}%
                  </span>
                </div>
                <p className="text-xs text-gray-500">{q.notes}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

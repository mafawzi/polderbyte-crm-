import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getDeals } from '../lib/api'

const STAGES = ['lead', 'qualified', 'proposal', 'won', 'lost']

export default function Deals() {
  const [deals, setDeals] = useState<any[]>([])

  useEffect(() => {
    getDeals().then(setDeals)
  }, [])

  return (
    <div className="p-8">
      <h1 className="text-2xl font-semibold mb-6">Deal Pipeline</h1>
      <div className="grid grid-cols-5 gap-4">
        {STAGES.map(stage => (
          <div key={stage} className="bg-gray-100 rounded-lg p-3">
            <h2 className="font-medium capitalize mb-3 text-sm text-gray-600">{stage}</h2>
            <div className="space-y-2">
              {deals.filter(d => d.stage === stage).map(deal => (
                <Link
                  key={deal.id}
                  to={`/deals/${deal.id}`}
                  className="block bg-white rounded p-3 shadow-sm hover:shadow-md transition-shadow"
                >
                  <p className="font-medium text-sm">{deal.title}</p>
                  <p className="text-xs text-gray-500 mt-1">${deal.value.toLocaleString()}</p>
                </Link>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

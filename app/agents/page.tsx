import { Bot, TrendingUp, Activity, Play, Shield, Zap, Rocket } from 'lucide-react'

export default function AgentsPage() {
  const agents = [
    {
      name: 'Head Agent (Orchestrator)',
      type: 'orchestrator',
      status: 'active',
      desc: 'Breaks down tasks and coordinates all specialist agents',
      icon: Bot,
      color: 'text-red-400'
    },
    {
      name: 'Trend Scout',
      type: 'research',
      status: 'active',
      desc: 'Finds trending products from internet & e-commerce',
      icon: TrendingUp,
      color: 'text-blue-400'
    },
    {
      name: 'Analyst',
      type: 'analytics',
      status: 'active',
      desc: 'Analyzes revenue, traffic & conversion data',
      icon: Activity,
      color: 'text-green-400'
    },
    {
      name: 'Creative Studio',
      type: 'content',
      status: 'active',
      desc: 'Creates ad copy, video scripts & UGC content',
      icon: Zap,
      color: 'text-purple-400'
    },
    {
      name: 'Social Media Manager',
      type: 'social',
      status: 'active',
      desc: 'Posts content, replies to comments & sends DMs',
      icon: Rocket,
      color: 'text-orange-400'
    },
  ]

  return (
    <div className="min-h-screen bg-dark text-white px-6 py-12">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-end mb-12">
          <div>
            <h1 className="text-3xl font-bold mb-2">Agent Team</h1>
            <p className="text-gray-400">Five autonomous agents working 24/7</p>
          </div>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          {agents.map((agent, i) => (
            <div key={i} className="glass-card p-6 rounded-2xl hover:border-blue-500/50 transition-all" style={{ animationDelay: `${i * 0.1}s` }}>
              <div className="flex justify-between items-start mb-4">
                <div className="flex items-center gap-3">
                  <div className={`w-10 h-10 rounded-lg bg-${agent.color.split('-')[0]}-500/20 text-${agent.color} flex items-center justify-center`}>
                    <agent.icon className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="text-lg font-bold">{agent.name}</h3>
                    <p className="text-xs uppercase tracking-wider text-{agent.color.split('-')[0]}-400">{agent.type}</p>
                  </div>
                </div>
                <span className="flex items-center gap-1 px-2 py-1 rounded-full bg-green-500/20 text-green-400 text-xs font-medium">
                  <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
                  Online
                </span>
              </div>
              <p className="text-sm text-gray-400 mb-6">{agent.desc}</p>
              <div className="grid grid-cols-2 gap-3">
                <button className="btn-secondary w-full py-2 text-xs">View Details</button>
                <button className="btn-primary w-full py-2 text-xs">Configure</button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

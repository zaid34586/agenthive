import Link from 'next/link'
import { ArrowRight, Bot, TrendingUp, Activity, Play, Users, Shield, RefreshCw } from 'lucide-react'
import { useState, useEffect } from 'react'

export default function DashboardPage() {
  const [stats, setStats] = useState({ total_tasks: 0, active: 0, completed: 0 })
  const [recentTasks, setRecentTasks] = useState([])
  const [loading, setLoading] = useState(true)
  const token = localStorage.getItem('token')

  useEffect(() => {
    fetchStats()
    fetchTasks()
  }, [])

  const fetchStats = async () => {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/tasks/stats`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      if (res.ok) setStats(await res.json())
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }

  const fetchTasks = async () => {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/tasks/recent`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      if (res.ok) setRecentTasks(await res.json())
    } catch (e) {
      console.error(e)
    }
  }

  const createTask = async (e: React.FormEvent) => {
    e.preventDefault()
    const title = (e.target as any).elements[0].value
    const desc = (e.target as any).elements[1].value
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/tasks`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ title, description: desc }),
      })
      if (res.ok) {
        const data = await res.json()
        setRecentTasks([data, ...recentTasks].slice(0, 5))
        fetchStats()
        ;(e.target as any).reset()
      } else {
        alert('Failed to create task')
      }
    } catch (err) {
      alert('Error creating task')
    }
  }

  if (!token) {
    window.location.href = '/login'
    return null
  }

  return (
    <div className="min-h-screen bg-dark text-white">
      {/* Top Nav */}
      <nav className="fixed top-0 w-full z-50 px-6 py-4 glass-card backdrop-blur-xl border-b border-white/10">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div className="flex items-center gap-2">
            <div className="bg-blue-600 p-2 rounded-lg">
              <Bot className="w-5 h-5" />
            </div>
            <span className="text-xl font-bold">AgentHive</span>
          </div>
          <div className="flex gap-4">
            <Link href="/" className="text-sm text-gray-400 hover:text-white">Dashboard</Link>
            <Link href="/pricing" className="text-sm text-gray-400 hover:text-white">Pricing</Link>
            <button onClick={() => { localStorage.removeItem('token'); window.location.href = '/' }} className="text-sm text-red-400 hover:text-red-300">Logout</button>
          </div>
        </div>
      </nav>

      <div className="pt-20 px-6 pb-12">
        <div className="max-w-7xl mx-auto">
          {/* Welcome */}
          <div className="flex justify-between items-end mb-10">
            <div>
              <h1 className="text-3xl font-bold mb-2">Dashboard</h1>
              <p className="text-gray-400">Manage your agents and tasks</p>
            </div>
            <button
              onClick={fetchStats}
              className="flex items-center gap-2 px-4 py-2 bg-white/5 border border-white/10 rounded-lg hover:bg-white/10 transition-colors"
            >
              <RefreshCw className="w-4 h-4 animate-spin" />
              Refresh
            </button>
          </div>

          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-10">
            {[
              { label: 'Total Tasks', value: stats.total_tasks, color: 'text-blue-400', icon: Activity },
              { label: 'Active', value: stats.active, color: 'text-green-400', icon: Play },
              { label: 'Completed', value: stats.completed, color: 'text-purple-400', icon: Shield },
              { label: 'Success Rate', value: stats.total_tasks > 0 ? Math.round((stats.completed / stats.total_tasks) * 100) + '%' : '0%', color: 'text-orange-400', icon: TrendingUp },
            ].map((stat, i) => (
              <div key={i} className="glass-card p-6 rounded-2xl">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="text-sm text-gray-400">{stat.label}</p>
                    <h3 className="text-2xl font-bold {stat.color}">{stat.value}</h3>
                  </div>
                  <div className="w-10 h-10 rounded-lg bg-{stat.color.split('-')[0]}-500/20 text-{stat.color} flex items-center justify-center">
                    <stat.icon className="w-5 h-5" />
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Create Task */}
          <div className="glass-card p-8 rounded-2xl mb-10">
            <h2 className="text-lg font-bold mb-6">Create New Task</h2>
            <form onSubmit={createTask} className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="flex flex-col">
                <label className="text-sm text-gray-400 mb-2">Task Title</label>
                <input type="text" placeholder="e.g., Find trending winter products" className="input-field" required />
              </div>
              <div className="flex flex-col">
                <label className="text-sm text-gray-400 mb-2">Description</label>
                <textarea rows={2} placeholder="Describe what you want..." className="input-field" required></textarea>
              </div>
              <button
                type="submit"
                className="btn-primary w-full flex items-center justify-center gap-2"
              >
                <ArrowRight className="w-4 h-4" />
                Launch Agent Pipeline
              </button>
            </form>
          </div>

          {/* Recent Tasks */}
          <div className="glass-card rounded-2xl overflow-hidden">
            <div className="p-6 border-b border-white/10">
              <h2 className="text-lg font-bold">Recent Tasks</h2>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left">
                <thead>
                  <tr className="border-b border-white/10">
                    <th className="px-6 py-4 text-sm font-medium text-gray-400">Title</th>
                    <th className="px-6 py-4 text-sm font-medium text-gray-400">Status</th>
                    <th className="px-6 py-4 text-sm font-medium text-gray-400">Time</th>
                  </tr>
                </thead>
                <tbody>
                  {recentTasks.length > 0 ? (
                    recentTasks.map((task: any) => (
                      <tr key={task.id} className="border-b border-white/5 hover:bg-white/5 transition-colors">
                        <td className="px-6 py-4 text-sm font-medium">{task.title}</td>
                        <td className="px-6 py-4 text-sm">
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                            task.status === 'completed' ? 'bg-green-500/20 text-green-400' :
                            task.status === 'running' ? 'bg-blue-500/20 text-blue-400' :
                            'bg-red-500/20 text-red-400'
                          }`}>
                            {task.status}
                          </span>
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-400">
                          {task.created_at ? new Date(task.created_at).toLocaleString() : '-'}
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan={3} className="px-6 py-10 text-center text-gray-400">
                        No tasks yet. Create your first task above!
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

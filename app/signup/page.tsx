'use client'

import Link from 'next/link'
import { ArrowRight, Mail, Lock, User, Bot } from 'lucide-react'
import { useState } from 'react'

export default function SignupPage() {
  const [formData, setFormData] = useState({ email: '', password: '', full_name: '' })
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/auth/signup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      })
      if (res.ok) {
        alert('Account created! Please login.')
        window.location.href = '/login'
      } else {
        const err = await res.json()
        alert(err.detail || 'Signup failed')
      }
    } catch (err) {
      alert('Signup failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-dark flex items-center justify-center px-4">
      <div className="max-w-md w-full glass-card p-8 rounded-3xl">
        <div className="flex items-center gap-2 mb-8">
          <div className="bg-blue-600 p-2 rounded-lg">
            <Bot className="w-5 h-5" />
          </div>
          <span className="text-xl font-bold">AgentHive</span>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">Full Name</label>
            <input
              type="text"
              name="full_name"
              className="input-field w-full"
              placeholder="John Doe"
              onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">Email</label>
            <input
              type="email"
              name="email"
              className="input-field w-full"
              placeholder="you@company.com"
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">Password</label>
            <input
              type="password"
              name="password"
              className="input-field w-full"
              placeholder="••••••••"
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              required
            />
          </div>
          <button
            type="submit"
            className="btn-primary w-full flex items-center justify-center gap-2 disabled:opacity-50"
            disabled={loading}
          >
            {loading ? <span className="animate-spin"></span> : <ArrowRight className="w-4 h-4" />}
            Create Account
          </button>
        </form>

        <p className="mt-8 text-center text-sm text-gray-400">
          Already have an account?{' '}
          <Link href="/login" className="text-blue-400 hover:text-blue-300 font-medium">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  )
}

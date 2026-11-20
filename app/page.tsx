import Link from 'next/link'
import { ArrowRight, Rocket, Shield, Bot, TrendingUp, Zap } from 'lucide-react'

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-dark text-white">
      {/* Navbar */}
      <nav className="fixed w-full z-50 px-6 py-4">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div className="text-2xl font-bold flex items-center gap-2">
            <div className="bg-blue-600 p-2 rounded-lg">
              <Bot className="w-5 h-5" />
            </div>
            <span className="text-white">AgentHive</span>
          </div>
          <div className="hidden md:flex gap-6 text-sm font-medium">
            <Link href="/" className="text-blue-400">Home</Link>
            <Link href="#features" className="text-gray-400 hover:text-white">Features</Link>
            <Link href="#pricing" className="text-gray-400 hover:text-white">Pricing</Link>
            <Link href="/login" className="text-gray-400 hover:text-white">Login</Link>
            <Link href="/signup" className="btn-primary">Get Started</Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-6">
        <div className="max-w-7xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 text-blue-400 text-xs font-medium mb-6 animate-pulse-slow">
            <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
            All 5 Agents Active & Running
          </div>
          <h1 className="text-5xl md:text-7xl font-bold leading-tight mb-8">
            Build Your{' '}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-400">
              AI Agent Empire
            </span>
          </h1>
          <p className="text-xl text-gray-400 mb-10 max-w-2xl mx-auto">
            Multi-agent SaaS platform for trend research, content creation, social media automation, and revenue analytics. One dashboard, five specialized agents working for you 24/7.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/signup" className="btn-primary flex items-center justify-center gap-2 w-full sm:w-auto">
              Start Free Trial <ArrowRight className="w-4 h-4" />
            </Link>
            <Link href="/login" className="btn-secondary flex items-center justify-center gap-2 w-full sm:w-auto">
              Sign In
            </Link>
          </div>
        </div>
      </section>

      {/* Stats */}
      <section className="py-12 border-y border-white/10">
        <div className="max-w-7xl mx-auto px-6 grid grid-cols-2 md:grid-cols-4 gap-8">
          {[4250, 12500, 98, 4.5].map((stat, i) => (
            <div key={i} className="text-center animate-fade-in" style={{ animationDelay: `${i * 0.1}s` }}>
              <div className="text-3xl font-bold text-white mb-2">{stat}+</div>
              <div className="text-sm text-gray-400">
                {i === 0 ? 'Agents Deployed' : i === 1 ? 'Tasks Completed' : i === 2 ? 'Countries' : 'Avg ROI'}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Features */}
      <section id="features" className="py-24 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">Powerful AI Agents</h2>
            <p className="text-xl text-gray-400">Everything you need to automate your business</p>
          </div>
          <div className="grid md:grid-cols-3 gap-6">
            {[
              {
                icon: TrendingUp,
                title: 'Trend Scout',
                desc: 'Find trending products and keywords from internet and e-commerce platforms automatically.',
                color: 'text-blue-400'
              },
              {
                icon: Bot,
                title: 'Analyst',
                desc: 'Analyze revenue, traffic, conversion rates, and KPIs for data-driven decisions.',
                color: 'text-green-400'
              },
              {
                icon: Zap,
                title: 'Creative Studio',
                desc: 'Generate ad copy, video scripts, UGC content, and hashtags for your campaigns.',
                color: 'text-purple-400'
              },
              {
                icon: Rocket,
                title: 'Social Media',
                desc: 'Auto-post content, reply to comments, send DMs with affiliate links, manage traffic.',
                color: 'text-orange-400'
              },
              {
                icon: Shield,
                title: 'Head Agent',
                desc: 'Orchestrator that breaks down tasks and coordinates all specialist agents.',
                color: 'text-red-400'
              },
            ].map((feature, i) => (
              <div key={i} className="glass-card p-6 hover:border-blue-500/50 transition-all hover:-translate-y-1" style={{ animationDelay: `${i * 0.1}s` }}>
                <div className="w-10 h-10 rounded-lg bg-{feature.color.split('-')[0]}-500/20 text-{feature.color} flex items-center justify-center mb-4">
                  <feature.icon className="w-5 h-5" />
                </div>
                <h3 className="text-lg font-bold mb-2">{feature.title}</h3>
                <p className="text-gray-400 text-sm">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 px-6">
        <div className="max-w-4xl mx-auto glass-card p-12 text-center rounded-3xl">
          <h2 className="text-3xl font-bold mb-4">Ready to Automate?</h2>
          <p className="text-xl text-gray-400 mb-8">Join 4250+ businesses using AgentHive to grow revenue on autopilot.</p>
          <Link href="/signup" className="btn-primary">
            Get Started Free <ArrowRight className="w-4 h-4 ml-2" />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-6 border-t border-white/10">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div className="text-xl font-bold flex items-center gap-2">
            <div className="bg-blue-600 p-2 rounded-lg">
              <Bot className="w-5 h-5" />
            </div>
            AgentHive
          </div>
          <div className="flex gap-6 text-sm text-gray-400">
            <Link href="/" className="hover:text-white">Home</Link>
            <Link href="#features" className="hover:text-white">Features</Link>
            <Link href="#pricing" className="hover:text-white">Pricing</Link>
            <Link href="/login" className="hover:text-white">Login</Link>
            <div className="flex gap-4">
              <a href="#" className="hover:text-white"><span className="sr-only">Twitter</span>⭐</a>
              <a href="#" className="hover:text-white"><span className="sr-only">GitHub</span>💻</a>
            </div>
          </div>
          <div className="text-xs text-gray-500">
            © {new Date().getFullYear()} AgentHive. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  )
}

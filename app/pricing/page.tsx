export default function PricingPage() {
  return (
    <div className="min-h-screen bg-dark text-white px-6 py-12">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h1 className="text-4xl font-bold mb-4">Simple, Transparent Pricing</h1>
          <p className="text-xl text-gray-400">Choose the plan that fits your automation needs.</p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {/* Starter */}
          <div className="glass-card p-8 rounded-3xl border border-white/10">
            <h3 className="text-xl font-bold mb-2">Starter</h3>
            <div className="mb-6">
              <span className="text-4xl font-bold">$0</span>
              <span className="text-gray-400">/month</span>
            </div>
            <p className="text-sm text-gray-400 mb-8">For individuals testing automation</p>
            <ul className="space-y-4 mb-8 text-sm">
              <li className="flex items-center gap-3">
                <span className="text-gray-400">5</span> tasks/month
              </li>
              <li className="flex items-center gap-3">
                <span className="text-gray-400">Head Agent + Trend Scout</span>
              </li>
              <li className="flex items-center gap-3">
                <span className="text-gray-400">Basic analytics</span>
              </li>
              <li className="flex items-center gap-3 text-gray-600 line-through">
                <span className="text-gray-400">Creative Studio</span>
              </li>
              <li className="flex items-center gap-3 text-gray-600 line-through">
                <span className="text-gray-400">Social Media Manager</span>
              </li>
            </ul>
            <button className="btn-secondary w-full">Get Started</button>
          </div>

          {/* Pro */}
          <div className="glass-card p-8 rounded-3xl border-2 border-blue-500 relative">
            <div className="absolute -top-4 left-1/2 -translate-x-1/2 bg-green-500 text-white text-xs font-bold px-3 py-1 rounded-full">
              MOST POPULAR
            </div>
            <h3 className="text-xl font-bold mb-2">Pro</h3>
            <div className="mb-6">
              <span className="text-4xl font-bold">$499</span>
              <span className="text-gray-400">/month</span>
            </div>
            <p className="text-sm text-gray-400 mb-8">For serious creators & sellers</p>
            <ul className="space-y-4 mb-8 text-sm">
              <li className="flex items-center gap-3">
                <span className="text-green-400">✓</span> 50 tasks/month
              </li>
              <li className="flex items-center gap-3">
                <span className="text-green-400">✓</span> All 5 agents
              </li>
              <li className="flex items-center gap-3">
                <span className="text-green-400">✓</span> Creative Studio
              </li>
              <li className="flex items-center gap-3">
                <span className="text-green-400">✓</span> Social Media Manager
              </li>
              <li className="flex items-center gap-3">
                <span className="text-green-400">✓</span> Auto-reply comments & DMs
              </li>
              <li className="flex items-center gap-3">
                <span className="text-green-400">✓</span> Priority support
              </li>
            </ul>
            <button className="btn-primary w-full">Upgrade to Pro</button>
          </div>

          {/* Business */}
          <div className="glass-card p-8 rounded-3xl border border-white/10">
            <h3 className="text-xl font-bold mb-2">Business</h3>
            <div className="mb-6">
              <span className="text-4xl font-bold">$1,499</span>
              <span className="text-gray-400">/month</span>
            </div>
            <p className="text-sm text-gray-400 mb-8">For teams & agencies</p>
            <ul className="space-y-4 mb-8 text-sm">
              <li className="flex items-center gap-3">
                <span className="text-gray-400">✓</span> Unlimited tasks
              </li>
              <li className="flex items-center gap-3">
                <span className="text-gray-400">✓</span> All 5 agents + priority
              </li>
              <li className="flex items-center gap-3">
                <span className="text-gray-400">✓</span> Multi-user workspace
              </li>
              <li className="flex items-center gap-3">
                <span className="text-gray-400">✓</span> Custom API integration
              </li>
              <li className="flex items-center gap-3">
                <span className="text-gray-400">✓</span> Dedicated support
              </li>
              <li className="flex items-center gap-3">
                <span className="text-gray-400">✓</span> White-label reports
              </li>
            </ul>
            <button className="btn-secondary w-full">Contact Sales</button>
          </div>
        </div>
      </div>
    </div>
  )
}

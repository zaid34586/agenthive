import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'AgentHive - Multi-Agent AI SaaS Platform',
  description: 'Build, deploy, and manage AI agents for trend research, content creation, social media automation, and revenue analytics.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <head>
        <script src="https://cdn.tailwindcss.com"></script>
      </head>
      <body>{children}</body>
    </html>
  )
}

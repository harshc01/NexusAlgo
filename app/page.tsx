export default function Home() {
  return (
    <main className="min-h-screen p-8">
      <div className="max-w-6xl mx-auto space-y-6">
        
        <div className="bg-[#0D0D0D] border border-[#1A1A1A] rounded-xl p-8 shadow-2xl">
          <div className="flex items-center space-x-3 mb-4">
            <div className="w-3 h-3 rounded-full bg-[#10B981] animate-pulse"></div>
            <h1 className="text-[#10B981] font-mono text-xl tracking-wider">SYSTEM INITIALIZED</h1>
          </div>
          <p className="text-[#E5E7EB] font-mono opacity-70">
            The Vault is online. Awaiting data stream...
          </p>
        </div>

      </div>
    </main>
  );
}
import React, { useEffect, useState } from "react"
import {
  ShieldCheck,
  Lock,
  Unlock,
  Activity,
  FileText,
  Server,
  Zap,
} from "lucide-react"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { checkSystemHealth, type SystemHealth } from "@/lib/api"
import { CompressionMeter } from "@/components/medical/CompressionMeter"

export default function App() {
  const [health, setHealth] = useState<SystemHealth | null>(null)
  const [loadingHealth, setLoadingHealth] = useState<boolean>(true)

  useEffect(() => {
    checkSystemHealth()
      .then((data) => {
        setHealth(data)
        setLoadingHealth(false)
      })
      .catch(() => {
        setLoadingHealth(false)
      })
  }, [])

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      {/* Top PACS Navigation Header */}
      <header className="border-b border-slate-800 bg-slate-900/60 backdrop-blur sticky top-0 z-40 px-6 py-3.5 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-cyan-500/10 border border-cyan-500/20 text-cyan-400">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-base font-bold tracking-tight text-white">
                MedCrypt-Vault
              </h1>
              <Badge variant="outline" className="border-cyan-500/40 text-cyan-400 text-[10px] py-0">
                v1.0.0-phase2
              </Badge>
            </div>
            <p className="text-xs text-slate-400">
              Medical EHR Compression & Frequency-Domain Steganography Workstation
            </p>
          </div>
        </div>

        {/* Backend Connectivity Status */}
        <div className="flex items-center gap-3">
          {loadingHealth ? (
            <Badge variant="secondary" className="animate-pulse text-xs">
              <Server className="w-3 h-3 mr-1" /> Connecting to Engine...
            </Badge>
          ) : health ? (
            <Badge variant="success" className="text-xs">
              <span className="w-2 h-2 rounded-full bg-emerald-400 inline-block mr-1.5 animate-pulse" />
              Engine Online ({health.service})
            </Badge>
          ) : (
            <Badge variant="outline" className="border-amber-500/30 bg-amber-500/10 text-amber-400 text-xs">
              <Server className="w-3 h-3 mr-1" /> Engine Offline (Run Backend)
            </Badge>
          )}
          <Button variant="outline" size="sm" className="border-slate-800 text-xs text-slate-300 hover:text-white">
            <FileText className="w-3.5 h-3.5 mr-1" /> Docs & Rubrik
          </Button>
        </div>
      </header>

      {/* Main Workspace Body */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-6 space-y-6">
        <Tabs defaultValue="embed" className="w-full space-y-6">
          <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
            <TabsList className="bg-slate-900 border border-slate-800 p-1">
              <TabsTrigger value="embed" className="data-[state=active]:bg-cyan-500 data-[state=active]:text-slate-950 font-medium">
                <Lock className="w-3.5 h-3.5 mr-1.5" /> 1. Secure & Embed
              </TabsTrigger>
              <TabsTrigger value="extract" className="data-[state=active]:bg-cyan-500 data-[state=active]:text-slate-950 font-medium">
                <Unlock className="w-3.5 h-3.5 mr-1.5" /> 2. Extract & Restore
              </TabsTrigger>
              <TabsTrigger value="forensics" className="data-[state=active]:bg-cyan-500 data-[state=active]:text-slate-950 font-medium">
                <Activity className="w-3.5 h-3.5 mr-1.5" /> 3. Forensic & Quality Lab
              </TabsTrigger>
            </TabsList>

            <div className="text-xs text-slate-400 hidden sm:flex items-center gap-2">
              <Zap className="w-3.5 h-3.5 text-cyan-400" />
              <span>Engine Status: Fase 2 (LZ77 + Canonical Huffman) Active</span>
            </div>
          </div>

          {/* TAB 1: Secure & Embed */}
          <TabsContent value="embed" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2 space-y-6">
                <Card className="bg-slate-900/60 border-slate-800">
                  <CardHeader>
                    <CardTitle className="text-base text-white flex items-center gap-2">
                      <Lock className="w-4 h-4 text-cyan-400" /> Medical Image Cover & Payload Injection
                    </CardTitle>
                    <CardDescription className="text-slate-400">
                      Citra radiologi pembawa muatan terkompresi & terenkripsi
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="border border-dashed border-slate-800 rounded-xl p-8 text-center bg-slate-950/40">
                      <p className="text-sm text-slate-300 font-medium">Drag & Drop Citra Radiologi (Chest X-Ray / Brain MRI)</p>
                      <p className="text-xs text-slate-500 mt-1">Mendukung format PNG 8-bit lossless (Sampel: chest_xray_512.png)</p>
                    </div>
                  </CardContent>
                </Card>

                {/* Compression Engine Live Performance Meter */}
                <CompressionMeter />
              </div>

              {/* Sidebar Status Card */}
              <Card className="bg-slate-900/60 border-slate-800 h-fit">
                <CardHeader>
                  <CardTitle className="text-base text-white">Status Engine Modul</CardTitle>
                  <CardDescription className="text-slate-400">Verifikasi Kurikulum TK-PD</CardDescription>
                </CardHeader>
                <CardContent className="space-y-3 text-xs">
                  <div className="flex justify-between items-center py-1.5 border-b border-slate-800/60">
                    <span className="text-slate-400">Modul 1 & 2: Shannon Entropy</span>
                    <Badge variant="success" className="text-[10px]">Tuntas</Badge>
                  </div>
                  <div className="flex justify-between items-center py-1.5 border-b border-slate-800/60">
                    <span className="text-slate-400">Modul 4: Canonical Huffman</span>
                    <Badge variant="success" className="text-[10px]">Tuntas</Badge>
                  </div>
                  <div className="flex justify-between items-center py-1.5 border-b border-slate-800/60">
                    <span className="text-slate-400">Modul 6: LZ77 Sliding Window</span>
                    <Badge variant="success" className="text-[10px]">Tuntas (32 KB)</Badge>
                  </div>
                  <div className="flex justify-between items-center py-1.5 border-b border-slate-800/60">
                    <span className="text-slate-400">Test Suite Kompresi</span>
                    <Badge variant="success" className="text-[10px]">16/16 Passed</Badge>
                  </div>
                  <div className="flex justify-between items-center py-1.5">
                    <span className="text-slate-400">Next Milestone</span>
                    <Badge variant="default" className="text-[10px] bg-cyan-500 text-slate-950 font-bold">Fase 3: AES-256-GCM</Badge>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* TAB 2: Extract & Restore */}
          <TabsContent value="extract">
            <Card className="bg-slate-900/60 border-slate-800">
              <CardHeader>
                <CardTitle className="text-base text-white">Ekstraksi & Pemulihan Rekam Medis</CardTitle>
                <CardDescription className="text-slate-400">
                  DWT Extraction & AES-256-GCM Decryption Station
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-slate-400">Modul ekstraksi siap dihubungkan pada Fase 4 & 6.</p>
              </CardContent>
            </Card>
          </TabsContent>

          {/* TAB 3: Forensic Lab */}
          <TabsContent value="forensics">
            <Card className="bg-slate-900/60 border-slate-800">
              <CardHeader>
                <CardTitle className="text-base text-white">Laboratorium Steganalisis & Evaluasi Kualitas</CardTitle>
                <CardDescription className="text-slate-400">
                  Analisis PSNR, SSIM, Uji Statistik Chi-Square (χ²), dan Peta Selisih Frekuensi
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-slate-400">Modul forensik siap dihubungkan pada Fase 5 & 6.</p>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800/80 py-4 px-6 text-center text-xs text-slate-500 bg-slate-950">
        Tugas Akhir Teknik Kompresi dan Penyamaran Data (TK-PD) Kelas 7A — FTII UHAMKA (Dosen: Ir. Dimas Febriawan, S.Kom., M.T.I.)
      </footer>
    </div>
  )
}

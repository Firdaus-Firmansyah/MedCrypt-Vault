import React from "react"
import { Cpu, Zap, CheckCircle2, BarChart2 } from "lucide-react"
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

export interface CompressionStats {
  rawBytes: number
  compressedBytes: number
  compressionRatio: number
  spaceSavingPercent: number
  rawEntropy: number
  compressedEntropy: number
  algorithm: string
}

interface Props {
  stats?: CompressionStats
}

export function CompressionMeter({
  stats = {
    rawBytes: 8465,
    compressedBytes: 1536,
    compressionRatio: 5.51,
    spaceSavingPercent: 81.85,
    rawEntropy: 4.8987,
    compressedEntropy: 7.684,
    algorithm: "Pure LZ77 (32KB Window) + Canonical Huffman",
  },
}: Props) {
  return (
    <Card className="bg-slate-900/60 border-slate-800">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-base text-white flex items-center gap-2">
            <Cpu className="w-4 h-4 text-cyan-400" /> Compression Engine Metrik (Modul 1, 2, 4, 6)
          </CardTitle>
          <Badge variant="success" className="text-[11px]">
            <CheckCircle2 className="w-3 h-3 mr-1" /> Lossless (BER = 0.00%)
          </Badge>
        </div>
        <CardDescription className="text-xs text-slate-400">
          Algoritma Hibrida: LZ77 Sliding Window + Canonical Huffman Coding
        </CardDescription>
      </CardHeader>

      <CardContent className="space-y-4">
        {/* Space Saving Progress Bar */}
        <div className="space-y-1.5">
          <div className="flex justify-between items-center text-xs">
            <span className="text-slate-400">Penghematan Ruang Penyimpanan (Space Saving)</span>
            <span className="text-cyan-400 font-bold text-sm">{stats.spaceSavingPercent}%</span>
          </div>
          <Progress value={stats.spaceSavingPercent} className="h-2.5 bg-slate-800" />
        </div>

        {/* Statistical Table */}
        <Table>
          <TableHeader>
            <TableRow className="border-slate-800 hover:bg-transparent">
              <TableHead className="text-slate-400 text-xs">Parameter</TableHead>
              <TableHead className="text-slate-400 text-xs">Data Mentah (Raw)</TableHead>
              <TableHead className="text-slate-400 text-xs">Hasil Kompresi</TableHead>
              <TableHead className="text-slate-400 text-xs text-right">Efisiensi</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody className="text-xs">
            <TableRow className="border-slate-800/60">
              <TableCell className="font-medium text-slate-300">Ukuran Berkas</TableCell>
              <TableCell className="text-slate-400 font-mono">{stats.rawBytes.toLocaleString()} Byte</TableCell>
              <TableCell className="text-cyan-400 font-mono">{stats.compressedBytes.toLocaleString()} Byte</TableCell>
              <TableCell className="text-right text-emerald-400 font-bold">Rasio {stats.compressionRatio}:1</TableCell>
            </TableRow>
            <TableRow className="border-slate-800/60">
              <TableCell className="font-medium text-slate-300">Shannon Entropy</TableCell>
              <TableCell className="text-slate-400 font-mono">{stats.rawEntropy} bit/B</TableCell>
              <TableCell className="text-cyan-400 font-mono">{stats.compressedEntropy} bit/B</TableCell>
              <TableCell className="text-right text-slate-400">Max teoritis: 8.0</TableCell>
            </TableRow>
            <TableRow className="border-slate-800/60">
              <TableCell className="font-medium text-slate-300">Struktur Kamus</TableCell>
              <TableCell className="text-slate-400">Sliding Window 32 KB</TableCell>
              <TableCell className="text-cyan-400">Canonical Bit-Lengths</TableCell>
              <TableCell className="text-right text-emerald-400">Prefix-Free</TableCell>
            </TableRow>
          </TableBody>
        </Table>

        <div className="rounded-lg bg-cyan-950/20 border border-cyan-500/20 p-2.5 flex items-center gap-2 text-xs text-cyan-300">
          <Zap className="w-4 h-4 text-cyan-400 shrink-0" />
          <span>
            <strong>Inspeksi Akademik:</strong> Tokenisasi LZ77 memangkas redundansi pola kata berulang, disusul Canonical Huffman yang mengoptimalkan panjang bit simbol frekuensi tinggi secara deterministik.
          </span>
        </div>
      </CardContent>
    </Card>
  )
}

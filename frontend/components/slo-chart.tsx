'use client';
import { LineChart, Line, ResponsiveContainer, Tooltip, XAxis, YAxis, CartesianGrid } from "recharts";
import { Card } from "@/components/ui/card";

const data = [
  { name: "T-30m", latency: 210, error: 0.002 },
  { name: "T-20m", latency: 190, error: 0.0018 },
  { name: "T-10m", latency: 180, error: 0.0015 },
  { name: "Now", latency: 175, error: 0.0013 },
];

export function SLOChart() {
  return (
    <Card className="mt-3 p-3">
      <div className="text-sm text-muted-foreground mb-2">Latency p95 & error rate</div>
      <div className="h-48">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
            <XAxis dataKey="name" stroke="#9ca3af" />
            <YAxis yAxisId="left" stroke="#22d3ee" />
            <YAxis yAxisId="right" orientation="right" stroke="#a855f7" />
            <Tooltip contentStyle={{ background: "#0b1220", border: "1px solid #1f2937" }} />
            <Line yAxisId="left" type="monotone" dataKey="latency" stroke="#22d3ee" dot={false} />
            <Line yAxisId="right" type="monotone" dataKey="error" stroke="#a855f7" dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}

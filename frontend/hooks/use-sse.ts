import { useEffect } from "react";

export function useSSE(path: string, onMessage: (data: any) => void) {
  useEffect(() => {
    const url = `${process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000"}${path}`;
    const es = new EventSource(url);
    es.onmessage = (event) => {
      try {
        const parsed = JSON.parse(event.data);
        onMessage(parsed);
      } catch {
        onMessage(event.data);
      }
    };
    return () => es.close();
  }, [path, onMessage]);
}

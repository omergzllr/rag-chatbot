import { NextRequest, NextResponse } from "next/server";

const API_URL = process.env.PYTHON_API_URL ?? "http://localhost:8000";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const response = await fetch(`${API_URL}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: body.question })
    });

    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    return NextResponse.json(
      { error: "Demo servisine baglanirken hata olustu", details: String(error) },
      { status: 500 }
    );
  }
}

import { NextResponse } from "next/server";

const API_URL = process.env.PYTHON_API_URL ?? "http://localhost:8000";

export async function GET(_req: Request, { params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params;
    const response = await fetch(`${API_URL}/api/citizen/session/${id}`);
    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    return NextResponse.json(
      { error: "Vatandas oturumu alinamadi", details: String(error) },
      { status: 500 }
    );
  }
}


import { NextResponse } from "next/server";

const API_URL = process.env.PYTHON_API_URL ?? "http://localhost:8000";

export async function GET() {
  try {
    const response = await fetch(`${API_URL}/api/citizen/doc-types`);
    const data = await response.json();
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    return NextResponse.json(
      { error: "Vatandas dokuman turleri alinamadi", details: String(error) },
      { status: 500 }
    );
  }
}


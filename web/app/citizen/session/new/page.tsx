import NewSessionClient from "./new-session-client";

type NewCitizenSessionPageProps = {
  searchParams?: Promise<{ docType?: string }>;
};

export default async function NewCitizenSessionPage({ searchParams }: NewCitizenSessionPageProps) {
  const resolved = (await searchParams) ?? {};
  const docType = resolved.docType ?? "";
  return <NewSessionClient docType={docType} />;
}


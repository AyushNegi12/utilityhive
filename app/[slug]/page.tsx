import { createClient } from "@supabase/supabase-js";
import { notFound } from "next/navigation";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

export default async function Page({ params }: { params: { slug: string } }) {
  const { data } = await supabase
    .from("pages")
    .select("*")
    .eq("slug", params.slug)
    .single();

  if (!data) return notFound();

  return (
    <main style={{ maxWidth: 800, margin: "0 auto", padding: "40px 20px", fontFamily: "Georgia, serif" }}>
      <h1 style={{ fontSize: 32, marginBottom: 16 }}>{data.title}</h1>
      <div dangerouslySetInnerHTML={{ __html: data.content_html }} />
    </main>
  );
}

export async function generateStaticParams() {
  const { data } = await supabase
    .from("pages")
    .select("slug")
    .eq("status", "live");
  return (data || []).map((p) => ({ slug: p.slug }));
}
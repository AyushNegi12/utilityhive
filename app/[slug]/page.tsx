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
    <>
      <style>{`
        body { margin: 0; background: #f9fafb; font-family: 'Georgia', serif; color: #1a1a1a; }
        .wrap { max-width: 780px; margin: 0 auto; padding: 40px 20px 80px; }
        h1 { font-size: 2rem; font-weight: 800; line-height: 1.25; margin-bottom: 12px; color: #111; }
        h2 { font-size: 1.35rem; font-weight: 700; margin: 32px 0 12px; color: #222; border-left: 4px solid #2563eb; padding-left: 12px; }
        p { line-height: 1.85; font-size: 1.05rem; margin-bottom: 16px; color: #374151; }
        ul { padding-left: 20px; margin-bottom: 16px; }
        li { line-height: 1.8; margin-bottom: 6px; color: #374151; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; font-family: sans-serif; font-size: 0.95rem; }
        th { background: #2563eb; color: white; padding: 10px 14px; text-align: left; }
        td { padding: 9px 14px; border-bottom: 1px solid #e5e7eb; }
        tr:hover td { background: #f0f7ff; }
        details { border: 1px solid #e5e7eb; border-radius: 8px; padding: 12px 16px; margin-bottom: 10px; background: white; }
        summary { font-weight: 600; cursor: pointer; font-family: sans-serif; font-size: 0.97rem; color: #1e40af; }
        details p { margin: 10px 0 0; font-size: 0.95rem; color: #4b5563; }
        .meta { font-family: sans-serif; font-size: 0.88rem; color: #6b7280; margin-bottom: 28px; }
        .tag { background: #dbeafe; color: #1d4ed8; padding: 3px 10px; border-radius: 20px; font-size: 0.82rem; font-weight: 600; margin-right: 6px; }
        .original-data { background: white; border: 1px solid #e5e7eb; border-radius: 10px; padding: 16px; margin: 20px 0; overflow-x: auto; }
      `}</style>
      <div className="wrap">
        <div className="meta">
          <span className="tag">{data.niche?.toUpperCase()}</span>
          <span>{data.word_count} words</span>
          <span style={{margin:"0 8px"}}>·</span>
          <span>{new Date(data.created_at).toLocaleDateString("en-US", {month:"long", day:"numeric", year:"numeric"})}</span>
        </div>
        <div dangerouslySetInnerHTML={{ __html: data.content_html }} />
      </div>
    </>
  );
}

export async function generateStaticParams() {
  const { data } = await supabase
    .from("pages")
    .select("slug")
    .eq("status", "live");
  return (data || []).map((p: any) => ({ slug: p.slug }));
}
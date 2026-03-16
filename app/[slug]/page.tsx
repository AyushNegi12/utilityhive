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

  const nicheColors: Record<string, string> = {
    gaming:  "#f97316",
    tools:   "#06b6d4",
    finance: "#10b981",
    health:  "#ec4899",
  };
  const accent = nicheColors[data.niche] || "#6366f1";

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=Source+Serif+4:ital,wght@0,400;0,600;1,400&display=swap');
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        :root { --accent: ${accent}; --bg: #fafaf9; --text: #1c1917; --muted: #78716c; --border: #e7e5e4; --card: #ffffff; }
        html { scroll-behavior: smooth; }
        body { background: var(--bg); color: var(--text); font-family: 'Source Serif 4', Georgia, serif; line-height: 1.7; }
        .nav { position: sticky; top: 0; z-index: 50; background: rgba(250,250,249,0.92); backdrop-filter: blur(12px); border-bottom: 1px solid var(--border); padding: 0 24px; height: 56px; display: flex; align-items: center; justify-content: space-between; }
        .nav-logo { font-family: 'Sora', sans-serif; font-weight: 800; font-size: 1.1rem; color: var(--text); text-decoration: none; display: flex; align-items: center; gap: 8px; }
        .nav-logo span { background: var(--accent); color: white; width: 28px; height: 28px; border-radius: 7px; display: inline-flex; align-items: center; justify-content: center; font-size: 0.75rem; }
        .nav-tag { background: color-mix(in srgb, var(--accent) 12%, transparent); color: var(--accent); padding: 4px 12px; border-radius: 20px; font-family: 'Sora', sans-serif; font-size: 0.78rem; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase; }
        .hero { padding: 56px 24px 40px; max-width: 800px; margin: 0 auto; }
        .hero-badge { display: inline-flex; align-items: center; gap: 6px; background: color-mix(in srgb, var(--accent) 10%, transparent); border: 1px solid color-mix(in srgb, var(--accent) 25%, transparent); color: var(--accent); padding: 5px 14px; border-radius: 20px; font-family: 'Sora', sans-serif; font-size: 0.78rem; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 20px; }
        .hero-badge::before { content: ''; width: 6px; height: 6px; background: var(--accent); border-radius: 50%; }
        .hero h1 { font-family: 'Sora', sans-serif; font-size: clamp(1.75rem, 4vw, 2.6rem); font-weight: 800; line-height: 1.2; color: var(--text); margin-bottom: 16px; letter-spacing: -0.5px; }
        .hero-meta { display: flex; align-items: center; gap: 16px; flex-wrap: wrap; font-family: 'Sora', sans-serif; font-size: 0.85rem; color: var(--muted); padding-top: 16px; border-top: 1px solid var(--border); }
        .content { max-width: 800px; margin: 0 auto; padding: 0 24px 80px; }
        .content h2 { font-family: 'Sora', sans-serif; font-size: 1.3rem; font-weight: 700; color: var(--text); margin: 44px 0 14px; padding-left: 14px; border-left: 3px solid var(--accent); letter-spacing: -0.3px; }
        .content p { font-size: 1.05rem; line-height: 1.85; color: #44403c; margin-bottom: 18px; }
        .content ul { padding-left: 0; margin-bottom: 20px; list-style: none; }
        .content li { padding: 8px 0 8px 24px; position: relative; color: #44403c; font-size: 1rem; border-bottom: 1px solid #f5f5f4; }
        .content li::before { content: '→'; position: absolute; left: 0; color: var(--accent); font-weight: 700; }
        .original-data { margin: 28px 0; border-radius: 14px; overflow: hidden; border: 1px solid var(--border); box-shadow: 0 4px 24px rgba(0,0,0,0.06); }
        table { width: 100%; border-collapse: collapse; font-family: 'Sora', sans-serif; font-size: 0.9rem; }
        thead tr { background: var(--accent); }
        th { color: white; padding: 13px 16px; text-align: left; font-weight: 600; font-size: 0.82rem; letter-spacing: 0.5px; text-transform: uppercase; }
        td { padding: 12px 16px; border-bottom: 1px solid var(--border); color: #44403c; }
        tbody tr:last-child td { border-bottom: none; }
        tbody tr:hover td { background: color-mix(in srgb, var(--accent) 4%, transparent); }
        tbody tr:nth-child(even) { background: #fafaf9; }
        details { background: var(--card); border: 1px solid var(--border); border-radius: 10px; margin-bottom: 10px; overflow: hidden; }
        details[open] { border-color: color-mix(in srgb, var(--accent) 40%, transparent); }
        summary { padding: 16px 20px; font-family: 'Sora', sans-serif; font-weight: 600; font-size: 0.95rem; cursor: pointer; list-style: none; display: flex; justify-content: space-between; align-items: center; color: var(--text); }
        summary::-webkit-details-marker { display: none; }
        summary::after { content: '+'; font-size: 1.2rem; color: var(--accent); font-weight: 300; }
        details[open] summary::after { content: '−'; }
        details p { padding: 0 20px 16px; font-size: 0.95rem; color: #78716c; line-height: 1.75; }
        .cta-box { background: color-mix(in srgb, var(--accent) 6%, white); border: 1px solid color-mix(in srgb, var(--accent) 20%, transparent); border-radius: 16px; padding: 32px; margin: 44px 0 0; text-align: center; }
        .cta-box p { font-family: 'Sora', sans-serif; font-size: 1rem; color: var(--muted); margin: 0; }
        footer { border-top: 1px solid var(--border); padding: 28px 24px; text-align: center; font-family: 'Sora', sans-serif; font-size: 0.82rem; color: var(--muted); }
        @media (max-width: 640px) { .hero { padding: 32px 16px 28px; } .content { padding: 0 16px 60px; } .hero h1 { font-size: 1.6rem; } }
      `}</style>

      <nav className="nav">
        <a href="/" className="nav-logo"><span>U</span> UtilityHive</a>
        <span className="nav-tag">{data.niche}</span>
      </nav>

      <div className="hero">
        <div className="hero-badge">{data.niche}</div>
        <h1>{data.title}</h1>
        <div className="hero-meta">
          <span>📄 {data.word_count} words</span>
          <span>🕒 {Math.ceil(data.word_count / 200)} min read</span>
          <span>📅 {new Date(data.created_at).toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" })}</span>
        </div>
      </div>

      <div className="content">
        <div dangerouslySetInnerHTML={{ __html: data.content_html }} />
        <div className="cta-box">
          <p>⭐ Found this helpful? Bookmark UtilityHive for more free guides, calculators and tools.</p>
        </div>
      </div>

      <footer>© {new Date().getFullYear()} UtilityHive · Free tools and guides for everyone</footer>
    </>
  );
}

export async function generateStaticParams() {
  const { data } = await supabase.from("pages").select("slug").eq("status", "live");
  return (data || []).map((p: any) => ({ slug: p.slug }));
}
// pages/[slug].tsx
// Next.js SSG — pre-renders every page from Supabase at build time
// Deploy to Vercel FREE tier — edge CDN, global, instant

import type { GetStaticPaths, GetStaticProps } from "next";
import Head from "next/head";
import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

interface Page {
  keyword:      string;
  slug:         string;
  title:        string;
  meta_desc:    string;
  content_html: string;
  niche:        string;
}

export const getStaticPaths: GetStaticPaths = async () => {
  const { data } = await supabase
    .from("pages")
    .select("slug")
    .eq("status", "live");   // Only published pages

  return {
    paths: (data || []).map(p => ({ params: { slug: p.slug } })),
    fallback: "blocking",    // New pages generate on first visit
  };
};

export const getStaticProps: GetStaticProps = async ({ params }) => {
  const { data, error } = await supabase
    .from("pages")
    .select("*")
    .eq("slug", params?.slug as string)
    .single();

  if (error || !data) return { notFound: true };

  return {
    props: { page: data },
    revalidate: 3600,   // ISR: revalidate every hour
  };
};

export default function UtilityPage({ page }: { page: Page }) {
  return (
    <>
      <Head>
        <title>{page.title} | UtilityHive</title>
        <meta name="description" content={page.meta_desc} />
        <meta property="og:title" content={page.title} />
        <meta property="og:description" content={page.meta_desc} />
        <link rel="canonical" href={`https://yourdomain.com/${page.slug}`} />
      </Head>

      <main className="max-w-3xl mx-auto px-4 py-8">
        {/* AdSense — Top */}
        <ins
          className="adsbygoogle"
          style={{ display: "block" }}
          data-ad-client="ca-pub-XXXXXXXXXX"
          data-ad-slot="XXXXXXXXXX"
          data-ad-format="auto"
        />

        {/* Page Content */}
        <article
          className="prose prose-lg max-w-none"
          dangerouslySetInnerHTML={{ __html: page.content_html }}
        />

        {/* AdSense — Bottom */}
        <ins
          className="adsbygoogle"
          style={{ display: "block" }}
          data-ad-client="ca-pub-XXXXXXXXXX"
          data-ad-slot="XXXXXXXXXX"
          data-ad-format="auto"
        />
      </main>
    </>
  );
}

# Research Brief — Sample

> This is a format sample showing how I structure source-cited research deliverables.
> Every claim is tied to a citation slot; nothing is asserted without a source.

## Question
*Example:* "Is server-side rendering (SSR) or static generation better for SEO on a content site in 2025?"

## Bottom line (1 paragraph)
For a content-heavy site where pages change infrequently, static generation with
incremental revalidation gives the best crawl reliability and Core Web Vitals, while
SSR is preferable when content is highly personalized or updated per-request. The
SEO difference is driven less by the rendering mode itself than by how fast and
consistently crawlable HTML is served [1][2].

## Evidence
| Claim | Source type | Citation |
|-------|-------------|----------|
| Googlebot renders JS but with a crawl-budget cost; pre-rendered HTML is indexed faster | Official docs | [1] |
| Core Web Vitals are a ranking signal; TTFB/LCP favor cached static output | Official docs | [2] |
| Incremental Static Regeneration keeps static pages fresh without full rebuilds | Framework docs | [3] |

## Method
- Scope limited to public, primary sources (search-engine documentation, framework docs).
- Each claim mapped to exactly one citation; secondary blogs used only for corroboration.
- Conflicting guidance flagged explicitly rather than averaged.

## Citations
1. Google Search Central — JavaScript SEO basics. (official documentation URL)
2. Google Search Central — Core Web Vitals & page experience. (official documentation URL)
3. Next.js Docs — Incremental Static Regeneration. (framework documentation URL)

*(In a real delivery, citation slots contain live URLs and access dates.)*

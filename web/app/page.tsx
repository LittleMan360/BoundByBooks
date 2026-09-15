"use client";

import { FormEvent, useState } from "react";

type Edition = {
  isbn: string;
  title: string;
  authors: string[];
  publisher?: string | null;
  publication_date?: string | null;
  page_count?: number | null;
  cover_url?: string | null;
  source: string;
};

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export default function Home() {
  const [isbn, setIsbn] = useState("");
  const [edition, setEdition] = useState<Edition | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function findBook(event: FormEvent) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setEdition(null);

    try {
      const response = await fetch(`${API_URL}/api/books/isbn/${encodeURIComponent(isbn)}`);
      if (!response.ok) throw new Error(response.status === 404 ? "We couldn't find that edition." : "ISBN lookup failed.");
      setEdition(await response.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main>
      <nav className="nav">
        <div className="brand">Bound By Books</div>
        <div className="navLinks"><span>Library</span><span>Shelves</span><span>Statistics</span><span>Wishlist</span></div>
      </nav>

      <section className="hero">
        <p className="eyebrow">YOUR BOOKS. YOUR EDITIONS. YOUR LIBRARY.</p>
        <h1>A digital home for your <em>physical</em> book collection.</h1>
        <p className="lede">Identify the edition you own, build your virtual shelves, and eventually understand what your collection is worth.</p>

        <form className="search" onSubmit={findBook}>
          <input value={isbn} onChange={(e) => setIsbn(e.target.value)} placeholder="Enter an ISBN — e.g. 9780140328721" aria-label="ISBN" />
          <button disabled={loading}>{loading ? "Finding…" : "Find my edition"}</button>
        </form>
        <p className="hint">Barcode camera scanning comes next. ISBN entry lets us prove edition matching first.</p>
      </section>

      {error && <section className="result error">{error}</section>}

      {edition && (
        <section className="result bookResult">
          {edition.cover_url ? <img src={edition.cover_url} alt={`Cover of ${edition.title}`} /> : <div className="coverPlaceholder">No cover</div>}
          <div>
            <p className="eyebrow">EDITION FOUND</p>
            <h2>{edition.title}</h2>
            <p className="author">{edition.authors.join(", ") || "Unknown author"}</p>
            <dl>
              <div><dt>ISBN</dt><dd>{edition.isbn}</dd></div>
              <div><dt>Publisher</dt><dd>{edition.publisher || "Unknown"}</dd></div>
              <div><dt>Published</dt><dd>{edition.publication_date || "Unknown"}</dd></div>
              <div><dt>Pages</dt><dd>{edition.page_count ?? "Unknown"}</dd></div>
            </dl>
            <button className="secondary" disabled>Add to my library — coming next</button>
          </div>
        </section>
      )}

      <section className="features">
        <article><strong>01</strong><h3>Exact editions</h3><p>Track the physical version you actually own, not just a generic title.</p></article>
        <article><strong>02</strong><h3>Virtual shelves</h3><p>Organize your collection visually and arrange books the way you want.</p></article>
        <article><strong>03</strong><h3>Collection value</h3><p>Build toward transparent market estimates and collection-level statistics.</p></article>
      </section>
    </main>
  );
}

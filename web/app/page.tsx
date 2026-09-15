"use client";

import { FormEvent, useEffect, useState } from "react";

type Edition = {
  isbn: string; title: string; authors: string[]; publisher?: string | null;
  publication_date?: string | null; page_count?: number | null; cover_url?: string | null; source: string;
};

type LibraryCopy = {
  id: number; isbn: string; title: string; authors: string[]; publisher?: string | null;
  publication_date?: string | null; cover_url?: string | null; condition?: string | null;
};

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export default function Home() {
  const [isbn, setIsbn] = useState("");
  const [edition, setEdition] = useState<Edition | null>(null);
  const [library, setLibrary] = useState<LibraryCopy[]>([]);
  const [condition, setCondition] = useState("Good");
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [adding, setAdding] = useState(false);

  async function loadLibrary() {
    try {
      const response = await fetch(`${API_URL}/api/library`);
      if (response.ok) setLibrary(await response.json());
    } catch { /* API may not be running yet. */ }
  }

  useEffect(() => { void loadLibrary(); }, []);

  async function findBook(event: FormEvent) {
    event.preventDefault(); setLoading(true); setError(""); setMessage(""); setEdition(null);
    try {
      const response = await fetch(`${API_URL}/api/books/isbn/${encodeURIComponent(isbn)}`);
      if (!response.ok) throw new Error(response.status === 404 ? "We couldn't find that edition." : "ISBN lookup failed.");
      setEdition(await response.json());
    } catch (err) { setError(err instanceof Error ? err.message : "Something went wrong."); }
    finally { setLoading(false); }
  }

  async function addToLibrary() {
    if (!edition) return;
    setAdding(true); setError(""); setMessage("");
    try {
      const response = await fetch(`${API_URL}/api/library`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ isbn: edition.isbn, condition }),
      });
      if (!response.ok) throw new Error("We couldn't add this copy to your library.");
      setMessage("Added to your library.");
      await loadLibrary();
    } catch (err) { setError(err instanceof Error ? err.message : "Something went wrong."); }
    finally { setAdding(false); }
  }

  return (
    <main>
      <nav className="nav"><div className="brand">Bound By Books</div><div className="navLinks"><span>Library</span><span>Shelves</span><span>Statistics</span><span>Wishlist</span></div></nav>
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
      {message && <section className="result success">{message}</section>}

      {edition && <section className="result bookResult">
        {edition.cover_url ? <img src={edition.cover_url} alt={`Cover of ${edition.title}`} /> : <div className="coverPlaceholder">No cover</div>}
        <div><p className="eyebrow">EDITION FOUND</p><h2>{edition.title}</h2><p className="author">{edition.authors.join(", ") || "Unknown author"}</p>
          <dl><div><dt>ISBN</dt><dd>{edition.isbn}</dd></div><div><dt>Publisher</dt><dd>{edition.publisher || "Unknown"}</dd></div><div><dt>Published</dt><dd>{edition.publication_date || "Unknown"}</dd></div><div><dt>Pages</dt><dd>{edition.page_count ?? "Unknown"}</dd></div></dl>
          <div className="addRow"><select value={condition} onChange={(e) => setCondition(e.target.value)}><option>New</option><option>Like New</option><option>Very Good</option><option>Good</option><option>Acceptable</option></select><button className="secondary" onClick={addToLibrary} disabled={adding}>{adding ? "Adding…" : "Add to my library"}</button></div>
        </div>
      </section>}

      <section className="librarySection">
        <p className="eyebrow">MY LIBRARY</p><h2>{library.length ? `${library.length} ${library.length === 1 ? "book" : "books"}` : "Your shelves start here."}</h2>
        {library.length === 0 ? <p className="emptyLibrary">Find your first ISBN above and add the exact edition you own.</p> : <div className="bookGrid">{library.map((copy) => <article className="libraryCard" key={copy.id}>{copy.cover_url ? <img src={copy.cover_url} alt={copy.title} /> : <div className="cardPlaceholder" />}<h3>{copy.title}</h3><p>{copy.authors.join(", ")}</p><small>{copy.condition || "Condition not set"}</small></article>)}</div>}
      </section>

      <section className="features"><article><strong>01</strong><h3>Exact editions</h3><p>Track the physical version you actually own, not just a generic title.</p></article><article><strong>02</strong><h3>Virtual shelves</h3><p>Organize your collection visually and arrange books the way you want.</p></article><article><strong>03</strong><h3>Collection value</h3><p>Build toward transparent market estimates and collection-level statistics.</p></article></section>
    </main>
  );
}

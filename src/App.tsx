import { ChangeEvent, useMemo, useRef, useState } from 'react';
import { BookOpen, FilePlus2, GitPullRequest, Search, Trash2, UploadCloud, Users } from 'lucide-react';
import { knowledgeSources, type CancerType, type EvidenceSource } from './data/knowledgeSources';
import { useKnowledgeBase, type GuidelineDocument } from './hooks/useKnowledgeBase';
import './styles/app.css';

const formatDate = (date: Date) =>
  date.toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });

function PlaceholderLogo() {
  return (
    <div className="logo">
      <div className="logo-mark">K</div>
      <span>Karkinos</span>
    </div>
  );
}

const navItems = [
  { id: 'intelligence', label: 'Intelligence', icon: <BookOpen size={18} /> },
  { id: 'tumor-board', label: 'Tumor Board', icon: <Users size={18} /> },
  { id: 'trial-matching', label: 'Trial Matching', icon: <GitPullRequest size={18} /> }
];

const App = () => {
  const [activeSource, setActiveSource] = useState<EvidenceSource>(knowledgeSources[0]);
  const [selectedCancer, setSelectedCancer] = useState<CancerType | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const uploadInputRef = useRef<HTMLInputElement>(null);
  const { addDocument, getDocuments, removeDocument } = useKnowledgeBase();

  const filteredSources = useMemo(() => {
    if (!searchQuery.trim()) {
      return knowledgeSources;
    }

    const query = searchQuery.toLowerCase();
    return knowledgeSources.filter((source) => {
      const inSource = source.name.toLowerCase().includes(query) || source.description.toLowerCase().includes(query);
      const inCancer = source.cancers.some((cancer) => cancer.name.toLowerCase().includes(query));
      return inSource || inCancer;
    });
  }, [searchQuery]);

  const handleSelectSource = (source: EvidenceSource) => {
    setActiveSource(source);
    setSelectedCancer(null);
  };

  const handleSelectCancer = (cancer: CancerType) => {
    setSelectedCancer(cancer);
  };

  const handleUploadClick = () => {
    uploadInputRef.current?.click();
  };

  const handleFileUpload = (event: ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (!files || !activeSource || !selectedCancer) return;

    Array.from(files).forEach((file) => {
      const document: GuidelineDocument = {
        id: `${file.name}-${Date.now()}`,
        name: file.name,
        size: file.size,
        origin: 'upload',
        uploadedAt: formatDate(new Date())
      };

      addDocument(activeSource, selectedCancer, document);
    });

    event.target.value = '';
  };

  const handleMockApiIngest = () => {
    if (!activeSource || !selectedCancer) return;

    const document: GuidelineDocument = {
      id: `api-${Date.now()}`,
      name: `${selectedCancer.name} – Latest literature bundle`,
      origin: 'api',
      uploadedAt: formatDate(new Date()),
      notes: 'Simulated sync via PubMed Central API.'
    };

    addDocument(activeSource, selectedCancer, document);
  };

  const activeDocuments = useMemo(() => {
    if (!activeSource || !selectedCancer) return [];
    return getDocuments(activeSource.id, selectedCancer.id);
  }, [activeSource, selectedCancer, getDocuments]);

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <PlaceholderLogo />
        <nav className="nav-section">
          <h2>Navigation</h2>
          <div style={{ display: 'grid', gap: '0.5rem' }}>
            {navItems.map((item) => (
              <div
                key={item.id}
                className={`nav-item ${item.id === 'intelligence' ? 'active' : ''}`}
                aria-current={item.id === 'intelligence' ? 'page' : undefined}
              >
                {item.icon}
                {item.label}
              </div>
            ))}
          </div>
        </nav>
      </aside>
      <main className="main-panel">
        <header className="panel-header">
          <div>
            <div className="badge">Knowledge Base</div>
            <h1 style={{ margin: '0.35rem 0 0', fontSize: '2rem' }}>Curate oncology evidence in one place</h1>
          </div>
          <label style={{ position: 'relative', display: 'inline-flex', alignItems: 'center', gap: '0.5rem' }}>
            <Search size={18} color="#ff6b2c" />
            <input
              className="search-input"
              placeholder="Search sources or cancer types"
              value={searchQuery}
              onChange={(event) => setSearchQuery(event.target.value)}
            />
          </label>
        </header>

        <section>
          <h2 style={{ margin: '0 0 1rem' }}>Evidence sources</h2>
          <div className="source-grid">
            {filteredSources.map((source) => (
              <article
                key={source.id}
                className={`source-card ${activeSource.id === source.id ? 'active' : ''}`}
                style={{ borderColor: `${source.accent}20` }}
                onClick={() => handleSelectSource(source)}
              >
                <div className="badge" style={{ background: `${source.accent}26`, color: source.accent }}>
                  {source.cancers.length} cancer types
                </div>
                <div>
                  <h3>{source.name}</h3>
                  <p>{source.description}</p>
                </div>
                <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                  {source.cancers.slice(0, 3).map((cancer) => (
                    <span key={cancer.id} className="badge" style={{ background: `${source.accent}1a`, color: source.accent }}>
                      {cancer.name}
                    </span>
                  ))}
                </div>
              </article>
            ))}
          </div>
        </section>

        <section className="cancer-panel" aria-live="polite">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '1rem' }}>
            <div>
              <h2 style={{ margin: 0 }}>{activeSource.name} cancer libraries</h2>
              <p style={{ margin: '0.35rem 0 0', color: 'rgba(15, 23, 42, 0.6)' }}>{activeSource.description}</p>
            </div>
          </div>
          <div className="cancer-list">
            {activeSource.cancers.map((cancer) => (
              <button
                key={cancer.id}
                className={`cancer-chip ${selectedCancer?.id === cancer.id ? 'active' : ''}`}
                onClick={() => handleSelectCancer(cancer)}
              >
                <h4>{cancer.name}</h4>
                <p>{cancer.summary}</p>
                {cancer.supportApi && (
                  <span className="badge" style={{ marginTop: '0.75rem' }}>
                    API sync available
                  </span>
                )}
              </button>
            ))}
          </div>

          {selectedCancer ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
              <div className="guideline-toolbar">
                <div>
                  <h3 style={{ margin: 0 }}>{selectedCancer.name} knowledge workspace</h3>
                  <p style={{ margin: '0.35rem 0 0', color: 'rgba(15, 23, 42, 0.6)' }}>
                    Upload internal PDFs or pull structured data from trusted APIs.
                  </p>
                </div>
                <div style={{ display: 'flex', gap: '0.75rem' }}>
                  <button className="primary-button" onClick={handleUploadClick}>
                    <UploadCloud size={18} style={{ marginRight: '0.5rem' }} /> Upload guidelines
                  </button>
                  {selectedCancer.supportApi && (
                    <button className="secondary-button" onClick={handleMockApiIngest}>
                      <FilePlus2 size={18} style={{ marginRight: '0.5rem' }} /> Sync via API
                    </button>
                  )}
                </div>
                <input
                  ref={uploadInputRef}
                  type="file"
                  multiple
                  hidden
                  accept=".pdf,.doc,.docx,.txt"
                  onChange={handleFileUpload}
                />
              </div>

              {activeDocuments.length ? (
                <div className="guideline-list" role="list">
                  {activeDocuments.map((document) => (
                    <div key={document.id} className="guideline-row" role="listitem">
                      <div>
                        <strong>{document.name}</strong>
                        {document.notes && (
                          <p style={{ margin: '0.35rem 0 0', color: 'rgba(15, 23, 42, 0.6)', fontSize: '0.85rem' }}>
                            {document.notes}
                          </p>
                        )}
                      </div>
                      <div style={{ color: 'rgba(15, 23, 42, 0.6)', fontSize: '0.85rem' }}>{document.uploadedAt}</div>
                      <div style={{ color: document.origin === 'upload' ? '#ff6b2c' : '#1d4ed8', fontWeight: 600 }}>
                        {document.origin === 'upload' ? 'Manual upload' : 'API capture'}
                      </div>
                      <button
                        className="secondary-button"
                        style={{ padding: '0.5rem', borderRadius: '0.75rem' }}
                        onClick={() => removeDocument(activeSource, selectedCancer, document.id)}
                        aria-label={`Remove ${document.name}`}
                      >
                        <Trash2 size={18} />
                      </button>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="empty-state">
                  No guidelines stored yet. Upload documents or sync using the available APIs to populate this workspace.
                </div>
              )}
            </div>
          ) : (
            <div className="empty-state">Select a cancer library to view and manage evidence assets.</div>
          )}
        </section>
      </main>
    </div>
  );
};

export default App;

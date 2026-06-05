import { motion } from 'framer-motion'
import { HeroScene } from './components/HeroScene'
import { DonutChart3D } from './components/DonutChart3D'
import { ToolsChart3D } from './components/ToolsChart3D'
import './App.css'

const fadeUp = {
  hidden: { opacity: 0, y: 28 },
  show: { opacity: 1, y: 0, transition: { duration: 0.6, ease: 'easeOut' } },
}

const stagger = {
  hidden: {},
  show: { transition: { staggerChildren: 0.1 } },
}

// ─── Nav ────────────────────────────────────────────────────────────────────

function Nav() {
  return (
    <nav className="nav">
      <div className="nav-logo">
        <span>KDG</span> × IA 2026
      </div>
      <ul className="nav-links">
        <li><a href="#usage">Synthèse</a></li>
        <li><a href="#tools">Outils</a></li>
        <li><a href="#departments">Pôles</a></li>
        <li><a href="#barriers">Leviers</a></li>
        <li><a href="#plan">Plan</a></li>
      </ul>
      <span className="nav-badge">Confidentiel — Cellule IA</span>
    </nav>
  )
}

// ─── Hero ────────────────────────────────────────────────────────────────────

function HeroSection() {
  return (
    <section className="section" style={{ paddingTop: 0 }}>
      <div className="container">
        <div className="hero">
          <motion.div
            className="hero-content"
            initial="hidden"
            animate="show"
            variants={stagger}
          >
            <motion.div className="hero-tag" variants={fadeUp}>
              Consultation IA · Juin 2026
            </motion.div>
            <motion.h1 className="hero-title" variants={fadeUp}>
              L'IA au cœur<br />du groupe <span className="accent">KDG</span>
            </motion.h1>
            <motion.p className="hero-desc" variants={fadeUp}>
              Synthèse de l'enquête menée auprès de 32 collaborateurs répartis sur
              4 pôles — Abidjan & Cotonou. Usages, outils, freins et plan d'action.
            </motion.p>
            <motion.div className="hero-stats" variants={fadeUp}>
              <div className="hero-stat">
                <span className="hero-stat-num">81%</span>
                <span className="hero-stat-label">utilisent l'IA</span>
              </div>
              <div className="hero-stat" style={{ borderLeft: '1px solid rgba(255,255,255,0.08)', paddingLeft: 32 }}>
                <span className="hero-stat-num">47%</span>
                <span className="hero-stat-label">usage régulier</span>
              </div>
              <div className="hero-stat" style={{ borderLeft: '1px solid rgba(255,255,255,0.08)', paddingLeft: 32 }}>
                <span className="hero-stat-num">32</span>
                <span className="hero-stat-label">répondants</span>
              </div>
            </motion.div>
          </motion.div>

          <motion.div
            className="hero-canvas"
            initial={{ opacity: 0, scale: 0.96 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 1, delay: 0.3 }}
          >
            <HeroScene />
          </motion.div>
        </div>
      </div>
    </section>
  )
}

// ─── Usage ───────────────────────────────────────────────────────────────────

const USAGE = [
  { label: 'Utilisation régulière', count: '15 pers.', pct: '47%', color: '#C9A84C' },
  { label: 'Utilisation occasionnelle', count: '11 pers.', pct: '34%', color: '#3B82F6' },
  { label: 'Essayé mais abandonné', count: '5 pers.', pct: '16%', color: '#8B5CF6' },
  { label: 'Jamais utilisé', count: '1 pers.', pct: '3%', color: '#475569' },
]

function UsageSection() {
  return (
    <section className="section" id="usage" style={{ background: 'linear-gradient(180deg, #080A14 0%, #0F1221 100%)' }}>
      <div className="container">
        <motion.div initial="hidden" whileInView="show" viewport={{ once: true }} variants={stagger}>
          <motion.span className="label" variants={fadeUp}>Maturité IA</motion.span>
          <motion.h2 className="section-title" variants={fadeUp}>
            81% ont déjà adopté<br />l'intelligence artificielle
          </motion.h2>
          <motion.p className="section-sub" variants={fadeUp}>
            Sur 32 répondants, 26 utilisent l'IA à des degrés divers.
            Un seul collaborateur n'a jamais essayé.
          </motion.p>
        </motion.div>

        <div className="usage-grid" style={{ marginTop: 52 }}>
          <motion.div
            className="usage-canvas"
            initial={{ opacity: 0, x: -30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.7 }}
          >
            <DonutChart3D />
          </motion.div>

          <motion.div
            className="usage-legend"
            initial="hidden"
            whileInView="show"
            viewport={{ once: true }}
            variants={stagger}
          >
            {USAGE.map((item) => (
              <motion.div key={item.label} className="legend-item" variants={fadeUp}>
                <div className="legend-dot" style={{ background: item.color }} />
                <div className="legend-info">
                  <div className="legend-label">{item.label}</div>
                  <div className="legend-count">{item.count}</div>
                </div>
                <div className="legend-pct" style={{ color: item.color }}>{item.pct}</div>
              </motion.div>
            ))}

            <motion.div variants={fadeUp} style={{
              marginTop: 8,
              padding: '16px 20px',
              background: 'rgba(201,168,76,0.08)',
              border: '1px solid rgba(201,168,76,0.2)',
              borderRadius: 12,
            }}>
              <div style={{ fontSize: 13, color: '#94A3B8', marginBottom: 6 }}>
                Consensus sur le chatbot chantier
              </div>
              <div style={{ fontSize: 24, fontWeight: 700, color: '#C9A84C', fontFamily: 'Space Grotesk, sans-serif' }}>
                15 / 15 <span style={{ fontSize: 14, opacity: 0.7 }}>membres favorables</span>
              </div>
            </motion.div>
          </motion.div>
        </div>
      </div>
    </section>
  )
}

// ─── Tools ───────────────────────────────────────────────────────────────────

const TOOL_DETAILS = [
  { name: 'ChatGPT', desc: 'Standard — toutes équipes', count: 26, color: '#10A37F' },
  { name: 'Copilot', desc: 'Fort sur le pôle Chantier', count: 13, color: '#0078D4' },
  { name: 'Claude', desc: 'Utilisateurs avancés (rédaction & analyse)', count: 8, color: '#C9A84C' },
  { name: 'Gemini', desc: 'Architecture & Économie', count: 7, color: '#4285F4' },
  { name: 'Autres', desc: 'DeepSeek, NotebookLM, Krea, Rendair…', count: 6, color: '#8B5CF6' },
]

function ToolsSection() {
  return (
    <section className="section" id="tools">
      <div className="container">
        <motion.div initial="hidden" whileInView="show" viewport={{ once: true }} variants={stagger}>
          <motion.span className="label" variants={fadeUp}>Outils utilisés</motion.span>
          <motion.h2 className="section-title" variants={fadeUp}>
            ~10 outils en circulation<br />sans gouvernance
          </motion.h2>
          <motion.p className="section-sub" variants={fadeUp}>
            ChatGPT domine, mais une "Shadow AI" s'est installée sur des comptes
            personnels sans cadre ni validation.
          </motion.p>
        </motion.div>

        <motion.div
          className="tools-canvas"
          initial={{ opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.7 }}
        >
          <ToolsChart3D />
        </motion.div>

        <motion.div
          style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: 16, marginTop: 28 }}
          initial="hidden"
          whileInView="show"
          viewport={{ once: true }}
          variants={stagger}
        >
          {TOOL_DETAILS.map((t) => (
            <motion.div key={t.name} className="card" style={{ padding: '18px 20px' }} variants={fadeUp}>
              <div style={{
                width: 10, height: 10, borderRadius: 3,
                background: t.color, marginBottom: 10
              }} />
              <div style={{ fontWeight: 700, fontSize: 16, marginBottom: 4 }}>{t.name}</div>
              <div style={{ fontSize: 12, color: '#64748B', marginBottom: 10, lineHeight: 1.4 }}>{t.desc}</div>
              <div style={{
                fontSize: 22, fontWeight: 700, color: t.color,
                fontFamily: 'Space Grotesk, sans-serif'
              }}>
                {t.count} <span style={{ fontSize: 13, color: '#64748B', fontWeight: 500 }}>cit.</span>
              </div>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  )
}

// ─── Departments ─────────────────────────────────────────────────────────────

const DEPTS = [
  {
    icon: '🏗️',
    name: 'Architecture Production',
    count: '~10 répondants',
    color: '#C9A84C',
    bg: 'rgba(201,168,76,0.1)',
    items: [
      { label: 'Production visuelle & rendu', score: 4.50 },
      { label: 'Rédaction notices & cahiers des charges', score: 3.80 },
      { label: 'Recherches de références', score: 3.80 },
    ],
  },
  {
    icon: '🏛️',
    name: 'Suivi de Chantier',
    count: '15 répondants',
    color: '#3B82F6',
    bg: 'rgba(59,130,246,0.1)',
    items: [
      { label: 'Capitalisation / apprentissage', score: 3.93 },
      { label: 'Accès & recherche documentaire', score: 3.73 },
      { label: 'Rédaction & diffusion comptes rendus', score: 3.73 },
    ],
  },
  {
    icon: '💰',
    name: 'Économie de la Construction',
    count: '~6 répondants',
    color: '#14B8A6',
    bg: 'rgba(20,184,166,0.1)',
    items: [
      { label: 'Rédaction documents administratifs', score: 4.60 },
      { label: 'Analyse comparative des offres', score: 4.17 },
      { label: 'Structuration DPGF', score: 3.67 },
    ],
  },
  {
    icon: '📐',
    name: 'BIM',
    count: '~4 répondants',
    color: '#8B5CF6',
    bg: 'rgba(139,92,246,0.1)',
    items: [
      { label: 'Vérification réglementaire', score: 3.44 },
      { label: 'Coordination de phase', score: 3.00 },
      { label: 'Mise en page documentaire', score: 3.20 },
    ],
  },
]

function ProgressBar({ score, color }) {
  return (
    <div className="progress-bar">
      <motion.div
        className="progress-fill"
        style={{ background: color }}
        initial={{ width: 0 }}
        whileInView={{ width: `${(score / 5) * 100}%` }}
        viewport={{ once: true }}
        transition={{ duration: 0.9, ease: 'easeOut' }}
      />
    </div>
  )
}

function DepartmentsSection() {
  return (
    <section className="section" id="departments" style={{ background: 'linear-gradient(180deg, #0F1221 0%, #080A14 100%)' }}>
      <div className="container">
        <motion.div initial="hidden" whileInView="show" viewport={{ once: true }} variants={stagger}>
          <motion.span className="label" variants={fadeUp}>Par pôle</motion.span>
          <motion.h2 className="section-title" variants={fadeUp}>
            Utilité de l'IA par département
          </motion.h2>
          <motion.p className="section-sub" variants={fadeUp}>
            Score d'utilité perçue sur 5 — les usages prioritaires par équipe.
          </motion.p>
        </motion.div>

        <motion.div
          className="dept-grid"
          initial="hidden"
          whileInView="show"
          viewport={{ once: true }}
          variants={stagger}
        >
          {DEPTS.map((d) => (
            <motion.div key={d.name} className="card dept-card" variants={fadeUp}>
              <div className="dept-header">
                <div className="dept-icon" style={{ background: d.bg }}>
                  {d.icon}
                </div>
                <div>
                  <div className="dept-name">{d.name}</div>
                  <div className="dept-count">{d.count}</div>
                </div>
              </div>
              <div className="dept-items">
                {d.items.map((item) => (
                  <div key={item.label} className="dept-item">
                    <div className="dept-item-label">
                      <span>{item.label}</span>
                      <span className="dept-item-score" style={{ color: d.color }}>
                        {item.score.toFixed(2)} / 5
                      </span>
                    </div>
                    <ProgressBar score={item.score} color={d.color} />
                  </div>
                ))}
              </div>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  )
}

// ─── Barriers & Enablers ─────────────────────────────────────────────────────

const BARRIERS = [
  { label: 'Aucun frein / prêt à adopter', count: 10 },
  { label: 'Manque de formation', count: 7 },
  { label: 'Confidentialité des données', count: 6 },
  { label: 'Doutes sur la fiabilité', count: 6 },
  { label: 'Manque de temps', count: 4 },
]

const ENABLERS = [
  { label: 'Formation pratique en petits groupes', count: 19 },
  { label: 'Pilote concret sur un projet KDG', count: 8 },
  { label: 'Exemples métier spécifiques', count: 5 },
]

function BarriersSection() {
  return (
    <section className="section" id="barriers">
      <div className="container">
        <motion.div initial="hidden" whileInView="show" viewport={{ once: true }} variants={stagger}>
          <motion.span className="label" variants={fadeUp}>Analyse</motion.span>
          <motion.h2 className="section-title" variants={fadeUp}>
            Freins identifiés &<br />leviers d'action
          </motion.h2>
          <motion.p className="section-sub" variants={fadeUp}>
            La majorité est prête — les obstacles sont structurels, pas culturels.
          </motion.p>
        </motion.div>

        <div className="barriers-grid">
          <motion.div
            initial="hidden"
            whileInView="show"
            viewport={{ once: true }}
            variants={stagger}
          >
            <motion.div className="barrier-col-title" variants={fadeUp}>
              <span style={{ fontSize: 22 }}>⚠️</span>
              <span>Freins perçus</span>
            </motion.div>
            <div className="barrier-items">
              {BARRIERS.map((b) => (
                <motion.div key={b.label} className="barrier-item" variants={fadeUp}>
                  <span style={{ fontSize: 14 }}>{b.label}</span>
                  <span className="barrier-count" style={{
                    background: 'rgba(249,115,22,0.1)',
                    color: '#F97316',
                  }}>
                    {b.count}
                  </span>
                </motion.div>
              ))}
            </div>
          </motion.div>

          <motion.div
            initial="hidden"
            whileInView="show"
            viewport={{ once: true }}
            variants={stagger}
          >
            <motion.div className="barrier-col-title" variants={fadeUp}>
              <span style={{ fontSize: 22 }}>🚀</span>
              <span>Leviers prioritaires</span>
            </motion.div>
            <div className="barrier-items">
              {ENABLERS.map((e) => (
                <motion.div key={e.label} className="barrier-item" variants={fadeUp}>
                  <span style={{ fontSize: 14 }}>{e.label}</span>
                  <span className="barrier-count" style={{
                    background: 'rgba(16,185,129,0.1)',
                    color: '#10B981',
                  }}>
                    {e.count}
                  </span>
                </motion.div>
              ))}
            </div>

            <motion.div variants={fadeUp} style={{
              marginTop: 16,
              padding: '18px 20px',
              background: 'rgba(16,185,129,0.06)',
              border: '1px solid rgba(16,185,129,0.2)',
              borderRadius: 12,
            }}>
              <div style={{ fontSize: 13, color: '#94A3B8', marginBottom: 6 }}>
                Gouvernance demandée par les équipes
              </div>
              <div style={{ fontSize: 14, color: '#E2E8F0', lineHeight: 1.6 }}>
                Charte interne · Outils validés · Sécurité des données · Validation humaine
              </div>
            </motion.div>
          </motion.div>
        </div>
      </div>
    </section>
  )
}

// ─── Action Plan ──────────────────────────────────────────────────────────────

const PHASES = [
  {
    num: '01',
    phase: 'Phase 1 · M1-2',
    title: 'Formation & Gouvernance',
    desc: 'Lancer des sessions pratiques en petits groupes. Établir la charte IA, valider les outils, définir les règles de confidentialité.',
    tags: ['Formation', 'Charte IA', 'Validation outils'],
    color: '#C9A84C',
    bg: 'rgba(201,168,76,0.12)',
    border: 'rgba(201,168,76,0.25)',
    why: 'Priorité n°1 — 19 demandes de formation',
  },
  {
    num: '02',
    phase: 'Phase 2 · M3-4',
    title: 'Pilote Chatbot Chantier',
    desc: 'Déployer un chatbot sur un dossier chantier pilote. Capitaliser les données, tester avec le pôle Suivi (15/15 favorables).',
    tags: ['Chatbot', 'Pilote Chantier', 'Capitalisation'],
    color: '#3B82F6',
    bg: 'rgba(59,130,246,0.12)',
    border: 'rgba(59,130,246,0.25)',
    why: '100% consensus pôle Chantier',
  },
  {
    num: '03',
    phase: 'Phase 3 · M5-6',
    title: 'Déploiement & Mesure',
    desc: "Étendre à tous les pôles. Mesurer l'impact (temps gagné, qualité, adoption). Itérer sur les cas d'usage par département.",
    tags: ['Déploiement', 'KPIs', 'Itération'],
    color: '#14B8A6',
    bg: 'rgba(20,184,166,0.12)',
    border: 'rgba(20,184,166,0.25)',
    why: "Consolidation et passage à l'échelle",
  },
]

function ActionPlanSection() {
  return (
    <section className="section" id="plan" style={{ background: 'linear-gradient(180deg, #080A14 0%, #0F1221 100%)' }}>
      <div className="container">
        <motion.div initial="hidden" whileInView="show" viewport={{ once: true }} variants={stagger}>
          <motion.span className="label" variants={fadeUp}>Recommandation</motion.span>
          <motion.h2 className="section-title" variants={fadeUp}>
            Plan d'action en 3 phases
          </motion.h2>
          <motion.p className="section-sub" variants={fadeUp}>
            Formation et gouvernance d'abord — le chatbot vient après les fondations.
          </motion.p>
        </motion.div>

        <motion.div
          className="plan-steps"
          initial="hidden"
          whileInView="show"
          viewport={{ once: true }}
          variants={stagger}
        >
          {PHASES.map((p) => (
            <motion.div key={p.num} className="card plan-step" variants={fadeUp}
              style={{ borderColor: p.border, background: `linear-gradient(135deg, ${p.bg}, var(--card-bg))` }}
            >
              <div className="plan-num" style={{ background: p.bg, color: p.color, border: `1.5px solid ${p.border}` }}>
                {p.num}
              </div>
              <div className="plan-phase" style={{ color: p.color }}>{p.phase}</div>
              <div className="plan-title">{p.title}</div>
              <div className="plan-desc">{p.desc}</div>
              <div className="plan-tags">
                {p.tags.map((t) => (
                  <span key={t} className="plan-tag" style={{
                    background: p.bg,
                    color: p.color,
                    border: `1px solid ${p.border}`,
                  }}>
                    {t}
                  </span>
                ))}
              </div>
              <div style={{
                marginTop: 16,
                padding: '10px 14px',
                background: 'rgba(255,255,255,0.03)',
                borderRadius: 8,
                fontSize: 12,
                color: '#64748B',
                borderLeft: `2px solid ${p.color}`,
              }}>
                {p.why}
              </div>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  )
}

// ─── Footer ───────────────────────────────────────────────────────────────────

function Footer() {
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-logo">
          <span>KDG</span> · Cellule IA
        </div>
        <div className="footer-text">
          Rapport confidentiel — Consultation IA Koffi &amp; Diabaté Group · Juin 2026
          <br />
          <span style={{ color: '#475569', fontSize: 12, marginTop: 6, display: 'block' }}>
            Abidjan · Cotonou · 32 répondants · 4 pôles
          </span>
        </div>
      </div>
    </footer>
  )
}

// ─── App ─────────────────────────────────────────────────────────────────────

export default function App() {
  return (
    <>
      <Nav />
      <HeroSection />
      <div className="divider" />
      <UsageSection />
      <div className="divider" />
      <ToolsSection />
      <div className="divider" />
      <DepartmentsSection />
      <div className="divider" />
      <BarriersSection />
      <div className="divider" />
      <ActionPlanSection />
      <Footer />
    </>
  )
}

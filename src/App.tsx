/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useEffect, useRef, useState } from 'react';

type Category = 'All' | 'AI & Web' | 'Games' | 'Python';

interface ProjectItem {
  title: string;
  category: Exclude<Category, 'All'>;
  tech: string;
  summary: string[];
  liveLabel: string;
  liveUrl: string;
  codeUrl?: string;
}

const PROJECTS: ProjectItem[] = [
  {
    title: 'My Manga Tracker',
    category: 'AI & Web',
    tech: 'HTML · CSS · JavaScript · AniList API · Gemini API',
    summary: [
      'A single-page app loading live manga data from the AniList GraphQL API with search, status filters, and pagination.',
      'Calls the Google Gemini API to recommend new series from completed lists, with CSV import and browser persistence.',
    ],
    liveLabel: 'Open live app',
    liveUrl: 'https://mymangatracke.netlify.app',
    codeUrl: 'https://github.com/praneeth3112/python-learning/blob/main/animegng%20.html',
  },
  {
    title: 'Neon Arena',
    category: 'Games',
    tech: 'HTML5 Canvas · JavaScript',
    summary: [
      'A twin-stick arena shooter in the browser supporting 2-player local versus or 3 AI bots that chase, strafe, and fire.',
      'Built collision detection, bullet physics, dash and reload mechanics, particle effects, and keyboard, touch, or gamepad input.',
    ],
    liveLabel: 'Play it live',
    liveUrl: 'https://neonarenapvpandbot.netlify.app',
    codeUrl: 'https://github.com/praneeth3112/python-learning/blob/main/pythonlearning/neon-arena-2p-keyboard-mobile-console-shooter.html',
  },
  {
    title: 'Python Learning',
    category: 'Python',
    tech: 'Python · Flask · Git',
    summary: [
      'Practice repository of Python programs, algorithms, and exercises maintained under version control.',
    ],
    liveLabel: 'View repository',
    liveUrl: 'https://github.com/praneeth3112/python-learning',
  },
];

const SKILLS = [
  { title: 'Languages', items: 'Python, C, JavaScript, TypeScript' },
  { title: 'AI and data', items: 'NumPy, SQL, Google Gemini API' },
  { title: 'Web', items: 'HTML, CSS, React, Flask' },
  { title: 'Tools', items: 'Git, Linux, VS Code' },
];

const CATEGORIES: Category[] = ['All', 'AI & Web', 'Games', 'Python'];

function NeuralCanvas() {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    let width = 0;
    let height = 0;
    let rafId = 0;
    const mouse = { x: -999, y: -999 };
    let nodes: Array<{ x: number; y: number; vx: number; vy: number }> = [];

    const resize = () => {
      const rect = canvas.getBoundingClientRect();
      const dpr = window.devicePixelRatio || 1;
      width = rect.width;
      height = rect.height;
      canvas.width = width * dpr;
      canvas.height = height * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const count = Math.max(22, Math.min(64, Math.round((width * height) / 17000)));
      nodes = Array.from({ length: count }, () => ({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: (Math.random() - 0.5) * 0.35,
        vy: (Math.random() - 0.5) * 0.35,
      }));
    };

    const draw = () => {
      ctx.clearRect(0, 0, width, height);
      for (let i = 0; i < nodes.length; i++) {
        const p = nodes[i];
        if (!reduced) {
          const dx = p.x - mouse.x;
          const dy = p.y - mouse.y;
          const dist = Math.hypot(dx, dy);
          if (dist > 0 && dist < 120) {
            p.vx += (dx / dist) * 0.03;
            p.vy += (dy / dist) * 0.03;
          }
          p.vx *= 0.995;
          p.vy *= 0.995;
          p.x += p.vx;
          p.y += p.vy;
          if (p.x < 0 || p.x > width) p.vx *= -1;
          if (p.y < 0 || p.y > height) p.vy *= -1;
        }
        for (let j = i + 1; j < nodes.length; j++) {
          const q = nodes[j];
          const edge = Math.hypot(p.x - q.x, p.y - q.y);
          if (edge < 140) {
            ctx.strokeStyle = `rgba(255, 179, 71, ${(1 - edge / 140) * 0.32})`;
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(q.x, q.y);
            ctx.stroke();
          }
        }
        ctx.fillStyle = 'rgba(255, 179, 71, 0.85)';
        ctx.beginPath();
        ctx.arc(p.x, p.y, 2, 0, Math.PI * 2);
        ctx.fill();
      }
      if (!reduced) rafId = requestAnimationFrame(draw);
    };

    const onMove = (e: MouseEvent) => {
      const rect = canvas.getBoundingClientRect();
      mouse.x = e.clientX - rect.left;
      mouse.y = e.clientY - rect.top;
    };

    resize();
    draw();
    window.addEventListener('mousemove', onMove);
    window.addEventListener('resize', resize);
    return () => {
      cancelAnimationFrame(rafId);
      window.removeEventListener('mousemove', onMove);
      window.removeEventListener('resize', resize);
    };
  }, []);

  return <canvas ref={canvasRef} aria-hidden="true" className="absolute inset-0 h-full w-full pointer-events-none" />;
}

export default function App() {
  const [filter, setFilter] = useState<Category>('All');
  const visible = filter === 'All' ? PROJECTS : PROJECTS.filter((p) => p.category === filter);

  return (
    <div className="min-h-screen bg-[#050505] text-[#f2efe9] selection:bg-[#ffb347] selection:text-black">
      <header className="sticky top-0 z-20 border-b border-[#26241f] bg-[#050505]/95 backdrop-blur-sm">
        <div className="mx-auto flex h-16 max-w-5xl items-center justify-between gap-8 px-6">
          <a href="#top" className="font-display text-lg font-extrabold tracking-tight whitespace-nowrap shrink-0">
            Praneeth
          </a>
          <nav aria-label="Main" className="hidden sm:flex items-center gap-6 text-sm text-[#9a968e]">
            <a href="#projects" className="hover:text-[#f2efe9] transition-colors whitespace-nowrap shrink-0">Projects</a>
            <a href="#skills" className="hover:text-[#f2efe9] transition-colors whitespace-nowrap shrink-0">Skills</a>
            <a href="#education" className="hover:text-[#f2efe9] transition-colors whitespace-nowrap shrink-0">Education</a>
            <a href="#contact" className="hover:text-[#f2efe9] transition-colors whitespace-nowrap shrink-0">Contact</a>
          </nav>
          <a
            href="https://github.com/praneeth3112"
            target="_blank"
            rel="noopener noreferrer"
            className="rounded-full bg-[#ffb347] px-4 py-2 text-xs font-semibold text-black hover:bg-[#f2efe9] transition-colors whitespace-nowrap shrink-0"
          >
            GitHub
          </a>
        </div>
      </header>

      <main id="top">
        <section className="relative overflow-hidden border-b border-[#26241f]">
          <NeuralCanvas />
          <div className="relative mx-auto max-w-5xl px-6 py-24 sm:py-32">
            <h1 className="font-display max-w-3xl text-balance text-5xl font-extrabold leading-[0.96] tracking-tight sm:text-7xl">
              Praneeth Reddy Kadavakolla
            </h1>
            <p className="mt-7 max-w-2xl text-lg leading-relaxed text-[#cfcac0] sm:text-xl">
              I’m a second-year B.Tech student in AI &amp; ML at Jain University. I build with Python and JavaScript,
              and I’m looking for an AI/ML internship where I can learn by shipping real models.
            </p>
            <div className="mt-9 flex flex-wrap gap-3">
              <a
                href="#projects"
                className="rounded-full bg-[#ffb347] px-6 py-3 text-sm font-semibold text-black hover:bg-[#f2efe9] transition-colors whitespace-nowrap shrink-0"
              >
                See my projects
              </a>
              <a
                href="https://github.com/praneeth3112/python-learning"
                target="_blank"
                rel="noopener noreferrer"
                className="rounded-full border border-[#f2efe9]/60 px-6 py-3 text-sm font-semibold text-[#f2efe9] hover:bg-[#f2efe9] hover:text-black transition-colors whitespace-nowrap shrink-0"
              >
                View Python repo
              </a>
            </div>
          </div>
        </section>

        <section id="projects" className="border-b border-[#26241f] py-20">
          <div className="mx-auto max-w-5xl px-6">
            <div className="mb-10 flex flex-wrap items-end justify-between gap-4">
              <h2 className="font-display text-3xl font-extrabold tracking-tight sm:text-4xl">Projects</h2>
              <div className="flex flex-wrap gap-1 rounded-lg border border-[#26241f] bg-[#0e0d0b] p-1">
                {CATEGORIES.map((cat) => (
                  <button
                    key={cat}
                    type="button"
                    onClick={() => setFilter(cat)}
                    className={`rounded-md px-3 py-1.5 text-xs font-semibold transition-colors whitespace-nowrap shrink-0 ${
                      filter === cat ? 'bg-[#ffb347] text-black' : 'text-[#9a968e] hover:text-[#f2efe9]'
                    }`}
                  >
                    {cat}
                  </button>
                ))}
              </div>
            </div>

            <div className="divide-y divide-[#26241f]">
              {visible.map((project) => (
                <article key={project.title} className="grid gap-4 py-8 first:pt-0 last:pb-0 md:grid-cols-[1fr_1.6fr] md:gap-12">
                  <div>
                    <h3 className="font-display text-2xl font-semibold">{project.title}</h3>
                    <p className="mt-1.5 text-sm text-[#ffb347]">{project.tech}</p>
                  </div>
                  <div>
                    {project.summary.map((line) => (
                      <p key={line} className="mb-3 max-w-2xl leading-relaxed text-[#cfcac0]">
                        {line}
                      </p>
                    ))}
                    <div className="mt-4 flex flex-wrap gap-6 text-sm font-semibold">
                      <a
                        href={project.liveUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="underline decoration-[#ffb347] underline-offset-4 hover:text-[#ffb347]"
                      >
                        {project.liveLabel}
                      </a>
                      {project.codeUrl && (
                        <a
                          href={project.codeUrl}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="underline decoration-[#ffb347] underline-offset-4 hover:text-[#ffb347]"
                        >
                          View the code
                        </a>
                      )}
                    </div>
                  </div>
                </article>
              ))}
            </div>
          </div>
        </section>

        <section id="skills" className="border-b border-[#26241f] py-20">
          <div className="mx-auto max-w-5xl px-6">
            <h2 className="font-display mb-10 text-3xl font-extrabold tracking-tight sm:text-4xl">Skills</h2>
            <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
              {SKILLS.map((group) => (
                <div key={group.title}>
                  <h3 className="font-display text-lg font-semibold text-[#ffb347]">{group.title}</h3>
                  <p className="mt-2 text-sm leading-relaxed text-[#cfcac0]">{group.items}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section id="education" className="border-b border-[#26241f] py-20">
          <div className="mx-auto max-w-5xl px-6">
            <h2 className="font-display mb-10 text-3xl font-extrabold tracking-tight sm:text-4xl">Education</h2>
            <div className="flex flex-wrap items-start justify-between gap-8">
              <div>
                <h3 className="font-display text-2xl font-semibold">
                  B.Tech in Computer Science &amp; Engineering (AI &amp; ML)
                </h3>
                <p className="mt-1 text-[#9a968e]">Jain University, currently in the second year</p>
              </div>
              <dl className="grid grid-cols-2 gap-x-8 gap-y-2 text-sm tabular-nums">
                <dt className="text-[#9a968e]">Semester 1</dt>
                <dd className="font-semibold text-right">7.65</dd>
                <dt className="text-[#9a968e]">Semester 2</dt>
                <dd className="font-semibold text-right">6.435</dd>
              </dl>
            </div>
          </div>
        </section>

        <section id="contact" className="border-b border-[#26241f] py-20">
          <div className="mx-auto max-w-5xl px-6">
            <h2 className="font-display mb-4 text-3xl font-extrabold tracking-tight sm:text-4xl">Contact</h2>
            <p className="mb-8 max-w-xl leading-relaxed text-[#cfcac0]">
              I’m open to AI/ML internships. The best way to reach me right now is through GitHub, where all of my work lives.
            </p>
            <a
              href="https://github.com/praneeth3112"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block rounded-full bg-[#ffb347] px-6 py-3 text-sm font-semibold text-black hover:bg-[#f2efe9] transition-colors whitespace-nowrap shrink-0"
            >
              Message me on GitHub
            </a>
          </div>
        </section>
      </main>

      <footer className="py-8">
        <div className="mx-auto max-w-5xl px-6 text-sm text-[#9a968e]">Praneeth Reddy Kadavakolla</div>
      </footer>
    </div>
  );
}

#!/usr/bin/env node
/**
 * Reconstruct a paper's section-scoped Knowledge Positions using JavaScript.
 * Independent implementation of the existing method in research/jit_index.py;
 * no Python process, LLM, graph DB or external npm packages required.
 *
 * Usage:
 *   node rebuild-paper-index.mjs build [paper.md] [jit-index.json]
 *   node rebuild-paper-index.mjs verify [paper.md] [jit-index.json]
 *
 * Requires Markdown headings annotated with [EKC:NN] (the paper convention).
 * This produces the data contract used by the original paper example,
 * not a universal Markdown knowledge parser or independent UKC certification.
 * The source document is never modified.
 */
import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
const defaultPaper = resolve(here, '../../research/paper.md');
const defaultIndex = resolve(here, '../../research/jit-index.json');
const [action = 'verify', paperArg = defaultPaper, indexArg = defaultIndex] = process.argv.slice(2);
const PAPER = resolve(paperArg);
const INDEX = resolve(indexArg);
const SHA = (bytes) => createHash('sha256').update(bytes).digest('hex');
const HEADING = /^(#{2,3})\s+(.+?)\s+\[(EKC:\d+)\]\s*$/;
const WORDS = /[a-z0-9][a-z0-9_-]{2,}/g;
const STOP = new Set('the and that this with from for are was were into not but can may its their they our has have had only than when what which while where how use uses using used one two three more also does each such these those been being should would could will must all any per through without'.split(' '));

function parseSections(raw) {
  const lines = raw.toString('utf8').match(/[^\n]*\n|[^\n]+$/g) || [];
  const sections = [];
  let current = null;
  let offset = 0;
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].replace(/[\r\n]+$/, '');
    const m = line.match(HEADING);
    if (m) {
      if (current) {
        current.end_byte = offset;
        current.end_line = i;
        sections.push(current);
      }
      current = { level: m[1].length, heading: m[2], tag: m[3], start_byte: offset, start_line: i + 1 };
    }
    offset += Buffer.byteLength(lines[i], 'utf8');
  }
  if (current) {
    current.end_byte = raw.length;
    current.end_line = lines.length;
    sections.push(current);
  }
  const ids = sections.map(s => s.tag);
  if (new Set(ids).size !== ids.length) throw new Error('Duplicate EKC section identity');
  return sections;
}

function termMap(text) {
  const counts = new Map();
  for (const word of text.toLowerCase().match(WORDS) || []) {
    if (!STOP.has(word)) counts.set(word, (counts.get(word) || 0) + 1);
  }
  return Object.fromEntries([...counts.entries()].sort((a, b) => b[1] - a[1] || (a[0] < b[0] ? -1 : a[0] > b[0] ? 1 : 0)).slice(0, 24));
}

function lexicalHashVector(text) {
  const v = Array(512).fill(0);
  for (const word of text.toLowerCase().match(/[\p{L}\p{N}_]+/gu) || []) {
    const hash = createHash('sha256').update(word).digest();
    const slot = hash.readUInt32BE(0) % 512;
    v[slot] += hash[4] % 2 ? 1 : -1;
  }
  const norm = Math.hypot(...v);
  return norm ? v.map(n => n / norm) : v;
}

function rebuild(raw, prior = {}) {
  const old = new Map((prior.nodes || []).map(n => [n.id, n]));
  const sections = parseSections(raw);
  const nodes = [], edges = [];
  let parent = null, retained = 0, recomputed = 0;
  for (const [i, section] of sections.entries()) {
    const span = raw.subarray(section.start_byte, section.end_byte);
    const id = 'paper.md#' + section.tag;
    const digest = SHA(span);
    const previous = old.get(id) || {};
    const same = previous.source_version_sha256 === digest;
    same ? retained++ : recomputed++;
    nodes.push({
      id, tag: section.tag, heading: section.heading, heading_level: section.level,
      source: 'paper.md',
      source_position: { start_byte: section.start_byte, end_byte: section.end_byte,
        start_line: section.start_line, end_line: section.end_line, unit: 'utf8_byte' },
      source_version_scope: 'section', source_version_sha256: digest,
      terms: same && previous.terms ? previous.terms : termMap(span.toString('utf8')),
      vector: same && previous.vector != null ? previous.vector : lexicalHashVector(span.toString('utf8')),
      vector_status: 'known',
      embedding_model: same && previous.vector != null ? (previous.embedding_model || 'lexical-hash-512') : 'lexical-hash-512'
    });
    if (i) edges.push({ source: nodes[i - 1].id, target: id,
      relation: 'next_section', qualification: 'manuscript_structure' });
    if (section.level === 2) parent = id;
    else if (parent) edges.push({ source: id, target: parent,
      relation: 'part_of', qualification: 'manuscript_heading_structure' });
  }
  return {
    index: {
      schema_version: 1, authority: 'paper.md', maintenance: 'section_scoped_incremental',
      notes: 'Derived JIT navigation index. Stable EKC identity; exact section spans/hashes; deterministic lexical-hash-512 fallback vectors when no semantic encoder is used.',
      paper_sha256: SHA(raw), nodes, edges
    },
    retained, recomputed
  };
}

function verify(raw, index) {
  if (index.paper_sha256 !== SHA(raw)) throw new Error('Stale whole-paper SHA-256');
  const sections = parseSections(raw);
  if (sections.length !== index.nodes?.length) throw new Error('Incomplete section coverage');
  const ids = new Set();
  for (let i = 0; i < sections.length; i++) {
    const sec = sections[i], node = index.nodes[i], p = node.source_position;
    if (node.tag !== sec.tag || node.id !== 'paper.md#' + sec.tag || ids.has(node.id))
      throw new Error('Wrong/duplicate section identity or order: ' + sec.tag);
    ids.add(node.id);
    for (const field of ['start_byte', 'end_byte', 'start_line', 'end_line'])
      if (p[field] !== sec[field]) throw new Error('Stale ' + field + ': ' + sec.tag);
    if (SHA(raw.subarray(p.start_byte, p.end_byte)) !== node.source_version_sha256)
      throw new Error('Stale section SHA-256: ' + sec.tag);
  }
  if ((index.edges || []).some(e => !ids.has(e.source) || !ids.has(e.target)))
    throw new Error('Edge points to an unknown section');
  return { sections: sections.length, edges: index.edges.length, sha256: SHA(raw) };
}

if (action === 'build') {
  const raw = readFileSync(PAPER);
  const prior = existsSync(INDEX) ? JSON.parse(readFileSync(INDEX, 'utf8')) : {};
  const { index, retained, recomputed } = rebuild(raw, prior);
  verify(raw, index);
  writeFileSync(INDEX, JSON.stringify(index, null, 2) + '\n');
  console.log('built ' + index.nodes.length + ' sections, ' + index.edges.length + ' edges; retained ' + retained + ', recomputed ' + recomputed);
} else if (action === 'verify') {
  const stats = verify(readFileSync(PAPER), JSON.parse(readFileSync(INDEX, 'utf8')));
  console.log('verified ' + stats.sections + ' sections, ' + stats.edges + ' edges, SHA-256 ' + stats.sha256);
} else {
  console.error('Usage: node rebuild-paper-index.mjs [build|verify] [paper.md] [jit-index.json]');
  process.exitCode = 2;
}

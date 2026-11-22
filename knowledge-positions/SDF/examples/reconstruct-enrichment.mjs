#!/usr/bin/env node
/**
 * Paper-specific deterministic UKC/1 reconstruction.
 * Original paper + archived companion -> version-scoped common records.
 * Public example; no model inference, filesystem source mutation, or DB.
 *
 * node reconstruct-enrichment.mjs build [paper.md] [history.json] [output.json]
 * node reconstruct-enrichment.mjs verify [paper.md] [history.json] [output.json]
 * node reconstruct-enrichment.mjs get <EKC:NN|id> [paper.md] [history.json] [output.json]
 * node reconstruct-enrichment.mjs resolve <EKC:NN|id> [paper.md] [history.json] [output.json]
 * node reconstruct-enrichment.mjs neighbors <EKC:NN|id> [paper.md] [history.json] [output.json]
 * node reconstruct-enrichment.mjs export-okf <EKC:NN|id> [paper.md] [history.json] [output.json]
 *
 * This handles only EKC-anchored Markdown sections, not arbitrary Markdown AST.
 * It demonstrates UKC/1 logical records; it does not claim SDK certification.
 */
import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { rebuild, verify as verifyIndex } from './rebuild-paper-index.mjs';

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(HERE, '../../research');
const SHA = bytes => createHash('sha256').update(bytes).digest('hex');
const AUTHORITY = 'repo:l00p3rl00p/barely-passable-ai-stuff';
const SOURCE_KEY = 'knowledge-positions/research/paper.md';

function canonical(tag, digest) {
  const input = JSON.stringify([AUTHORITY, SOURCE_KEY, tag, digest]);
  return 'ukc:v1:' + SHA(Buffer.from(input));
}
function recover(paperBytes, history) {
  const {index} = rebuild(paperBytes);
  verifyIndex(paperBytes, index);
  const byOldID = new Map(history.nodes.map(n => [n.id, n]));
  const byTag = new Map(index.nodes.map(n => [n.tag, n]));
  if (byOldID.size !== history.nodes.length || byTag.size !== index.nodes.length)
    throw new Error('Duplicate historical identity or current tag');

  const valid = new Map();
  for (const n of history.nodes) {
    const current = byTag.get(n.tag);
    if (current && n.content_hash === current.source_version_sha256) valid.set(n.id, current);
  }
  const records = index.nodes.map((n, order) => ({
    schema: 'ukc/1',
    id: canonical(n.tag, n.source_version_sha256),
    source: {
      authority: AUTHORITY, key: SOURCE_KEY, realm: 'public_repository',
      version: 'sha256:' + index.paper_sha256,
      unit_version: 'sha256:' + n.source_version_sha256,
      access: 'public'
    },
    kind: 'markdown_section',
    location: {
      status: 'known', basis: 'ekc_heading_parser',
      anchor: n.tag,
      spans: [{unit: 'utf8_byte', start: n.source_position.start_byte,
        end: n.source_position.end_byte}],
      start_line: n.source_position.start_line, end_line: n.source_position.end_line
    },
    relations: [],
    proximity: [{space: 'lexical-hash-512', status: 'known', vector: n.vector}],
    values: {title: n.heading, tag: n.tag, order, terms: n.terms},
    native: {parser: 'ekc_heading_regex', heading_level: n.heading_level,
      source_ref: n.id, source_bytes_retained: false},
    evidence: {source_sha256: index.paper_sha256,
      span_sha256: n.source_version_sha256, precision: 'verified_utf8_span'}
  }));
  const recordsByTag = new Map(records.map(r => [r.values.tag, r]));
  const oldToCurrent = new Map([...valid].map(([id,n]) => [id, recordsByTag.get(n.tag)]));
  const used = new Set();
  const accepted = [];
  function link(a, b, relation, qualification, evidence, provenance) {
    const key = JSON.stringify([a.id, b.id, relation, qualification]);
    if (used.has(key)) return false;
    used.add(key);
    const edge = {source: a.id, target: b.id, relation, qualification, evidence, provenance};
    a.relations.push({...edge, direction: 'out', neighbor: b.id});
    b.relations.push({...edge, direction: 'in', neighbor: a.id});
    return true;
  }
  for (const e of index.edges) {
    link(recordsByTag.get(e.source.slice('paper.md#'.length)),
      recordsByTag.get(e.target.slice('paper.md#'.length)),
      e.relation, e.qualification, {origin: 'parsed_heading_structure'},
      {source: SOURCE_KEY, source_sha256: index.paper_sha256});
  }
  const inactive = [];
  const matchedEdges = [];
  const compatibleVectors = [];
  for (const [oldId, n] of valid) {
    const old = byOldID.get(oldId);
    const current = recordsByTag.get(n.tag);
    const vector = current.proximity[0].vector;
    if (old.embedding_model === 'lexical-hash-512' &&
        Array.isArray(old.vector) && old.vector.length === vector.length &&
        old.vector.every((v, i) => Math.abs(v - vector[i]) < 1e-12))
      compatibleVectors.push(n.tag);
  }
  for (const e of history.edges) {
    const aOld = byOldID.get(e.source), bOld = byOldID.get(e.target);
    if (!aOld || !bOld) throw new Error('Historical edge has missing endpoint');
    const a = oldToCurrent.get(e.source), b = oldToCurrent.get(e.target);
    const note = {from: aOld.tag, to: bOld.tag, relation: e.relation,
      old_source_hash: aOld.content_hash, old_target_hash: bOld.content_hash};
    if (!a || !b) {
      inactive.push({...note, reason: 'one_or_both_source_hashes_changed'});
      continue;
    }
    if (e.relation === 'next_section') {
      matchedEdges.push(note);
      continue; // structure comes from the current manuscript
    }
    if (!link(a, b, e.relation, 'historical_editorial_navigation',
      e.evidence, {artifact: 'evolving-knowledge-context.json',
        source_sha256: history.source_sha256,
        source_span_sha256: aOld.content_hash,
        target_span_sha256: bOld.content_hash})) {
      throw new Error('Duplicate editorial edge: ' + JSON.stringify(note));
    }
    accepted.push(note);
  }
  records.forEach(r => r.relations.sort((a,b) =>
    JSON.stringify([a.direction,a.relation,a.neighbor]).localeCompare(
      JSON.stringify([b.direction,b.relation,b.neighbor]))));
  const report = {
    current_sections: records.length,
    source_hash_matches: valid.size,
    compatible_legacy_vectors: compatibleVectors.sort(),
    structural_edges: index.edges.length,
    recovered_editorial_edges: accepted,
    inactive_historical_edges: inactive,
    matched_historical_sequence_edges: matchedEdges.length,
    current_edges: index.edges.length + accepted.length,
    qualification: 'Historical editorial links are navigation only'
  };
  return {schema: 'ukc-reconstruction/1', source_sha256: index.paper_sha256,
    records, report};
}
function check(paperBytes, result) {
  if (SHA(paperBytes) !== result.source_sha256) throw new Error('source_changed');
  const ids = new Set(result.records.map(r => r.id));
  if (ids.size !== result.records.length) throw new Error('duplicate_conflict');
  for (const r of result.records) {
    const p = r.location.spans[0];
    if (r.schema !== 'ukc/1' ||
        r.id !== canonical(r.values.tag, r.evidence.span_sha256) ||
        SHA(paperBytes.subarray(p.start, p.end)) !== r.evidence.span_sha256)
      throw new Error('corrupt_record: ' + r.values.tag);
    if (!Array.isArray(r.proximity[0].vector) || r.proximity[0].vector.length !== 512)
      throw new Error('vector_space_mismatch');
    for (const e of r.relations) if (!ids.has(e.neighbor))
      throw new Error('invalid edge endpoint');
  }
  return true;
}
function lookup(data, key) {
  const r = data.records.find(x => x.id === key || x.values.tag === key);
  if (!r) throw new Error('Unknown section or knowledge identity: ' + key);
  return r;
}
function exportOkf(record) {
  // JSON is a valid YAML 1.2 flow mapping: preserve every x_ukc value literally.
  return '---\n' + JSON.stringify({type: 'SourceUnit', title: record.values.title,
    x_ukc: record}, null, 2) + '\n---\n\n' +
    '# ' + record.values.title + '\n\n' +
    'Source-backed knowledge position; resolve original bytes through x_ukc.source and x_ukc.location.\n';
}
const [command = 'build', arg1, arg2, arg3, arg4] = process.argv.slice(2);
const isQuery = ['get','neighbors','resolve','export-okf'].includes(command);
const key = isQuery ? arg1 : null;
const source = resolve(isQuery ? arg2 || ROOT + '/paper.md' : arg1 || ROOT + '/paper.md');
const archived = resolve(isQuery ? arg3 || ROOT + '/evolving-knowledge-context.json' :
  arg2 || ROOT + '/evolving-knowledge-context.json');
const destination = resolve(isQuery ? arg4 || HERE + '/paper-ukc.json' :
  arg3 || HERE + '/paper-ukc.json');
if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  if (destination === source || destination === archived) throw new Error('Output must not overwrite authoritative source or history');
  const bytes = readFileSync(source), history = JSON.parse(readFileSync(archived, 'utf8'));
  if (command === 'build') {
    const output = recover(bytes, history);
    check(bytes, output);
    writeFileSync(destination, JSON.stringify(output, null, 2) + '\n');
    console.log(JSON.stringify({file: destination, ...output.report,
      recovered_editorial_edges: output.report.recovered_editorial_edges.length,
      inactive_historical_edges: output.report.inactive_historical_edges.length}, null, 2));
  } else if (command === 'verify') {
    const saved = JSON.parse(readFileSync(destination, 'utf8'));
    check(bytes, saved);
    const fresh = recover(bytes, history);
    if (JSON.stringify(fresh) !== JSON.stringify(saved))
      throw new Error('Saved knowledge differs from deterministic rebuild');
    console.log('verified ' + saved.records.length + ' UKC/1 paper records');
  } else if (isQuery) {
    const saved = JSON.parse(readFileSync(destination, 'utf8'));
    check(bytes, saved);
    const record = lookup(saved, key);
    if (command === 'get') console.log(JSON.stringify(record, null, 2));
    if (command === 'neighbors') console.log(JSON.stringify(record.relations, null, 2));
    if (command === 'resolve') {
      const p = record.location.spans[0];
      console.log(bytes.subarray(p.start, p.end).toString('utf8'));
    }
    if (command === 'export-okf') console.log(exportOkf(record));
  } else throw new Error('Unknown operation: ' + command);
}
export { recover, check, lookup, exportOkf };

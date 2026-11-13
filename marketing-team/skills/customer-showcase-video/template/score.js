// The showcase score: soft pad intro, a warm electric-piano groove under the app tour that
// stretches to any number of features, the logo lockup on the downbeat. Wordless, original.
kit.score(function (S, T) {
  const ids = kit.json('showcase.json').features.map((f) => f.id);
  const t0 = T[ids[0]], tour = T.lockup - t0;
  // whole 8-beat bars from the first app screen to the lockup, at about 104 bpm
  const bars = Math.max(3, Math.round(tour / (8 * 0.58)));
  const B = tour / (8 * bars), end = 8 + 8 * bars;
  S.tempo(60 / B, { t0: t0 - 8 * B });
  S.program('pad', 'pad', { rev: 0.6, gain: -4 });
  S.program('keys', 'ep', { rev: 0.3 });
  S.program('bass', 'bass');
  S.program('mallet', 'marimba', { pan: 0.2 });
  // intro: soft pad, a mallet note as "live" lands, two dings for the pulses, the launch whoosh
  S.chord('pad', ['F3', 'A3', 'C4', 'E4'], { t: 0, dur: t0 + 0.2, vel: 34 });
  S.note('mallet', 'C6', { t: 0.62, dur: 0.6, vel: 46 });
  S.fx('ding', 1.3, { vel: 26 }); S.fx('ding', 1.9, { vel: 20, pitch: 2 });
  S.fx('whoosh', t0 - 1.2, { dur: 1.2, vel: 60 });
  // groove: I - iii - vi - IV, closing on I in the last bar
  const chords = [['F3', 'A3', 'C4', 'E4'], ['A3', 'C4', 'E4', 'G4'], ['D3', 'F3', 'A3', 'C4'], ['Bb2', 'D3', 'F3', 'A3']];
  const bass = ['F2', 'A2', 'D2', 'Bb1'];
  const arp = [['C5', 'A4', 'F5', 'E5'], ['E5', 'C5', 'A5', 'G5'], ['A4', 'F4', 'D5', 'C5'], ['F4', 'D4', 'Bb4', 'A4']];
  for (let i = 0; i < bars; i++) {
    const k = i === bars - 1 ? 0 : i % 4, b0 = 8 + i * 8;
    S.chord('keys', chords[k], { beat: b0, beats: 4, vel: 48 });
    S.chord('keys', chords[k], { beat: b0 + 4, beats: 4, vel: 42 });
    S.note('bass', bass[k], { beat: b0, beats: 2.5, vel: 72 });
    S.note('bass', bass[k], { beat: b0 + 4, beats: 1.5, vel: 60 });
    S.pattern('mallet', 'x.x.X.xx', { from: b0, repeat: 2, pitch: arp[k], vel: 40 });
  }
  S.drums({ kick: 'x...x...', sidestick: '..x...x.', shaker: 'oxoxoxox' }, { from: 8, repeat: 2 * bars, vel: 50 });
  // foley on the picture's own moments: the app opens, each screen slides in, the phone fades
  S.fx('pop', t0 + 0.05, { vel: 50 });
  ids.slice(1).forEach((id) => { S.fx('whoosh', T[id], { dur: 0.45, vel: 50 }); S.fx('pop', T[id] + 0.35, { vel: 50 }); });
  S.fx('whoosh', T.lockup - 1.2, { dur: 1.2, vel: 45, into: 1 });
  // the lockup lands on the downbeat
  S.fx('revswell', T.lockup, { dur: 1.2 });
  S.run('mallet', ['F5', 'A5', 'C6', 'E6'], { t: T.lockup - 0.48, step: 0.12, vel: 44, cresc: 8 });
  S.chord('keys', ['F3', 'A3', 'C4', 'E4', 'G4'], { beat: end, beats: 6, vel: 64 });
  S.note('bass', 'F2', { beat: end, beats: 6, vel: 76 });
  S.drum('kick', { beat: end, vel: 80 });
  S.fx('ding', T.lockup, { vel: 52 });
  S.chord('pad', ['F3', 'C4', 'E4', 'A4'], { t: T.lockup, dur: T.END - T.lockup, vel: 38 });
  if (T.quote !== undefined) {
    S.fx('chime', T.quote + 0.3, { vel: 34 });
    S.chord('keys', ['D3', 'F3', 'A3', 'C4'], { t: T.quote + 0.3, dur: 2.4, vel: 36 });
    S.chord('keys', ['Bb2', 'F3', 'A3', 'C4'], { t: T.quote + 2.7, dur: Math.max(1.2, T.END - T.quote - 2.7), vel: 34 });
  }
  S.master({ gain: -6, fadeOut: 1.2 });
});

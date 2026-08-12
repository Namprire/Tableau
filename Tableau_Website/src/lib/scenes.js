const hidden = { x: 0, y: 0, width: 100, opacity: 0, scale: 1, rotate: 0, z: 1 };

function layer(overrides = {}) {
  return { ...hidden, ...overrides };
}

export const introSteps = [
  'A few years ago I bought a vintage watch for $200.',
  'Later I found out I overpaid by $50.',
  'But I figured I would eventually even out this bad purchase with a good purchase.',
  'And over time, I would buy and sell more things…',
  '…and my money would all even out.',
  'Instead, the uneven trades compound rather than cancelling out.',
  'Oligarchy – a few rich people, and very little for everyone else.'
];

export const introLayers = [
  ['pawnshop', '/assets/pawnshop.png'],
  ['watchZoom', '/assets/watch-zoom.png'],
  ['phone', '/assets/phone.png'],
  ['watchZoom2', '/assets/watch-zoom2.png'],
  ['gains', '/assets/plus-minus1.png'],
  ['gainsMore', '/assets/plus-minus2.png'],
  ['oligarch', '/assets/oligarch.png']
].map(([id, src]) => ({ id, src, alt: '' }));

export const introScenes = [
  {
    background: '#433448',
    layers: { pawnshop: layer({ width: 104, opacity: 1, z: 1 }) }
  },
  {
    background: '#917d96',
    layers: {
      watchZoom: layer({ x: -18, y: -18, width: 136, opacity: 1, z: 2 }),
      phone: layer({ x: 10, y: 19, width: 30, opacity: 1, z: 3 })
    }
  },
  {
    background: '#917d96',
    layers: {
      watchZoom: layer({ x: -18, y: -18, width: 136, opacity: 1, z: 2 }),
      watchZoom2: layer({ x: -17, y: 8, width: 136, opacity: 1, z: 3 })
    }
  },
  {
    background: '#917d96',
    layers: { gains: layer({ x: 5, y: 5, width: 90, opacity: 1, z: 2 }) }
  },
  {
    background: '#917d96',
    layers: { gainsMore: layer({ width: 100, opacity: 1, z: 2 }) }
  },
  {
    background: '#917d96',
    layers: { gainsMore: layer({ width: 100, opacity: 1, z: 2 }) }
  },
  {
    background: '#917d96',
    layers: { oligarch: layer({ width: 100, opacity: 1, z: 4 }) }
  }
];

export const gameSteps = [
  "Imagine you're in a room with 99 other people.",
  'Everyone pairs with a random person for a coin-flip game.',
  'Everyone starts with $1,000.',
  'The most anyone risks is 20%, making the first wager $200.',
  'You call heads.',
  "It's tails. You lose.",
  'Play often enough and you should win about half the flips. So things should even out, right?',
  'Another round begins with a different partner.',
  'Jon won his first game, so he now has more money than you.',
  'He can risk 20% of his money: $240.',
  'You have less money, so your 20% limit is only $160.',
  'You call tails.',
  "It's tails. You win.",
  'But why are you still below the $1,000 you started with?'
];

export const gameLayers = [
  ['crowd', '/assets/the-100.png'],
  ['player1', '/assets/player1-full.png'],
  ['player2', '/assets/player2-full.png'],
  ['player3', '/assets/player3-full.png'],
  ['player1Happy', '/assets/player1-happy.png'],
  ['player1Sad', '/assets/player1-sad.png'],
  ['player2Happy', '/assets/player2-happy.png'],
  ['player2Sad', '/assets/player2-sad.png'],
  ['player3Happy', '/assets/player3-happy.png'],
  ['player3Sad', '/assets/player3-sad.png'],
  ['coinFlip', '/assets/coin-flipping.png'],
  ['coinTails', '/assets/coin-tails.png']
].map(([id, src]) => ({ id, src, alt: '' }));

const crowdDim = layer({ x: -40, y: -38, width: 180, opacity: 0.11 });
const leftFull = layer({ x: 5, y: 29, width: 28, opacity: 1, z: 3 });
const rightFull = layer({ x: 67, y: 29, width: 28, opacity: 1, z: 3 });
const leftMood = layer({ x: 6, y: 33, width: 30, opacity: 1, z: 3 });
const rightMood = layer({ x: 64, y: 33, width: 30, opacity: 1, z: 3 });
const coinCenter = layer({ x: 44, y: 34, width: 12, opacity: 1, z: 4 });

export const gameScenes = [
  {
    background: '#c8becf',
    layers: { crowd: layer({ width: 100, opacity: 1 }) }
  },
  {
    background: '#917d96',
    layers: { crowd: layer({ width: 100, opacity: 0.28 }), player1: leftFull, player2: rightFull }
  },
  {
    background: '#917d96',
    layers: { crowd: crowdDim, player1: leftFull, player2: rightFull },
    stats: { left: 1000, right: 1000, wager: 0, leftRecord: '0–0', rightRecord: '0–0', rightName: 'Fiona' }
  },
  {
    background: '#917d96',
    layers: { crowd: crowdDim, player1: leftFull, player2: rightFull },
    stats: { left: 1000, right: 1000, wager: 200, leftRecord: '0–0', rightRecord: '0–0', rightName: 'Fiona' },
    speechLeft: 'I can risk $200.'
  },
  {
    background: '#917d96',
    layers: { crowd: crowdDim, player1Happy: leftMood, player2Happy: rightMood, coinFlip: coinCenter },
    faceCards: { left: '#e7dde9', right: '#e7dde9' },
    stats: { left: 1000, right: 1000, wager: 200, leftRecord: '0–0', rightRecord: '0–0', rightName: 'Fiona' },
    speechLeft: 'Heads!'
  },
  {
    background: '#917d96',
    layers: { crowd: crowdDim, player1Sad: leftMood, player2Happy: rightMood, coinTails: coinCenter },
    faceCards: { left: '#e7dde9', right: '#f4d24f' },
    stats: { left: 800, right: 1200, wager: 200, leftRecord: '0–1', rightRecord: '1–0', rightName: 'Fiona' },
    speechLeft: 'Ugh.',
    speechRight: 'I won $200!'
  },
  {
    background: '#917d96',
    layers: { crowd: crowdDim, player1Sad: leftMood, player2Happy: rightMood, coinTails: coinCenter },
    faceCards: { left: '#e7dde9', right: '#f4d24f' },
    stats: { left: 800, right: 1200, wager: 0, leftRecord: '0–1', rightRecord: '1–0', rightName: 'Fiona' }
  },
  {
    background: '#917d96',
    layers: { crowd: layer({ width: 100, opacity: 0.22 }), player1: leftFull, player3: rightFull },
    stats: { left: 800, right: 1200, wager: 0, leftRecord: '0–1', rightRecord: '1–0', rightName: 'Jon' }
  },
  {
    background: '#917d96',
    layers: { crowd: crowdDim, player1: leftFull, player3: rightFull },
    stats: { left: 800, right: 1200, wager: 0, leftRecord: '0–1', rightRecord: '1–0', rightName: 'Jon' }
  },
  {
    background: '#917d96',
    layers: { crowd: crowdDim, player1: leftFull, player3Happy: rightMood },
    stats: { left: 800, right: 1200, wager: 240, leftRecord: '0–1', rightRecord: '1–0', rightName: 'Jon' },
    speechRight: 'I can bet $240.'
  },
  {
    background: '#917d96',
    layers: { crowd: crowdDim, player1Sad: leftMood, player3: rightFull },
    stats: { left: 800, right: 1200, wager: 160, leftRecord: '0–1', rightRecord: '1–0', rightName: 'Jon' },
    speechLeft: 'I can only bet $160.',
    speechRight: 'Fine.'
  },
  {
    background: '#917d96',
    layers: { crowd: crowdDim, player1Happy: leftMood, player3Happy: rightMood, coinFlip: coinCenter },
    faceCards: { left: '#e7dde9', right: '#e7dde9' },
    stats: { left: 800, right: 1200, wager: 160, leftRecord: '0–1', rightRecord: '1–0', rightName: 'Jon' },
    speechLeft: 'Tails!'
  },
  {
    background: '#917d96',
    layers: { crowd: crowdDim, player1Happy: leftMood, player3Sad: rightMood, coinTails: coinCenter },
    faceCards: { left: '#f4d24f', right: '#e7dde9' },
    stats: { left: 960, right: 1040, wager: 160, leftRecord: '1–1', rightRecord: '1–1', rightName: 'Jon' },
    speechLeft: 'I won!',
    speechRight: 'Ugh.'
  },
  {
    background: '#917d96',
    layers: { crowd: crowdDim, player1Happy: leftMood, player3Sad: rightMood, coinTails: coinCenter },
    faceCards: { left: '#f4d24f', right: '#e7dde9' },
    stats: { left: 960, right: 1040, wager: 160, leftRecord: '1–1', rightRecord: '1–1', rightName: 'Jon' },
    speechLeft: 'Wait…'
  }
];

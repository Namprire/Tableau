export const overallBalance = {
  automation: 43,
  augmentation: 57,
  classifiedExposure: 94.39,
  validRows: 2573,
  totalRows: 3963
};

export const interactionModes = [
  { name: 'Directive', description: 'AI receives a task and performs it directly.', value: 30.5, side: 'automation' },
  { name: 'Feedback loop', description: 'AI completes work through feedback and corrections.', value: 12.6, side: 'automation' },
  { name: 'Iteration', description: 'The person and AI improve the result together.', value: 24.8, side: 'augmentation' },
  { name: 'Learning', description: 'AI explains, teaches, or develops the person’s skill.', value: 28.5, side: 'augmentation' },
  { name: 'Validation', description: 'AI checks or reviews the person’s work.', value: 3.6, side: 'augmentation' }
];

export const topOccupations = [
  { name: 'Computer programmers', exposure: 7.64 },
  { name: 'Systems software developers', exposure: 7.13 },
  { name: 'Web developers', exposure: 4.58 },
  { name: 'Applications software developers', exposure: 3.64 },
  { name: 'Network & systems administrators', exposure: 3.06 }
];

export const qaTasks = [
  {
    id: 'debug',
    short: 'Find the source of a software breakdown',
    name: 'Perform initial debugging procedures by reviewing configuration files, logs, or code pieces to determine breakdown source.',
    exposure: 0.658,
    automation: 57.4,
    augmentation: 42.6,
    leaning: 'automation'
  },
  {
    id: 'feedback',
    short: 'Recommend usability improvements to developers',
    name: 'Provide feedback and recommendations to developers on software usability and functionality.',
    exposure: 0.589,
    automation: 21.1,
    augmentation: 78.9,
    leaning: 'augmentation'
  }
];

export const occupationContrast = [
  {
    name: 'Actors',
    exposure: 1.06,
    automation: 71.9,
    augmentation: 28.1,
    balance: -0.437,
    setting: 'stage'
  },
  {
    name: 'Computer & information research scientists',
    exposure: 0.99,
    automation: 29,
    augmentation: 71,
    balance: 0.42,
    setting: 'lab'
  }
];

export const familyProfiles = [
  { name: 'Healthcare practitioners', exposure: 2.94, automation: 26.5, augmentation: 73.5 },
  { name: 'Community & social service', exposure: 2.19, automation: 27.8, augmentation: 72.2 },
  { name: 'Business & financial operations', exposure: 3.69, automation: 34.4, augmentation: 65.6 },
  { name: 'Education & library', exposure: 10.97, automation: 36.6, augmentation: 63.4 },
  { name: 'Office & administrative support', exposure: 6.72, automation: 43.3, augmentation: 56.7 },
  { name: 'Computer & mathematical', exposure: 39.06, automation: 49.3, augmentation: 50.7 },
  { name: 'Production', exposure: 1.87, automation: 54.8, augmentation: 45.2 }
];

export const zoneProfiles = [
  { zone: 2, label: 'Some preparation', classifiedExposure: 7.11, augmentation: 53.2 },
  { zone: 3, label: 'Medium preparation', classifiedExposure: 13.68, augmentation: 55.1 },
  { zone: 4, label: 'High preparation', classifiedExposure: 52.89, augmentation: 53.5 },
  { zone: 5, label: 'Extensive preparation', classifiedExposure: 20.6, augmentation: 68.3 }
];

export const quizTasks = [
  {
    prompt: 'Find the source of a software breakdown by reviewing logs and code.',
    answer: 'automation',
    automation: 57.4,
    augmentation: 42.6,
    note: 'This software-QA task leans toward AI executing the work.'
  },
  {
    prompt: 'Recommend usability and functionality improvements to developers.',
    answer: 'augmentation',
    automation: 21.1,
    augmentation: 78.9,
    note: 'Here AI is much more often supporting human judgment and feedback.'
  },
  {
    prompt: 'Review class material by discussing a text and working through solutions.',
    answer: 'augmentation',
    automation: 30,
    augmentation: 70,
    note: 'For tutors, this task is primarily collaborative and learning-oriented.'
  }
];

/**
 * Conference Papers Mode
 * Handles conference paper selection and display
 */

let viewMode = 'daily'; // 'daily' | 'conference'
let conferenceList = [];
let currentConference = null;
let selectedLanguage = 'Chinese'; // Default language

/**
 * Initialize conference mode
 */
async function initConferenceMode() {
  await loadConferenceList();
  attachConferenceModeEventListeners();
}

/**
 * Load conference list from assets/conference-list.json
 */
async function loadConferenceList() {
  try {
    const response = await fetch('assets/conference-list.json');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    conferenceList = data.conferences || [];
    console.log(`Loaded ${conferenceList.length} conferences`);
    return conferenceList;
  } catch (error) {
    console.error('Failed to load conference list:', error);
    conferenceList = [];
    return [];
  }
}

/**
 * Switch view mode between daily and conference
 */
function switchViewMode(mode) {
  if (viewMode === mode) return;

  viewMode = mode;

  // Update button states
  const dailyButton = document.getElementById('dailyModeButton');
  const conferenceButton = document.getElementById('conferenceModeButton');

  if (mode === 'daily') {
    dailyButton.classList.add('active');
    conferenceButton.classList.remove('active');
    showDailyMode();
  } else {
    dailyButton.classList.remove('active');
    conferenceButton.classList.add('active');
    showConferenceMode();
  }

  console.log(`Switched to ${mode} mode`);
}

/**
 * Show daily mode UI
 */
function showDailyMode() {
  document.getElementById('dailySelector').style.display = 'flex';
  document.getElementById('conferenceSelector').style.display = 'none';

  // Load daily papers
  if (availableDates.length > 0) {
    const latestDate = availableDates[0];
    loadPapersByDate(latestDate);
  }
}

/**
 * Show conference mode UI
 */
function showConferenceMode() {
  document.getElementById('dailySelector').style.display = 'none';
  document.getElementById('conferenceSelector').style.display = 'flex';

  // If first time, load first conference
  if (!currentConference && conferenceList.length > 0) {
    loadConference(conferenceList[0]);
  } else if (currentConference) {
    // Reload current conference
    loadConference(currentConference);
  } else {
    // No conferences available
    showNoConferencesMessage();
  }
}

/**
 * Toggle conference picker modal
 */
function toggleConferencePicker() {
  const modal = document.getElementById('conferencePickerModal');
  const isVisible = modal.style.display !== 'none';

  if (isVisible) {
    modal.style.display = 'none';
  } else {
    renderConferenceList();
    modal.style.display = 'flex';
  }
}

/**
 * Render conference list in modal
 */
function renderConferenceList() {
  const listContainer = document.getElementById('conferenceList');

  if (conferenceList.length === 0) {
    listContainer.innerHTML = `
      <div style="text-align: center; padding: 40px; color: var(--text-secondary);">
        <p>No conferences available</p>
        <p style="font-size: 13px; margin-top: 8px;">Add conferences to assets/conference-list.json</p>
      </div>
    `;
    return;
  }

  listContainer.innerHTML = conferenceList.map(conf => `
    <div class="conference-item" data-id="${conf.id}" onclick="selectConferenceFromList('${conf.id}')">
      <div class="conference-item-header">
        <div class="conference-item-name">${conf.name}</div>
        <div class="conference-item-count">${conf.count} papers</div>
      </div>
      <div class="conference-item-meta">
        <span>📅 ${conf.date}</span>
        <span>🏷️ ${conf.category}</span>
        <span>📖 Year: ${conf.year}</span>
      </div>
      ${conf.description ? `<div class="conference-item-description">${conf.description}</div>` : ''}
    </div>
  `).join('');
}

/**
 * Select conference from list
 */
function selectConferenceFromList(conferenceId) {
  const conference = conferenceList.find(c => c.id === conferenceId);
  if (conference) {
    loadConference(conference);
    toggleConferencePicker(); // Close modal
  }
}

/**
 * Load papers from a conference
 */
async function loadConference(conference) {
  currentConference = conference;

  // Update UI
  document.getElementById('currentConference').textContent = conference.name;

  // Show loading
  const container = document.getElementById('paperContainer');
  container.innerHTML = `
    <div class="loading-container">
      <div class="loading-spinner"></div>
      <p>Loading ${conference.name}...</p>
    </div>
  `;

  try {
    // Load papers from conference file
    const response = await fetch(`data/${conference.file}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const text = await response.text();
    const papers = text.trim().split('\n')
      .filter(line => line.trim())
      .map(line => JSON.parse(line));

    // Store in global paperData (reuse existing structure)
    paperData[conference.id] = papers;

    // Set current category to conference ID
    currentCategory = 'all';  // Show all papers in conference
    currentFilteredPapers = papers;

    // Render papers using existing render function
    renderPapers(papers);

    console.log(`Loaded ${papers.length} papers from ${conference.name}`);

  } catch (error) {
    console.error('Failed to load conference papers:', error);
    container.innerHTML = `
      <div style="text-align: center; padding: 40px; color: var(--text-secondary);">
        <p>❌ Failed to load conference papers</p>
        <p style="font-size: 13px; margin-top: 8px;">${error.message}</p>
        <p style="font-size: 13px; margin-top: 8px;">File: data/${conference.file}</p>
      </div>
    `;
  }
}

/**
 * Show "no conferences" message
 */
function showNoConferencesMessage() {
  const container = document.getElementById('paperContainer');
  container.innerHTML = `
    <div style="text-align: center; padding: 40px; color: var(--text-secondary);">
      <h3>No Conference Papers Available</h3>
      <p style="margin-top: 16px;">Add conferences to <code>assets/conference-list.json</code> to get started.</p>
      <p style="margin-top: 8px; font-size: 13px;">See <a href="specs/neurips-paper-crawler/README.md" target="_blank">NeurIPS Crawler README</a> for instructions.</p>
    </div>
  `;
}

/**
 * Attach event listeners for conference mode
 */
function attachConferenceModeEventListeners() {
  // Mode toggle buttons
  document.getElementById('dailyModeButton').addEventListener('click', () => {
    switchViewMode('daily');
  });

  document.getElementById('conferenceModeButton').addEventListener('click', () => {
    switchViewMode('conference');
  });

  // Conference selector button
  document.getElementById('conferenceButton').addEventListener('click', (e) => {
    e.stopPropagation();
    toggleConferencePicker();
  });

  // Click outside modal to close
  document.getElementById('conferencePickerModal').addEventListener('click', (e) => {
    if (e.target.id === 'conferencePickerModal') {
      toggleConferencePicker();
    }
  });

  console.log('Conference mode event listeners attached');
}

/**
 * Initialize on page load
 */
document.addEventListener('DOMContentLoaded', function() {
  // Wait for app.js to initialize first
  setTimeout(() => {
    initConferenceMode();
  }, 500);
});

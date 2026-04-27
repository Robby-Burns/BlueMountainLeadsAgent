document.addEventListener('DOMContentLoaded', () => {
    fetchLeads();
    checkStatus();
    
    // Refresh leads and status every 10 seconds
    setInterval(() => {
        fetchLeads();
        checkStatus();
    }, 10000);

    const runCrewBtn = document.getElementById('runCrewBtn');
    runCrewBtn.addEventListener('click', runCrew);

    const closeModalBtn = document.getElementById('closeModalBtn');
    closeModalBtn.addEventListener('click', closeDispatchModal);

    const dispatchForm = document.getElementById('dispatchForm');
    dispatchForm.addEventListener('submit', handleDispatchSubmit);
});

async function fetchLeads() {
    try {
        const response = await fetch('/api/leads');
        const leads = await response.json();
        renderLeads(leads);
    } catch (err) {
        console.error('Failed to fetch leads:', err);
    }
}

function renderLeads(leads) {
    const grid = document.getElementById('leadsGrid');
    const countBadge = document.getElementById('leadCount');
    
    countBadge.textContent = leads.length;
    grid.innerHTML = '';

    leads.forEach(lead => {
        const card = document.createElement('div');
        card.className = 'glass-card';
        
        const isSent = lead.email_status === 'Sent';
        
        card.innerHTML = `
            <div class="card-header">
                <h3>${lead.business_name}</h3>
                <div class="location">
                    ${lead.city}, ${lead.state}
                    ${lead.source_url ? ` | <a href="${lead.source_url}" target="_blank" style="color:var(--accent);">View Website</a>` : ''}
                </div>
            </div>
            <div class="tech-gap">⚠️ ${lead.tech_gap || 'Unknown Gap'}</div>
            <div class="email-preview" id="preview-${lead.id}">${lead.email_draft}</div>
            
            ${isSent 
                ? '<div class="status-badge sent">✓ Dispatched</div>'
                : '<button class="btn primary" onclick="openDispatchModal(' + lead.id + ', \'' + lead.business_name.replace(/'/g, "\\'") + '\')">Approve & Send</button>'
            }
        `;
        grid.appendChild(card);
    });
}

async function checkStatus() {
    try {
        const response = await fetch('/api/status');
        const status = await response.json();
        
        const btn = document.getElementById('runCrewBtn');
        const text = btn.querySelector('.btn-text');
        const loader = btn.querySelector('.loader');

        if (status.is_crew_running) {
            text.textContent = 'Running Agents...';
            loader.classList.remove('hidden');
            btn.disabled = true;
        } else {
            text.textContent = 'Run AI Crew';
            loader.classList.add('hidden');
            btn.disabled = false;
        }
    } catch (err) {
        console.error('Failed to check status:', err);
    }
}

async function runCrew() {
    try {
        const response = await fetch('/api/run-crew', { method: 'POST' });
        const result = await response.json();
        
        if (!response.ok) {
            alert(result.detail || 'Failed to start crew');
            return;
        }

        // Instantly check status to update UI
        checkStatus();

    } catch (err) {
        console.error('Failed to run crew:', err);
    }
}

function openDispatchModal(leadId, businessName) {
    document.getElementById('modalLeadId').value = leadId;
    document.getElementById('modalBusinessName').textContent = businessName;
    document.getElementById('contactEmail').value = '';
    
    // Pre-fill the editable text area with the specific draft text
    const draftText = document.getElementById('preview-' + leadId).textContent;
    document.getElementById('emailDraft').value = draftText;
    
    const modal = document.getElementById('dispatchModal');
    modal.classList.remove('hidden');
}

function closeDispatchModal() {
    const modal = document.getElementById('dispatchModal');
    modal.classList.add('hidden');
}

async function handleDispatchSubmit(e) {
    e.preventDefault();
    
    const leadId = document.getElementById('modalLeadId').value;
    const email = document.getElementById('contactEmail').value;
    const editedDraft = document.getElementById('emailDraft').value;
    const submitBtn = e.target.querySelector('button[type="submit"]');
    
    submitBtn.disabled = true;
    submitBtn.textContent = 'Sending...';

    try {
        const response = await fetch('/api/dispatch/' + leadId, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                contact_email: email,
                email_draft: editedDraft
            })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            closeDispatchModal();
            fetchLeads(); // Refresh grid
        } else {
            alert(result.detail || 'Failed to send email');
        }
    } catch (err) {
        console.error('Dispatch error:', err);
        alert('A network error occurred.');
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Send Now';
    }
}

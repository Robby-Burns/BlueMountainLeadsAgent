document.addEventListener('DOMContentLoaded', () => {
    fetchLeads();
    
    // Refresh leads every 10 seconds
    setInterval(fetchLeads, 10000);

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
                <div class="location">${lead.city}, ${lead.state}</div>
            </div>
            <div class="tech-gap">⚠️ ${lead.tech_gap || 'Unknown Gap'}</div>
            <div class="email-preview">${lead.email_draft}</div>
            
            ${isSent 
                ? '<div class="status-badge sent">✓ Dispatched</div>'
                : '<button class="btn primary" onclick="openDispatchModal(' + lead.id + ', \'' + lead.business_name.replace(/'/g, "\\'") + '\')">Approve & Send</button>'
            }
        `;
        grid.appendChild(card);
    });
}

async function runCrew() {
    const btn = document.getElementById('runCrewBtn');
    const text = btn.querySelector('.btn-text');
    const loader = btn.querySelector('.loader');

    text.textContent = 'Running Agents...';
    loader.classList.remove('hidden');
    btn.disabled = true;

    try {
        const response = await fetch('/api/run-crew', { method: 'POST' });
        const result = await response.json();
        
        if (!response.ok) {
            alert(result.detail || 'Failed to start crew');
            text.textContent = 'Run AI Crew';
            loader.classList.add('hidden');
            btn.disabled = false;
            return;
        }

        // Leave it spinning for a bit to indicate background work
        setTimeout(() => {
            text.textContent = 'Run AI Crew';
            loader.classList.add('hidden');
            btn.disabled = false;
        }, 5000);

    } catch (err) {
        console.error('Failed to run crew:', err);
        text.textContent = 'Run AI Crew';
        loader.classList.add('hidden');
        btn.disabled = false;
    }
}

function openDispatchModal(leadId, businessName) {
    document.getElementById('modalLeadId').value = leadId;
    document.getElementById('modalBusinessName').textContent = businessName;
    document.getElementById('contactEmail').value = '';
    
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
    const submitBtn = e.target.querySelector('button[type="submit"]');
    
    submitBtn.disabled = true;
    submitBtn.textContent = 'Sending...';

    try {
        const response = await fetch('/api/dispatch/' + leadId, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ contact_email: email })
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

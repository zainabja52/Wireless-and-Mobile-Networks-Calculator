document.addEventListener('DOMContentLoaded', function() {
    updateFormFields();  // Call this function on page load to display the relevant input fields
});

function updateFormFields() {
    const calculationType = document.getElementById('calculation_type').value;
    const inputsContainer = document.getElementById('dynamic_inputs');
    inputsContainer.innerHTML = ''; // Clear previous inputs

    // Define input fields and labels for each type
    let inputs = [];
    if (calculationType === 'sampler_and_interleaver') {
        inputs = [
            {id: 'bandwidth', placeholder: 'Enter Bandwidth (Hz)', label: 'Bandwidth:', type: 'number', units: ['Hz', 'kHz', 'MHz']},
            {id: 'num_bits_per_sample', placeholder: 'Enter Number of Bits per Sample', label: 'Number of Bits per Sample:'},
            {id: 'compression_ratio', placeholder: 'Enter Compression Ratio', label: 'Compression Ratio (Rs):'},
            {id: 'redundancy_ratio', placeholder: 'Enter Redundancy Ratio', label: 'Redundancy Ratio (Rc):'},
            {id: 'interleaver_bits', placeholder: 'Select Interleaver Bits', label: 'Interleaver Bits:', type: 'select', options: generatePowerOfTwoOptions(1, 16384)}
        ];
    }
    

    if (calculationType === 'ofdm') {
    inputs = [
        {id: 'bandwidth', placeholder: 'Enter Bandwidth', label: 'Bandwidth:', type: 'number', units: ['Hz', 'kHz', 'MHz']},
        {id: 'num_subcarriers', placeholder: 'Enter Number of Subcarriers', label: 'Number of Subcarriers:', type: 'number', units: ['Hz', 'kHz', 'MHz']},
        {id: 'num_symbols_per_rb', placeholder: 'Enter Number of Symbols per Resource Block', label: 'Number of Symbols per RB:'},
        {id: 'symbol_duration', placeholder: 'Enter Symbol Duration', label: 'Symbol Duration:', units: ['ms', 'μs']},
        {id: 'qam', placeholder: 'Enter QAM (e.g., 1024)', label: 'QAM:'},
        {id: 'num_parallel_rb', placeholder: 'Enter Number of Parallel Resource Blocks', label: 'Number of Parallel RBs:'}
    ];
}
    if (calculationType === 'power_transmitted') {
        inputs = [
        {id: 'Lp', placeholder: 'Enter Path Losses', label: 'Path Losses Lp:', type: 'number', units: ['dB', 'dBm']},
        {id: 'f', placeholder: 'Enter Frequency', label: 'Frequency:', type: 'number', units: ['Hz', 'kHz', 'MHz']},
        {id: 'Gt', placeholder: 'Enter Antenna Gain at Transmitter', label: 'Antenna Gain at Transmitter Gt:', type: 'number', units: ['dB', 'dBm']},
        {id: 'Gr', placeholder: 'Enter Antenna Gain at Receiver', label: 'Antenna Gain at Receiver Gr:', type: 'number', units: ['dB', 'dBm']},
        {id: 'Lf', placeholder: 'Enter Feed Line Loss', label: 'Feed Line Loss Lf:', type: 'number', units: ['dB', 'dBm']},
        {id: 'R', placeholder: 'Enter Data Rate', label: 'Data Rate R:', type: 'number', units: ['bps', 'kbps', 'Mbps', 'dB', 'dBm']},
        {id: 'L0', placeholder: 'Enter other Path Losses', label: 'Other Path Losses L0:', type: 'number', units: ['dB', 'dBm']},
        {id: 'At', placeholder: 'Enter Transmitter Amplifier Gain', label: 'Transmitter Amplifier Gain At:', type: 'number', units: ['dB', 'dBm']},
        {id: 'Ar', placeholder: 'Enter Receiver Amplifier Gain', label: 'Receiver Amplifier Gain Ar:', type: 'number', units: ['dB', 'dBm']},
        {id: 'Nf', placeholder: 'Enter Noise Figure', label: 'Noise Figure Nf:', type: 'number', units: ['dB', 'dBm']},
        {id: 'T', placeholder: 'Enter Temperature', label: 'Temperature T:', type: 'number', units: ['Kelvin', 'Celsius','dB','dBm']},
        {id: 'Fmargin', placeholder: 'Enter FMargin', label: 'FMargin:', type: 'number', units: ['dB', 'dBm']},
        {id: 'M', placeholder: 'Enter Link Margin', label: 'Link Margin M:', type: 'number', units: ['dB', 'dBm']},
        {id: 'modulation', placeholder: 'Select Modulation', label: 'Modulation:', type: 'select', options: ['BPSK/QPSK', '8-PSK', '16-PSK']},
        {id: 'ber_value', placeholder: 'Select BER Value', label: 'BER Value:', type: 'select', options: []},
         {id: 'output_unit', placeholder: 'Select Output Unit:', label: 'Output Unit:', type: 'select', options: ['dB', 'Watt']}
    ];
} else if (calculationType === 'throughput') {
        inputs = [
            {id: 'calculation_method', placeholder: 'Select Throughput Calculation Method', label: 'Calculation Method:', type: 'select', options: ['unslottednonpersistent', 'slottednonpersistent', 'unslotted1persistent', 'slotted1persistent']},
            {id: 'R_rate', placeholder: 'Enter Data Transmission Rate', label: 'Data Transmission Rate (R_rate):', units: ['bps', 'kbps', 'Mbps']},
            {id: 'tau', placeholder: 'Enter Maximum Signal Propagation Time', label: 'Maximum Signal Propagation Time (tau):', units: ['us', 'ms', 's']},
            {id: 'F_size', placeholder: 'Enter Frame Size', label: 'Frame Size (F_size):', units: ['bits', 'Kbits', 'Mbits']},
            {id: 'f_rate', placeholder: 'Enter Frame Rate', label: 'Frame Rate (f_rate):', units: ['fps', 'Kfps', 'Mfps']}
        ];
    }
if (calculationType === 'cellular_system') {
    inputs = [
        {id: 'transmitted_power', placeholder: 'Enter Transmitted Power (W)', label: 'Transmitted Power (W):'},
        {id: 'path_loss_exponent', placeholder: 'Enter Path Loss Exponent', label: 'Path Loss Exponent:'},
        {id: 'frequency', placeholder: 'Enter Frequency (Hz)', label: 'Frequency (Hz):'},
        {id: 'required_coverage', placeholder: 'Enter Required Coverage Area (m²)', label: 'Required Coverage Area (m²):'}
    ];
}



inputs.forEach(input => {
    const inputRow = document.createElement('div');
    inputRow.classList.add('input-row');

    const label = document.createElement('label');
    label.setAttribute('for', input.id);
    label.textContent = input.label;
    inputRow.appendChild(label);

    const inputElement = document.createElement(input.type === 'select' ? 'select' : 'input');
    inputElement.id = input.id;
    if (input.type !== 'select') {
        inputElement.setAttribute('type', input.type || 'text');
        inputElement.setAttribute('placeholder', input.placeholder || '');
    } else {
        // Handling dropdown options for select elements
        input.options.forEach(option => {
            const optionElement = document.createElement('option');
            optionElement.value = option;
            optionElement.textContent = option;
            inputElement.appendChild(optionElement);
        });
        if (input.id === 'modulation') {
                inputElement.addEventListener('change', function() {
                    updateBERValues(); // Update BER values based on selected modulation
                });
            }
    }

    inputRow.appendChild(label);
    inputRow.appendChild(inputElement);
    if (input.units && input.type !== 'select') {
        const selectElement = document.createElement('select');
        selectElement.id = `${input.id}_unit`;
        input.units.forEach(unit => {
            const optionElement = document.createElement('option');
            optionElement.value = unit;
            optionElement.textContent = unit;
            selectElement.appendChild(optionElement);
        });
        inputRow.appendChild(selectElement);
    }
    inputsContainer.appendChild(inputRow);
});
}

function updateBERValues() {
    const modulationSelect = document.getElementById('modulation');
    const berSelect = document.getElementById('ber_value');
    berSelect.innerHTML = ''; // Clear existing options

    const berValues = {
        'BPSK/QPSK': ["10^-1", "10^-2", "10^-3", "10^-4", "10^-5", "10^-6", "10^-7", "10^-8"],
        '8-PSK': ["10^-1", "10^-2", "10^-3", "10^-4", "10^-5", "10^-6", "10^-7", "10^-8"],
        '16-PSK': ["10^-1", "10^-2", "10^-3", "10^-4", "10^-5", "10^-6"]
    };

    const selectedModulation = modulationSelect.value;
    const berOptions = berValues[selectedModulation] || [];

    berOptions.forEach(ber => {
        const optionElement = document.createElement('option');
        optionElement.value = ber;
        optionElement.textContent = `BER: ${ber}`;
        berSelect.appendChild(optionElement);
    });
}

function generatePowerOfTwoOptions(min, max) {
    const options = [];
    for (let i = min; i <= max; i *= 2) {
        options.push(i.toString()); // ensure values are strings if needed
    }
    return options;
}

function submitData() {
    const calculationType = document.getElementById('calculation_type').value;
    const inputsContainer = document.getElementById('dynamic_inputs');
    const inputs = inputsContainer.querySelectorAll('input, select'); // Include selects in the query
    const data = { type: calculationType };

    inputs.forEach(input => {
        if (input.tagName === 'SELECT' && input.hasAttribute('id')) {
            data[input.id] = input.value; // Correctly capture select inputs
        } else if (input.tagName === 'INPUT') {
            data[input.id] = input.value;
        }
    });

    fetch('/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => handleResponse(data))
    .catch(error => handleError(error));
}
function handleResponse(data) {
    if (data.error) {
        console.error('Error:', data.error);
        document.getElementById('results').innerHTML = `<div style='color: red;'>Error: ${data.error}</div>`;
    } else {
        let resultsHtml = '<table class="results-table">';
        resultsHtml += '<tr><th>Component</th><th>Value</th></tr>';
        for (const key in data) {
            resultsHtml += `<tr><td>${key}</td><td>${data[key]}</td></tr>`;
        }
        resultsHtml += '</table>';
        document.getElementById('results').innerHTML = resultsHtml;
    }
}

function clearForm() {
    document.getElementById('calcForm').reset();
    document.getElementById('results').innerHTML = '';
    updateFormFields();  // Update fields after clearing form to reflect the default or selected calculation type
}

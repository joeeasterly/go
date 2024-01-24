function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, '\\$&');
    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
}

// Retrieve the "s" parameter from the URL
const sParameter = getParameterByName('s');

if (sParameter) {
    const jsonUrl = `data/${sParameter.charAt(0)}/${sParameter}.json`;

    // Fetch JSON data from the specified URL
    fetch(jsonUrl)
        .then(response => response.json())
        .then(data => renderShelvingRecord(data))
        .catch(error => console.error('Error fetching JSON:', error));
} else {
    console.error('Missing "s" parameter in the URL.');
}

function renderShelvingRecord(record) {
const shelvingRecordDiv = document.createElement('div');
shelvingRecordDiv.className = 'shelving-record';

// Define the order of fields for each type
const fieldOrder = {
    inventory: ['label', 'last_updated', 'identifier'],
    item: ['label', 'last_updated', 'type', 'identifier'],
    storage: ['label', 'last_updated', 'field3', 'identifier'],
    consumable: ['label', 'last_updated', 'expires', 'identifier'],
    consumable_instance: ['label', 'last_updated', 'expires', 'identifier'],
};

// Render shelving record details
const shelvingRecordDetails = document.createElement('div');
shelvingRecordDetails.innerHTML = `<strong>Shelving Record:</strong>`;
const type = record.shelving_record.type || ''; // Assuming type is present in shelving_record
const orderedFields = fieldOrder[type] || Object.keys(record.shelving_record);
orderedFields.forEach(fieldName => {
    if (record.shelving_record.hasOwnProperty(fieldName)) {
        const fieldSpan = document.createElement('span');
        fieldSpan.className = `field ${fieldName}`;
        const fieldValue = fieldName === 'last_updated'
            ? new Date(record.shelving_record[fieldName].$date).toLocaleString()
            : record.shelving_record[fieldName];
        fieldSpan.innerHTML = `<span class="label ${fieldName}">${fieldName}:</span><span class="field-value ${fieldName}">${fieldValue}</span>`;
        shelvingRecordDetails.appendChild(fieldSpan);
    }
});
shelvingRecordDiv.appendChild(shelvingRecordDetails);

// Render shelf contents
const shelfContentsDiv = document.createElement('div');
shelfContentsDiv.innerHTML = `<strong>Shelf Contents:</strong>`;
record.shelf_contents.forEach((item, index) => {
    const itemDiv = document.createElement('div');
    itemDiv.className = `shelf-content-item ${item.type || ''}`; // Add the type as a class
    const itemType = item.type || ''; // Assuming type is present in shelf_contents
    const orderedItemFields = fieldOrder[itemType] || Object.keys(item);
    orderedItemFields.forEach(fieldName => {
        if (item.hasOwnProperty(fieldName)) {
            const fieldSpan = document.createElement('span');
            fieldSpan.className = `field ${fieldName}`;
            const fieldValue = fieldName === 'last_updated'
                ? new Date(item[fieldName].$date).toLocaleString()
                : item[fieldName];
            fieldSpan.innerHTML = `<span class="label ${fieldName}">${fieldName}:</span><span class="field-value ${fieldName}">${fieldValue}</span>`;
            itemDiv.appendChild(fieldSpan);
        }
    });
    shelfContentsDiv.appendChild(itemDiv);
});
shelvingRecordDiv.appendChild(shelfContentsDiv);

document.body.appendChild(shelvingRecordDiv);
}
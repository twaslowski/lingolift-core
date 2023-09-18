document.getElementById('translation-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const sentence = document.getElementById('sentence-input').value;
    getTranslation(sentence);
});

function getTranslation(sentence) {
    // Display the loading message
    document.getElementById('loading-message').style.display = 'block';

    // Clear the previous translation data
    document.getElementById('summary').textContent = '';
    document.getElementById('sentence-container').innerHTML = '';
    document.getElementById('responses').innerHTML = '';

    // Using the fetch API to POST the sentence to the backend
    fetch('http://127.0.0.1:5000/translate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ sentence: sentence }), // Assuming your backend expects a JSON with this format
    })
        .then(response => response.json())
        .then(data => {
            renderTranslation(data);
        })
        .catch(error => {
            console.error("There was an error translating the sentence:", error);
            document.getElementById('loading-message').textContent = 'Error translating the sentence.';
        });
}

function renderTranslation(data) {
    document.getElementById('summary').textContent = data.summary;

    const sentenceContainer = document.getElementById('sentence-container');
    data.sentence_breakdown.forEach(item => {
        const wordContainer = document.createElement('div');
        wordContainer.classList.add('word-container');

        const originalWord = document.createElement('span');
        originalWord.classList.add('original-word');
        originalWord.textContent = item.word;
        wordContainer.appendChild(originalWord);

        const translation = document.createElement('span');
        translation.classList.add('translation');
        translation.textContent = item.translation;
        wordContainer.appendChild(translation);

        const grammaticalContext = document.createElement('span');
        grammaticalContext.classList.add('grammatical-context');
        grammaticalContext.textContent = item.grammatical_context;
        wordContainer.appendChild(grammaticalContext);

        sentenceContainer.appendChild(wordContainer);
    });

    const responseList = document.getElementById('responses');
    data.response_suggestions.forEach(item => {
        const li = document.createElement('li');
        li.textContent = `${item.response} (${item.translation})`;
        responseList.appendChild(li);
    });
}
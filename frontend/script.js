document.getElementById('translation-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const sentence = document.getElementById('sentence-input').value;
    getTranslation(sentence);
});

function getTranslation(sentence) {
    // Display the loading message
    document.getElementById('loading-message').style.display = 'block';

    // Clear the previous translation data
    document.getElementById('summary').textContent = '';
    document.getElementById('literal-translation').textContent = '';
    document.getElementById('sentence-container').innerHTML = '';

    // Using the fetch API to POST the sentence to the backend
    fetch('http://127.0.0.1:5000/translate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({sentence: sentence}), // Assuming your backend expects a JSON with this format
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
    document.getElementById('original-sentence').textContent = data.original_sentence;
    document.getElementById('summary').textContent = data.summary;

    // construct literal translation
    let literalTranslationHTML = '';
    const words = data.literal_translation.split(' ');
    words.forEach(word => {
        const wordId = words.indexOf(word);
        literalTranslationHTML += `<span data-word-id="${wordId}">${word}</span> `;
    });

    // construct sentence breakdown
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

        const matches = words.find(word => word.toLowerCase() === item.translation.toLowerCase());
        if (matches) {
            wordContainer.setAttribute("data-word-id", words.indexOf(matches))
        }

        sentenceContainer.appendChild(wordContainer);
    });
    document.getElementById('literal-translation').innerHTML = literalTranslationHTML
    addDecorators()
}

// Function to highlight a word
function highlightWord(wordId) {
    document.querySelector(`#literal-translation [data-word-id="${wordId}"]`).classList.add('highlight');
    document.querySelector(`#sentence-container [data-word-id="${wordId}"]`).classList.add('highlight');
    document.querySelector(`[data-word-id="${wordId}"]`).classList.add('highlight');
}

// Function to remove the highlight
function removeHighlight(wordId) {
    document.querySelector(`#literal-translation [data-word-id="${wordId}"]`).classList.remove('highlight');
    document.querySelector(`#sentence-container [data-word-id="${wordId}"]`).classList.remove('highlight');
    document.querySelector(`[data-word-id="${wordId}"]`).classList.remove('highlight');
}

function addDecorators() {
// Add event listeners to the words in the literal translation
    document.querySelectorAll('#literal-translation [data-word-id]').forEach(wordElement => {
        const wordId = wordElement.getAttribute('data-word-id');

        wordElement.addEventListener('mouseover', () => highlightWord(wordId));
        wordElement.addEventListener('mouseout', () => removeHighlight(wordId));
    });

    document.querySelectorAll('#sentence-container [data-word-id]').forEach(wordElement => {
        const wordId = wordElement.getAttribute('data-word-id');

        wordElement.addEventListener('mouseover', () => highlightWord(wordId));
        wordElement.addEventListener('mouseout', () => removeHighlight(wordId));
    });
}
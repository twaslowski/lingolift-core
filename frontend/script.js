document.getElementById('translation-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const sentence = document.getElementById('sentence-input').value;
    getTranslation(sentence);
});

function getTranslation(sentence) {
    cleanup();
    fetch('http://127.0.0.1:5000/translate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({sentence: sentence})
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

function cleanup() {
    // Display the loading message
    document.getElementById('loading-message').style.display = 'block';

    // Clear the previous translation data
    document.getElementById('natural-translation').textContent = '';
    document.getElementById('literal-translation').textContent = '';
    document.getElementById('sentence-container').innerHTML = '';
}

function renderTranslation(data) {
    document.getElementById('natural-translation').textContent = data.natural_translation;
    document.getElementById('original-sentence').textContent = data.original_sentence;
    document.getElementById('literal-translation').textContent = data.literal_translation;
}

function tokenizeSentence(sentence) {
    // Use regex to split the sentence into words and punctuation
    return sentence.match(/([\u0400-\u04FF\w]+|\S)/g);
}

function constructAnalysis() {
    // construct literal translation html
    let literalTranslationHTML = '';
    const literal_translation = tokenizeSentence(data.literal_translation);

    literal_translation.forEach(word => {
        const wordId = literal_translation.indexOf(word);
        literalTranslationHTML += `<span translation-word-id="${wordId}">${word}</span> `;
    });

    // construct source sentence html
    let originalSentenceHTML = '';
    const original_sentence = tokenizeSentence(data.original_sentence)
    original_sentence.forEach(word => {
        const wordId = original_sentence.indexOf(word);
        originalSentenceHTML += `<span original-word-id="${wordId}">${word}</span> `;
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

        const translationMatches = literal_translation.find(word => word.toLowerCase() === item.translation.toLowerCase());
        if (translationMatches) {
            wordContainer.setAttribute("translation-word-id", literal_translation.indexOf(translationMatches))
        }

        const originalMatches = original_sentence.find(word => word.toLowerCase() === item.word.toLowerCase());
        if (originalMatches) {
            wordContainer.setAttribute("original-word-id", original_sentence.indexOf(originalMatches))
        }


        sentenceContainer.appendChild(wordContainer);
    });
    document.getElementById('literal-translation').innerHTML = literalTranslationHTML
    document.getElementById('original-sentence').innerHTML = originalSentenceHTML
    addDecorators()
}

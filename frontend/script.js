document.getElementById('translation-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const sentence = document.getElementById('sentence-input').value;
    getTranslation(sentence);
    getSuggestions(sentence);
});

function getSuggestions(sentence) {
    console.log("getting suggestions for sentence " + sentence)
    fetch('http://127.0.0.1:5000/responses', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({sentence: sentence})
    })
        .then(response => response.json())
        .then(data => {
            renderSuggestions(data);
        })
        .catch(error => {
            console.error("There was an error translating the sentence:", error);
            document.getElementById('loading-message').textContent = 'Error translating the sentence.';
        });
}

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
            getAnalysis(sentence, data.literal_translation)
        })
        .catch(error => {
            console.error("There was an error translating the sentence:", error);
            document.getElementById('loading-message').textContent = 'Error translating the sentence.';
        });
}


function getAnalysis(sentence, literal_translation) {
    fetch('http://127.0.0.1:5000/syntactical-analysis', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({sentence: sentence, literal_translation: literal_translation})
    })
        .then(response => response.json())
        .then(data => {
            renderSyntacticalAnalysis(data);
        })
        .catch(error => {
            console.error("There was an error translating the sentence:", error);
            document.getElementById('loading-message').textContent = 'Error translating the sentence.';
        });
}

function cleanup() {
    // Display the loading message
    document.getElementById('loading-message-translation').style.display = 'block';
    document.getElementById('loading-message-responses').style.display = 'block';

    // Clear the previous translation data
    document.getElementById('natural-translation').textContent = '';
    document.getElementById('literal-translation').textContent = '';
    document.getElementById('sentence-container').innerHTML = '';

    // clear suggestions table
    document.getElementById('response-suggestions').innerHTML = '';
}

function renderTranslation(data) {
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
    document.getElementById('natural-translation').textContent = data.natural_translation;
    document.getElementById('literal-translation').innerHTML = literalTranslationHTML;
    document.getElementById('original-sentence').innerHTML = originalSentenceHTML;
    document.getElementById('loading-message-translation').style.display = 'none'
    document.getElementById('translation-container').style.display = 'block'
}

function renderSuggestions(data) {
    document.getElementById('response-suggestions-header').style.display = 'block'
    document.getElementById('loading-message-responses').style.display = 'none'
    const responseList = document.getElementById('response-suggestions');
    data.response_suggestions.forEach(item => {
        const li = document.createElement('li');
        li.textContent = `${item.suggestion} (${item.translation})`;
        responseList.appendChild(li);
    });
}

function tokenizeSentence(sentence) {
    // Use regex to split the sentence into words and punctuation
    return sentence.match(/([\u0400-\u04FF\w]+|\S)/g);
}

function renderSyntacticalAnalysis(data) {
    // construct sentence breakdown
    const sentenceContainer = document.getElementById('sentence-container');
    data.syntactical_analysis.forEach(item => {
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

        let literal_translation = tokenizeSentence(data.literal_translation)
        const translationMatches = literal_translation.find(word => word.toLowerCase() === item.translation.toLowerCase());
        if (translationMatches) {
            wordContainer.setAttribute("translation-word-id", literal_translation.indexOf(translationMatches))
        }

        let original_sentence = tokenizeSentence(data.original_sentence)
        const originalMatches = original_sentence.find(word => word.toLowerCase() === item.word.toLowerCase());
        if (originalMatches) {
            wordContainer.setAttribute("original-word-id", original_sentence.indexOf(originalMatches))
        }


        sentenceContainer.appendChild(wordContainer);
    });
    addDecorators()
}

// evil chatgpt copypaste
function highlightWord(wordIdTranslation, wordIdOriginal) {
    let translationElement, originalElement;

    if (!wordIdTranslation && wordIdOriginal) {
        translationElement = document.querySelector(`#sentence-container [original-word-id="${wordIdOriginal}"]`);
        wordIdTranslation = translationElement ? translationElement.getAttribute("translation-word-id") : null;
    }
    if (!wordIdOriginal && wordIdTranslation) {
        originalElement = document.querySelector(`#sentence-container [translation-word-id="${wordIdTranslation}"]`);
        wordIdOriginal = originalElement ? originalElement.getAttribute("original-word-id") : null;
    }

    console.log("add highlighting for " + wordIdTranslation + " and " + wordIdOriginal)

    if (wordIdTranslation) {
        const targetTranslationElement = document.querySelector(`#literal-translation [translation-word-id="${wordIdTranslation}"]`);
        if (targetTranslationElement) targetTranslationElement.classList.add('highlight');

        const sentenceTranslationElement = document.querySelector(`#sentence-container [translation-word-id="${wordIdTranslation}"]`);
        if (sentenceTranslationElement) sentenceTranslationElement.classList.add('highlight');

        const generalTranslationElement = document.querySelector(`[translation-word-id="${wordIdTranslation}"]`);
        if (generalTranslationElement) generalTranslationElement.classList.add('highlight');
    }

    if (wordIdOriginal) {
        const targetOriginalElement = document.querySelector(`#original-sentence [original-word-id="${wordIdOriginal}"]`);
        if (targetOriginalElement) targetOriginalElement.classList.add('highlight');
    }
}

// Function to remove the highlight
function removeHighlight(wordIdTranslation, wordIdOriginal) {
    let translationElement, originalElement;

    if (!wordIdTranslation && wordIdOriginal) {
        translationElement = document.querySelector(`#sentence-container [original-word-id="${wordIdOriginal}"]`);
        wordIdTranslation = translationElement ? translationElement.getAttribute("translation-word-id") : null;
    }
    if (!wordIdOriginal && wordIdTranslation) {
        originalElement = document.querySelector(`#sentence-container [translation-word-id="${wordIdTranslation}"]`);
        wordIdOriginal = originalElement ? originalElement.getAttribute("original-word-id") : null;
    }

    console.log("remove highlighting for " + wordIdTranslation + " and " + wordIdOriginal)

    if (wordIdTranslation) {
        const targetTranslationElement = document.querySelector(`#literal-translation [translation-word-id="${wordIdTranslation}"]`);
        if (targetTranslationElement) targetTranslationElement.classList.remove('highlight');

        const sentenceTranslationElement = document.querySelector(`#sentence-container [translation-word-id="${wordIdTranslation}"]`);
        if (sentenceTranslationElement) sentenceTranslationElement.classList.remove('highlight');

        const generalTranslationElement = document.querySelector(`[translation-word-id="${wordIdTranslation}"]`);
        if (generalTranslationElement) generalTranslationElement.classList.remove('highlight');
    }

    if (wordIdOriginal) {
        const targetOriginalElement = document.querySelector(`#original-sentence [original-word-id="${wordIdOriginal}"]`);
        if (targetOriginalElement) targetOriginalElement.classList.remove('highlight');
    }}

function addDecorators() {
// Add event listeners to the words in the literal translation
    document.querySelectorAll('#literal-translation [translation-word-id]').forEach(wordElement => {
        const wordIdTranslation = wordElement.getAttribute('translation-word-id');

        wordElement.addEventListener('mouseover', () => highlightWord(wordIdTranslation, null));
        wordElement.addEventListener('mouseout', () => removeHighlight(wordIdTranslation, null));
    });

    document.querySelectorAll('#original-sentence [original-word-id]').forEach(wordElement => {
        const wordIdOriginal = wordElement.getAttribute('original-word-id');

        wordElement.addEventListener('mouseover', () => highlightWord(null, wordIdOriginal));
        wordElement.addEventListener('mouseout', () => removeHighlight(null, wordIdOriginal));
    });

    document.querySelectorAll('#sentence-container [original-word-id]').forEach(wordElement => {
        console.log(wordElement)
        const wordIdTranslation = wordElement.getAttribute('translation-word-id');
        const wordIdOriginal = wordElement.getAttribute('original-word-id');

        wordElement.addEventListener('mouseover', () => highlightWord(wordIdTranslation, wordIdOriginal));
        wordElement.addEventListener('mouseout', () => removeHighlight(wordIdTranslation, wordIdOriginal));
    });
}
// Function to highlight a word
function highlightWord(wordIdTranslation, wordIdOriginal) {
    if (!wordIdTranslation) {
        wordIdTranslation = document.querySelector(`#sentence-container [original-word-id="${wordIdOriginal}"]`).getAttribute("translation-word-id")
    }
    if (!wordIdOriginal) {
        wordIdOriginal = document.querySelector(`#sentence-container [translation-word-id="${wordIdTranslation}"]`).getAttribute("original-word-id")
    }

    document.querySelector(`#literal-translation [translation-word-id="${wordIdTranslation}"]`).classList.add('highlight');
    document.querySelector(`#original-sentence [original-word-id="${wordIdOriginal}"]`).classList.add('highlight');
    document.querySelector(`#sentence-container [translation-word-id="${wordIdTranslation}"]`).classList.add('highlight');
    document.querySelector(`[translation-word-id="${wordIdTranslation}"]`).classList.add('highlight');
}

// Function to remove the highlight
function removeHighlight(wordIdTranslation, wordIdOriginal) {
    if (!wordIdTranslation) {
        wordIdTranslation = document.querySelector(`#sentence-container [original-word-id="${wordIdOriginal}"]`).getAttribute("translation-word-id")
    }
    if (!wordIdOriginal) {
        wordIdOriginal = document.querySelector(`#sentence-container [translation-word-id="${wordIdTranslation}"]`).getAttribute("original-word-id")
    }

    document.querySelector(`#literal-translation [translation-word-id="${wordIdTranslation}"]`).classList.remove('highlight');
    document.querySelector(`#original-sentence [original-word-id="${wordIdOriginal}"]`).classList.remove('highlight');
    document.querySelector(`#sentence-container [translation-word-id="${wordIdTranslation}"]`).classList.remove('highlight');
    document.querySelector(`[translation-word-id="${wordIdTranslation}"]`).classList.remove('highlight');
}

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

    document.querySelectorAll('#sentence-container [translation-word-id]').forEach(wordElement => {
        const wordIdTranslation = wordElement.getAttribute('translation-word-id');
        const wordIdOriginal = wordElement.getAttribute('original-word-id');

        wordElement.addEventListener('mouseover', () => highlightWord(wordIdTranslation, wordIdOriginal));
        wordElement.addEventListener('mouseout', () => removeHighlight(wordIdTranslation, wordIdOriginal));
    });
}
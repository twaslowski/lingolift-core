fetch('http://127.0.0.1:5000/translate')
    .then(response => response.json())
    .then(data => {
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
    });

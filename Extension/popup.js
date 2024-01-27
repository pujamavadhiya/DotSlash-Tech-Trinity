document.addEventListener('DOMContentLoaded', async function () {
    async function checkTermsAndConditions() {
        try {
            const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
            const tab = tabs[0];
            const url = tab.url;

            const response = await fetch(url);
            const html = await response.text();
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const elements = Array.from(doc.querySelectorAll('a'));

            const privacyPolicy = elements.find((element) => {
                return element.innerText.toLowerCase().includes('privacy');
            });

            if (privacyPolicy) {
                alert(privacyPolicy.href);

                try {
                    // make the post request to the backend and send the privacy policy link
                    const backendResponse = await fetch('http://127.0.0.1:5000/test1', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ privacy_url: privacyPolicy.href }),
                    });
                    alert(backendResponse);
                    const data = await backendResponse.json();
                    console.log(data);
                    alert(data);
                    return data;
                } catch (error) {
                    console.log(error);
                    throw new Error('Error during backend request: ' + error.message);
                }
            } else {
                throw new Error('Privacy Policy link not found.');
            }
        } catch (error) {
            console.error('Error fetching or parsing the document:', error);
            throw new Error('Error during checkTermsAndConditions: ' + error.message);
        }
    }

    document.querySelector('.loader').style.display = 'block';

    try {
        const hasTermsAndConditions = await checkTermsAndConditions();

        document.querySelector('.loader').style.display = 'none';
        

        if (hasTermsAndConditions && hasTermsAndConditions.response && hasTermsAndConditions.response.response && hasTermsAndConditions.response.response.termsAndConditions) {
            document.getElementById('points-container').innerHTML = '<h2>Terms And Conditions Found</h2><ul id="points-list"></ul>';

            document.getElementById('points-list').innerHTML = '';

           
            
            for (const point of hasTermsAndConditions.response.response.termsAndConditions) {
                const li = document.createElement('li');
                li.innerText = point.point
                document.getElementById('points-list').appendChild(li);
                               
            }
        } else {
            document.getElementById('points-container').innerHTML = '<h2>No Terms And Conditions Found</h2><div id="img-nodata"><img src="images/nodata.jpg"></div><ul id="points-list"></ul>';
        }
    } catch (error) {
        console.error('Error during checkTermsAndConditions:', error);
        // Optionally, provide user feedback about the error.
    }
});

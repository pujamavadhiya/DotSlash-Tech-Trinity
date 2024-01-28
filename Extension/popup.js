document.addEventListener('DOMContentLoaded', async function () {
    let fetchInProgress = false;

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

            const privacyPolicy = elements.find((element) => element.innerText.toLowerCase().includes('privacy'));

            if (privacyPolicy) {
                const backendResponse = await fetchBackend(privacyPolicy.href);

                return backendResponse;
            } else {
                throw new Error('Privacy Policy link not found.');
            }
        } catch (error) {
            console.error('Error fetching or parsing the document:', error);
            throw new Error('Error during checkTermsAndConditions: ' + error.message);
        }
    }

    async function fetchBackend(privacyPolicyUrl) {
        try {
            fetchInProgress = true;

            const backendResponse = await fetch('http://127.0.0.1:5000/getAnalysis', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ privacy_url: privacyPolicyUrl }),
            });

            const data = await backendResponse.json();
            console.log(data);

            return data;
        } catch (error) {
            console.log(error);
            throw new Error('Error during backend request: ' + error.message);
        } finally {
            fetchInProgress = false;
        }
    }

    document.querySelector('.loader').style.display = 'block';

    try {
        if (!fetchInProgress) {
            const hasTermsAndConditions = await checkTermsAndConditions();

            document.querySelector('.loader').style.display = 'none';

            if (hasTermsAndConditions && hasTermsAndConditions.response && hasTermsAndConditions.response.privacyPolicy) {
                document.getElementById('points-container').innerHTML = '<h1>Terms And Conditions Found</h1><ul id="points-list"></ul>';
            
                document.getElementById('points-list').innerHTML = '';
    
                // inceased the font size of whole page
                document.body.style.fontSize = '25px';
                for (const point of hasTermsAndConditions.response.privacyPolicy) {
                    const li = document.createElement('li');
                    
                    // Display the point in bold
                    const b = document.createElement('b');
                    b.innerText = point.point;
                    li.appendChild(document.createElement('br'));
                    li.appendChild(document.createElement('br'));
                    li.appendChild(b);
                    li.appendChild(document.createElement('br'));
                
                    // Display the point.brief
                    const p = document.createElement('p');
                    p.innerText = point.brief;
                    li.appendChild(p);
                
                    // Color code based on concernRating
                    const color = getColorBasedOnRating(point.concernRating);
                    li.style.color = color;
                
                    document.getElementById('points-list').appendChild(li);
                }
                
                // Function to get color based on concernRating
                function getColorBasedOnRating(concernRating) {
                    switch (concernRating) {
                        case 3:
                            return 'red'; // or any color code for the highest concern
                        case 2:
                            return 'orange'; // or any color code for medium concern
                        case 1:
                        default:
                            return 'green'; // or any color code for the lowest concern
                    }
                }
            } else {
                document.getElementById('points-container').innerHTML = '<h2>No Terms And Conditions Found</h2><div id="img-nodata"><img src="images/nodata.jpg"></div><ul id="points-list"></ul>';
            }
        } else {
            console.log('Fetch already in progress. Please wait for the current request to complete.');
        }
    } catch (error) {
        console.error('Error during checkTermsAndConditions:', error);
        // Optionally, provide user feedback about the error.
    }
});

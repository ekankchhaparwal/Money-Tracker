console.log("This is my index js file");

// Initialize the news api parameters
let source = 'the-times-of-india';
let apiKey = 'd093053d72bc40248998159804e0e67d'


let newsAccordion = document.getElementById('newsAccordion');
const xhr = new XMLHttpRequest();
xhr.open('GET', `https://newsapi.org/v2/everything?q=finance&sources=${source}&apiKey=${apiKey}`, true);

// What to do when response is ready
xhr.onload = function () {
    if (this.status === 200) {
        let x = 0;
        let json = JSON.parse(this.responseText);
        let articles = json.articles;
        let newsHtml = "";
        articles.forEach(function (element, index) {
            // console.log(element, index)
            let news = `<div class="card" style="background-color: #f5f5f5; padding: 20px; margin-bottom: 20px;">
            <div class="card-header" id="heading${index}" style="text-align: center; padding: 10px;">
                <img src="${element['urlToImage']}" alt="News" style="width: 500px; height: auto; border-radius: 10px;">
                <h2 class="mb-0" style="font-size: 24px; margin-top: 20px;">
                    <button class="btn btn-link collapsed" type="button" data-toggle="collapse" data-target="#collapse${index}"
                        aria-expanded="false" aria-controls="collapse${index}" style="font-weight: bold; color: #333;">
                        Breaking News ${index + 1}: ${element["title"]}
                    </button>
                </h2>
            </div>
        
            <div id="collapse${index}" class="collapse" aria-labelledby="heading${index}" data-parent="#newsAccordion">
                <div class="card-body" style="font-size: 16px;">
                    ${element["description"]}. <a href="${element['url']}" target="_blank" style="color: #333;">Read more here</a> 
                </div>
            </div>
        </div>
        
        `;
            if (x <= 19) {
                newsHtml += news;
            }
            x++;

        });
        newsAccordion.innerHTML = newsHtml;
    }
    else {
        console.log("Some error occured")
    }
}

xhr.send()
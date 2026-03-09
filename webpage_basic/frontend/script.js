async function uploadFile(input){

const file = input.files[0];

const formData = new FormData();
formData.append("file", file);

const response = await fetch("/upload",{
method:"POST",
body:formData
});

const data = await response.json();

if(data.type === "pdf"){

window.location.href="/static/result.html";

}

else if(data.type === "mp3"){

localStorage.setItem("audioData", JSON.stringify(data));

window.location.href="/static/audio_result.html";

}

}

if (window.location.pathname.includes("result.html")) {

fetch("/upload_result")
.then(response => response.json())
.then(data => {

    if (!data || !data.pdf_url) {
        console.error("No PDF result returned");
        return;
    }

    document.getElementById("pdfViewer").src = data.pdf_url;

    const container = document.getElementById("extractedText");

    if (data.content && data.content.length > 0) {

      let cleaned = data.content
       .replace(/Slangle/g,"\\langle")
       .replace(/rangle/g,"\\rangle")
       .replace(/loplus/g,"\\oplus")
       .replace(/stackrel\{\?\}\{=\}/g,"\\stackrel{?}{=}")
       .replace(/\|\|/g,"\\|\\|");

        container.innerHTML = marked.parse(cleaned);

        // KaTeX equation rendering
      if (typeof renderMathInElement !== "undefined") {
          renderMathInElement(container, {
            delimiters: [
                {left: "$$", right: "$$", display: true},
                {left: "$", right: "$", display: false},
                {left: "\\(", right: "\\)", display: false},
                {left: "\\[", right: "\\]", display: true}
            ],
            throwOnError: false
        });
      }

    } else {
        container.innerHTML = "No text extracted from PDF.";
    }

})
.catch(err => {
    console.error("Error loading PDF result:", err);
});

}

async function uploadFile(input) {

const file = input.files[0]

if(!file){
return
}

const formData = new FormData()
formData.append("file", file)

const response = await fetch("/upload", {
method: "POST",
body: formData
})

const data = await response.json()

localStorage.setItem("extractedData", JSON.stringify(data))

window.location.href = "/static/result.html"

}



window.onload = function(){

if(window.location.pathname.includes("result.html")){

const stored = localStorage.getItem("extractedData")

if(!stored){
return
}

const data = JSON.parse(stored)

if(data.type === "pdf"){

document.getElementById("pdfViewer").src = data.pdf_url

}
marked.setOptions({ breaks: true })
const html = marked.parse(data.content)
document.getElementById("extractedText").innerHTML = html

renderMathInElement(document.getElementById("extractedText"), {
delimiters: [
{left: "$$", right: "$$", display: true},
{left: "$", right: "$", display: false}
]
})
}

}
